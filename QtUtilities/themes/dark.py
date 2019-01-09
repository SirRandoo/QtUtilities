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
from PyQt5 import QtCore, QtGui, QtWidgets


class Dark:
    """Transforms the application's palette into a darker look."""
    
    @classmethod
    def apply(cls, app: QtWidgets.QWidget):
        """Applies the theme."""
        # Declarations #
        palette = QtGui.QPalette()
        qcolor = QtGui.QColor
        white = QtCore.Qt.white
        yellow = QtCore.Qt.yellow
        light_gray = QtCore.Qt.lightGray
        
        # Color Assignments #
        palette.setColor(palette.Window, qcolor(50, 50, 50))
        palette.setColor(palette.WindowText, white)
        palette.setColor(palette.Base, qcolor(90, 90, 90))
        palette.setColor(palette.AlternateBase, qcolor(100, 100, 100))
        palette.setColor(palette.ToolTipBase, qcolor(120, 120, 120))
        palette.setColor(palette.ToolTipText, white)
        palette.setColor(palette.Text, white)
        palette.setColor(palette.Button, qcolor(70, 70, 70))
        palette.setColor(palette.ButtonText, white)
        palette.setColor(palette.BrightText, yellow)
        palette.setColor(palette.Link, QtCore.Qt.cyan)
        palette.setColor(palette.LinkVisited, QtCore.Qt.darkCyan)
        
        palette.setColor(palette.Disabled, palette.Text, light_gray)
        palette.setColor(palette.Disabled, palette.ButtonText, light_gray)
        
        app.setPalette(palette)
