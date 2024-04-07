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


class NusexError(Exception):
    """The base exception class for nusex."""


class NusexUserError(NusexError):
    """An error occurred due to user error."""


class ProfileError(NusexUserError):
    """Something went wrong when working with a profile."""


class TemplateError(NusexUserError):
    """Something went wrong when working with a template."""


class BuildError(TemplateError):
    """A template failed to build."""


class DeploymentError(TemplateError):
    """A template failed to deploy."""


class AlreadyExists(NusexUserError):
    """A profile or template already exists."""


class DoesNotExist(NusexUserError):
    """A profile or template does not exist."""


class MigrationError(NusexUserError):
    """A migration or migration reversion failed."""


class DownloadError(NusexError):
    """A download failed to complete, or an invalid download request
    was submitted."""


class UnsupportedFile(NusexError):
    """An invalid file has been passed to a decoder, or a file larger
    than the file size limit has been included in a template."""


class IncompatibilityError(NusexError):
    """A operation is incompatible with your OS, Python version, or
    Python implementation."""
