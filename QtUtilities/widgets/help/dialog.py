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
import logging
import typing

from PyQt5 import QtCore, QtGui, QtHelp, QtWidgets

from .page import HelpPage
from ...signals import wait_for_signal
from ...utils import should_create_widget

__all__ = ['Help']

logger = logging.getLogger(__name__)


class Help(QtWidgets.QDialog):
    """A dialog for displaying documentation.
    
    TODO: Tree view of all topics and sub-topics, and maybe documentation headers.
    TODO: Maybe different tabs?
    TODO: Documentation search
    """
    
    def __init__(self, collection_file: str, parent: QtWidgets.QWidget = None):
        # Super call
        super(Help, self).__init__(parent=parent)
        
        # Ui attributes
        self.tabs: typing.Optional[QtWidgets.QTabBar] = None
        self.new_tab: typing.Optional[QtWidgets.QToolButton] = None
        self.url_box: typing.Optional[QtWidgets.QLineEdit] = None
        self.back_button: typing.Optional[QtWidgets.QToolButton] = None
        self.forward_button: typing.Optional[QtWidgets.QToolButton] = None
        self.home_button: typing.Optional[QtWidgets.QToolButton] = None
        self.page_container: typing.Optional[QtWidgets.QStackedWidget] = None
        
        # Url attributes
        self.url_completer: typing.Optional[QtWidgets.QCompleter] = None
        self.url_validator: typing.Optional[QtGui.QRegularExpressionValidator] = None
        
        # Internal attributes
        self._engine: QtHelp.QHelpEngineCore = QtHelp.QHelpEngineCore(collection_file)
        self._pages: typing.Dict[str, HelpPage] = {}
    
    # Ui methods
    def setup_ui(self):
        """Sets up the dialog's UI."""
        # UI validation
        if should_create_widget(self.tabs):
            self.tabs = QtWidgets.QTabBar()
            self.tabs.setTabsClosable(True)
            self.tabs.setDocumentMode(True)
            self.tabs.setElideMode(QtCore.Qt.ElideRight)
            self.tabs.setUsesScrollButtons(False)
            self.tabs.setExpanding(False)
            self.tabs.setMovable(True)
            self.tabs.setSelectionBehaviorOnRemove(self.tabs.SelectLeftTab)
            self.tabs.setShape(self.tabs.RoundedNorth)
            
            self.tabs.currentChanged.connect(self.change_page)
        
        if should_create_widget(self.new_tab):
            self.new_tab = QtWidgets.QToolButton()
            self.new_tab.setText('+')
            self.new_tab.setAutoRaise(True)
            self.new_tab.triggered.connect(self.handle_new_tab)
        
        if should_create_widget(self.url_box):
            self.url_box = QtWidgets.QLineEdit()
            self.url_box.setReadOnly(False)
            self.url_box.setClearButtonEnabled(True)
            self.url_box.setPlaceholderText('Search or type a url')
        
        if should_create_widget(self.back_button):
            self.back_button = QtWidgets.QToolButton()
            self.back_button.setText('◀️')
        
        if should_create_widget(self.forward_button):
            self.forward_button = QtWidgets.QToolButton()
            self.forward_button.setText('▶️')
        
        if should_create_widget(self.home_button):
            self.home_button = QtWidgets.QToolButton()
            self.home_button.setText('🏠')
        
        if should_create_widget(self.page_container):
            self.page_container = QtWidgets.QStackedWidget()
        
        if should_create_widget(self.url_completer):
            self.url_completer = QtWidgets.QCompleter()
            self.url_box.setCompleter(self.url_completer)
        
        if should_create_widget(self.url_validator):
            self.url_validator = QtGui.QRegExpValidator()
            self.url_box.setValidator(self.url_validator)
        
        # Layout validation
        layout: QtWidgets.QGridLayout = self.layout()
        
        if layout is None:
            layout = QtWidgets.QGridLayout(self)
        
        # Layout insertion
        if layout.indexOf(self.tabs) == -1:
            layout.addWidget(self.tabs, 0, 0, -1, -1)
        
        if layout.indexOf(self.back_button) == -1:
            layout.addWidget(self.back_button, 1, 0)
        
        if layout.indexOf(self.forward_button) == -1:
            layout.addWidget(self.forward_button, 1, 1)
        
        if layout.indexOf(self.home_button) == -1:
            layout.addWidget(self.home_button, 1, 2)
        
        if layout.indexOf(self.url_box) == -1:
            layout.addWidget(self.url_box, 1, 3, -1, -1)
        
        if layout.indexOf(self.page_container) == -1:
            layout.addWidget(self.page_container, 2, 0, -1, -1)
        
        # QTabBar prep
        if self.tabs.count() > 0 and self.tabs.isTabEnabled(self.tabs.count() - 1):
            self.tabs.addTab('')
            self.tabs.setTabEnabled(self.tabs.count() - 1, False)
            self.tabs.setTabButton(self.tabs.count() - 1, self.tabs.RightSide, self.new_tab)
        
        elif self.tabs.count() <= 0:
            self.tabs.addTab('')
            self.tabs.setTabEnabled(self.tabs.count() - 1, False)
            self.tabs.setTabButton(self.tabs.count() - 1, self.tabs.RightSide, self.new_tab)
        
        # QHelpEngineCore prepare_ui
        prepare_ui = self._engine.setupData()
        wait_for_signal(self._engine.setupFinished)
        
        if not prepare_ui:
            logger.warning(f'QHelpEngineCore prepare_ui failed!  ({self._engine.error()})')
        
        # Ensure there's one tab open
        if self.tabs.count() <= 1:
            self.new_tab.click()
    
    # QTabBar slots
    def change_page(self, index: int):
        """Changes the current visible page to the user's requested page."""
        text = self.tabs.tabText(index)
        
        # Validation
        if text in self._pages:
            self.page_container.setCurrentWidget(self._pages[text])
        
        else:
            self.tabs.removeTab(index)
    
    def handle_new_tab(self):
        """Creates a new tab."""
        self.tabs.insertTab(self.tabs.count() - 2, '')
        self.tabs.setCurrentIndex(self.tabs.count() - 2)
