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

import os

from nusex import PROFILE_DIR, Profile
from nusex.errors import AlreadyExists, DoesNotExist
from nusex.helpers import cprint


def _build_profile(name):
    if os.path.isfile(PROFILE_DIR / f"{name}.nsp"):
        raise AlreadyExists("A profile with that name already exists")

    profile = Profile(name)
    profile.setup()
    profile.save()
    profile.select()
    cprint("aok", f"Profile '{profile.name}' successfully created!")


def run(show_current, create_new, switch, **kwargs):
    if show_current:
        return print(Profile.current().name)

    if create_new:
        return _build_profile(create_new)

    if switch:
        profile = Profile(switch)
        if not profile.exists:
            raise DoesNotExist(f"Profile '{switch}' not found")
        profile.select()
        return cprint("aok", f"Switched to profile '{profile}'!")

    profile = Profile.current()

    if any(kwargs.values()):
        profile.update(**kwargs)
        profile.save()
        return cprint("aok", f"Profile '{profile}' updated!")

    profile.setup()
    profile.save()
    cprint("aok", f"Profile '{profile}' updated!")


def setup(subparsers):
    s = subparsers.add_parser(
        "profile",
        description="Create, modify and switch user profiles.",
    )
    s.add_argument(
        "-c",
        "--show-current",
        help="show the currently selected profile and exit",
        action="store_true",
    )
    s.add_argument(
        "-n",
        "--create-new",
        help="create a new profile",
        metavar="NAME",
        default="",
    )
    s.add_argument(
        "-s",
        "--switch",
        help="switch to a different profile",
        metavar="NAME",
        default="",
    )
    s.add_argument(
        "-a",
        "--author-name",
        help="change the author name for this profile",
        metavar="NAME",
        default="",
    )
    s.add_argument(
        "-e",
        "--author-email",
        help="change the author email for this profile",
        metavar="EMAIL",
        default="",
    )
    s.add_argument(
        "-g",
        "--git-profile-url",
        help="change the Git profile URL for this profile",
        metavar="URL",
        default="",
    )
    s.add_argument(
        "-v",
        "--starting-version",
        help="change the starting version for this profile",
        metavar="VERSION",
        default="",
    )
    s.add_argument(
        "-d",
        "--default-description",
        help="change the default description for this profile",
        metavar="DESCRIPTION",
        default="",
    )
    s.add_argument(
        "-l",
        "--preferred-license",
        help="change the preferred license for this profile",
        metavar="LICENSE",
        default="",
    )
    return subparsers
