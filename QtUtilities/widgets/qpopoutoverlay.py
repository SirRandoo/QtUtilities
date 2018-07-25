#  This file is part of QtUtilities.
#
#  QtUtilities is free software: you can
#  redistribute it and/or modify it under the
#  terms of the GNU Lesser General Public
#  License as published by the Free Software
#  Foundation, either version 3 of the License,
#  or (at your option) any later version.
#
#  QtUtilities is distributed in the hope
#  that it will be useful, but WITHOUT ANY
#  WARRANTY; without even the implied warranty
#  of MERCHANTABILITY or FITNESS FOR A PARTICULAR
#  PURPOSE.  See the GNU Lesser General Public
#  License for more details.
#
#  You should have received a copy of the GNU
#  General Lesser Public License along with
#  QtUtilities.  If not,
#  see <http://www.gnu.org/licenses/>.
#
# Author: RandomShovel
# File Date: 10/14/2017
import traceback

from PyQt5 import QtWidgets, QtCore, QtGui


__all__ = ["QPopoutOverlay"]


class QPopoutOverlay(QtWidgets.QWidget):
    """Creates an overlay with a singular button.
    This overlay is used to define "popout-able" 
    widgets."""
    popout_widget = QtCore.pyqtSignal()
    
    def __init__(self, parent: QtWidgets.QWidget=None):
        #  Super Call  #
        super(QPopoutOverlay, self).__init__(parent=parent)
        
        #  Attributes  #
        self.size_policy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        self.size_policy.setHorizontalStretch(0)
        self.size_policy.setVerticalStretch(0)
        self.size_policy.setWidthForHeight(False)
        
        self.popout = QtWidgets.QPushButton(parent=self)
        self.popout.setText("◹")
        self.popout.setIconSize(QtCore.QSize(8, 8))
        self.popout.setMaximumSize(16, 16)
        self.popout.setFlat(True)
        self.popout.setSizePolicy(self.size_policy)
        self.popout.setStyleSheet("QPushButton:focus {border: none; outline: none;}")
        
        self.layout_ = QtWidgets.QGridLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setHorizontalSpacing(0)
        self.layout_.setVerticalSpacing(0)
        
        self.layout_.addItem(
            QtWidgets.QSpacerItem(12, 0, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Ignored),
            0, 0
        )
        self.layout_.addWidget(self.popout, 0, 1, 1, 1)
        self.layout_.addItem(
            QtWidgets.QSpacerItem(0, 12, QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Expanding),
            1, 1
        )
        
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.setLayout(self.layout_)
        
        self.popout.clicked.connect(self.popout_widget.emit)
    
    #  Methods  #
    def setIcon(self, icon: QtGui.QIcon):
        self.popout.setIcon(icon)
        
        if icon.isNull():
            self.popout.setText("⬈")
    
        else:
            self.popout.setText("")
