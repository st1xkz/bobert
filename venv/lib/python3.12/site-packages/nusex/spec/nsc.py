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

from nusex import CONFIG_FILE
from nusex.errors import UnsupportedFile

SPEC_ID = b"\x99\x63"


class NSCSpecIO:
    __slots__ = ("defaults",)

    def __init__(self):
        self.defaults = {
            "profile": "default",
            "last_update": "000101",
            "use_wildmatch_ignore": False,
            "auto_update": False,
        }

    def read(self):
        data = self.defaults.copy()
        with open(CONFIG_FILE, "rb") as f:
            # Validate format.
            if f.read(2) != SPEC_ID:
                raise UnsupportedFile("Not a valid NSC file")

            # Load profile data.
            data["profile"] = f.read(24).decode().strip()
            date = f.read(6).decode()
            try:
                int(date)
                data["last_update"] = date
            except ValueError:
                # Some invalid or broken config.
                ...

            # Not guaranteed from here.
            attrs = ("use_wildmatch_ignore", "auto_update")
            for attr in attrs:
                try:
                    data[attr] = f.read(1) == b"\x01"
                except Exception as exc:
                    # Most likely no more options to read, so exit.
                    break

        return data

    def write(self, data):
        with open(CONFIG_FILE, "wb") as f:
            # Identify format.
            f.write(SPEC_ID)

            # Write data.
            f.write(data["profile"].ljust(24).encode())
            f.write(data["last_update"].encode())

            # Not guaranteed, so write a default value if not present.
            f.write((b"\x00", b"\x01")[data.get("use_wildmatch_ignore", 0)])
            f.write((b"\x00", b"\x01")[data.get("auto_update", 0)])
