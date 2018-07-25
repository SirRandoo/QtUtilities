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

from PyQt5 import QtCore, QtWidgets

from .converter import Converter

__all__ = {"Option"}


class Option(QtCore.QObject):
    """Represents a key-value option."""
    
    def __init__(self, key: str, value: typing.Any = None, *, parent: QtCore.QObject = None):
        # Super Call #
        super(Option, self).__init__(parent=parent)
        
        self.key = key.lower()
        self.value = value
        self.display_name = self.key.split(".")[-1].title()
        self.tooltip = None  # type: str
        self.converter = None  # type: Converter
        self._manager = None
        
        self._serializer = None  # type: typing.Callable
        self._deserializer = None  # type: typing.Callable
        
        self.label = QtWidgets.QLabel()
        self._widget = None  # type: QtWidgets.QWidget
        
        if self._manager is not None:
            self._manager = self._manager(self)
        
        if self._widget is None and self.value is not None:
            self._generate_widget()
    
    # Properties #
    @property
    def widget(self) -> QtWidgets.QWidget:
        """The "physical" representation of this option on the config GUI."""
        return self._widget
    
    @property
    def manager(self) -> object:
        return self._manager
    
    @property
    def serializer(self) -> typing.Callable:
        """Returns the serializer for this option's value."""
        return self._serializer
    
    @property
    def deserializer(self) -> typing.Callable:
        """Returns the deserializer identifier for this option's value."""
        return self._deserializer
    
    # Ui Methods #
    def _build_widget(self, widget: QtWidgets.QWidget):
        """Builds a widget from the current data."""
        if isinstance(widget, QtWidgets.QCheckBox):
            self.label.setText("")
            self.label.setDisabled(True)
            widget.setChecked(bool(self.value))
            widget.setText(self.display_name)
            
            if self.tooltip is not None:
                widget.setToolTip(self.tooltip)
            
            widget.clicked.connect(self._data_watcher)
        
        else:
            self.label.setText(self.display_name)
            self.label.setEnabled(True)
            
            if isinstance(widget, QtWidgets.QLineEdit):
                widget.setText(self.value if self.value is not None else "")
                widget.setClearButtonEnabled(True)
                widget.textChanged.connect(self._data_watcher)

                if self.tooltip is not None:
                    widget.setToolTip(self.tooltip)
            
            elif isinstance(widget, QtWidgets.QSpinBox) or \
                    isinstance(widget, QtWidgets.QDoubleSpinBox):
                widget.setValue(self.value if self.value is not None else 0)
                widget.setRange(-10000, 10000)
                widget.valueChanged.connect(self._data_watcher)

                if self.tooltip is not None:
                    widget.setToolTip(self.tooltip)
        
        self._widget = widget
    
    def _generate_widget(self):
        """Generates a widget based on the current value."""
        if isinstance(self.value, str):
            self.set_widget(QtWidgets.QLineEdit())

        elif isinstance(self.value, bool):
            self.set_widget(QtWidgets.QCheckBox())

        elif isinstance(self.value, int):
            self.set_widget(QtWidgets.QSpinBox())

        elif isinstance(self.value, float):
            self.set_widget(QtWidgets.QDoubleSpinBox())
    
    def _data_watcher(self):
        """Watches the option's widget for changes."""
        if isinstance(self._widget, QtWidgets.QCheckBox):
            self.value = self._widget.isChecked()
        
        elif isinstance(self._widget, QtWidgets.QLineEdit):
            self.value = self._widget.text()
        
        elif isinstance(self._widget, QtWidgets.QSpinBox) or isinstance(self._widget, QtWidgets.QDoubleSpinBox):
            self.value = self._widget.value()
    
    # Setter Methods #
    def set_serializer(self, serializer: str) -> 'Option':
        """Sets the serializer for this option."""
        if self.converter is not None:
            if self.converter.has_serializer(serializer):
                self._serializer = self.converter.get_serializer(serializer)
            
            else:
                raise KeyError(f'Serializer "{serializer}" does not exist!')
        
        else:
            raise ValueError("Converter object has not been set!")
    
        return self
    
    def set_deserializer(self, deserializer: str) -> 'Option':
        """Sets the option's current deserializer."""
        if self.converter is not None:
            if self.converter.has_deserializer(deserializer):
                self._deserializer = self.converter.get_deserializer(deserializer)
            
            else:
                raise KeyError(f'Deserializer "{deserializer}" does not exist!')
        
        else:
            raise ValueError("Converter object has not been set!")
        
        return self

    def set_manager(self, manager: typing.Callable) -> 'Option':
        """Sets the option's current manager."""
        if self._manager is not None:
            if hasattr(self._manager, "deleteLater"):
                self._manager.deleteLater()
        
        self._manager = manager(self)
        
        return self

    def set_widget(self, widget: QtWidgets.QWidget, from_manager: bool = None) -> 'Option':
        """Sets the option's current widget."""
        if self._widget is not None and not from_manager:
            try:
                self._widget.disconnect()
        
            except TypeError:
                pass
        
            self._widget.deleteLater()
    
        self._build_widget(widget)
    
        if self._manager is not None and not from_manager:
            self._manager.update_widget(self._widget)
        
        if self.parent() is not None:
            self.parent().prepare_widget()
        
        return self
    
    def set_display_name(self, display_name: str) -> 'Option':
        """Sets the option's current display name."""
        self.display_name = display_name
        return self
    
    def set_tooltip(self, tooltip: str) -> 'Option':
        """Sets the option's tooltip."""
        self.tooltip = tooltip
        return self
    
    # Conversion Methods #
    def serialize(self) -> object:
        """Serializes a Python object into a raw object."""
        if self._serializer is not None:
            serializer_id = self.converter.get_serializer_id(self._serializer)
        
        else:
            serializer_id = None
        
        if self._deserializer is not None:
            deserializer_id = self.converter.get_deserializer_id(self._deserializer)
        
        else:
            deserializer_id = None
        
        if self._manager is not None:
            manager_id = self._manager.id
        
        else:
            manager_id = None
        
        if self._serializer is not None:
            return dict(
                key=self.key,
                value=self._serializer(self.value),
                manager=manager_id,
                serializer=serializer_id,
                deserializer=deserializer_id,
                tooltip=self.tooltip,
                display=self.display_name
            )
        
        else:
            if isinstance(self.value, bool) \
                    or isinstance(self.value, int) \
                    or isinstance(self.value, float) \
                    or isinstance(self.value, list) \
                    or isinstance(self.value, str) \
                    or isinstance(self.value, dict) \
                    or self.value is None:
                return dict(
                    key=self.key,
                    value=self.value,
                    manager=manager_id,
                    serializer=serializer_id,
                    deserializer=deserializer_id,
                    tooltip=self.tooltip,
                    display=self.display_name
                )
            
            else:
                return dict(
                    key=self.key,
                    value=str(self.value),
                    manager=manager_id,
                    serializer=serializer_id,
                    deserializer=deserializer_id,
                    tooltip=self.tooltip,
                    display=self.display_name
                )
    
    @classmethod
    def deserialize(cls, data: dict, converters: Converter) -> 'Option':
        """Converts an option object into a JSON object."""
        obj = cls(data.pop("key"), data.get("value"))
        obj.tooltip = data.get("tooltip", obj.key)
        obj.display_name = data.get("display", obj.key.title())
        obj.converter = converters
        
        if data.get("manager"):
            if converters.has_manager(data.get("manager")):
                obj._manager = converters.get_manager(data.get("manager"))
        
        if data.get("serializer"):
            if converters.has_serializer(data.get("serializer")):
                obj._serializer = converters.get_serializer(data.get("serializer"))
                
                try:
                    obj.value = obj._serializer(obj.value)
                
                except ValueError:
                    pass
        
        if data.get("serializer"):
            if converters.has_deserializer(data.get("deserializer")):
                obj._deserializer = converters.get_deserializer(data.get("deserializer"))
        
        if obj._manager is not None:
            obj._manager = obj._manager(obj)
            
        if isinstance(obj.value, str):
            obj.set_widget(QtWidgets.QLineEdit())

        elif isinstance(obj.value, bool):
            obj.set_widget(QtWidgets.QCheckBox())
        
        elif isinstance(obj.value, int):
            obj.set_widget(QtWidgets.QSpinBox())
        
        elif isinstance(obj.value, float):
            obj.set_widget(QtWidgets.QDoubleSpinBox())
        
        return obj
