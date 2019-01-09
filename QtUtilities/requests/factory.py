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
from PyQt5 import QtCore, QtNetwork

from . import errors
from .response import Response

__all__ = {"Factory"}


class Factory(QtCore.QObject):
    def __init__(self, parent=None, manager: QtNetwork.QNetworkAccessManager = None):
        # Super Call  #
        super(Factory, self).__init__(parent=parent)
        
        #  Internal Attributes  #
        self._manager = manager if manager is not None else QtNetwork.QNetworkAccessManager(parent=self)
    
    def request(self, **kwargs) -> Response:
        """Performs a `requests` like request."""
        
        #  Validation  #
        if "url" not in kwargs:
            raise errors.UrlMissingError
        
        if "operation" not in kwargs:
            raise errors.OperationMissingError
        
        # Stitching  #
        _url = QtCore.QUrl(kwargs.pop("url"))
        _request = QtNetwork.QNetworkRequest(_url)
        _data = QtCore.QBuffer()
        
        if "params" in kwargs:
            query = QtCore.QUrlQuery()
            
            for k, v in kwargs.pop("params", {}).items():
                query.addQueryItem(k, v)
            
            _url.setQuery(query)
        
        if "data" in kwargs:
            _data.setData(kwargs.pop("data").encode())
        
        if "headers" in kwargs:
            for k, v in kwargs.pop("headers").items():
                _request.setRawHeader(k.encode(), v.encode())
        
        _operation = kwargs.pop("operation").upper()  # type: str
        
        _reply = self._manager.sendCustomRequest(_request, _operation.encode(), _data if _data.size() > 0 else None)
        _response = Response()
        _response.follow_reply(_reply)
        return _response
    
    def get(self, url: str, params: dict = None, **kwargs) -> Response:
        """Performs a get operation."""
        if params is None:
            params = dict()
        
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(operation="GET", url=url, params=params, **kwargs)
    
    def put(self, url: str, data: str = None, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(operation="PUT", url=url, data=data, **kwargs)
    
    def post(self, url: str, data: str = None, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(url=url, operation="POST", data=data, **kwargs)
    
    def head(self, url: str, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(url=url, operation="HEAD")
    
    def patch(self, url: str, data: str = None, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(url=url, operation="PATCH", data=data, **kwargs)
    
    def delete(self, url: str, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(operation="DELETE", url=url, **kwargs)
    
    def options(self, url: str, **kwargs) -> Response:
        if "operation" in kwargs:
            kwargs.pop("operation")
        
        return self.request(operation="OPTIONS", url=url, **kwargs)
