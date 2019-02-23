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

__all__ = ['dark', 'high_contrast']


def dark(app: QtWidgets.QWidget):
    """Transforms the widget's palette into a darker look."""
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


def high_contrast(app: QtWidgets.QWidget):
    """Transforms the widget's palette into a darker, higher contrast look."""
    # Declarations #
    palette = QtGui.QPalette()
    qcolor = QtGui.QColor
    yellow: QtGui.QColor = qcolor(QtCore.Qt.yellow)
    dark_yellow: QtGui.QColor = qcolor(QtCore.Qt.darkYellow)
    light_yellow: QtGui.QColor = yellow.lighter()

    # Color Assignments #
    palette.setColor(palette.Window, qcolor(10, 10, 10))
    palette.setColor(palette.WindowText, yellow)
    palette.setColor(palette.Base, qcolor(50, 50, 50))
    palette.setColor(palette.AlternateBase, qcolor(65, 65, 65))
    palette.setColor(palette.ToolTipBase, qcolor(90, 90, 90))
    palette.setColor(palette.ToolTipText, yellow)
    palette.setColor(palette.Text, yellow)
    palette.setColor(palette.Button, qcolor(40, 40, 40))
    palette.setColor(palette.ButtonText, yellow)
    palette.setColor(palette.BrightText, light_yellow)
    palette.setColor(palette.Link, light_yellow)
    palette.setColor(palette.LinkVisited, yellow)

    palette.setColor(palette.Disabled, palette.Text, dark_yellow)
    palette.setColor(palette.Disabled, palette.ButtonText, dark_yellow)

    app.setPalette(palette)
