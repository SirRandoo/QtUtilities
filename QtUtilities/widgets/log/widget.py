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

# TODO: Figure out a way to link the QTableWidget to the QLog's record list.
# TODO: Allow for the panels to be collapsible when no longer in use.
# TODO: Allow the user to specify custom colors for the QTableWidget.
#
# TODO: Add a context menu to the QTableWidget that allows users to...
#       - Clear the log
#       - Show details about a record
#
# TODO: Allow for users to filter the log by...
#       - Level
#       - Date
#       - Time
#       - Message content
#       - Function name
#       - Thread name
#       - Logger name
#       - Process name
#       - Path
#       - Module name
import datetime
import typing

from PyQt5 import QtCore, QtWidgets

from QtUtilities.utils import append_table, set_table_headers, should_create_widget

# from ...utils import set_table_headers, should_create_widget

__all__ = ['QLog']


class QLog(QtWidgets.QDialog):
    """A dialog for displaying output from Python's logging module."""
    
    def __init__(self, *, parent: QtWidgets.QWidget = None):
        # Super Call #
        super(QLog, self).__init__(parent=parent)
        
        # Ui Attributes #
        # Top-Level
        self.toolbar: typing.Optional[QtWidgets.QToolBar] = None
        self.toolbar_container: typing.Optional[QtWidgets.QStackedWidget] = None
        self.display: typing.Optional[QtWidgets.QTableWidget] = None
        self.details: typing.Optional[QtWidgets.QTableWidget] = None
        
        # Filter elements
        self.filter_container: typing.Optional[QtWidgets.QWidget] = None
        
        self.level_panel: typing.Optional[QtWidgets.QGroupBox] = None
        self.level_filter: typing.Optional[QtWidgets.QListWidget] = None
        
        self.logger_panel: typing.Optional[QtWidgets.QGroupBox] = None
        self.logger_filter: typing.Optional[QtWidgets.QTreeWidget] = None
        
        # Toolbar elements
        self.filter_action: typing.Optional[QtWidgets.QAction] = None
        self.color_action: typing.Optional[QtWidgets.QAction] = None
        
        # Misc
        self.deselect_action: typing.Optional[QtWidgets.QAction] = None
        
        # "Internal" Attributes #
        self._records: typing.List[dict] = []
        
        # Internal Calls #
        self.setup_ui()
        self.bind()
    
    # Ui Methods #
    def setup_ui(self):
        """Sets up the dialog's ui."""
        # Top-Level elements
        if should_create_widget(self.toolbar):
            self.toolbar = QtWidgets.QToolBar()
            self.toolbar.setAllowedAreas(QtCore.Qt.AllToolBarAreas)
            self.toolbar.setFloatable(False)
            self.toolbar.setOrientation(QtCore.Qt.Vertical)
            self.toolbar.setToolButtonStyle(QtCore.Qt.ToolButtonTextBesideIcon)
        
        if should_create_widget(self.toolbar_container):
            self.toolbar_container = QtWidgets.QStackedWidget()
            self.toolbar_container.setHidden(True)
        
        if should_create_widget(self.display):
            self.display = QtWidgets.QTableWidget()
            self.display.setWordWrap(True)
            self.display.setEditTriggers(self.display.NoEditTriggers)
            self.display.setDropIndicatorShown(False)
            self.display.setDragDropOverwriteMode(False)
            self.display.setSortingEnabled(True)
            self.display.verticalHeader().setHidden(True)
            
            set_table_headers(self.display, ['Timestamp', 'Name', 'Level', 'Message'])
            append_table(self.display, Timestamp=datetime.datetime.now(tz=datetime.timezone.utc).isoformat(),
                         Name='root', Level='INFO', Message='Testing')
        
        if should_create_widget(self.details):
            self.details = QtWidgets.QTableWidget()
            self.details.setWordWrap(True)
            self.details.setEditTriggers(self.details.NoEditTriggers)
            self.details.setDropIndicatorShown(False)
            self.details.setDragDropOverwriteMode(False)
            self.details.setSortingEnabled(False)
            self.details.verticalHeader().setHidden(True)
            self.details.setHidden(True)
            
            set_table_headers(self.details, ['Key', 'Value'])
        
        # Toolbar elements
        if should_create_widget(self.filter_action):
            self.filter_action = QtWidgets.QAction('⧩')
            self.filter_action.setToolTip('Opens the filter panel.')
        
        if should_create_widget(self.color_action):
            self.color_action = QtWidgets.QAction('🖌')
            self.color_action.setToolTip('Opens the color panel.')
        
        # Filter elements
        if should_create_widget(self.filter_container):
            self.filter_container = QtWidgets.QWidget()
        
        if should_create_widget(self.level_panel):
            self.level_panel = QtWidgets.QGroupBox('Level Filter')
            self.level_panel.setFlat(True)
        
        if should_create_widget(self.level_filter):
            self.level_filter = QtWidgets.QListWidget()
            self.level_filter.setEditTriggers(self.level_filter.NoEditTriggers)
            self.level_filter.setWordWrap(True)
            self.level_filter.setDropIndicatorShown(False)
            self.level_filter.setDragDropOverwriteMode(False)
            self.level_filter.setSortingEnabled(True)
        
        if should_create_widget(self.logger_panel):
            self.logger_panel = QtWidgets.QGroupBox('Logger Filter')
            self.logger_panel.setFlat(True)
        
        if should_create_widget(self.logger_filter):
            self.logger_filter = QtWidgets.QTreeWidget()
            self.logger_filter.setWordWrap(True)
            self.logger_filter.setEditTriggers(self.logger_filter.NoEditTriggers)
            self.logger_filter.setDropIndicatorShown(False)
            self.logger_filter.setDragEnabled(False)
            self.logger_filter.setSortingEnabled(True)
            self.logger_filter.setDragDropOverwriteMode(False)
            self.logger_filter.setHeaderHidden(True)
        
        # Misc
        if should_create_widget(self.deselect_action):
            self.deselect_action = QtWidgets.QAction('Deselect')
            self.deselect_action.setShortcut('ESC')
        
        layout = QtWidgets.QGridLayout(self)
        
        layout.addWidget(self.toolbar, 0, 0)
        layout.addWidget(self.toolbar_container, 0, 1)
        layout.addWidget(self.display, 0, 2)
        layout.addWidget(self.details, 1, 2)
        
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Toolbar insertion
        self.toolbar.addAction(self.filter_action)
        self.toolbar.addAction(self.color_action)
        
        # Filter panel
        self.toolbar_container.addWidget(self.filter_container)
        f_layout = QtWidgets.QGridLayout(self.filter_container)
        
        f_layout.addWidget(self.logger_panel, 0, 0)
        f_layout.addWidget(self.level_panel, 1, 0)
        
        # Level filter
        f_le_layout = QtWidgets.QGridLayout(self.level_panel)
        f_le_layout.addWidget(self.level_filter)
        
        # Logger filter
        f_lo_layout = QtWidgets.QGridLayout(self.logger_panel)
        f_lo_layout.addWidget(self.logger_filter)
        
        # Misc
        self.display.addAction(self.deselect_action)
    
    def bind(self):
        """Binds the ui's signals to their respective slots."""
        # Display signals
        self.display.itemActivated.connect(self.open_detailed_display)
        
        # Filter signals
        self.level_filter.itemActivated.connect(self.reset_display_filter)
        self.logger_filter.itemActivated.connect(self.reset_display_filter)
        
        # Toolbar signals
        self.filter_action.triggered.connect(self.toggle_filter_panel)
        self.color_action.triggered.connect(self.toggle_color_panel)
        
        # Misc signals
        self.deselect_action.triggered.connect(self.display.clearSelection)
    
    # Slots
    def open_detailed_display(self, item: QtWidgets.QTableWidgetItem = None):
        """Opens the detailed display for the selected record."""
        if item is not None:
            pass
    
    def reset_display_filter(self):
        pass
    
    def toggle_filter_panel(self):
        pass
    
    def toggle_color_panel(self):
        pass


if __name__ == '__main__':
    a = QtWidgets.QApplication([])
    
    l = QLog()
    l.show()
    
    a.exec()
