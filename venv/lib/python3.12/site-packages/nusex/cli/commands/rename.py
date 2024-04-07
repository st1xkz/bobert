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

from nusex import PROFILE_DIR, TEMPLATE_DIR, Profile, Template
from nusex.errors import DoesNotExist, ProfileError, TemplateError
from nusex.helpers import cprint


def run(name, new_name):
    if name.startswith("nsx"):
        raise TemplateError("You cannot rename premade templates")

    if (PROFILE_DIR / f"{name}.nsp").exists():
        profile = Profile(name)
        if profile.is_selected:
            raise ProfileError(
                "You cannot rename the currently selected profile"
            )
        profile.rename(new_name)
        cprint(
            "aok", f"Profile '{name}' successfully renamed to '{new_name}'!"
        )

    elif (TEMPLATE_DIR / f"{name}.nsx").exists():
        template = Template(name)
        template.rename(new_name)
        cprint(
            "aok", f"Template '{name}' successfully renamed to '{new_name}'!"
        )

    else:
        raise DoesNotExist(f"No profile or template with name '{name}' found")


def setup(subparsers):
    s = subparsers.add_parser(
        "rename", description="Rename a profile or template."
    )
    s.add_argument(
        "name",
        help="the name of the profile or template to rename",
    )
    s.add_argument(
        "new_name",
        help="the new name for the profile or template",
    )
    return subparsers
