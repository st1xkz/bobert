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
import subprocess as sp
import sys

from . import INVALID_NAME_PATTERN, PROFILE_DIR, TEMPLATE_DIR
from .errors import AlreadyExists, ProfileError, TemplateError

MESSAGE_TYPES = {
    "aok": ("🎉", "\33[92m"),
    "war": ("💣", "\33[93m"),
    "err": ("💥", "\33[91m"),
    "prc": ("⌛", ""),
    "inf": ("📢", "\33[94m"),
}


def cprint(type, text, **kwargs):
    emoji, colour = MESSAGE_TYPES[type]
    print(f"{emoji} {colour}{text}\33[0m", **kwargs)


def validate_name(name, for_type):
    err = {
        "Profile": ProfileError,
        "Template": TemplateError,
    }[for_type]

    if len(name) > 24:
        raise err(f"{for_type} names are limited to 24 characters")

    if INVALID_NAME_PATTERN.search(name):
        raise err(
            f"{for_type} names can only contain lower case letters, numbers, "
            "and underscores"
        )

    if name.startswith("nsx"):
        raise err("That name is reserved")

    in_dir = {
        "Profile": TEMPLATE_DIR,
        "Template": PROFILE_DIR,
    }[for_type]

    if name in (f.split(".")[0] for f in os.listdir(in_dir)):
        raise AlreadyExists(
            f"A {'profile' if for_type == 'Template' else 'template'} is "
            "already using that name"
        )


def run(command):
    if sys.version_info >= (3, 7, 0):
        return sp.run(command, shell=True, capture_output=True)

    if os.name != "nt":
        return sp.run(f"{command} > /dev/null 2>&1", shell=True)

    # Windows users will have to put up with the output for 3.6 tests.
    return sp.run(command, shell=True)


def options_as_set(values):
    s = set(values.split(","))

    if s == {""}:
        return {}

    return s


def options_as_list(values):
    l = values.split(",")

    if l == [""]:
        return []

    return l
