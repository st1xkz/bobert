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

import datetime as dt
import json
import os
import shutil
from pathlib import Path

from nusex import CONFIG_DIR, LICENSE_DIR, PROFILE_DIR, TEMPLATE_DIR, Profile
from nusex.errors import MigrationError
from nusex.helpers import cprint
from nusex.spec import NSCSpecIO, NSXSpecIO
from nusex.utils import Downloader


def _migrate():
    # Back-up
    shutil.copytree(CONFIG_DIR, f"{CONFIG_DIR}-old")

    # Create directories
    for dir in (LICENSE_DIR, PROFILE_DIR, TEMPLATE_DIR):
        os.makedirs(dir, exist_ok=True)

    # Download assets
    for dl in ("templates", "licenses"):
        Downloader(dl).download()

    # Create new profile
    profile = Profile.from_legacy()
    profile.save()

    # Convert templates
    for file in Path(CONFIG_DIR).glob("*.nsx"):
        with open(file) as f:
            data = json.load(f)

        for k, v in data["files"].items():
            data["files"][k] = v.encode()
        data.update({"installs": [], "as_addon_for": ""})
        NSXSpecIO().write(TEMPLATE_DIR / f"{file.stem[:24]}.nsx", data)

    # Remove old files
    for file in Path(CONFIG_DIR).glob("*.*"):
        os.remove(file)

    # Create config file
    settings = {
        "profile": "default",
        "last_update": dt.date.today().strftime("%y%m%d"),
        "use_wildmatch_ignore": False,
    }
    NSCSpecIO().write(settings)


def _revert():
    shutil.rmtree(CONFIG_DIR)
    shutil.move(f"{CONFIG_DIR}-old", CONFIG_DIR)


def run(revert):
    if revert:
        if not (CONFIG_DIR.parent / f"{CONFIG_DIR}-old").exists():
            raise MigrationError("No old configurations to revert to")

        _revert()
        return cprint("aok", "Migration successfully reverted!")

    if not (CONFIG_DIR / "user.nsc").exists():
        raise MigrationError("Nothing to migrate from")

    try:
        _migrate()
        cprint("aok", "Migration successful!")
    except Exception as exc:
        _revert()
        cprint(
            "err",
            "Migration aborted. Your old configuration has been restored.",
        )
        raise exc


def setup(subparsers):
    s = subparsers.add_parser(
        "migrate", description="Migrate from a 0.x config to a 1.x one."
    )
    s.add_argument(
        "--revert",
        help="revert back to a 0.x config, if possible",
        action="store_true",
    )
    return subparsers
