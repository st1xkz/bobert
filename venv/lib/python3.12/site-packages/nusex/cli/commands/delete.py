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

from nusex import PROFILE_DIR, TEMPLATE_DIR, Profile
from nusex.errors import ProfileError, TemplateError
from nusex.helpers import cprint
from nusex.template import Template


def run(names):
    count = 0

    for name in names:
        if (PROFILE_DIR / f"{name}.nsp").exists():
            profile = Profile(name)
            if profile.is_selected:
                raise ProfileError(
                    "You cannot delete the currently selected profile"
                )
            profile.delete()
            count += 1

        elif (TEMPLATE_DIR / f"{name}.nsx").exists():
            template = Template(name)
            template.delete()
            count += 1

        else:
            cprint(
                "war", f"Profile or template '{name}' not found, skipping..."
            )
            continue

    if not count:
        raise TemplateError("No profiles or templates deleted")

    cprint("aok", f"Successfully deleted {count:,} profiles/templates!")


def setup(subparsers):
    s = subparsers.add_parser(
        "delete", description="Delete one or more profiles or templates."
    )
    s.add_argument(
        "names",
        help="the name(s) of the profile(s) or template(s) to delete",
        nargs="+",
    )
    return subparsers
