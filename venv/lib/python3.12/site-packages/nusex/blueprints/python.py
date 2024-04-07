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

from nusex.blueprints import with_files
from nusex.blueprints.generic import GenericBlueprint

INIT_ATTR_MAPPING = {
    "__productname__": '"PROJECTNAME"',
    "__version__": '"PROJECTVERSION"',
    "__description__": '"PROJECTDESCRIPTION"',
    "__url__": '"PROJECTURL"',
    "__docs__": '"https://PROJECTNAME.readthedocs.io/en/latest"',
    "__author__": '"PROJECTAUTHOR"',
    "__author_email__": '"PROJECTAUTHOREMAIL"',
    "__license__": '"PROJECTLICENSE"',
    "__bugtracker__": '"PROJECTURL/issues"',
    "__ci__": '"PROJECTURL/actions"',
}
PYPROJECT_ATTR_MAPPING = {
    "name": '"PROJECTNAME"',
    "version": '"PROJECTVERSION"',
    "description": '"PROJECTDESCRIPTION"',
    "license": '"PROJECTLICENSE"',
    "authors": '["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]',
    "maintainers": '["PROJECTAUTHOR <PROJECTAUTHOREMAIL>"]',
    "homepage": '"PROJECTURL"',
    "repository": '"PROJECTURL"',
    "documentation": '"https://PROJECTNAME.readthedocs.io/en/latest"',
}


class PythonBlueprint(GenericBlueprint):
    @with_files("PROJECTNAME/__init__.py$")
    def modify_init(self, lines):
        for i, line in enumerate(lines[:]):
            if line.startswith("__"):
                k, v = line.split(" = ")
                v = v.strip('"').strip("'")
                new_v = INIT_ATTR_MAPPING.get(k, v)
                lines[i] = f"{k} = {new_v}"

        return "\n".join(lines)

    @with_files("pyproject.toml$")
    def modify_pyproject(self, lines):
        in_tool_poetry = False

        for i, line in enumerate(lines[:]):
            if in_tool_poetry:
                if line.startswith("["):
                    in_tool_poetry = False
                    continue

                try:
                    k, v = line.split(" = ")
                    v = v.strip('"').strip("'")
                    new_v = PYPROJECT_ATTR_MAPPING.get(k, v)
                    lines[i] = f"{k} = {new_v}"
                except ValueError:
                    ...

            elif line.strip() == "[tool.poetry]":
                in_tool_poetry = True

        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("MANIFEST.in$", "setup.(cfg|py)$")
    def modify_other_files(self, lines):
        # TODO: Make the setup files more complete:
        # https://docs.python.org/3/distutils/setupscript.html
        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("requirements.*\.txt$")
    def modify_requirements_files(self, lines):
        for i, line in enumerate(lines[:]):
            if line.startswith("git+") and self.project_name in line:
                lines[i] = "git+PROJECTURL"

        return "\n".join(lines).replace(self.project_name, "PROJECTNAME")

    @with_files("PROJECTNAME/errors?.py$")
    def modify_error_files(self, lines):
        for line in lines[:]:
            if line.startswith("class"):
                base_exc = line.split("(")[0][6:]
                break

        if base_exc == "Error":
            return "\n".join(lines)

        return "\n".join(lines).replace(base_exc, "PROJECTBASEEXC")
