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

import json
import logging
import os

from nusex import CONFIG_DIR, LICENSE_DIR, PROFILE_DIR, VERSION_PATTERN
from nusex.errors import ProfileError
from nusex.helpers import cprint, validate_name
from nusex.spec import NSCSpecIO, NSPSpecIO

VALID_CONFIG_KEYS = (
    "author_name",
    "author_email",
    "git_profile_url",
    "starting_version",
    "default_description",
    "preferred_license",
)

log = logging.getLogger(__name__)


class Profile:
    """A class in which to create, load, modify, and save profiles.

    Keyword Args:
        name (:obj:`str`): The name of the profile. If the profile does
            not exist, a new one is created, otherwise an existing one
            is loaded. Defaults to "default".

    Attributes:
        path (:obj:`pathlib.Path`): The complete filepath to the
            profile.
        data (:obj:`dict[str, Any]`): The data for the profile.
    """

    __slots__ = ("path", "data")

    def __init__(self, name="default"):
        self.path = PROFILE_DIR / f"{name}.nsp"

        if not os.path.isfile(self.path):
            log.info(f"[{name}] Not found; creating new...")
            return self.create_new(name)

        log.info(f"[{name}] Loading data...")
        self.load()

    def __str__(self):
        return self.path.stem

    def __repr__(self):
        return f"<Profile name={self.name!r}>"

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __getitem__(self, key):
        return self.data[key]

    @property
    def name(self):
        """The name of this profile.

        Returns:
            :obj:`str`
        """
        return self.path.stem

    @property
    def exists(self):
        """Whether this profile exists on disk.

        Returns:
            :obj:`bool`
        """
        return self.path.is_file()

    def create_new(self, name):
        """Create a new profile.

        Args:
            name (:obj:`str`): The name of the profile.

        Raises:
            :obj:`ProfileError`: The provided name is invalid.
            :obj:`AlreadyExists`: The profile already exists on disk.
        """
        validate_name(name, self.__class__.__name__)
        self.data = NSPSpecIO().defaults
        log.debug(f"[{self.name}] Data = {self.data}")

    def load(self):
        """Load an existing profile. This should never need to be called
        as profiles are loaded automatically when necessary upon object
        creation.

        Raises:
            :obj:`FileNotFoundError`: The profile does not exist on
                disk.
        """
        self.data = NSPSpecIO().read(self.path)
        log.debug(f"[{self.name}] Data = {self.data}")

    def save(self):
        """Save this profile.

        Raises:
            :obj:`ProfileError`: The profile data has been improperly
                modified.
        """
        NSPSpecIO().write(self.path, self.data)
        log.info(f"[{self.name}] Saved to {self.path}")

    def delete(self):
        """Delete this profile.

        Raises:
            :obj:`FileNotFoundError`: The profile does not exist on
                disk.
        """
        os.remove(self.path)
        log.info(f"[{self.name}] Deleted from {self.path}")

    def rename(self, new_name):
        """Rename this profile.

        Args:
            new_name (:obj:`str`): The new name for the profile.

        Raises:
            :obj:`ProfileError`: The new name for the profile is
                invalid.
            :obj:`AlreadyExists`: The new name for the profile is
                already being used by a template.
            :obj:`FileNotFoundError`: The profile does not exist on
                disk.
        """
        validate_name(new_name, self.__class__.__name__)
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path.rename(new_path)
        self.path = PROFILE_DIR / f"{new_name}.nsp"
        log.info(f"[{self.name}] Renamed")

    @classmethod
    def current(cls):
        """Create an instance for the currently selected profile.

        Returns:
            :obj:`Profile`: The currently selected profile.
        """
        return cls(NSCSpecIO().read()["profile"])

    @classmethod
    def from_legacy(cls, name="default"):
        """Create a profile from a 0.x spec user.nsc file.

        Keyword Args:
            name (:obj:`str`): The name of the profile. Defaults to
                "default".

        Returns:
            :obj:`Profile`: The newly created profile.

        Raises:
            :obj:`FileNotFoundError`: No user.nsc file exists in the
                config directory.
        """
        with open(CONFIG_DIR / "user.nsc") as f:
            data = json.load(f)
            log.debug(f"[{name}] Old config data: {data}")

        c = cls(name)
        values = list(data.values())
        order = (3, 4, 2, 0, 1, 5)

        for i, k in enumerate(c.data.keys()):
            v = values[order[i]]

            if k == "starting_version":
                if v != "CALVER" and not VERSION_PATTERN.match(v):
                    v = (
                        input(f"🎤 Starting version [0.1.0]: ").strip()
                        or "0.1.0"
                    )
                    v = c._validate_option(k, v)
                    log.info(f"[{name}] Option '{k}' resolved to '{v}'")

            elif k == "preferred_license":
                v = c._resolve_license(v)
                if not v:
                    v = (
                        input(f"🎤 Preferred license [unlicense]: ").strip()
                        or "unlicense"
                    )
                    v = c._validate_option(k, v)
                    log.info(f"[{name}] Option '{k}' resolved to '{v}'")

            c.data[k] = v
            log.debug(f"[{name}] Option '{k}' set to '{v}' in profile data")

        return c

    @property
    def is_selected(self):
        """Whether this profile is currently selected.

        Returns:
            :obj:`bool`
        """
        return NSCSpecIO().read()["profile"] == self.path.stem

    def select(self):
        """Select this profile. This will not error if the profile is
        already selected; use the :obj:`is_selected` property to check
        if this profile is already selected instead.
        """
        data = NSCSpecIO().read()
        data["profile"] = self.path.stem
        NSCSpecIO().write(data)
        log.info(f"[{self.name}] Selected")

    def _resolve_license(self, value):
        def _sanitise(text):
            return (
                text.replace("License", "")
                .replace("  ", "")
                .replace("-", " ")
                .replace("_", " ")
                .strip()
            )

        value = value.lower()

        for file in LICENSE_DIR.glob("*.txt"):
            if value == file.stem:
                log.debug(f"[{self.name}] License found: {file.stem}")
                return file.stem

            attrs = {}
            with open(LICENSE_DIR / file, encoding="utf-8") as f:
                for line in f:
                    if line == "---\n":
                        continue
                    if line == "\n":
                        break

                    k, v = line.split(": ")
                    attrs.update({k: v.strip().lower()})

            nickname = attrs.get("nickname", "")
            spdx_id = attrs.get("spdx-id", "")
            title = attrs.get("title", "")

            if (
                title == value
                or spdx_id == value
                or title == value
                or _sanitise(value)
                in (_sanitise(nickname), _sanitise(spdx_id), _sanitise(title))
            ):
                log.debug(f"[{self.name}] License attrs ({value}): {attrs}")
                return file.stem

    def _validate_option(self, key, option):
        if key == "git_profile_url":
            option = option.strip("/")

        if key == "starting_version":
            if option != "CALVER" and not VERSION_PATTERN.match(option):
                raise ProfileError(
                    "That version number does not conform to PEP 440 "
                    "standards, or is not 'CALVER'"
                )

        if key == "preferred_license":
            option = self._resolve_license(option)
            if not option:
                raise ProfileError(
                    "Your input could not be resolved to a valid license"
                )

        log.debug(f"[{self.name}] Option '{key}' resolved to '{option}'")
        return option

    def setup(self):
        """Set up this profile. You will be prompted to input some
        information.

        Raises:
            :obj:`ProfileError`: An invalid value was provided to one of
                the inputs.
        """
        for k, v in self.data.items():
            kq = (k[0].upper() + k[1:].replace("_", " ")).replace("url", "URL")
            option = input(f"🎤 {kq} [{v}]: ").strip() or v.strip()
            option = self._validate_option(k, option)
            self.data[k] = option

    def update(self, **kwargs):
        """Update this profile's configuration. All options must be
        passed through as kwargs. Invalid configuration keys raise
        warnings, not errors.

        Keyword Args:
            author_name (:obj:`str`): An author name.
            author_email (:obj:`str`): An author email.
            git_profile_url (:obj:`str`): Your
                GitHub/Gitlab/BitBucket/etc. profile link.
            starting_version (:obj:`str`): The version to initialise
                project with.
            default_description (:obj:`str`): The description to
                initialise projects with.
            preferred_license (:obj:`str`): Your preferred license.
        """
        for k, v in kwargs.items():
            if k not in VALID_CONFIG_KEYS:
                cprint("war", f"'{k}' is not a valid key, skipping...")
                continue

            if v:
                v = self._validate_option(k, v)
                self.data[k] = v
                log.debug(f"[{self.name}] Option '{k}' updated to '{v}'")
