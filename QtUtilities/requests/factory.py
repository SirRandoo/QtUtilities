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
import typing

from PyQt5 import QtCore, QtNetwork

from .response import Response

__all__ = ['Factory']


class Factory(QtCore.QObject):
    """The core of the requests package.
    
    This class is responsible for issuing requests through the application's
    QNetworkAccessManager, and returning the response in a synchronous way."""
    
    def __init__(self, manager: QtNetwork.QNetworkAccessManager = None, *, parent: QtCore.QObject = None):
        # Super call
        super(Factory, self).__init__(parent=parent)
        
        # Aliases
        self.get = functools.partial(self.request, 'GET')
        self.put = functools.partial(self.request, 'PUT')
        self.post = functools.partial(self.request, 'POST')
        self.head = functools.partial(self.request, 'HEAD')
        self.patch = functools.partial(self.request, 'PATCH')
        self.delete = functools.partial(self.request, 'DELETE')
        self.options = functools.partial(self.request, 'OPTIONS')
        
        # Private attributes
        self._manager = manager
        
        # Attribute validation
        if self._manager is None:
            self._manager = QtNetwork.QNetworkAccessManager(parent=self)
    
    # Core request method
    def request(self, op: str, url: typing.Union[QtCore.QUrl, str], *,
                params: typing.Dict[str, str] = None,
                headers: typing.Dict[typing.AnyStr, typing.AnyStr] = None,
                data: typing.Union[str, bytes, QtCore.QBuffer] = None,
                request: QtNetwork.QNetworkRequest = None):
        """Issues a new request.
        
        This method was designed to mimic standard synchronous libraries on PyPi,
        but on the Qt5 event loop.
        
        If request is passed, `url`, `params`, and `headers` will be ignored."""
        # Request object validation
        if request is not None:
            return self._request(op.upper(), request, data=data)
        
        else:
            request = QtNetwork.QNetworkRequest()
        
        # Url conversion
        if isinstance(url, str):
            url = QtCore.QUrl(url)
        
        # Url assignment
        request.setUrl(url)
        
        # Parameter stitching
        if params is not None:
            # Declaration and assignment
            q = QtCore.QUrlQuery()
            url.setQuery(q)
            
            # Populate the QUrlQuery
            for k, v in params.items():
                q.addQueryItem(k, v)
        
        # Header stitching
        if headers is not None:
            for k, v in headers.items():
                # Declarations
                key, value = None, None
                
                # Item validation
                if not isinstance(k, bytes):
                    key = k.encode(encoding='UTF-8')
                
                if not isinstance(v, bytes):
                    value = v.encode(encoding='UTF-8')
                
                # Populate request header
                request.setRawHeader(key, value)
        
        if data is not None:
            # Declarations
            buffer: QtCore.QBuffer = None
            
            # Buffer validation
            if isinstance(data, QtCore.QBuffer):
                buffer = data
            
            else:
                buffer = QtCore.QBuffer()
            
            # Data validation
            if isinstance(data, str):
                buffer.setData(data.encode(encoding='UTF-8'))
            
            elif isinstance(data, bytes):
                buffer.setData(data)
        
        else:
            buffer = None
        
        return self._request(op.upper(), request, data=buffer)
    
    def _request(self, op: str, request: QtNetwork.QNetworkRequest, *, data: QtCore.QBuffer = None):
        """The real implementation of the request method."""
        # Send the request & return the Response object
        return Response.from_reply(self._manager.sendCustomRequest(request, op.encode(encoding='UTF-8'), data))
