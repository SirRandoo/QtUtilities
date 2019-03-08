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
import functools
import os

from PyQt5 import QtCore, QtGui, QtWidgets

from .setting import Setting

__all__ = {'qcombobox', 'qaddablelist', 'qdir', 'qfile', 'qlist', 'char',
           'text', 'number', 'decimal', 'boolean'}


def qcombobox(obj: Setting) -> QtWidgets.QComboBox:
    """Converts a settings object into a visible QComboBox."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    combobox = QtWidgets.QComboBox(parent=parent)
    
    if combobox.isWindow():
        combobox.hide()
    
    # Adjustments
    combobox.setMaxVisibleItems(obj.data.get('max_visible', 200))
    combobox.setMinimumContentsLength(obj.data.get('min_content_length', 1))
    
    # Population
    if 'choices' in obj.data:
        for choice in obj.data.get('choices', []):
            if isinstance(choice, dict):
                if 'icon' in choice:
                    combobox.addItem(QtGui.QIcon(choice['icon']), choice.get('text', ''))
                
                else:
                    combobox.addItem(choice.get('text', ''))
            
            elif isinstance(choice, str):
                combobox.addItem(choice)
        
        combobox.setCurrentIndex(obj.value)
    
    # Validation
    if obj.converter != 'qcombobox':
        obj.data['converter'] = 'qcombobox'
    
    # Signals
    combobox.currentIndexChanged.connect(functools.partial(setattr, obj, 'value'))
    
    # Return
    return combobox


def qfontbox(obj: Setting) -> QtWidgets.QFontComboBox:
    """Converts a settings object into a visible QFontComboBox."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    combobox = QtWidgets.QFontComboBox(parent=parent)
    
    if combobox.isWindow():
        combobox.hide()
    
    # Adjustments
    combobox.setMaxVisibleItems(obj.data.get('max_visible', 200))
    combobox.setMinimumContentsLength(obj.data.get('min_content_length', 1))
    
    # Population
    combobox.setCurrentFont(QtGui.QFont(obj.value))
    
    # Validation
    if obj.converter != 'qfontbox':
        obj.data['converter'] = 'qfontbox'
    
    # Signals
    def store_font(font: QtGui.QFont):
        obj.value = font.rawName()
    
    combobox.currentFontChanged.connect(store_font)
    
    # Return
    return combobox


# noinspection PyArgumentList
def qfile(obj: Setting) -> QtWidgets.QWidget:
    """Converts a settings object into a visible QWidget."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    widget = QtWidgets.QWidget(parent=parent)
    line = QtWidgets.QLineEdit(parent=widget)
    button = QtWidgets.QPushButton('Open...', parent=widget)
    layout = QtWidgets.QHBoxLayout(widget)
    
    if widget.isWindow():
        widget.hide()
    
    if line.isWindow():
        widget.hide()
    
    if button.isWindow():
        button.hide()
    
    # noinspection PyArgumentList
    def show_dialog():
        dialog = QtWidgets.QFileDialog()
        url, _ = dialog.getOpenFileUrl(parent=widget,
                                       caption='Select a file...',
                                       directory=os.getcwd())
        
        if url.isValid():
            path: str = url.toDisplayString(url.RemoveScheme | url.NormalizePathSegments).lstrip("/")
            
            line.setText(path)
            obj.value = path
        
        dialog.deleteLater()
    
    # Adjustments
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Population
    layout.addWidget(line)
    layout.addWidget(button)
    
    if obj.value is not None:
        line.setText(str(obj.value))
    
    # Validation
    if obj.converter != 'qfile':
        obj.data['converter'] = 'qfile'
    
    # Signals
    button.clicked.connect(show_dialog)
    
    # Return
    return widget


# noinspection PyArgumentList
def qdir(obj: Setting) -> QtWidgets.QWidget:
    """Converts a settings object into a visible QWidget."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    widget = QtWidgets.QWidget(parent=parent)
    line = QtWidgets.QLineEdit(parent=widget)
    button = QtWidgets.QPushButton('Open...', parent=widget)
    layout = QtWidgets.QHBoxLayout(widget)
    
    def show_dialog():
        dialog = QtWidgets.QFileDialog()
        url: QtCore.QUrl = dialog.getExistingDirectoryUrl(parent=widget,
                                                          caption='Select a directory...',
                                                          directory=QtCore.QUrl(os.getcwd()))
        
        if url.isValid():
            # noinspection PyTypeChecker
            path: str = url.toDisplayString(url.RemoveScheme | url.NormalizePathSegments).lstrip("/")
            
            line.setText(path)
            obj.value = path
        
        dialog.deleteLater()
    
    # Adjustments
    layout.setContentsMargins(0, 0, 0, 0)
    
    # Population
    layout.addWidget(line)
    layout.addWidget(button)
    
    if obj.value is not None:
        line.setText(str(obj.value))
    
    # Validation
    if obj.converter != 'qdir':
        obj.data['converter'] = 'qdir'
    
    # Signals
    button.clicked.connect(show_dialog)
    
    # Return
    return widget


# noinspection PyArgumentList
def qlist(obj: Setting) -> QtWidgets.QWidget:
    """Converts a settings object into a QWidget."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    widget = QtWidgets.QWidget(parent=parent)
    surrogate = QtWidgets.QWidget(parent=widget)
    list_widget = QtWidgets.QListWidget(parent=widget)
    up = QtWidgets.QPushButton('▲', parent=surrogate)
    down = QtWidgets.QPushButton('▼', parent=surrogate)
    layout = QtWidgets.QHBoxLayout(widget)
    s_layout = QtWidgets.QVBoxLayout(surrogate)
    
    def move_up():
        index = list_widget.currentRow()
        
        if index > 0:
            item = list_widget.takeItem(index)
            list_widget.insertItem(index - 1, item)
            list_widget.setCurrentRow(index - 1)
    
    def move_down():
        index = list_widget.currentRow()
        
        if index > 0 and list_widget.count() > 1:
            item = list_widget.takeItem(index)
            list_widget.insertItem(index + 1, item)
            list_widget.setCurrentRow(index + 1)
    
    # Adjustments
    up.setMaximumSize(16, 16)
    down.setMaximumSize(16, 16)
    
    layout.setContentsMargins(0, 0, 0, 0)
    s_layout.setContentsMargins(0, 0, 0, 0)
    
    list_widget.setEditTriggers(list_widget.DoubleClicked)
    list_widget.setViewMode(obj.data.get('view_mode', list_widget.ListMode))
    
    # Population
    if not isinstance(obj.value, list):
        obj.value = [obj.value]
    
    list_widget.addItems(obj.value)
    
    s_layout.addWidget(up)
    s_layout.addWidget(down)
    
    layout.addWidget(list_widget)
    layout.addWidget(surrogate)
    
    # Validation
    if obj.converter != 'qlist':
        obj.data['converter'] = 'qlist'
    
    # Signals
    up.clicked.connect(move_up)
    down.clicked.connect(move_down)
    
    # Return
    return widget


# noinspection PyArgumentList
def qaddablelist(obj: Setting) -> QtWidgets.QWidget:
    """Converts a setting object into a QWidget."""
    """Converts a settings object into a QWidget."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    widget = QtWidgets.QWidget(parent=parent)
    surrogate = QtWidgets.QWidget(parent=widget)
    list_widget = QtWidgets.QListWidget(parent=widget)
    add = QtWidgets.QPushButton('+', parent=surrogate)
    remove = QtWidgets.QPushButton('-', parent=surrogate)
    up = QtWidgets.QPushButton('▲', parent=surrogate)
    down = QtWidgets.QPushButton('▼', parent=surrogate)
    layout = QtWidgets.QHBoxLayout(widget)
    s_layout = QtWidgets.QVBoxLayout(surrogate)
    
    def add_item():
        item = QtWidgets.QListWidgetItem()
        list_widget.addItem(item)
        list_widget.editItem(item)
    
    def remove_item():
        index = list_widget.currentRow()
        
        if index != -1:
            list_widget.takeItem(index)
    
    def move_up():
        index = list_widget.currentRow()
        
        if index > 0:
            item = list_widget.takeItem(index)
            list_widget.insertItem(index - 1, item)
            list_widget.setCurrentRow(index - 1)
    
    def move_down():
        index = list_widget.currentRow()
        
        if index > 0 and list_widget.count() > 1:
            item = list_widget.takeItem(index)
            list_widget.insertItem(index + 1, item)
            list_widget.setCurrentRow(index + 1)
    
    def save():
        data = []
        
        for index in range(list_widget.count()):
            item: QtWidgets.QListWidgetItem = list_widget.item(index)
            
            if item:
                data.append(item.text())
        
        obj.value = data
    
    # Adjustments
    add.setMaximumSize(16, 16)
    remove.setMaximumSize(16, 16)
    
    up.setMaximumSize(16, 16)
    down.setMaximumSize(16, 16)
    
    layout.setContentsMargins(0, 0, 0, 0)
    s_layout.setContentsMargins(0, 0, 0, 0)
    
    list_widget.setEditTriggers(list_widget.DoubleClicked)
    list_widget.setViewMode(obj.data.get('view_mode', list_widget.ListMode))
    
    # Population
    if not isinstance(obj.value, list):
        obj.value = [str(obj.value)]
    
    list_widget.addItems(obj.value)
    
    s_layout.addWidget(add)
    s_layout.addWidget(remove)
    
    s_layout.addWidget(up)
    s_layout.addWidget(down)
    
    layout.addWidget(list_widget)
    layout.addWidget(surrogate)
    
    # Validation
    if obj.converter != 'qaddablelist':
        obj.data['converter'] = 'qaddablelist'
    
    # Signals
    add.clicked.connect(add_item)
    remove.clicked.connect(remove_item)
    
    up.clicked.connect(move_up)
    down.clicked.connect(move_down)
    
    list_widget.model().rowsInserted.connect(save)
    list_widget.model().rowsRemoved.connect(save)
    list_widget.model().rowsMoved.connect(save)
    
    # Return
    return widget


def char(obj: Setting) -> QtWidgets.QLineEdit:
    """Converts a settings object into a QLineEdit."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    line = QtWidgets.QLineEdit(parent=parent)
    
    if line.isWindow():
        line.hide()
    
    # Population
    if obj.value is not None:
        line.setText(str(obj.value))

    line.setMaxLength(obj.data.get('max_length', 260))
    line.setClearButtonEnabled(obj.data.get('clear_button', False))
    line.setEchoMode(obj.data.get('echo_mode', line.NoEcho))
    line.setPlaceholderText(obj.data.get('placeholder', ''))
    
    # Validation
    if obj.converter != 'char':
        obj.data['converter'] = 'char'
    
    # Signals
    line.textChanged.connect(functools.partial(setattr, obj, 'value'))
    
    # Return
    return line


def text(obj: Setting) -> QtWidgets.QTextEdit:
    """Converts a settings object into a QTextEdit."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    edit = QtWidgets.QTextEdit(parent=parent)
    
    # Population
    if obj.value is not None:
        edit.setText(str(obj.value))
    
    # Validation
    if obj.converter != 'text':
        obj.data['converter'] = 'text'
    
    # Signals
    edit.textChanged.connect(functools.partial(setattr, obj, 'value', edit.toPlainText()))
    
    # Return
    return edit


def number(obj: Setting) -> QtWidgets.QSpinBox:
    """Converts a settings object into a QSpinBox."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    spin = QtWidgets.QSpinBox(parent=parent)
    
    if spin.isWindow():
        spin.hide()
    
    # Population
    if obj.value is not None:
        spin.setValue(int(obj.value))
    
    # Adjustments
    spin.setRange(obj.data.get('minimum', -1000000), obj.data.get('maximum', 1000000))
    spin.setButtonSymbols(obj.data.get('buttons', spin.UpDownArrows))
    spin.setGroupSeparatorShown(obj.data.get('separator', False))
    
    # Validation
    if obj.converter != 'number':
        obj.data['converter'] = 'number'
    
    # Signals
    spin.valueChanged.connect(functools.partial(setattr, obj, 'value'))
    
    # Return
    return spin


def decimal(obj: Setting) -> QtWidgets.QDoubleSpinBox:
    """Converts a settings object into a QDoubleSpinBox."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    spin = QtWidgets.QDoubleSpinBox(parent=parent)
    
    # Population
    if obj.value is not None:
        spin.setValue(float(obj.value))
    
    # Adjustments
    spin.setRange(obj.data.get('minimum', -1000000), obj.data.get('maximum', 1000000))
    spin.setGroupSeparatorShown(obj.data.get('separator', False))
    spin.setButtonSymbols(obj.data.get('buttons', spin.UpDownArrows))
    
    # Validation
    if obj.converter != 'decimal':
        obj.data['converter'] = 'decimal'
    
    # Signals
    spin.valueChanged.connect(functools.partial(setattr, obj, 'value'))
    
    # Return
    return spin


def boolean(obj: Setting) -> QtWidgets.QCheckBox:
    """Converts a settings object into a QCheckBox."""
    # Declarations
    parent = obj.parent()
    parent = getattr(parent, '_container', None)
    
    check = QtWidgets.QCheckBox(parent=parent)
    
    if check.isWindow():
        check.hide()
    
    def change_value(state: int):
        if state == QtCore.Qt.PartiallyChecked or state == QtCore.Qt.Checked:
            obj.value = True
        
        else:
            obj.value = False
    
    # Adjustments
    check.setTristate(obj.data.get('tristate', False))
    
    # Population
    if obj.value is not None:
        check.setChecked(bool(obj.value))
    
    # Validation
    if obj.converter != 'boolean':
        obj.data['converter'] = 'boolean'
    
    # Signals
    check.stateChanged.connect(change_value)
    
    # Return
    return check
