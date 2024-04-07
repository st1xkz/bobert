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

from nusex import __url__
from nusex.blueprints import with_files
from nusex.blueprints.base import Blueprint

DOCS_ATTR_MAPPING = {
    "project": '"PROJECTNAME"',
    "copyright": '"PROJECTYEAR, PROJECTAUTHOR"',
    "author": '"PROJECTAUTHOR"',
    "release": "PROJECTNAME.__version__",
}


class GenericBlueprint(Blueprint):
    @with_files("README")
    def modify_readme(self, lines):
        last_line = len(lines) - 1
        found_acks = False
        ack = (
            "This project was created in part by the [nusex project "
            f"templating utility]({__url__})."
        )

        for i, line in enumerate(lines[:]):
            if line.startswith("#"):
                if found_acks:
                    lines.insert(i, ack)
                    lines.insert(i + 1, "")
                    break

                if "acknowledgements" in line.lower():
                    found_acks = True

            elif i == last_line and found_acks:
                lines.extend([ack, ""])

        if not found_acks:
            lines.extend(["## Acknowledgements", "", ack, ""])

        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("LICEN[SC]E", "COPYING")
    def modify_license(self, _):
        return "LICENSEBODY"

    @with_files("CONTRIBUTING")
    def modify_contributing(self, lines):
        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("docs/(source/)?conf.py$")
    def modify_docs_conf(self, lines):
        in_project_info = False

        for i, line in enumerate(lines[:]):
            if in_project_info:
                if line.startswith("# --"):
                    in_project_info = False
                    continue

                try:
                    k, v = line.split(" = ")
                    v = v.strip('"').strip("'")
                    new_v = DOCS_ATTR_MAPPING.get(k, v)
                    lines[i] = f"{k} = {new_v}"
                except ValueError:
                    ...

            elif line.startswith("# -- Project information"):
                in_project_info = True

            elif line.strip() == f"import {self.project_name}":
                lines[i] = "import PROJECTNAME"

        return "\n".join(lines)
