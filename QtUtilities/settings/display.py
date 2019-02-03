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

from PyQt5 import QtCore, QtGui, QtWidgets

from . import converters
from .setting import Setting
from ..utils import should_create_widget

__all__ = {"Display"}


# noinspection PyArgumentList,PyProtectedMember
class Display(QtWidgets.QDialog):
    """A pre-built settings display."""
    
    def __init__(self, **kwargs):
        """
        :param parent: The parent of the display.
        :type parent: QtWidgets.QWidget
        """
        # Super Call #
        super(Display, self).__init__(parent=kwargs.get('parent'))
        
        # "Public" Attributes #
        self.settings_tree: QtWidgets.QTreeWidget = None
        self.stacked_widget: QtWidgets.QStackedWidget = None
        
        # Top-level settings.
        #
        # Design:
        # If a setting has children, the setting will be displayed in the tree.
        # displayed in the tree and have an option in its own menu.
        self.settings: typing.List[Setting] = []
        
        # "Private" Attributes #
        #
        # "Internal" Attributes #
        #
        # Internal Calls #
    
    # Settings Methods #
    def register(self, setting: Setting):
        """Registers a setting."""
        if setting not in self.settings:
            self.settings.append(setting)
        
        else:
            raise ValueError(f'Setting {setting.key} is already registered!')
    
    def unregister(self, setting: Setting):
        """Unregisters a setting."""
        try:
            self.settings.remove(setting)
        
        except ValueError:
            raise LookupError(f'Setting {setting.key} is not registered!')
    
    # Display Methods #
    def display_checkup(self):
        """Checks up on the display to see if any objects need to be recreated."""
        layout = QtWidgets.QHBoxLayout(self)
        
        if should_create_widget(self.settings_tree):
            self.settings_tree = QtWidgets.QTreeWidget()
            self.settings_tree.setHeaderHidden(True)
            self.settings_tree.setEditTriggers(self.settings_tree.NoEditTriggers)
            
            self.settings_tree.setIndentation(14)
            self.settings_tree.setSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Expanding)
            self.settings_tree.currentItemChanged.connect(self.tree_tracker)
        
        if should_create_widget(self.stacked_widget):
            self.stacked_widget = QtWidgets.QStackedWidget()
            self.stacked_widget.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        
        layout.addWidget(self.settings_tree)
        layout.addWidget(self.stacked_widget)
        
        for setting in self.settings:
            self._check_display(setting)
    
    def _check_display(self, setting: Setting):
        """Creates a display for the settings object."""
        if should_create_widget(setting._display):
            # Display creation
            parent: Setting = setting.parent()
            parent_display: typing.Optional[QtWidgets.QWidget] = getattr(parent, '_container', None)
            
            if setting.converter is not None:
                converter = getattr(converters, setting.converter, None)
                
                if converter is not None:
                    setting._display = converter(setting)
                
                else:
                    setting._display = QtWidgets.QWidget(parent=parent_display or self.stacked_widget)
                    
                    if setting._display.isWindow():
                        setting._display.hide()
            
            else:
                setting._display = QtWidgets.QWidget(parent=parent_display or self.stacked_widget)
                
                if setting._display.isWindow():
                    setting._display.hide()
            
            # Display adjustments
            setting._display.setToolTip(setting.tooltip or None)
            setting._display.setDisabled(setting.read_only)
            setting._display.setWhatsThis(setting.whats_this)
            setting._display.setStatusTip(setting.status_tip)
            setting._display.setHidden(setting.hidden)
            
            # Tree item
            setting._item = QtWidgets.QTreeWidgetItem()
            setting._item.setText(0, setting.display_name)
            
            if setting._display.__class__ != QtWidgets.QWidget:
                setting._container = QtWidgets.QWidget(parent_display or self.stacked_widget)
                
                if setting._container.isWindow():
                    setting._container.hide()
            
            else:
                setting._container = setting._display
            
            if setting.parent() and isinstance(setting.parent(), Setting):
                parent_item = setting.parent()._item
                
                if parent_item:
                    if setting.descendants():
                        setting._item.setText(0, setting.key.title())
                        
                        parent_item.addChild(setting._item)
                        self.stacked_widget.addWidget(setting._container)
                    
                    if setting.value is not None:
                        parent_layout = parent_display.layout()
                        
                        if not parent_layout:
                            parent_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout(parent_display)
                            parent_layout.setLabelAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                        
                        parent_layout.addRow(setting.display_name, setting._display)
            
            else:
                self.settings_tree.addTopLevelItem(setting._item)
                self.stacked_widget.addWidget(setting._container)
            
            # Tree hiding
            setting._item.setHidden(setting.hidden)
            
            # Check descendant displays
            for descendant in setting.descendants():
                self._check_display(descendant)
        
        else:
            if setting.parent() and isinstance(setting.parent(), Setting) and setting.value is not None:
                parent = setting.parent()
                parent_display = getattr(parent, '_display', None)
                
                if parent_display is not None:
                    parent_layout: QtWidgets.QFormLayout = parent_display.layout()
                    
                    if not parent_layout:
                        parent_layout: QtWidgets.QFormLayout = QtWidgets.QFormLayout(parent_display)
                        parent_layout.setLabelAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignRight)
                    
                    parent_layout.addRow(setting.display_name, setting._display)
    
    def _setting_from_item(self, item: QtWidgets.QTreeWidgetItem) -> Setting:
        """Returns the settings object associated with the QTreeWidgetItem."""
        
        def is_item_in_setting(s: Setting) -> Setting:
            for s_ in s.descendants():
                if s_._item == item:
                    return s_
                
                elif s_.descendants():
                    try:
                        set_ = is_item_in_setting(s_)
                    
                    except LookupError:
                        continue
                    
                    else:
                        if set_._item == item:
                            return set_
            
            raise LookupError
        
        for setting in self.settings:
            if setting._item == item:
                return setting
            
            elif setting.descendants():
                try:
                    setting_ = is_item_in_setting(setting)
                
                except LookupError:
                    continue
                
                else:
                    if setting_._item == item:
                        return setting_
        
        raise LookupError
    
    # Serialization #
    def to_data(self) -> list:
        """Creates a list object from this display's setting data."""
        return [s.to_data() for s in self.settings]
    
    @classmethod
    def from_data(cls, data: list) -> 'Display':
        """Creates a new Display object from raw data."""
        display = cls()
        
        for setting in data:
            display.register(Setting.from_data(setting))
        
        return display
    
    # Slots #
    def tree_tracker(self, current: QtWidgets.QTreeWidgetItem):
        """Tracks changes in the QTreeWidget's selection box."""
        try:
            setting = self._setting_from_item(current)
        
        except LookupError:
            pass
        
        else:
            if setting._container is not None and self.stacked_widget.indexOf(setting._container) != -1:
                self.stacked_widget.setCurrentWidget(setting._container)
            
            elif setting._display is not None and self.stacked_widget.indexOf(setting._display) != -1:
                self.stacked_widget.setCurrentWidget(setting._display)
    
    # Events #
    def showEvent(self, event: QtGui.QShowEvent):
        """An override to the default Qt showEvent.
        
        This implementation's job is to ensure widgets get recreated if they've
        been garbage collected."""
        self.display_checkup()
        
        if not event.isAccepted():
            event.accept()
    
    # Magic Methods #
    def __getitem__(self, item: str) -> Setting:
        for setting in self.settings:
            if setting.key == item:
                return setting
        
        raise KeyError
