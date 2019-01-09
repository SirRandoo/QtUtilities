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

__all__ = {"QCircleProgressBar"}


class QCircleProgressBar(QtWidgets.QWidget):
    CircularStyle = 0
    GaugeStyle = 1
    
    def __init__(self, parent: QtWidgets.QWidget = None):
        #  Super Call  #
        super(QCircleProgressBar, self).__init__(parent=parent)
        
        #  Internal Attributes  #
        self.__progressStyle = self.CircularStyle
        self.__padding = 5.0
        self.__value = 0
        self.__maximum = 100
        self.__minimum = 0
        
        self.__progressColor = QtGui.QColor(33, 150, 243)
        self.__basePlateColor = self.palette().color(self.backgroundRole())
        self.__progressBackColor = self.__progressColor.darker()
        self.__textColor = self.__basePlateColor
        
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        
        self.__textFormat = "{}%"
    
    def setTextFormat(self, form: str):
        self.__textFormat = form
    
    def setTextColor(self, color: QtGui.QColor):
        self.__textColor = color
    
    def textColor(self):
        return self.__textColor
    
    def padding(self):
        return self.__padding
    
    def setPadding(self, value: float):
        self.__padding = value
    
    def progressColor(self):
        return self.__progressColor
    
    def setProgressColor(self, color: QtGui.QColor):
        self.__progressColor = color
    
    def basePlateColor(self):
        return self.__basePlateColor
    
    def setBasePlateColor(self, color: QtGui.QColor):
        self.__basePlateColor = color
    
    def progressBackColor(self):
        return self.__progressBackColor
    
    def setProgressBackColor(self, color: QtGui.QColor):
        self.__progressBackColor = color
    
    def progressStyle(self):
        return self.__progressStyle
    
    def setProgressStyle(self, style: int):
        self.__progressStyle = style
    
    def setMinimum(self, value: int):
        if value <= self.maximum():
            self.__minimum = value
        
        if self.value() < self.minimum():
            self.setValue(self.minimum())
    
    def minimum(self):
        return self.__minimum
    
    def setMaximum(self, value: int):
        if value >= self.minimum():
            self.__maximum = value
        
        if self.value() > self.maximum():
            self.setValue(self.maximum())
    
    def maximum(self):
        return self.__maximum
    
    def value(self):
        return self.__value
    
    def incrementValue(self):
        self.setValue(self.value() + 1)
    
    def decrementValue(self):
        self.setValue(self.value() - 1)
    
    def setValue(self, value: int):
        if self.maximum() >= value >= self.minimum():
            self.__value = value
    
    def sizeHint(self):
        return QtCore.QSize(32, 32)
    
    def paintEvent(self, event: QtGui.QPaintEvent):
        progressRect = self.contentsRect()  # type: QtCore.QRect
        painter = QtGui.QPainter(self)
        painter.setRenderHint(QtGui.QPainter.Antialiasing)
        painter.setBrush(QtGui.QBrush(self.progressColor()))
        
        if progressRect.width() < progressRect.height():
            progressRect.setHeight(progressRect.width())
        
        elif progressRect.height() < progressRect.width():
            progressRect.setWidth(progressRect.height())
        
        progressFont = painter.font()
        progressBase = QtGui.QPainterPath()
        progressFront = QtGui.QPainterPath()
        progressBack = QtGui.QPainterPath()
        progressFore = QtGui.QPainterPath()
        
        progressBase.addEllipse(QtCore.QRectF(progressRect))
        painter.fillPath(progressBase, self.basePlateColor())
        
        progressBack.addEllipse(QtCore.QRectF(
            progressRect.x() + self.padding(),
            progressRect.y() + self.padding(),
            progressRect.width() - (self.padding() * 2),
            progressRect.height() - (self.padding() * 2)
        ))
        painter.fillPath(progressBack, self.progressBackColor())
        
        if self.value() > 0:
            progressFore.moveTo(progressRect.center())
            progressFore.arcTo(QtCore.QRectF(
                progressRect.x() + self.padding(),
                progressRect.y() + self.padding(),
                progressRect.width() - (self.padding() * 2),
                progressRect.height() - (self.padding() * 2)
            ), 91, -(360 * self.value() / self.maximum()))
            progressFore.closeSubpath()
            painter.fillPath(progressFore, self.progressColor())
        
        progressFront.addEllipse(QtCore.QRectF(
            progressRect.x() + self.padding() * 2,
            progressRect.y() + self.padding() * 2,
            progressRect.width() - (self.padding() * 4),
            progressRect.height() - (self.padding() * 4)
        ))
        painter.fillPath(progressFront, self.basePlateColor())
        
        textPercent = self.__textFormat.format(int(round((self.value() / self.maximum()) * 100, 0)))
        textWidth = progressRect.width() - (self.padding() * 15)
        textHeight = progressRect.height() - (self.padding() * 15)
        scaleFactor = textWidth / painter.fontMetrics().width(textPercent)
        fontSize = progressFont.pointSizeF() * scaleFactor
        font = QtGui.QFont()
        font.setPointSizeF(fontSize)
        fontMetrics = QtGui.QFontMetricsF(font)
        
        while (fontMetrics.width(textPercent) > textWidth) or (fontMetrics.height() > textHeight):
            fontMetrics = QtGui.QFontMetricsF(font)
            font.setPointSizeF(font.pointSizeF() - 1)
            
            if font.pointSizeF() < 1:
                break
        
        painter.setFont(font)
        painter.setPen(QtGui.QPen(self.textColor()))
        
        textRect = QtCore.QRectF(
            (progressRect.width() / 2) - painter.fontMetrics().width(textPercent) / 2,
            ((progressRect.height() / 2) - painter.fontMetrics().height() / 2) - textHeight / 20,
            textWidth,
            textHeight
        )
        painter.drawText(textRect, textPercent)
