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
from .section import Section

__all__ = {"Domain"}


class Domain(QtCore.QObject):
    """Represents a settings domain."""
    
    def __init__(self, domain: str, *, parent: QtCore.QObject = None):
        super(Domain, self).__init__(parent=parent)
        
        self.display_name = domain.split(".")[-1].capitalize()
        self.name = domain
        self.converter = None  # type: Converter
        
        self.tree_item = None  # type: QtWidgets.QTreeWidgetItem
        self.sections = list()  # type: typing.List[Section]
    
    # Setter Methods #
    def set_display_name(self, display_name: str) -> 'Domain':
        """Sets the display name for this domain."""
        self.display_name = display_name
        return self
    
    def set_converter(self, converter: Converter) -> 'Domain':
        """Sets the converter for this domain."""
        self.converter = converter
        return self
    
    # Settings Methods #
    def add_section(self, section: Section):
        """Adds a section to the domain's settings."""
        for s in self.sections:
            if s.node == section.node:
                raise ValueError(f'Section "{s.node}" already exists!')
        
        section.setParent(self)
        self.sections.append(section)
    
    def get_section(self, node: str):
        """Gets a section from the domain's settings."""
        for s in self.sections:
            if s.node == node:
                return s
        
        raise ValueError
    
    # Ui Methods #
    def populate(self, tree: QtWidgets.QTreeWidget, stackable: QtWidgets.QStackedWidget):
        """Populates a tree widget with the settings data."""
        if self.tree_item is None or sip.isdeleted(self.tree_item):
            self.tree_item = QtWidgets.QTreeWidgetItem()
            self.tree_item.setText(0, self.display_name)
        
        for section in self.sections:
            section.populate(tree, self.tree_item, stackable)
        
        tree.addTopLevelItem(self.tree_item)
    
    # Serialization Methods #
    def serialize(self) -> dict:
        """Serializes a domain into a JSON object."""
        return dict(name=self.name, display=self.display_name, settings=[s.serialize() for s in self.sections])
    
    @classmethod
    def deserialize(cls, data: dict, converters: Converter) -> 'Domain':
        """Deserializes a JSON object into a domain."""
        domain = cls(data.pop("name"))
        
        domain.converter = converters
        domain.sections = [Section.deserialize(raw, converters) for raw in data.get("settings", list())]
        
        if "display" in data:
            domain.display_name = data.get("display")
        
        else:
            domain.display_name = domain.name.split(".")[-1].title()
        
        return domain
    
    # Magic Methods #
    def __getitem__(self, item: str):
        for section in self.sections:
            if section.node.lower() == item.lower():
                return section
        
        raise KeyError
    
    def __setitem__(self, key: str, value: Section):
        for section in self.sections:
            if section.node.lower() == key.lower():
                section = value
                return
        
        self.sections.append(value)
    
    def __delitem__(self, key: str):
        lowered = key.lower()
        
        self.sections = [s for s in self.sections if s.node.lower() != lowered]
