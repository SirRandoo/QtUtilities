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
from PyQt5 import QtCore, QtWidgets

__all__ = {"ProgressWidget"}


class ProgressWidget(QtWidgets.QWidget):
    """Represents a label-progressbar pair within a widget."""
    
    def __init__(self, display_text: str = None, parent: QtWidgets.QWidget = None):
        super(ProgressWidget, self).__init__(parent=parent)
        
        self.label = QtWidgets.QLabel(parent=self)
        self.bar = QtWidgets.QProgressBar(parent=self)
        self._layout = QtWidgets.QVBoxLayout(self)
        
        self._layout.addWidget(self.label, None, QtCore.Qt.AlignCenter)
        self._layout.addWidget(self.bar, None, QtCore.Qt.AlignCenter)
        
        self.set_display_text = self.label.setText
        self.set_maximum = self.bar.setMaximum
        self.set_minimum = self.bar.setMinimum
        self.set_range = self.bar.setRange
        
        if display_text is not None:
            self.label.setText(display_text)
    
    def increment(self):
        """Increments the progress bar's progress by 1."""
        value = self.bar.value() + 1
        
        if value > self.bar.maximum():
            value = self.bar.maximum()
        
        self.bar.setValue(value)
    
    def decrement(self):
        """Decrements the progress bar's progress by 1."""
        value = self.bar.value() - 1
        
        if value < self.bar.minimum():
            value = self.bar.minimum()
        
        self.bar.setValue(value)
    
    def reset(self):
        """Resets the progress widget's values."""
        self.label.clear()
        self.bar.reset()
