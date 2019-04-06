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
import inspect
import typing
from collections import namedtuple

from PyQt5 import QtCore, QtGui, QtWidgets

from . import converters
from .setting import Setting
from ..utils import should_create_widget

__all__ = ['Display']

if typing.TYPE_CHECKING:
    class DisplayStub(typing.NamedTuple):
        display: typing.Optional[QtWidgets.QWidget]
        container: QtWidgets.QWidget
        item: QtWidgets.QTreeWidgetItem

SettingDisplay: 'DisplayStub' = namedtuple('SettingDisplay', ['display', 'container', 'item'])


# noinspection PyArgumentList,PyProtectedMember
class Display(QtWidgets.QDialog):
    """A pre-built settings display."""

    def __init__(self, *, parent: QtWidgets.QWidget = None):
        # Super call
        super(Display, self).__init__(parent=parent)
    
        # Internal attributes
        self.tree: typing.Optional[QtWidgets.QTreeWidget] = None
        self.stacked: typing.Optional[QtWidgets.QStackedWidget] = None
    
        self.view: typing.Dict[str, SettingDisplay] = {}
        self.converters: typing.Dict[str, typing.Callable[[Setting], QtWidgets.QWidget]] = {
            name: instance
            for name, instance in inspect.getmembers(converters)
            if callable(instance)
        }
    
        self._setup: bool = False
        
        # Top-level settings.
        self.settings: typing.Dict[str, Setting] = {}

    # Settings registry
    def register_setting(self, setting: Setting):
        """Registers a top-level setting to the display.  If the setting already
        exists, KeyError will be raised."""
        if setting.key in self.settings:
            raise KeyError(f'Setting {setting.key} is already registered!')
    
        self.settings[setting.key] = setting

    def unregister_setting(self, setting: Setting):
        """Unregisters a top-level setting from the display.  If the setting
        display doesn't exist, KeyError will be raised."""
        if setting.key not in self.settings:
            raise KeyError(f'Setting {setting.key} does not exist!')
    
        del self.settings[setting.key]

    # Converter registry
    def register_converter(self, converter: typing.Callable[[Setting], QtWidgets.QWidget]):
        """Registers a converter to the settings display.  If the converter
        already exists, KeyError will be raised."""
        if converter.__name__ in self.converters:
            raise KeyError(f'Converter {converter.__name__} is already registered!')
    
        self.converters[converter.__name__] = converter

    def unregister_converter(self, converter: typing.Union[str, typing.Callable[[Setting], None]]):
        """Unregisters a converter from the settings display.  If the converter
        doesn't exist, KeyError will be raised."""
        n = converter.__name__ if callable(converter) else converter
    
        if n not in self.converters:
            raise KeyError(f'Converter {n} does not exist!')
    
        del self.converters[n]

    # Display methods
    def setup_ui(self):
        """Checks up on the display to see if any objects need to be recreated."""
        # Declarations
        layout: QtWidgets.QHBoxLayout = self.layout()

        # Layout validation
        if layout is None:
            layout = QtWidgets.QHBoxLayout(self)

        # Widget validation
        if should_create_widget(self.tree):
            self.tree = QtWidgets.QTreeWidget()
            self.tree.setHeaderHidden(True)
            self.tree.setEditTriggers(self.tree.NoEditTriggers)
    
            self.tree.setIndentation(14)
            self.tree.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            self.tree.currentItemChanged.connect(self.tree_tracker)

        if should_create_widget(self.stacked):
            self.stacked = QtWidgets.QStackedWidget()
            self.stacked.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)

        # Layout insertion
        layout.addWidget(self.tree)
        layout.addWidget(self.stacked)

        # Setting display validation
        for setting in self.settings.values():
            self._check_setting_ui(setting)

    def _check_setting_ui(self, setting: Setting):
        """Creates a display for the settings object."""
        # Declarations
        parent: typing.Optional[QtCore.QObject] = setting.parent()
        path = setting.full_path

        # View validation
        if path not in self.view:
            self.view[path]: DisplayStub = SettingDisplay(None, QtWidgets.QWidget(), QtWidgets.QTreeWidgetItem())
            self.view[path].item.setFirstColumnSpanned(True)
    
            self.stacked.addWidget(self.view[path].container)
    
            # Hide top-level windows
            if self.view[path].container.isWindow():
                self.view[path].container.hide()

        # More declarations
        view: typing.Union[DisplayStub, SettingDisplay] = self.view[path]

        # Converter validation
        if setting.converter is not None and setting.converter in self.converters:
            c = self.converters[setting.converter]
    
            view = self.view[path] = SettingDisplay(c(setting), self.view[path].container, self.view[path].item)
    
            # Hide top-level windows
            if self.view[path].container.isWindow():
                self.view[path].container.hide()
    
            if self.view[path].display.isWindow():
                self.view[path].display.hide()

        else:
            # Just in case the Setting class doesn't generate one
            c: typing.Optional[typing.Callable[[Setting], QtWidgets.QWidget]] = None
    
            if isinstance(setting.value, bool):
                c = converters.boolean
    
            elif isinstance(setting.value, float):
                c = converters.decimal
    
            elif isinstance(setting.value, int):
                c = converters.number
    
            elif isinstance(setting.value, str) and len(setting.value) <= 255:
                c = converters.char
    
            elif isinstance(setting.value, str) and len(setting.value) > 255:
                c = converters.text
    
            if c is not None:
                view = self.view[path] = SettingDisplay(c(setting), self.view[path].container, self.view[path].item)
        
                # Hide top-level windows
                if self.view[path].container.isWindow():
                    self.view[path].container.hide()
        
                if self.view[path].display.isWindow():
                    self.view[path].display.hide()

        # Children validation
        for d in setting.descendants():
            self._check_setting_ui(d)

        # Display validation
        if view.display is not None:
            # Stitch display information
            view.display.setToolTip(setting.tooltip or None)
            view.display.setDisabled(setting.read_only)
            view.display.setWhatsThis(setting.whats_this)
            view.display.setStatusTip(setting.status_tip)
    
            view.item.setText(0, setting.display_name)
            view.item.setHidden(setting.hidden)
    
            # Attempt to get parent view
            if parent is not None and isinstance(parent, Setting):
                parent_path = parent.full_path
                parent_view: SettingDisplay = self.view[parent_path]
        
                # Parent assignment
                view.display.setParent(parent_view.container)
        
                # Update the hidden status of the display once it has a parent
                view.display.setHidden(setting.hidden)
        
                # Relationship stitching
                if any([not s.hidden for s in setting.descendants() if
                        isinstance(s, Setting)]) and parent_view.item.indexOfChild(view.item) == -1:
                    parent_view.item.addChild(view.item)
        
                if view.item.childCount() > 0:
                    view.item.setText(0, setting.key.replace('_', ' ').title())
        
                # Value validation
                if setting.value is not None:
                    parent_layout: QtWidgets.QFormLayout = parent_view.container.layout()
            
                    # Parent layout validation
                    if parent_layout is None:
                        parent_layout = QtWidgets.QFormLayout(parent_view.container)
                        parent_layout.setLabelAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
            
                    parent_layout.addRow(setting.display_name, view.display)
                    
            else:
                self.tree.addTopLevelItem(view.item)
        
        else:
            # Parent validation
            if parent is not None and isinstance(parent, Setting):
                parent_view: SettingDisplay = self.view[parent.full_path]
        
                # Relationship stitching
                if any([not s.hidden for s in setting.descendants() if
                        isinstance(s, Setting)]) and parent_view.item.indexOfChild(view.item) == -1:
                    parent_view.item.addChild(view.item)
        
                if view.item.childCount() > 0:
                    view.item.setText(0, setting.key.replace('_', ' ').title())
    
            else:
                self.tree.addTopLevelItem(view.item)
    
            # Stitch display information
            view.item.setHidden(setting.hidden)
            view.item.setDisabled(setting.read_only)
            view.item.setWhatsThis(0, setting.whats_this)
            view.item.setStatusTip(0, setting.status_tip)
            view.item.setToolTip(0, setting.tooltip or None)
            view.item.setText(0, setting.display_name)

    # Serialization
    def to_data(self) -> list:
        """Creates a list object from this display's setting data."""
        return [s.to_data() for s in self.settings.values()]
    
    @classmethod
    def from_data(cls, data: list) -> 'Display':
        """Creates a new Display object from raw data."""
        display = cls()
        
        for setting in data:
            display.register_setting(Setting.from_data(setting))
        
        return display

    # Slots
    def tree_tracker(self, current: QtWidgets.QTreeWidgetItem):
        """Tracks changes in the QTreeWidget's selection box."""
        for path, view in self.view.items():
            if view.item == current and self.stacked.indexOf(view.container) != -1:
                self.stacked.setCurrentWidget(view.container)

    # Events
    def showEvent(self, a0: QtGui.QShowEvent):
        if not self._setup:
            self._setup = True
            self.setup_ui()

    # Magic methods
    def __getitem__(self, item: str) -> Setting:
        return self.settings.__getitem__(item)

    def __contains__(self, item: str) -> bool:
        try:
            return bool(self.settings[item])
    
        except KeyError:
            return False
