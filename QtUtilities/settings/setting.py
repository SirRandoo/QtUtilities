# This file is part of Decision Descent.
#
# Decision Descent is free software:
# you can redistribute it
# and/or modify it under the
# terms of the GNU Lesser General
# Public License as published by
# the Free Software Foundation,
# either version 3 of the License,
# or (at your option) any later
# version.
#
# Decision Descent is distributed in
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
# with Decision Descent.  If not,
# see <https://www.gnu.org/licenses/>.
import typing

from PyQt5 import QtCore, QtWidgets

__all__ = {"Setting"}


class Setting(QtCore.QObject):
    """A unified settings object."""
    value_changed = QtCore.pyqtSignal(object)
    
    def __init__(self, key: str, value: typing.Any = None, **kwargs):
        """
        :param key: A unique string used to identify this setting.
        :param value: The value of this setting.
        
        :param tooltip: A string that will be displayed when the user hovers
        over the setting's GUI object.
        :param display_name: A string that will be displayed beside the
        setting's GUI object.  This is typically a pretty version of `key`.
        :param status_tip: A string that will be displayed in the status bar
        when the user hovers over the setting's GUI object.
        :param whats_this: A string that will be displayed when the user
        clicks on the setting's GUI object in "What's This?" mode.
        :param hidden: Whether or not the setting's GUI object will be hidden
        from the user.
        :param read_only: Whether or not the user will be able to modify the
        setting's GUI object.
        :param converter: A callable that will transform a settings object into
        a visible GUI object.  All data should be serialized manually within
        the converter callable.
        """
        # Super Call #
        super(Setting, self).__init__(parent=kwargs.pop('parent', None))
        
        # "Public" Attributes #
        self.key: str = key
        self._value: typing.Any = value
        
        # "Internal" Attributes #
        self._data: dict = self._generate_data()
        self._display: QtWidgets.QWidget = None
        self._container: QtWidgets.QWidget = None
        self._item: QtWidgets.QTreeWidgetItem = None
        
        # "Internal" Calls #
        self._data.update(kwargs)
        self.setup()
    
    # Properties #
    @property
    def full_path(self) -> str:
        """Returns the full path for this setting."""
        if self.parent():
            return '{}/{}'.format(self.parent().full_path, self.key)
        
        else:
            return self.key
    
    @property
    def value(self) -> typing.Any:
        return self._value
    
    @value.setter
    def value(self, value: typing.Any):
        self._value = value
        
        self.value_changed.emit(self._value)
    
    @value.deleter
    def value(self):
        self._value = None
        
        self.value_changed.emit(self._value)
    
    @property
    def display_name(self) -> str:
        """The display name for this setting."""
        return self._data.get('display_name', self.key.replace('_', ' ').title())
    
    @display_name.setter
    def display_name(self, value: str):
        if value:
            self._data['display_name'] = value
        
        else:
            self._data['display_name'] = self.key.replace('_', ' ').title()
        
        if self._display is not None:
            method: callable = getattr(self._display, 'setText', None)
            
            if method:
                method(self._data['display_name'])
    
    @display_name.deleter
    def display_name(self):
        self._data['display_name'] = self.key.replace('_', ' ').title()
        
        if self._display is not None:
            method: callable = getattr(self._display, 'setText', None)
            
            if method:
                method(self._data['display_name'])
    
    @property
    def tooltip(self) -> str:
        """The tooltip for this setting."""
        return self._data.get('tooltip', '')
    
    @tooltip.setter
    def tooltip(self, value: str):
        self._data['tooltip'] = value
        
        if self._display is not None:
            self._display.setToolTip(value)
    
    @tooltip.deleter
    def tooltip(self):
        self._data['tooltip'] = ''
        
        if self._display is not None:
            self._display.setToolTip('')
    
    @property
    def status_tip(self) -> str:
        """The status tip for this setting."""
        return self._data.get('status_tip', '')
    
    @status_tip.setter
    def status_tip(self, value: str):
        self._data['status_tip'] = value
        
        if self._display is not None:
            self._display.setStatusTip(value)
    
    @status_tip.deleter
    def status_tip(self):
        self._data['status_tip'] = ''
        
        if self._display is not None:
            self._display.setStatusTip('')
    
    @property
    def whats_this(self) -> str:
        """The what's this for this setting."""
        return self._data.get('whats_this', '')
    
    @whats_this.setter
    def whats_this(self, value: str):
        self._data['whats_this'] = value
        
        if self._display is not None:
            self._display.setWhatsThis(value)
    
    @whats_this.deleter
    def whats_this(self):
        self._data['whats_this'] = ''
        
        if self._display is not None:
            self._display.setWhatsThis('')
    
    @property
    def hidden(self) -> bool:
        """Whether or not this setting should be hidden."""
        return bool(self._data.get('hidden'))
    
    @hidden.setter
    def hidden(self, value: bool):
        self._data['hidden'] = value
        
        if self._display is not None:
            self._display.setHidden(value)
    
    @hidden.deleter
    def hidden(self):
        self._data['hidden'] = False
        
        if self._display is not None:
            self._display.setHidden(False)
    
    @property
    def read_only(self) -> bool:
        """Whether or not this setting's widget should be considered read only."""
        return bool(self._data.get('read_only'))
    
    @read_only.setter
    def read_only(self, value: bool):
        self._data['read_only'] = bool(value)
        
        if self._display is not None:
            self._display.setDisabled(self._data['read_only'])
    
    @read_only.deleter
    def read_only(self):
        self._data['read_only'] = False
        
        if self._display is not None:
            self._display.setDisabled(self._data['read_only'])
    
    @property
    def converter(self) -> typing.Optional[callable]:
        return self._data.get('converter', None)
    
    @converter.setter
    def converter(self, value: callable):
        self._data['converter'] = value
        
        if self._display is not None:
            self._display.deleteLater()
        
        self._display = value(self)
    
    @converter.deleter
    def converter(self):
        del self._data['converter']

    @property
    def data(self) -> dict:
        """The raw data for this setting."""
        return self._data

    @property
    def display(self) -> typing.Optional[QtWidgets.QWidget]:
        """The QWidget for this setting."""
        return self._display
    
    # Data Methods #
    def _generate_data(self) -> dict:
        """Generates settings data."""
        return {'display_name': self.key.replace('_', ' ').title()}
    
    def setup(self):
        """Sets up the settings object."""
        if self.converter and callable(self.converter):
            self._data['converter'] = self.converter.__name__
        
        else:
            if isinstance(self.value, bool):
                self._data['converter'] = 'boolean'
            
            elif isinstance(self.value, str):
                if len(self.value) <= 255:
                    self._data['converter'] = 'char'
                
                else:
                    self._data['converter'] = 'text'
            
            elif isinstance(self.value, int):
                self._data['converter'] = 'number'
            
            elif isinstance(self.value, float):
                self._data['converter'] = 'decimal'
        
        if self._display is not None:
            self._display.setToolTip(self.tooltip)
            self._display.setStatusTip(self.status_tip)
            self._display.setWhatsThis(self.whats_this)
            self._display.setDisabled(self.read_only)
            
            if self._display.parent():
                self._display.setHidden(self.hidden)
    
    # Relationship Methods #
    def set_parent(self, parent: 'Setting'):
        """Sets the parent for this settings object."""
        if isinstance(parent, Setting):
            self.setParent(parent)
        
        else:
            raise TypeError('Parent must be of instance of Setting!')
    
    def add_child(self, child: 'Setting'):
        """Adds a child for this settings object."""
        if isinstance(child, Setting):
            child.set_parent(self)
        
        else:
            raise TypeError('Child must be of instance Setting!')
    
    def add_children(self, *children: 'Setting'):
        """Bulk adds children to this settings object."""
        for child in children:
            if isinstance(child, Setting):
                child.setParent(self)
            
            else:
                raise TypeError('Child must be of instance Setting!')
    
    @staticmethod
    def remove_child(child: 'Setting', *, new_parent: 'Setting' = None):
        """Removes a child from this settings object.
        
        If `new_parent` is not specified, the child will remain orphaned."""
        if isinstance(child, Setting):
            if new_parent is not None:
                child.set_parent(new_parent)
            
            else:
                child.setParent(None)
        
        else:
            raise TypeError('Child must of instance Setting!')
    
    @staticmethod
    def remove_children(*children, new_parent: 'Setting' = None):
        """Bulk removes children from this settings object.
        
        If `new_parent` is not specified, the child will remain orphaned."""
        for child in children:
            if isinstance(child, Setting):
                if new_parent is not None:
                    child.set_parent(new_parent)
                
                else:
                    child.setParent(None)
            
            else:
                raise TypeError('Child must be of instance Setting!')
    
    def descendants(self) -> typing.List['Setting']:
        """Returns a list this setting's descendants."""
        return [c for c in self.children() if isinstance(c, Setting)]
    
    # Serialization Methods #
    @classmethod
    def from_data(cls, data: dict) -> 'Setting':
        """Creates a new Setting object from raw data."""
        inst: Setting = cls(data['key'], data.get('value'))
        inst._data = data.get('data')
        
        for child in data.get('descendants'):  # type: dict
            c = Setting.from_data(child)
            inst.add_child(c)
        
        inst.setup()
        
        return inst
    
    def to_data(self) -> dict:
        """Creates a dict object from this setting's data."""
        return {
            'key': self.key,
            'value': self._value,
            'descendants': [d.to_data() for d in self.descendants()],
            'data': self._data
        }
    
    # Magic Methods #
    def __repr__(self) -> str:
        return '<{0.__class__.__name__} key="{0.full_path}" children={1}>'.format(self, len(self.descendants()))
    
    def __getitem__(self, key: str) -> 'Setting':
        children = self.descendants()
        
        for child in children:
            if child.key == key:
                return child
        
        raise KeyError
