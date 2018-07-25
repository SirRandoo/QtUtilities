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
import sip
import typing

from PyQt5 import QtCore, QtWidgets

from .converter import Converter
from .option import Option

__all__ = {"Section"}


class Section(QtCore.QObject):
    """A class for accessing setting values."""
    
    def __init__(self, node: str, *, parent: QtCore.QObject = None):
        # Super Call #
        super(Section, self).__init__(parent)
        
        self.node = node
        self.display_name = node.split(".")[-1].capitalize()
        self.sections = []  # type: typing.List[typing.Union[Section, Option]]
        self.converter = None  # type: Converter
        
        self.tree_item = None  # type: QtWidgets.QTreeWidgetItem
        self.scrollable = None  # type: QtWidgets.QScrollArea
        self.container = None  # type: QtWidgets.QWidget
        self.stackable = None  # type: QtWidgets.QStackedWidget
        self.tree = None  # type: QtWidgets.QTreeWidget
        
        self._bound = False
        self._prepare_widget()
    
    # Properties #
    def is_spacer(self) -> bool:
        """Returns whether or not this section is classified as a spacer.
        A spacer section is simply a section of sections."""
        return all([isinstance(i, Section) for i in self.sections])
    
    # Settings Methods #
    def add_section(self, section: 'Section'):
        """Adds a section to this section."""
        self.sections.append(section)
        section.setParent(self)
    
    def add_option(self, option: Option):
        """Adds an option to this section."""
        self.sections.append(option)
        option.setParent(self)
    
    def get_section(self, node: str):
        """Gets a section from this section."""
        for s in self.sections:
            if isinstance(s, Section):
                if s.node == node:
                    return s
        
        raise KeyError
    
    def get_option(self, key: str):
        """Gets an option from this section."""
        for o in self.sections:
            if isinstance(o, Option):
                if o.key == key:
                    return o
        
        raise KeyError
    
    # Setter Methods #
    def set_display_name(self, display_name: str) -> 'Section':
        """Sets the display name for this section."""
        self.display_name = display_name
        return self
    
    # Ui Methods #
    def populate(self, tree: QtWidgets.QTreeWidget, item: QtWidgets.QTreeWidgetItem,
                 stackable: QtWidgets.QStackedWidget):
        """Populates a tree widget with settings data."""
        self._prepare_widget()
        
        if self.tree_item is None or sip.isdeleted(self.tree_item):
            self.tree_item = QtWidgets.QTreeWidgetItem(item)
            self.tree_item.setText(0, self.display_name)
        
        item.addChild(self.tree_item)
        
        for section in self.sections:
            if isinstance(section, Section):
                section.populate(tree, self.tree_item, stackable)
        
        if self._is_widget_in_stackable(stackable):
            stackable.removeWidget(self.scrollable)
        
        stackable.addWidget(self.scrollable)
        
        if not self._bound:
            tree.itemSelectionChanged.connect(self._watch_tree)
            self._bound = True
        
        self.stackable = stackable
        self.tree = tree
    
    def _prepare_widget(self):
        """Prepares the widget for display."""
        if self.scrollable is None:
            self.scrollable = QtWidgets.QScrollArea()
            self.container = QtWidgets.QWidget()
            self.container.setLayout(QtWidgets.QFormLayout())
            self.scrollable.setWidget(self.container)
            self.container.show()
            self.scrollable.setWidgetResizable(True)
        
        for section in self.sections:
            if isinstance(section, Option):
                self.container.layout().addRow(section.label, section.widget)
    
    def _watch_tree(self):
        """Watches the tree for our item."""
        item = self.tree.currentItem()
        
        if item == self.tree_item:
            self.stackable.setCurrentWidget(self.scrollable)
    
    def _is_widget_in_stackable(self, stackable: QtWidgets.QStackedWidget):
        """Returns whether or not the section widget is in the stackable."""
        return stackable.indexOf(self.scrollable) != -1
    
    # Serialization Methods #
    def serialize(self) -> dict:
        """Serializes a section into a JSON object."""
        return dict(
            node=self.node,
            display=self.display_name,
            sections=[s.serialize() for s in self.sections]
        )
    
    @classmethod
    def deserialize(cls, data: dict, converters: Converter) -> 'Section':
        """Deserializes a JSON object into a Section."""
        section = cls(data.pop("node"))
        
        section.display_name = data.get("display", section.node.split(".")[-1].title())
        section.sections = list()
        section.converter = converters
        
        for raw in data.get("sections", list()):
            if "value" in raw:
                _temp = Option.deserialize(raw, converters)
            
            else:
                _temp = Section.deserialize(raw, converters)
            
            section.sections.append(_temp)
        
        section._prepare_widget()
        
        return section
    
    # Magic Method #
    def __getitem__(self, item: str):
        for section in self.sections:
            if isinstance(section, Option):
                if section.key.lower() == item.lower():
                    return section
            
            elif isinstance(section, Section):
                if section.node == item:
                    return section
        
        raise KeyError
    
    def __setitem__(self, key: str, value: typing.Union[Option, 'Section']):
        for section in self.sections:
            if isinstance(section, Option):
                if section.key.lower() == key.lower():
                    section = value
                    return
            
            elif isinstance(section, Section):
                if section.node.lower() == key.lower():
                    section = value
                    return
        
        self.sections.append(value)
    
    def __delitem__(self, key: str):
        lowered = key.lower()
        
        self.sections = [s for s in self.sections
                         if getattr(s, "key", lowered).lowered() != lowered
                         and getattr(s, "node", lowered).lowered() != lowered]
