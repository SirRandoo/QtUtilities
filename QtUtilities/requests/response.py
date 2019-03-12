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
import dataclasses
import functools
import io
import json
import typing

from PyQt5 import QtCore, QtNetwork

from .. import signals

__all__ = ['Response']


@dataclasses.dataclass(frozen=True)
class Response:
    """The response from a factory request.  This alone does nothing without
    a QNetworkReply to populate itself."""
    # Instance attributes
    urls: typing.List[QtCore.QUrl] = dataclasses.field(init=False, default_factory=list)
    params: typing.Dict[str, str] = dataclasses.field(init=False, default_factory=dict)
    host: str = dataclasses.field(init=False, default_factory=str)
    scheme: str = dataclasses.field(init=False, default_factory=str)
    domain: str = dataclasses.field(init=False, default_factory=str)
    port: int = dataclasses.field(init=False, default_factory=int)
    cookies: typing.Dict[str, typing.Any] = dataclasses.field(init=False, default_factory=dict)
    all_headers: typing.List[typing.Dict[str, str]] = dataclasses.field(init=False, default_factory=list)
    code: int = dataclasses.field(init=False, default=QtNetwork.QNetworkReply.NoError)
    error_string: str = dataclasses.field(init=False, default_factory=str)
    raw_content: io.BytesIO = dataclasses.field(init=False, default_factory=io.BytesIO)
    
    # Properties
    @property
    def url(self) -> QtCore.QUrl:
        """The last QUrl the request was redirected through, assuming redirects
        are allowed.  If no urls were cached, an empty QUrl will be returned."""
        try:
            return self.urls[-1]
        
        except IndexError:
            return QtCore.QUrl()
    
    @property
    def headers(self) -> typing.Dict[str, str]:
        """The last headers the request obtained from the host.  If no headers
        were received, an empty dict will be returned."""
        try:
            return self.all_headers[-1]
        
        except IndexError:
            return {}
        
    @property
    def redirected(self) -> bool:
        """Whether or not the request was redirected."""
        return len(self.urls) > 1
    
    @property
    def content(self):
        """The raw content received from the request transformed into a string."""
        self.raw_content.seek(0)
        
        return self.raw_content.read().decode()
    
    # Internal methods
    # noinspection PyUnresolvedReferences
    @classmethod
    def from_reply(cls, reply: QtNetwork.QNetworkReply) -> 'Response':
        """Slowly populates a new Response object with data from the request."""
        r = cls()
        
        # Signal mapping
        reply.metaDataChanged.connect(functools.partial(r._insert_headers, reply.rawHeaderPairs()))
        reply.redirected.connect(r._insert_url)
        reply.error.connect(r._update_code)
        reply.error.connect(functools.partial(r._update_error_string, reply.errorString()))
        
        # Wait until the request is finished before continuing
        signals.wait_for_signal(reply.finished)
        
        # Strip the remaining data from the reply, then mark it for deletion
        r._from_reply(reply)
        
        reply.close()
        reply.deleteLater()
        
        # Return the object
        return r
    
    def _from_reply(self, reply: QtNetwork.QNetworkReply):
        """Updates the Response object with the remaining data from the reply."""
        # Read the reply's body
        if reply.isReadable():
            self.raw_content.seek(0)
            self.raw_content.write(reply.readAll())
        
        # Store the cookies
        manager: QtNetwork.QNetworkAccessManager = reply.manager()
        jar: QtNetwork.QNetworkCookieJar = manager.cookieJar()
        object.__setattr__(self, 'cookies', {c.name().data().decode(): c.value() for c in jar.allCookies()})
    
    def _insert_headers(self, headers: typing.List[typing.Tuple[QtCore.QByteArray, QtCore.QByteArray]]):
        """Inserts the passed headers into the classes' header list."""
        # Declarations
        h = self.all_headers.copy()
        
        # Append passed headers to header list
        h.append({k.data().decode(): v.data().decode() for k, v in headers})
        
        # Forcibly update the header list
        object.__setattr__(self, 'headers', h)
    
    def _insert_url(self, url: QtCore.QUrl):
        """Inserts the passed url into the classes' url list."""
        # Declarations
        u = self.urls.copy()
        
        # Append passed url to url list
        u.append(url)
        
        # Forcible update the url list
        object.__setattr__(self, 'urls', u)
    
    def _update_code(self, code: int):
        """Updates the classes' code with the one passed."""
        object.__setattr__(self, 'code', code)
    
    def _update_error_string(self, string: str):
        """Updates the classes' error string with the one passed."""
        object.__setattr__(self, 'error_string', string)
    
    # Utility methods
    def is_okay(self) -> bool:
        """Whether or not the request was successful."""
        return self.code == QtNetwork.QNetworkReply.NoError
    
    def json(self, encoder: typing.Callable[[str], dict] = None) -> dict:
        """Converts the reply's body into a JSON object."""
        if encoder is None:
            encoder = json.loads
        
        return encoder(self.content)
    
    # Magic methods
    def __repr__(self):
        return f'<{self.__class__.__name__} url="{self.url.toDisplayString()}" code={self.code}>'
