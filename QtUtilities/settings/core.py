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
# QtUtilities is distributed in the
# hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even
# the implied warranty of MERCHANTABILITY
# or FITNESS FOR A PARTICULAR PURPOSE.
# See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of
# the GNU Lesser General Public License
# along with QtUtilities.
# If not, see <http://www.gnu.org/licenses/>.
import json
import logging
import typing

from PyQt5 import QtCore, QtGui, QtWidgets

from .domain import Domain

__all__ = {"QSettings"}


class QSettings(QtWidgets.QDialog):
    """A class for managing application settings.  This class automatically
    handles conversion between the basic python types.  Extra types should
    be specified through the conversion methods."""
    logger = logging.getLogger(__name__)
    
    def __init__(self, file_name: str = None, *, parent: QtWidgets.QWidget = None):
        # Super Call #
        super(QSettings, self).__init__(parent=parent)
        
        # "Private" Attributes #
        self._settings = list()  # type: typing.List[Domain]
        self._file = QtCore.QSaveFile(file_name or "settings.json")
        self._quitting = False
        
        # Ui Attributes #
        self.searchable_tree = QtWidgets.QWidget(parent=self)
        self.stackable = QtWidgets.QStackedWidget(parent=self)
        self.search_bar = QtWidgets.QLineEdit(parent=self.searchable_tree)
        self.tree = QtWidgets.QTreeWidget(parent=self.searchable_tree)
        
        # Internal Calls #
        self._prepare_search_bar()
        self._prepare_tree()
        self._prepare_searchable_tree()
        self._prepare_dialog()
    
    # Properties #
    @property
    def file_name(self):
        return self._file.fileName()
    
    @file_name.setter
    def file_name(self, value: str):
        self._file.setFileName(value)
    
    # Ui Methods #
    def _prepare_search_bar(self):
        """Prepares the search bar for display."""
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.MinimumExpanding, QtWidgets.QSizePolicy.Fixed)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.search_bar.sizePolicy().hasHeightForWidth())
        
        self.search_bar.setClearButtonEnabled(True)
        self.search_bar.setSizePolicy(size_policy)
        self.search_bar.setDisabled(True)
        self.search_bar.setPlaceholderText("Not implemented")
    
    def _prepare_tree(self):
        """Prepares the tree widget for display."""
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding)
        size_policy.setVerticalStretch(0)
        size_policy.setHorizontalStretch(0)
        size_policy.setHeightForWidth(self.tree.sizePolicy().hasHeightForWidth())
        
        self.tree.setEditTriggers(self.tree.NoEditTriggers)
        self.tree.setTabKeyNavigation(True)
        self.tree.setProperty("showDropIndicator", False)
        self.tree.setIndentation(12)
        self.tree.setUniformRowHeights(True)
        self.tree.setAnimated(True)
        self.tree.setWordWrap(True)
        self.tree.setHeaderHidden(True)
        
        self.tree.setSizePolicy(size_policy)
    
    def _prepare_searchable_tree(self):
        """Prepares the searchable tree widget for display."""
        size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        size_policy.setHorizontalStretch(0)
        size_policy.setVerticalStretch(0)
        size_policy.setHeightForWidth(self.searchable_tree.sizePolicy().hasHeightForWidth())
        
        layout = QtWidgets.QGridLayout(self.searchable_tree)
        layout.setContentsMargins(0, 0, 0, 0)
        
        layout.addWidget(self.tree, 1, 0, 1, 2)
        layout.addWidget(self.search_bar, 0, 0, 1, 2)
    
    def _prepare_dialog(self):
        """Prepares the dialog for display."""
        layout = QtWidgets.QHBoxLayout(self)
        layout.addWidget(self.searchable_tree)
        layout.addWidget(self.stackable)
        
        self.setSizeGripEnabled(True)
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
    
    def repopulate(self):
        """Repopulates the dialog with the current settings."""
        self.tree.clear()
        
        while self.stackable.count() > 0:
            self.stackable.removeWidget(self.stackable.currentWidget())
        
        for domain in self._settings:
            domain.populate(self.tree, self.stackable)
    
    # Settings Methods #
    def add_domain(self, domain: Domain):
        """Adds a domain to the settings repository."""
        domain.setParent(self)
        
        self._settings.append(domain)
        self.repopulate()
    
    def get_domain(self, name: str):
        """Gets a domain from the settings repository."""
        for d in self._settings:
            if d.name == name:
                return d
        
        raise KeyError
    
    def remove_domain(self, dom: str):
        """Removes a domain from the settings repository."""
        if dom in self._settings:
            self._settings.remove(dom)
        
        return dom
    
    # Serialization Methods #
    def serialize(self, *, encoder: typing.Callable=None, pretty: bool=None) -> int:
        """Serializes the config to the file's format.
        
        If `pretty` is specified, the output will be formatted prettily.
        This functionality depends entirely on the encoder's ability to
        support indents.
        
        If `encoder` is specified, the serializers will use this encoder
        to serialize itself.  Encoders are excepted to raise a ValueError
        if serialization failed; all other exceptions are not handled."""
        if encoder is None:
            encoder = json.dumps
        
        if pretty is None:
            pretty = False
        
        try:
            data = [d.serialize() for d in self._settings]
        
        except ValueError as e:
            self.logger.warning("Could not serialize settings! ({})".format(str(e)))
            self.logger.debug(e.__traceback__)
        
        else:
            if not self._file.isOpen():
                self._file.open(QtCore.QSaveFile.WriteOnly | QtCore.QSaveFile.Text | QtCore.QSaveFile.Truncate)
            
            try:
                data = encoder(data, indent=2 if pretty else None)
                
                if type(data) == str:
                    bytes_written = self._file.write(data.encode())
                
                elif type(data) == bytes:
                    bytes_written = self._file.write(data.encode())
                
                else:
                    raise TypeError("Unsupported return type: {}".format(type(data)))
            
            except ValueError as e:
                self.logger.warning("Could not serialize settings! ({}}".format(str(e)))
                self.logger.debug(e.__traceback__)
                return -1
            
            else:
                if bytes_written == -1:
                    self.logger.warning("Could not write to file!")
                    self.logger.warning("Error #{} - {}".format(self._file.error(), self._file.errorString()))
                    return 0
    
                else:
                    return bytes_written
        
        finally:
            self._file.commit()
    
    # Aliases #
    def quit(self):
        """The true quit method for this class."""
        self._quitting = True
        self.close()
    
    # Events #
    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.serialize()
        
        if self._quitting:
            a0.accept()
        
        else:
            a0.ignore()
            self.hide()
    
    # Magic Methods #
    def __getitem__(self, item: str):
        for domain in self._settings:
            if domain.name.lower() == item.lower():
                return domain
        
        raise KeyError
    
    def __setitem__(self, key: str, value: Domain):
        for domain in self._settings:
            if key.lower() == domain.name.lower():
                domain = value
                return
        
        self._settings.append(value)
        self.repopulate()
    
    def __delitem__(self, key: str):
        lowered = key.lower()
        
        self._settings = [d for d in self._settings if d.name.lower() != lowered]
