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
import logging
import os
import sys
from pathlib import Path
from platform import python_implementation

from nusex import TEMP_DIR, TEMPLATE_DIR, Profile
from nusex.blueprints import PythonBlueprint
from nusex.constants import LICENSE_DIR
from nusex.errors import BuildError, IncompatibilityError
from nusex.helpers import cprint, run, validate_name
from nusex.spec import NSXSpecIO

ATTRS = (
    "PROJECTNAME",
    "PROJECTAUTHOR",
    "PROJECTAUTHOREMAIL",
    "PROJECTURL",
    "PROJECTVERSION",
    "PROJECTDESCRIPTION",
    "PROJECTLICENSE",
    "PROJECTYEAR",
    "LICENSEBODY",
    "PROJECTBASEEXC",
)

log = logging.getLogger(__name__)


class Template:
    """A class in which to create, load, modify, and save templates.

    Args:
        name (:obj:`str`): The name of the template. If the template
            does not exist, a new one is created, otherwise an existing
            one is loaded.

    Keyword Args:
        installs (:obj:`list[str]`): A list of dependancies to be
            installed when the template is deployed. Defaults to an
            empty list.
        as_addon_for (:obj:`str`): The name of the template this
            template is an add-on for. Defaults to an empty string.

    Attributes:
        path (:obj:`pathlib.Path`): The complete filepath to the
            template.
        data (:obj:`dict[str, Any]`): The data for the template.

    .. versionchanged:: 1.2
            Added ``as_addon_for`` keyword argument.
    """

    __slots__ = ("path", "data", "_installs", "_as_addon_for")

    def __init__(self, name, *, installs=[], as_addon_for=""):
        self.path = TEMPLATE_DIR / f"{name}.nsx"
        self._installs = installs
        self._as_addon_for = as_addon_for

        if not self.path.exists():
            log.info(f"[{name}] Not found; creating new...")
            return self.create_new(name)

        log.info(f"[{name}] Loading data...")
        self.load()

    def __str__(self):
        return self.path.stem

    def __repr__(self):
        return (
            f"<Template name={self.name!r} files={len(self.data['files'])!r}>"
        )

    def __eq__(self, other):
        return self.name == other.name

    def __ne__(self, other):
        return self.name != other.name

    def __getitem__(self, key):
        return self.data["files"][key]

    @property
    def name(self):
        """The name of the template.

        Returns:
            :obj:`str`
        """
        return self.path.stem

    @property
    def exists(self):
        """Whether the template exists on disk.

        Returns:
            :obj:`bool`
        """
        return self.path.is_file()

    def create_new(self, name):
        """Create a new template. This should never need to be
        called as templates are created automatically when necessary
        upon object instantiation.

        Args:
            name (:obj:`str`): The name of the template.

        Raises:
            :obj:`TemplateError`: The provided name is invalid.
            :obj:`AlreadyExists`: The template already exists on disk.
        """
        validate_name(name, self.__class__.__name__)
        self.data = NSXSpecIO().defaults
        log.debug(f"[{self.name}] Data = {self.data}")

    def load(self):
        """Load an existing template. This should never need to be
        called as templates are loaded automatically when necessary upon
        object instantiation.

        Raises:
            :obj:`FileNotFoundError`: The template does not exist on
                disk.
        """
        self.data = NSXSpecIO().read(self.path)
        log.debug(f"[{self.name}] Files = {list(self.data['files'].keys())}")

    def save(self):
        """Save this profile.

        Raises:
            :obj:`TemplateError`: The profile data has been improperly
                modified.
        """
        NSXSpecIO().write(self.path, self.data)
        log.info(f"[{self.name}] Saved to {self.path}")

    def delete(self):
        """Delete this template.

        Raises:
            :obj:`FileNotFoundError`: The template does not exist on
                disk.
        """
        os.remove(self.path)
        log.info(f"[{self.name}] Deleted from {self.path}")

    def rename(self, new_name):
        """Rename this template.

        Args:
            new_name (:obj:`str`): The new name for the template.

        Raises:
            :obj:`TemplateError`: The new name for the template is
                invalid.
            :obj:`AlreadyExists`: The new name for the template is
                already being used by a profile.
            :obj:`FileNotFoundError`: The template does not exist on
                disk.
        """
        validate_name(new_name, self.__class__.__name__)
        new_path = f"{self.path}".replace(self.path.stem, new_name)
        self.path.rename(new_path)
        self.path = TEMPLATE_DIR / f"{new_name}.nsx"
        log.info(f"[{self.name}] Renamed")

    @classmethod
    def from_cwd(
        cls,
        name,
        *,
        project_name=None,
        blueprint=None,
        installs=[],
        as_addon_for="",
        ignore_exts=set(),
        ignore_dirs=set(),
    ):
        """Create a template using files from the current working
        directory.

        Args:
            name (:obj:`str`): The name of the template.

        Keyword Args:
            project_name (:obj:`str`): The name to use as the project
                name when building the project. If this is None, the
                name of the parent directory is used. Defaults to None.
            blueprint (:obj:`Blueprint`): The language blueprint to use.
                If this is None, the Python blueprint is selected.
                Defaults to None.
            installs (:obj:`list[str]`): A list of dependencies to
                install when this template is deployed. Defaults to an
                empty list.
            as_addon_for (:obj:`str`): The name of the template this
                template is an add-on for. Defaults to an empty string.
            ignore_exts (:obj:`set[str]`): A set of file extensions to
                ignore. Defaults to an empty set.
            ignore_dirs (:obj:`set[str]`): A set of directories to
                ignore. Defaults to an empty set.

        Returns:
            :obj:`Template`: The newly created template.

        .. versionchanged:: 1.1
            Added ``project_name`` and ``blueprint`` keyword arguments.

        .. versionchanged:: 1.2
            Added ``as_addon_for`` keyword argument.
        """
        c = cls(name, installs=installs, as_addon_for=as_addon_for)
        c.build(
            project_name=project_name,
            blueprint=blueprint,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_dir(
        cls,
        name,
        path,
        *,
        project_name=None,
        blueprint=None,
        installs=[],
        as_addon_for="",
        ignore_exts=set(),
        ignore_dirs=set(),
    ):
        """Create a template using files from a specific directory.

        Args:
            name (:obj:`str`): The name of the template.
            path (:obj:`str` | :obj:`os.PathLike`): The path to the
                files to build the template with.

        Keyword Args:
            project_name (:obj:`str`): The name to use as the project
                name when building the project. If this is None, the
                name of the parent directory is used. Defaults to None.
            blueprint (:obj:`Blueprint`): The language blueprint to use.
                If this is None, the Python blueprint is selected.
                Defaults to None.
            installs (:obj:`list[str]`): A list of dependencies to
                install when this template is deployed. Defaults to an
                empty list.
            as_addon_for (:obj:`str`): The name of the template this
                template is an add-on for. Defaults to an empty string.
            ignore_exts (:obj:`set[str]`): A set of file extensions to
                ignore. Defaults to an empty set.
            ignore_dirs (:obj:`set[str]`): A set of directories to
                ignore. Defaults to an empty set.

        Returns:
            :obj:`Template`: The newly created template.

        .. versionchanged:: 1.1
            Added ``project_name`` and ``blueprint`` keyword arguments.

        .. versionchanged:: 1.2
            Added ``as_addon_for`` keyword argument.
        """
        c = cls(name, installs=installs, as_addon_for=as_addon_for)
        c.build(
            project_name=project_name,
            root_dir=path,
            blueprint=blueprint,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )
        return c

    @classmethod
    def from_repo(
        cls,
        name,
        url,
        *,
        project_name=None,
        blueprint=None,
        installs=[],
        as_addon_for="",
        ignore_exts=set(),
        ignore_dirs=set(),
    ):
        """Create a template using files from a GitHub repository.

        Args:
            name (:obj:`str`): The name of the template.
            url (:obj:`str`): The URL of the GitHub repository to clone.

        Keyword Args:
            project_name (:obj:`str`): The name to use as the project
                name when building the project. If this is None, the
                name of the parent directory is used. Defaults to None.
            blueprint (:obj:`Blueprint`): The language blueprint to use.
                If this is None, the Python blueprint is selected.
                Defaults to None.
            installs (:obj:`list[str]`): A list of dependencies to
                install when this template is deployed. Defaults to an
                empty list.
            as_addon_for (:obj:`str`): The name of the template this
                template is an add-on for. Defaults to an empty string.
            ignore_exts (:obj:`set[str]`): A set of file extensions to
                ignore. Defaults to an empty set.
            ignore_dirs (:obj:`set[str]`): A set of directories to
                ignore. Defaults to an empty set.

        Returns:
            :obj:`Template`: The newly created template.

        Raises:
            :obj:`BuildError`: Cloning the repository failed.

        .. versionchanged:: 1.1
            Added ``project_name`` and ``blueprint`` keyword arguments.

        .. versionchanged:: 1.2
            Added ``as_addon_for`` keyword argument.
        """
        os.makedirs(TEMP_DIR, exist_ok=True)
        os.chdir(TEMP_DIR)

        log.debug(f"[{name}] Cloning {url} into {TEMP_DIR}...")
        run(f"git clone {url}")

        repo_dir = TEMP_DIR / url.split("/")[-1].replace(".git", "")
        if not repo_dir.exists():
            raise BuildError(
                "Cloning the repo failed. Is Git installed? Is the URL "
                "correct?"
            )

        os.chdir(repo_dir)
        log.debug(f"[{name}] Building from {os.path.abspath(os.curdir)}...")
        return cls.from_cwd(
            name,
            project_name=project_name,
            blueprint=blueprint,
            installs=installs,
            as_addon_for=as_addon_for,
            ignore_exts=ignore_exts,
            ignore_dirs=ignore_dirs,
        )

    def get_file_listing(
        self, root_dir, *, ignore_exts=set(), ignore_dirs=set()
    ):
        """Get a list of files to include in this template.

        Args:
            root_dir (:obj:`str`): The root directory that nusex will
                search from.

        Keyword Args:
            ignore_exts (:obj:`set[str]`): A set of file extensions to
                ignore. Defaults to an empty set.
            ignore_dirs (:obj:`set[str]`): A set of directories to
                ignore. Defaults to an empty set.

        Returns:
            :obj:`list[pathlib.Path]`: A list of filepaths.
        """

        def is_valid(path):
            return (
                path.is_file()
                and all(i not in path.parts for i in true_dir_ignores)
                and all(i[1:] not in f"{path}" for i in wild_dir_ignores)
                and all(i != path.suffix[1:] for i in ignore_exts)
            )

        wild_dir_ignores = set(
            filter(lambda x: x.startswith("*"), ignore_dirs)
        )
        true_dir_ignores = ignore_dirs - wild_dir_ignores
        log.debug(f"[{self.name}] Ignoring exts: {ignore_exts}")
        log.debug(f"[{self.name}] Ignoring dirs (true): {true_dir_ignores}")
        log.debug(f"[{self.name}] Ignoring dirs (wild): {wild_dir_ignores}")

        files = filter(lambda p: is_valid(p), Path(root_dir).rglob("*"))
        return list(files)

    def build(
        self,
        *,
        project_name=None,
        files=[],
        root_dir=".",
        blueprint=None,
        **kwargs,
    ):
        """Build this template. View the
        :doc:`template guide <../guide/templates>` to see what this
        command does in more detail.

        Keyword Args:
            project_name (:obj:`str`): The name to use as the project
                name when building the project. If this is None, the
                name of the parent directory is used. Defaults to None.
            files (:obj:`list[str]`): The list of files to include in
                this template. If no files are specified, the file
                listing is automatically retrieved.
            root_dir (:obj:`str`): The root directory that nusex will
                search from. Defaults to the current directory.
            blueprint (:obj:`Blueprint`): The language blueprint to use.
                If this is None, the Python blueprint is selected.
                Defaults to None.
            **kwargs (:obj:`Any`): Arguments for the
                :obj:`get_file_listing` method.

        .. versionchanged:: 1.1
            Added ``blueprint`` keyword argument.
        """

        def resolve_key(path):
            path = "/".join(f"{path.resolve()}".split(os.sep)[nparts:])
            return path.replace(project_name, "PROJECTNAME")

        if not project_name:
            project_name = Path(root_dir).resolve().parts[-1]

        if not blueprint:
            blueprint = PythonBlueprint

        if not files:
            files = self.get_file_listing(
                root_dir,
                ignore_exts=kwargs.pop("ignore_exts", set()),
                ignore_dirs=kwargs.pop("ignore_dirs", set()),
            )

        self.data["installs"] = self._installs
        self.data["as_addon_for"] = self._as_addon_for

        log.info(f"[{self.name}] Using project name: {project_name}")
        log.info(f"[{self.name}] Using blueprint: {blueprint.__name__}")
        log.info(f"[{self.name}] As add-on for: " + self.data["as_addon_for"])
        log.info(f"[{self.name}] For language: " + self.data["language"])
        log.info(f"[{self.name}] With {len(files):,} files")
        log.debug(f"[{self.name}] With files: {files}")

        nparts = len(Path(root_dir).resolve().parts)
        self.data["files"] = {resolve_key(f): f.read_bytes() for f in files}

        bp = blueprint(project_name, self.data)
        self.data = bp().data

        log.info(f"[{self.name}] Build successful")

    def deploy(self, *, project_name=None, destination="."):
        """Deploy this template.

        Keyword Args:
            project_name (:obj:`str`): The name to use as the project
                name when deploying the project. If this is None, the
                name of the parent directory is used. Defaults to None.
            destination (:obj:`str`): The path to deploy this template
                to. Defaults to the current directory.

        .. versionchanged:: 1.1
            Added ``project_name`` keyword argument.
        """

        def resolve_version(key):
            if key == "CALVER":
                return dt.date.today().strftime("%Y.%m.%d")

            return key

        def resolve_license_info(key):
            with open(LICENSE_DIR / f"{key}.txt", encoding="utf-8") as f:
                lines = f.read().split("\n")

            start = [i for i, line in enumerate(lines) if line == "---"][
                -1
            ] + 2

            return (
                lines[1][7:].replace('"', "'"),
                "\n".join(lines[start:])
                .replace("[year]", f"{dt.date.today().year}")
                .replace("[fullname]", profile["author_name"]),
            )

        if not project_name:
            project_name = Path(destination).resolve().parts[-1]
        project_slug = project_name.lower().replace(" ", "_").replace("-", "_")
        project_error = project_name.replace("_", " ").title().replace(" ", "")

        profile = Profile.current()
        lic_name, lic_body = resolve_license_info(profile["preferred_license"])

        var_mapping = {
            b"PROJECTNAME": project_name,
            b"PROJECTVERSION": resolve_version(profile["starting_version"]),
            b"PROJECTDESCRIPTION": profile["default_description"],
            b"PROJECTURL": f"{profile['git_profile_url']}/{project_slug}",
            b"PROJECTAUTHOREMAIL": profile["author_email"],
            b"PROJECTAUTHOR": profile["author_name"],
            b"PROJECTLICENSE": lic_name,
            b"LICENSEBODY": lic_body,
            b"PROJECTYEAR": f"{dt.date.today().year}",
            b"PROJECTBASEEXC": f"{project_error}Error",
        }

        log.info(f"[{self.name}] Using project name: {project_name}")
        log.info(f"[{self.name}] Using project slug: {project_slug}")
        log.debug(f"[{self.name}] Using var mapping: {var_mapping}")

        for name, data in self.data["files"].items():
            name = name.replace("PROJECTNAME", project_slug)

            dirs = name.split("/")[:-1]
            if dirs:
                os.makedirs(f"{destination}/" + "/".join(dirs), exist_ok=True)

            for k, v in var_mapping.items():
                data = data.replace(k, v.encode())

            with open(f"{destination}/{name}", "wb") as f:
                f.write(data)

        meta = {
            "template": self.name,
            "files": list(self.data["files"].keys()),
            "language": self.data["language"],
        }
        if not self.data["as_addon_for"]:
            with open(f"{destination}/.nusexmeta", "w") as f:
                json.dump(meta, f)

        log.info(f"[{self.name}] Deployment successful")

    def install_dependencies(self):
        """Install this template's dependencies. Note that this does not
        work on PyPy Python implementations."""
        installs = self.data["installs"]

        if not installs:
            log.info(f"[{self.name}] No dependencies to install")
            return

        if python_implementation() == "PyPy":
            raise IncompatibilityError(
                "Dependency installation is not supported on PyPy "
                "implementations"
            )

        if self.data["language"] != "python":
            cprint(
                "war",
                "Dependency installation is not supported on languages other "
                "than Python.",
            )
            return

        log.info(f"[{self.name}] Installing {len(installs):,} dependencies...")
        run(f"{sys.executable} -m pip install " + " ".join(installs))

    def check(self):
        """Check the template manifest, including line changes.

        Returns:
            :obj:`dict[str, list[tuple[int, str]]]`: The template
            manifest. The keys are always file names, and the values are
            tuples of the line numbers and line values that have been
            changed. This may not always be present.
        """
        manifest = {}

        for file, data in self.data["files"].items():
            manifest.update({file: []})

            try:
                for i, line in enumerate(data.decode().split("\n")):
                    if any(a in line for a in ATTRS):
                        manifest[file].append((i + 1, line))
            except UnicodeDecodeError:
                # If it errors here, no modifications could have been
                # made.
                ...

        return manifest
