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

from nusex import PROFILE_DIR
from nusex.constants import TEMPLATE_DIR
from nusex.helpers import cprint


def run(profiles, templates):
    if not profiles and not templates:
        profiles = templates = True

    if profiles:
        cprint("inf", "Showing all profiles:")

        for p in sorted(PROFILE_DIR.glob("*.nsp")):
            print(p.stem)

        if templates:
            # Awkward lining up to make it prettier
            print()

    if templates:
        cprint("inf", "Showing all templates:")

        for t in sorted(TEMPLATE_DIR.glob("*.nsx")):
            print(t.stem)


def setup(subparsers):
    s = subparsers.add_parser(
        "list", description="Display a list of profiles and templates."
    )
    s.add_argument(
        "-p", "--profiles", help="only display profiles", action="store_true"
    )
    s.add_argument(
        "-t", "--templates", help="only display templates", action="store_true"
    )
    return subparsers
