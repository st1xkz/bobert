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

import asyncio
from urllib import request
from urllib.error import HTTPError

from nusex import CONFIG_DIR
from nusex.errors import DownloadError
from nusex.helpers import cprint

REPO_URL = "https://github.com/nusex/downloads"
RAW_URL = "https://raw.githubusercontent.com"
TEMPLATE_SUFFIX = "tree/main/templates1x"
LICENSE_URL = (
    "https://github.com/github/choosealicense.com/tree/gh-pages/_licenses"
)


class Downloader:
    """A utility class for downloading assets.

    Args:
        of_type(str): The type of asset to download (must be either
            "templates" or "licenses").

    Attributes:
        of_type(str): The type of asset to download (must be either
            "templates" or "licenses").
        extension (str): The file extension of the files to search for.
        url (str): The repo to search for files in.
        files (list[str]): A series of file URLs.
        completed (int): The number of files that have been downloaded.
    """

    __slots__ = ("of_type", "extension", "url", "files", "completed")

    def __init__(self, of_type):
        if of_type not in ("templates", "licenses"):
            return DownloadError("You can only download templates or licenses")

        self.of_type = of_type
        if of_type == "templates":
            self.extension = "nsx"
            self.url = f"{REPO_URL}/{TEMPLATE_SUFFIX}"
        else:
            self.extension = "txt"
            self.url = LICENSE_URL
        self.files = []
        self.completed = 0

    @property
    def progress(self):
        """The download progress as a percentage.

        Returns:
            float
        """
        return (100 / len(self.files)) * self.completed

    def fetch(self):
        """Fetch the files to download.

        Raises:
            DownloadError: There was a problem fetching the files.
        """
        self.files = []

        try:
            with request.urlopen(self.url) as r:
                data = r.readlines()
        except HTTPError as exc:
            raise DownloadError(
                f"Fetch failed (GitHub returned {exc.code})"
            ) from None

        for i, line in enumerate(data):
            if b'role="rowheader"' in line:
                path = data[i + 1].split(b'"')[-2].decode()
                if path.endswith(f".{self.extension.lstrip('.')}"):
                    self.files.append("".join(path.split("blob/")))

    async def _download_files(self):
        try:
            for f in self.files:
                with request.urlopen(f"{RAW_URL}/{f}") as r:
                    with open(
                        (CONFIG_DIR / self.of_type) / f.split("/")[-1], "wb"
                    ) as f:
                        f.write(r.read())
                        self.completed += 1

                await asyncio.sleep(0)

        except HTTPError as exc:
            raise DownloadError(
                f"Download failed (GitHub returned {exc.code})"
            ) from None

    async def _display_progress(self):
        while True:
            cprint(
                "prc",
                f"Downloading {self.of_type}... {self.progress:,.0f}%",
                end="\r",
            )
            if self.progress == 100:
                return
            await asyncio.sleep(0)

    def download(self, display_progress=False):
        """Download files. The files will be fetched automatically if
        they have not already been.

        Args:
            display_progress (bool): Whether to display the download's
                progress in the terminal. Defaults to False.

        Raises:
            DownloadError: There was a problem fetching the files.
        """
        if not self.files:
            self.fetch()

        loop = asyncio.get_event_loop()
        download = loop.create_task(self._download_files())
        if display_progress:
            display = loop.create_task(self._display_progress())
            display.add_done_callback(lambda x: print())
        loop.run_until_complete(download)
