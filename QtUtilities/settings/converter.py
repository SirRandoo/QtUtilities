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

__all__ = {"Converter"}


class Converter:
    """The main class for converting raw values into their Python representation."""
    
    def __init__(self, serializers: dict=None, deserializers: dict=None, managers: dict=None):
        self._serializers = serializers or dict()  # type: typing.Dict[str, typing.Callable]
        self._deserializers = deserializers or dict()  # type: typing.Dict[str, typing.Callable]
        self._managers = managers or dict()  # type: typing.Dict[str, typing.Callable]
    
    # Registry Methods #
    def add_serializer(self, identifier: str, serializer: typing.Callable):
        """Adds a serializer to the converter registry."""
        if identifier.lower() in self._serializers:
            raise KeyError(f'"{identifier}" is already registered!')
        
        else:
            self._serializers[identifier.lower()] = serializer
    
    def remove_serializer(self, identifier: str):
        """Removes a serializer from the converter registry."""
        if identifier.lower() in self._serializers:
            self._serializers.pop(identifier.lower())
            
        else:
            raise KeyError(f'"{identifier}" is not registered!')
    
    def add_deserializer(self, identifier: str, deserializer: typing.Callable):
        """Adds a deserializer to the converter registry."""
        if identifier.lower() in self._deserializers:
            raise KeyError(f'"{identifier}" is already registered!')
        
        else:
            self._deserializers[identifier.lower()] = deserializer
    
    def remove_deserializer(self, identifier: str):
        """Removes a deserializer from the converter registry."""
        if identifier.lower() in self._deserializers:
            self._deserializers.pop(identifier.lower())
            
        else:
            raise KeyError(f'"{identifier}" is not registered!')
    
    def add_manager(self, identifier: str, manager: typing.Callable):
        """Adds a manager to the converter registry."""
        if identifier.lower() in self._managers:
            raise KeyError(f'"{identifier} is already registered!')
        
        else:
            self._managers[identifier.lower()] = manager
        
    def remove_manager(self, identifier: str):
        """Removes a manager from the converter registry."""
        if identifier.lower() in self._managers:
            self._managers.pop(identifier.lower())
            
        else:
            raise KeyError(f'"{identifier}" is not registered!')
    
    def has_serializer(self, identifier: str) -> bool:
        """Returns whether or not a serializer is in the registry."""
        return identifier.lower() in self._serializers
    
    def has_deserializer(self, identifier: str) -> bool:
        """Returns whether or not a deserializer is in the registry."""
        return identifier.lower() in self._deserializers
    
    def has_manager(self, identifier: str) -> bool:
        """Returns whether or not a manager is in the registry."""
        return identifier.lower() in self._managers
    
    def get_serializer(self, identifier: str) -> typing.Callable:
        """Returns the serializer, if any, for the given identifier."""
        return self._serializers[identifier.lower()]
    
    def get_deserializer(self, identifier: str) -> typing.Callable:
        """Returns the deserializer, if any, for the given identifier."""
        return self._deserializers[identifier.lower()]
    
    def get_manager(self, identifier: str) -> typing.Callable:
        """Returns the manager, if any, for the given identifier."""
        return self._managers[identifier.lower()]
    
    def get_serializer_id(self, serializer: typing.Callable) -> str:
        """Returns the identifier, if any, for the given serializer."""
        for key, value in self._serializers.items():
            if value == serializer:
                return key
        
        raise IndexError
    
    def get_deserializer_id(self, deserializer: typing.Callable) -> str:
        """Returns the identifier, if any, for the given deserializer."""
        for key, value in self._deserializers.items():
            if value == deserializer:
                return key
        
        raise IndexError
    
    def get_manager_id(self, manager: typing.Callable) -> str:
        """Returns the identifier, if any, for the given manager."""
        for key, value in self._managers.items():
            if value == manager:
                return key
            
        raise IndexError
    
    # Conversion Methods #
    def deserialize(self, deserializer: str, raw) -> object:
        """Converts a raw value into a Python object."""
        if isinstance(raw, str) and self.has_deserializer(deserializer):
            try:
                return self._deserializers[deserializer.lower()](raw)
            
            except Exception as e:
                raise ValueError from e
            
        return raw
    
    def serialize(self, serializer: str, obj) -> object:
        """Converts a Python object into a raw value."""
        if self.has_serializer(serializer):
            try:
                return self._serializers[serializer.lower()](obj)
            
            except Exception as e:
                raise ValueError from e
        
        else:
            return str(obj)
