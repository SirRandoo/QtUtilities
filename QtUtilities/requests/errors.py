# This file is part of QtUtilities.
#
# QtUtilities is free software:
# you can redistribute it
# and/or modify it under the
# terms of the GNU Lesser General
# Public License as published by
# the Free Software Foundation,
# either version 3 of the License,
# or (at your option) any later
# version.
#
# QtUtilities is distributed in
# the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without
# even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A
# PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more
# details.
#
# You should have received a copy of the
# GNU Lesser General Public License along
# with QtUtilities.  If not,
# see <https://www.gnu.org/licenses/>.
__all__ = {"RequestError", "UrlMissingError", "DataMissingError",
           "OperationMissingError"}


#  Generic Exceptions  #
class RequestError(Exception):
    """The generic exception for request related errors."""


# Specified Exceptions  #
class UrlMissingError(RequestError):
    """The request required a url to perform the
    operation on, but no url was specified."""


class DataMissingError(RequestError):
    """The request operation required data, but no data
    was specified."""


class OperationMissingError(RequestError):
    """The request required an operation, but no operation
    was specified."""
