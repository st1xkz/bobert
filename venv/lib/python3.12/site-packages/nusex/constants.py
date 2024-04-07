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
import re
import sys
from pathlib import Path

from nusex import blueprints


def _suffix():
    # Determine whether this is a production copy or not. This
    # prevents actual user configs from getting messed up.
    parts = Path(__file__).parts
    if "nox" in " ".join(sys.argv) or ".nox" in parts:
        return "nusex-test"
    if "site-packages" not in parts:
        return "nusex-dev"
    return "nusex"


if os.name == "nt":
    CONFIG_DIR = Path.home() / f".{_suffix()}"
    TEMP_DIR = CONFIG_DIR / "tmp"
else:
    CONFIG_DIR = Path.home() / f".config/{_suffix()}"
    TEMP_DIR = Path(f"/tmp/{_suffix()}")

CONFIG_FILE = CONFIG_DIR / "config.nsc"
LICENSE_DIR = CONFIG_DIR / "licenses"
PROFILE_DIR = CONFIG_DIR / "profiles"
TEMPLATE_DIR = CONFIG_DIR / "templates"

INVALID_NAME_PATTERN = re.compile("[^a-z0-9_]")
# https://github.com/pypa/packaging/blob/16.7/packaging/version.py#L159
VERSION_PATTERN = re.compile(
    r"""
    v?
    (?:
        (?:(?P<epoch>[0-9]+)!)?                           # epoch
        (?P<release>[0-9]+(?:\.[0-9]+)*)                  # release segment
        (?P<pre>                                          # pre-release
            [-_\.]?
            (?P<pre_l>(a|b|c|rc|alpha|beta|pre|preview))
            [-_\.]?
            (?P<pre_n>[0-9]+)?
        )?
        (?P<post>                                         # post release
            (?:-(?P<post_n1>[0-9]+))
            |
            (?:
                [-_\.]?
                (?P<post_l>post|rev|r)
                [-_\.]?
                (?P<post_n2>[0-9]+)?
            )
        )?
        (?P<dev>                                          # dev release
            [-_\.]?
            (?P<dev_l>dev)
            [-_\.]?
            (?P<dev_n>[0-9]+)?
        )?
    )
    (?:\+(?P<local>[a-z0-9]+(?:[-_\.][a-z0-9]+)*))?       # local version
""",
    re.VERBOSE | re.IGNORECASE,
)

BLUEPRINT_MAPPING = {
    "none": blueprints.GenericBlueprint,
    "python": blueprints.PythonBlueprint,
    "rust": blueprints.RustBlueprint,
}
