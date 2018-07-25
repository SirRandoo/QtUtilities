# This file is part of QtUtilities.
#
# QtUtilities is free software:
# you can redistribute it and/or
# modify it under the terms of the
# GNU Lesser General Public License
# as published by the Free Software
# Foundation, either version 3 of
# the License, or (at your option)
# any later version.
#
# QtUtilities is
# distributed in the hope that it
# will be useful, but WITHOUT ANY
# WARRANTY; without even the implied
# warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of
# the GNU Lesser General Public License
# along with QtUtilities.
# If not, see <http://www.gnu.org/licenses/>.
import typing

from PyQt5 import QtCore


class File(QtCore.QObject):
    """A context manager for managing files through the Qt event loop."""

    def __init__(self, file: str, mode: typing.Union[QtCore.QIODevice.OpenMode, QtCore.QIODevice.OpenModeFlag]=None):
        if mode is None:
            mode = QtCore.QFile.ReadOnly | QtCore.QFile.Text

        super(File, self).__init__()
        self._file = QtCore.QFile(file)
        self._mode = mode

    # File Methods #
    def read_all(self) -> typing.Union[str, bytes]:
        """Reads the entire contents of the file."""
        if self._file.isOpen():
            if self._file.isReadable():
                self._file.seek(0)
                content = self._file.readAll()  # type: QtCore.QByteArray

                if not content.isNull():
                    if self.is_binary():
                        return content.data()

                    elif self.is_text():
                        return content.data().decode()

                else:
                    raise IOError("Content is null!")

            else:
                raise IOError("File not readable!")

        else:
            raise IOError("File not open!")

    def read_line(self) -> typing.Union[str, bytes]:
        """Reads a single line from the file."""
        if self._file.isOpen():
            if self._file.isReadable():
                content = self._file.readLine()  # type: QtCore.QByteArray

                if not content.isNull():
                    if self.is_binary():
                        return content.data()

                    elif self.is_text():
                        return content.data().decode()

                else:
                    raise IOError("Content is null!")

            else:
                raise IOError("File not readable!")

        else:
            raise IOError("File not open!")

    def read(self, size: int) -> typing.Union[str, bytes]:
        """Reads at most `size` from the file."""
        if self._file.isOpen():
            if self._file.isReadable():
                content = self._file.read(size)  # type: QtCore.QByteArray

                if not content.isNull():
                    if self.is_binary():
                        return content.data()

                    elif self.is_text():
                        return content.data().decode()

                else:
                    raise IOError("Content is null!")

            else:
                raise IOError("File not readable!")

        else:
            raise IOError("File not open!")

    def write(self, content: typing.Union[str, bytes]) -> int:
        """Writes content to the file."""
        if self._file.isOpen():
            if self._file.isWritable():
                if type(content) == str:
                    content = content.encode()

                return self._file.write(content)

            else:
                raise IOError("File not writeable!")

        else:
            raise IOError("File not open!")

    def seek(self, position: int):
        """Seeks to a position in the file."""
        if self._file.isOpen():
            self._file.seek(position)

        else:
            raise IOError("File not open!")

    def close(self):
        """Closes the underlying file."""
        if self._file.isOpen():
            self._file.close()

        else:
            raise IOError("File not open!")

    def at_end(self) -> bool:
        """Returns whether or not the cursor is at the end of the file."""
        if self._file.isOpen():
            return self._file.atEnd()

        else:
            raise IOError("File not open!")

    def size(self) -> int:
        """Returns the size of the file."""
        if self._file.isOpen():
            return self._file.size()

        else:
            raise IOError("File not open!")

    # Utility Methods #
    def is_binary(self) -> bool:
        """Returns whether or not this file is opened in binary mode."""
        return not bool(self._mode & QtCore.QFile.Text)

    def is_text(self) -> bool:
        """Returns whether or not this file is opened in text mode."""
        return bool(self._mode & QtCore.QFile.Text)

    def __enter__(self) -> 'File':
        if not self._file.isOpen():
            self._file.open(self._mode)

        if self._file.error() == QtCore.QFile.PermissionsError:
            raise PermissionError(self._file.errorString())

        elif self._file.error() == QtCore.QFile.UnspecifiedError:
            raise IOError(self._file.errorString())

        elif self._file.error() == QtCore.QFile.AbortError:
            raise IOError(self._file.errorString())

        elif self._file.error() == QtCore.QFile.OpenError:
            raise IOError(self._file.errorString())

        elif self._file.error() == QtCore.QFile.ResourceError:
            raise IOError(self._file.errorString())

        elif self._file.error() == QtCore.QFile.FatalError:
            raise RuntimeError(self._file.errorString())

        else:
            return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._file.isOpen():
            self._file.flush()
            self._file.close()

        self.deleteLater()
