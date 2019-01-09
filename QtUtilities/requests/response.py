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
import functools
import io
import json
import typing

from PyQt5 import QtCore, QtNetwork

__all__ = {"Response"}


class Response:
    """Represents a response dataclass for
    requests made with this package.  The
    reasoning behind this is that QNetworkReply's
    cannot be passed around without experiencing
    a fatal crash."""
    
    def __init__(self):
        #  Internal attributes  #
        self._urls: list = []
        self._params: dict = {}
        self._host: str = None
        self._scheme: str = None
        self._domain: str = None
        self._port: int = None
        self._cookies: list = []
        self._content = io.BytesIO()
        self._headers: list = []
        self._error_code: int = QtNetwork.QNetworkReply.NoError
        self._error_string: str = None
    
    #  Data Methods  #
    def was_redirected(self) -> bool:
        """Returns whether or not the request
        was redirected."""
        return len(self._urls) > 1
    
    def is_ok(self) -> bool:
        """Returns whether or not the request's
        status code is OK."""
        return self._error_code == QtNetwork.QNetworkReply.NoError
    
    def json(self, encoder=None) -> dict:
        """Attempts to encode the content into a
        JSON object.  For error handling, refer
        to the passed encoder or `json.loads`."""
        if encoder is not None:
            assert callable(encoder), "Decoder must be a callable!"
        
        else:
            encoder = json.loads
        
        return encoder(self.raw())
    
    def raw(self) -> bytes:
        """Returns the raw data received from
        the request."""
        self._content.seek(0)
        return self._content.read()
    
    def content(self) -> str:
        """Returns the raw data received from
        the request as a string"""
        return self.raw().decode()
    
    # Error Methods #
    def error_code(self) -> int:
        """Returns the error code, if any."""
        return self._error_code
    
    def error_string(self) -> typing.Optional[str]:
        """Returns the error string, if any."""
        return self._error_string
    
    # Properties  #
    @property
    def headers(self) -> dict:
        """Returns the latest headers."""
        return self._headers[-1]
    
    @property
    def cookies(self) -> dict:
        """Returns the latest cookies."""
        if self._cookies:
            return self._cookies[-1]
        
        else:
            return dict()
    
    @property
    def url(self) -> QtCore.QUrl:
        """Returns the latest url."""
        return self._urls[-1]
    
    @property
    def scheme(self) -> str:
        """Returns the latest scheme."""
        return self.url.scheme()
    
    @property
    def domain(self):
        """Returns the latest domain."""
        return self.url.topLevelDomain()
    
    @property
    def host(self):
        """Returns the latest host."""
        return self.url.host()
    
    #  Internal Handlers  #
    def follow_reply(self, reply: QtNetwork.QNetworkReply):
        # Follows a reply until it's finished.  It
        # documents changes in the reply while it's
        #  being completed.  Changes include header
        #  changes and redirects.
        
        loop = QtCore.QEventLoop()
        reply.metaDataChanged.connect(
            lambda: self._headers.append(
                {hKey.data().decode(): hValue.data().decode() for hKey, hValue in reply.rawHeaderPairs()}))
        reply.redirected.connect(lambda x: self._urls.append(x))
        reply.finished.connect(loop.quit)
        reply.error.connect(functools.partial(setattr, self, '_error_code'))
        reply.error.connect(lambda: setattr(self, '_error_string', reply.errorString()))
        loop.exec()
        
        self._strip_reply(reply)
        reply.close()
        loop.deleteLater()
        reply.deleteLater()
    
    def _strip_reply(self, reply: QtNetwork.QNetworkReply):
        # Strips the completed reply of useful information.
        # Headers
        headers = {hKey.data().decode(): hValue.data().decode() for hKey, hValue in reply.rawHeaderPairs()}
        
        if self.headers != headers:
            self._headers.append(headers)
        
        # Content
        if reply.isReadable():
            self._content = io.BytesIO(reply.readAll())
        
        # Cookies
        manager: QtNetwork.QNetworkAccessManager = reply.manager()
        jar: QtNetwork.QNetworkCookieJar = manager.cookieJar()
        cookies = {cookie.name().data().decode(): cookie.value() for cookie in jar.allCookies()}
        
        if cookies != self.cookies:
            self._cookies.append(cookies)
        
        # Request
        request: QtNetwork.QNetworkRequest = reply.request()
        headers = {hKey.data().decode(): request.rawHeader(hKey).data().decode() for hKey in request.rawHeaderList()}
        
        if self._urls:
            if self._urls[0] != request.url():
                self._urls.insert(0, request.url())
        
        else:
            self._urls.append(request.url())
        
        if self._headers:
            if self._headers[0] != headers:
                self._headers.insert(0, headers)
        
        else:
            self._headers.append(headers)
