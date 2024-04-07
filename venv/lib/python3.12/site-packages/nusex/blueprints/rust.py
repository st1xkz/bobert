# Copyright (c) 2021, Ethan Henderson
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice, this
#    list of conditions and the following disclaimer.
#
# 2. Redistributions in binary form must reproduce the above copyright notice,
#    this list of conditions and the following disclaimer in the documentation
#    and/or other materials provided with the distribution.
#
# 3. Neither the name of the copyright holder nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import re

from nusex.blueprints import with_files
from nusex.blueprints.generic import GenericBlueprint

CARGO_ATTR_MAPPING = {
    "name": '"PROJECTNAME"',
    "version": '"PROJECTVERSION"',
    "description": '"PROJECTDESCRIPTION"',
    "homepage": '"PROJECTURL"',
    "repository": '"PROJECTURL"',
    "docs": '"https://docs.rs/PROJECTNAME/PROJECTVERSION"',
    "authors": '["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]',
    "license": '"PROJECTLICENSE"',
}


class RustBlueprint(GenericBlueprint):
    @with_files("Cargo.toml$")
    def modify_cargo_toml(self, lines):
        in_package = False

        for i, line in enumerate(lines[:]):
            if in_package:
                if line.startswith("["):
                    in_package = True
                    continue

                try:
                    k, v = line.split(" = ")
                    v = v.strip('"').strip("'")
                    new_v = CARGO_ATTR_MAPPING.get(k, v)
                    lines[i] = f"{k} = {new_v}"
                except ValueError:
                    ...

            elif line.strip() == "[package]":
                in_package = True

        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("Cargo.lock$")
    def modify_cargo_lock(self, lines):
        for i, line in enumerate(lines[:]):
            if line == f'name = "{self.project_name}"':
                lines[i] = 'name = "PROJECTNAME"'
                lines[i + 1] = 'version = "PROJECTVERSION"'
                break

        return "\n".join(lines)

    @with_files("src/errors?.rs$")
    def modify_error_files(self, lines):
        found_derive = False

        for line in lines[:]:
            if found_derive:
                if line.startswith("#"):
                    continue

                base_exc = (
                    re.sub("[^a-zA-Z0-9_ ]", "", line).strip().split()[-1]
                )
                break

            elif line.startswith("#[derive"):
                found_derive = True

        if base_exc == "Error":
            return "\n".join(lines)

        return "\n".join(lines).replace(base_exc, "PROJECTBASEEXC")
