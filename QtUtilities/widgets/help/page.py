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
import functools
import typing

from PyQt5 import QtCore, QtWidgets

from ...utils import should_create_widget

__all__ = ['HelpPage']


class HelpPage(QtWidgets.QWidget):
    """A widget that houses a documentation page."""
    anchor_clicked = QtCore.pyqtSignal(QtCore.QUrl)
    
    def __init__(self, *, parent: QtWidgets.QWidget = None):
        # Super call
        super(HelpPage, self).__init__(parent=parent)
        
        # Ui attributes
        # Top-level elements
        self.container: typing.Optional[QtWidgets.QWidget] = None
        self.display: typing.Optional[QtWidgets.QTextBrowser] = None
        
        # Container elements
        self.find_flags: typing.Optional[QtWidgets.QGroupBox] = None
        self.find_next_button: typing.Optional[QtWidgets.QToolButton] = None
        self.find_input: typing.Optional[QtWidgets.QLineEdit] = None
        self.find_previous_button: typing.Optional[QtWidgets.QToolButton] = None
        self.find_sensitive: typing.Optional[QtWidgets.QCheckBox] = None
        self.find_words: typing.Optional[QtWidgets.QCheckBox] = None
        self.find_regex: typing.Optional[QtWidgets.QCheckBox] = None
        
        # Internal elements
        self.hide_finder_action: typing.Optional[QtWidgets.QAction] = None
        self.find_next_action: typing.Optional[QtWidgets.QAction] = None
        self.find_previous_action: typing.Optional[QtWidgets.QAction] = None
        self.show_finder_action: typing.Optional[QtWidgets.QAction] = None
    
    # Ui methods
    def setup_ui(self):
        """Sets up the page's UI."""
        # Validation
        if should_create_widget(self.container):
            self.container = QtWidgets.QWidget()
        
        if should_create_widget(self.display):
            self.display = QtWidgets.QTextBrowser()
            self.display.anchorClicked.connect(self.anchor_clicked)
        
        if should_create_widget(self.find_flags):
            self.find_flags = QtWidgets.QGroupBox('Flags')
        
        if should_create_widget(self.find_next_button):
            self.find_next_button = QtWidgets.QToolButton()
            self.find_next_button.setText('➡')
            self.find_next_button.triggered.connect(self.search)
        
        if should_create_widget(self.find_input):
            self.find_input = QtWidgets.QLineEdit()
            self.find_input.setClearButtonEnabled(True)
        
        if should_create_widget(self.find_previous_button):
            self.find_previous_button = QtWidgets.QToolButton()
            self.find_previous_button.setText('⬅')
            self.find_previous_button.triggered.connect(functools.partial(self.search, previous=True))
        
        if should_create_widget(self.find_sensitive):
            self.find_sensitive = QtWidgets.QCheckBox('Match Case')
        
        if should_create_widget(self.find_words):
            self.find_words = QtWidgets.QCheckBox('Words')
        
        if should_create_widget(self.find_regex):
            self.find_regex = QtWidgets.QCheckBox('Regex')
            self.find_regex.clicked.connect(self.handle_regex)
        
        if should_create_widget(self.find_previous_action):
            self.find_previous_action = QtWidgets.QAction('Find previous...')
            self.find_previous_action.setShortcut('SHIFT+ENTER')
            self.find_previous_action.triggered.connect(self.find_previous_button.click)
        
        if should_create_widget(self.find_next_action):
            self.find_next_action = QtWidgets.QAction('Find next...')
            self.find_next_action.setShortcut('ENTER')
            self.find_next_action.triggered.connect(self.find_next_button.click)
        
        if should_create_widget(self.hide_finder_action):
            self.hide_finder_action = QtWidgets.QAction('Hide')
            self.hide_finder_action.setShortcut('ESC')
            self.hide_finder_action.triggered.connect(self.container.hide)
        
        if should_create_widget(self.show_finder_action):
            self.show_finder_action = QtWidgets.QAction('Find...')
            self.show_finder_action.setShortcut('CTRL+F')
            self.show_finder_action.triggered.connect(self.container.show)
        
        # Layout validation
        page_layout: QtWidgets.QVBoxLayout = self.layout()
        find_layout: QtWidgets.QGridLayout = self.container.layout()
        flag_layout: QtWidgets.QHBoxLayout = self.find_flags.layout()
        
        if page_layout is None:
            page_layout = QtWidgets.QVBoxLayout(self)
        
        if find_layout is None:
            find_layout = QtWidgets.QGridLayout(self.container)
        
        if flag_layout is None:
            flag_layout = QtWidgets.QHBoxLayout(self.find_flags)
        
        # Page layout insertion
        if page_layout.indexOf(self.container) == -1:
            page_layout.insertWidget(0, self.container)
        
        if page_layout.indexOf(self.display) == -1:
            page_layout.addWidget(self.display)
        
        # Container layout insertion
        if find_layout.indexOf(self.find_previous_button) == -1:
            find_layout.addWidget(self.find_previous_button, 0, 0)
        
        if find_layout.indexOf(self.find_input) == -1:
            find_layout.addWidget(self.find_input, 0, 1)
        
        if find_layout.indexOf(self.find_next_button) == -1:
            find_layout.addWidget(self.find_next_button, 0, 2)
        
        if find_layout.indexOf(self.find_flags) == -1:
            # noinspection PyTypeChecker
            find_layout.addWidget(self.find_flags, 1, 0, -1, -1, 0)
        
        # Flags layout insertion
        if flag_layout.indexOf(self.find_sensitive) == -1:
            flag_layout.insertWidget(0, self.find_sensitive)
        
        if flag_layout.indexOf(self.find_words) == -1:
            flag_layout.insertWidget(1, self.find_words)
        
        if flag_layout.indexOf(self.find_regex) == -1:
            flag_layout.addWidget(self.find_regex)
        
        # QLineEdit action insertion
        self.find_input.addActions([self.find_previous_action, self.find_next_action, self.hide_finder_action])
        
        # QTextBrowser action insertion
        self.display.addAction(self.show_finder_action)
    
    # Display methods
    def set_html(self, html: str):
        """Sets the HTML for the QTextBrowser."""
        self.display.setHtml(html)
    
    def set_text(self, text: str):
        """Sets the text for the QTextBrowser."""
        self.display.setText(text)
    
    def set_plain_text(self, text: str):
        """Sets the plain text for the QTextBrowser."""
        self.display.setPlainText(text)
    
    # Finder slots
    def search(self, *args, previous: bool = None):
        """Finds the user's specified query, but backwards."""
        query = self.find_input.text()  # Get the user's query
        doc = self.display.document()  # Get the page's QTextDocument instance
        
        method: typing.Union[str, QtCore.QRegExp] = query
        
        # Regex check
        if self.find_regex.isChecked():
            method = QtCore.QRegExp(query)
            
            if self.find_sensitive.isChecked():
                method.setCaseSensitivity(QtCore.Qt.CaseSensitive)
            
            else:
                method.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
        
        # Flag validation
        flags = 0
        
        if previous:
            flags = doc.FindBackward
        
        if self.find_sensitive.isChecked():
            flags = flags | doc.FindCaseSensitively
        
        if self.find_words.isChecked() and self.find_words.isEnabled():
            flags = flags | doc.FindWholeWords
        
        # Find
        cursor = doc.find(method, self.display.cursor(), flags)
        
        # Cursor validation
        if cursor is not None:
            self.display.setCursor(cursor)
    
    def handle_regex(self):
        """Updates the flag checkboxes to reflect the user's options when regex
        is enabled/disabled."""
        self.find_words.setDisabled(self.find_regex.isChecked())
