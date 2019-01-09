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
import sys

from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = {"QSlideButton"}


class QSlideButton(QtWidgets.QAbstractButton):
    """Represents a slider button similar to
    Android/iOS buttons."""
    ButtonPadding = 4
    RoundedRadius = 12
    
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(QSlideButton, self).__init__(parent=parent)
        self.setCheckable(True)
        
        self.buttonBackgroundColor = QtGui.QColor(204, 204, 204)
        self.buttonForegroundColor = QtGui.QColor(33, 150, 243)
        self.buttonColor = QtGui.QColor(255, 255, 255)
        
        self.__circular = True
        self.isAnimationScheduled = False
        self.buttonXOffset = self.ButtonPadding
        
        self.toggled.connect(self.scheduleAnimation)
    
    def scheduleAnimation(self):
        self.isAnimationScheduled = True
    
    def setCircular(self, value: bool):
        self.__circular = value
    
    def isCircular(self):
        return self.__circular
    
    def slideButton(self, painter: QtGui.QPainter):
        if self.width() > 0 and self.height() > 0:
            path = QtGui.QPainterPath()
            path2 = QtGui.QPainterPath()
            
            widthDistance = self.width() - self.height()
            buttonXOffsetModifier = (widthDistance / self.width()) / 10
            alphaModifier = (1 / widthDistance) * buttonXOffsetModifier
            
            if self.isChecked():
                new_alpha = self.buttonForegroundColor.alphaF() + alphaModifier
                
                if new_alpha > 1:
                    new_alpha = 1
                
                self.buttonForegroundColor.setAlphaF(new_alpha)
                self.buttonXOffset += buttonXOffsetModifier
            
            else:
                new_alpha = self.buttonForegroundColor.alphaF() - alphaModifier
                
                if new_alpha < 0:
                    new_alpha = 0
                
                self.buttonForegroundColor.setAlphaF(new_alpha)
                self.buttonXOffset -= buttonXOffsetModifier
            
            if self.buttonXOffset >= (widthDistance + self.ButtonPadding) or self.buttonXOffset <= self.ButtonPadding:
                if self.buttonXOffset > (widthDistance + self.ButtonPadding):
                    self.buttonXOffset = widthDistance + self.ButtonPadding
                
                elif self.buttonXOffset < self.ButtonPadding:
                    self.buttonXOffset = self.ButtonPadding
                
                self.isAnimationScheduled = False
            
            else:
                if not self.isCircular():
                    painter.fillRect(self.rect(), self.buttonBackgroundColor)
                    painter.fillRect(self.rect(), self.buttonForegroundColor)
                    painter.fillRect(QtCore.QRect(
                        self.buttonXOffset,
                        self.ButtonPadding,
                        widthDistance - self.ButtonPadding * 2,
                        self.height() - self.ButtonPadding * 2
                    ), self.buttonColor)
                
                elif self.isCircular():
                    path.addRoundedRect(QtCore.QRectF(self.rect()), self.RoundedRadius, self.height() // 2)
                    painter.fillPath(path, self.buttonBackgroundColor)
                    painter.fillPath(path, self.buttonForegroundColor)
                    
                    path2.addEllipse(QtCore.QRectF(
                        self.buttonXOffset,
                        self.ButtonPadding,
                        self.height() - self.ButtonPadding * 2,
                        self.height() - self.ButtonPadding * 2
                    ))
                    
                    painter.fillPath(path2, self.buttonColor)
                    painter.drawPath(path)
    
    def paintEvent(self, event: QtGui.QPaintEvent):
        if self.height() > 0 and self.width() > 0:
            painter = QtGui.QPainter(self)
            path = QtGui.QPainterPath()
            path2 = QtGui.QPainterPath()
            pen = QtGui.QPen(QtCore.Qt.NoPen)
            
            painter.setPen(pen)
            painter.setRenderHint(QtGui.QPainter.HighQualityAntialiasing)
            widthDistance = self.width() - self.height()
            
            if not self.isAnimationScheduled:
                if self.isChecked():
                    if self.buttonForegroundColor.alpha() < 255:
                        self.buttonForegroundColor.setAlpha(255)
                
                else:
                    if self.buttonForegroundColor.alpha() > 0:
                        self.buttonForegroundColor.setAlpha(0)
                
                if not self.isCircular():
                    painter.fillRect(self.rect(), self.buttonBackgroundColor)
                    painter.fillRect(self.rect(), self.buttonForegroundColor)
                
                elif self.isCircular():
                    path.addRoundedRect(QtCore.QRectF(self.rect()), self.RoundedRadius, self.height())
                    painter.fillPath(path, self.buttonBackgroundColor)
                    painter.fillPath(path, self.buttonForegroundColor)
                
                if self.isChecked():
                    switch_rect = QtCore.QRect(
                        widthDistance + self.ButtonPadding,  # X Position
                        self.ButtonPadding,  # Y Position
                        widthDistance - self.ButtonPadding * 2,  # Width
                        self.height() - self.ButtonPadding * 2  # Height
                    )
                
                else:
                    switch_rect = QtCore.QRect(
                        self.ButtonPadding,  # X Position
                        self.ButtonPadding,  # Y Position
                        widthDistance - self.ButtonPadding * 2,  # Width
                        self.height() - self.ButtonPadding * 2  # Height
                    )
                
                if not self.isCircular():
                    painter.fillRect(switch_rect, self.buttonColor)
                
                elif self.isCircular():
                    path2.addEllipse(QtCore.QRectF(
                        self.buttonXOffset,
                        self.ButtonPadding,
                        self.height() - self.ButtonPadding * 2,
                        self.height() - self.ButtonPadding * 2
                    ))
                    
                    painter.fillPath(path2, self.buttonColor)
                    painter.drawPath(path2)
            
            else:
                if self.buttonXOffset >= (widthDistance + self.ButtonPadding) \
                        or self.buttonXOffset <= self.ButtonPadding:
                    self.buttonForegroundColor.setAlpha(0 if self.isChecked() else 255)
                
                self.slideButton(painter)
                self.update()
    
    def resizeEvent(self, event: QtGui.QResizeEvent):
        if (self.buttonXOffset > self.ButtonPadding) and not self.isAnimationScheduled:
            self.buttonXOffset = (self.width() - self.height()) + self.ButtonPadding
    
    def sizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(32, 23)
    
    def minimumSizeHint(self) -> QtCore.QSize:
        return QtCore.QSize(0, 0)
    
    def maximumSize(self) -> QtCore.QSize:
        return QtCore.QSize(sys.maxsize, sys.maxsize)
    
    def minimumSize(self) -> QtCore.QSize:
        return QtCore.QSize(0, 0)
