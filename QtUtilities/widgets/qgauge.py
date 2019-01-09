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
import traceback

from PyQt5 import QtCore, QtGui, QtWidgets

__all__ = {"QGauge"}


class QGauge(QtWidgets.QWidget):
    def __init__(self, parent: QtWidgets.QWidget = None):
        super(QGauge, self).__init__(parent=parent)
        
        self.__value = 0.0
        self.__maximum = 100.0
        self.__minimum = 0.0
        self.__text = str()
        
        self.__gaugeColor = QtGui.QColor(33, 150, 243)
        self.__gaugeBackColor = self.__gaugeColor.darker()
        self.__basePlateColor = self.palette().color(self.backgroundRole())
        self.__textColor = self.__basePlateColor
        
        self.__gaugePadding = 3.0
        self.__gaugeDepthAngle = 270
    
    def paintEvent(self, event: QtGui.QPaintEvent):
        try:
            painter = QtGui.QPainter(self)
            
            gaugeRect = self.contentsRect()
            basePBack = QtGui.QPainterPath()
            basePFore = QtGui.QPainterPath()
            gaugeFore = QtGui.QPainterPath()
            gaugeBack = QtGui.QPainterPath()
            
            basePBack.moveTo(gaugeRect.center())
            basePBack.arcTo(QtCore.QRectF(gaugeRect), 0, self.__gaugeDepthAngle)
            basePBack.closeSubpath()
            painter.fillPath(basePBack, self.basePlateColor())
            
            gaugeBack.moveTo(QtCore.QPointF(gaugeRect.center().x(), gaugeRect.center().y() - self.gaugePadding()))
            gaugeBack.arcTo(QtCore.QRectF(
                gaugeRect.x() + self.gaugePadding(),
                gaugeRect.y() + self.gaugePadding(),
                gaugeRect.width() - self.gaugePadding() * 2,
                gaugeRect.height() - self.gaugePadding() * 4
            ), -270 - self.__gaugeDepthAngle / 2, self.__gaugeDepthAngle)
            gaugeBack.closeSubpath()
            painter.fillPath(gaugeBack, self.gaugeBackgroundColor())
            
            gaugeFore.moveTo(QtCore.QPointF(gaugeRect.center().x(), gaugeRect.center().y() - self.gaugePadding()))
            gaugeFore.arcTo(QtCore.QRectF(
                gaugeRect.x() + self.gaugePadding(),
                gaugeRect.y() + self.gaugePadding(),
                gaugeRect.width() - self.gaugePadding() * 2,
                gaugeRect.height() - self.gaugePadding() * 4
            ), 360 - self.__gaugeDepthAngle / 2, -(self.__gaugeDepthAngle * self.value() / self.maximum()))
            gaugeFore.closeSubpath()
            painter.fillPath(gaugeFore, self.gaugeColor())
            
            basePFore.moveTo(gaugeRect.center())
            basePFore.arcTo(QtCore.QRectF(
                gaugeRect.x() + self.gaugePadding() * 8,
                gaugeRect.y() + self.gaugePadding() * 8,
                gaugeRect.width() - self.gaugePadding() * 16,
                gaugeRect.height() - self.gaugePadding() * 16
            ), 0, 360)
            basePFore.closeSubpath()
            painter.fillPath(basePFore, self.basePlateColor())
            
            if len(self.text()) > 0:
                gaugeFont = painter.font()
                textWidth = gaugeRect.width() - (self.gaugePadding() * 50)
                textHeight = gaugeRect.height() / 2 + (self.gaugePadding() * 15)
                scaleFactor = textWidth / painter.fontMetrics().width(self.text())
                fontSize = gaugeFont.pointSizeF() * scaleFactor
                font = QtGui.QFont()
                font.setPointSizeF(fontSize)
                fontMetrics = QtGui.QFontMetricsF(font)
                
                while (fontMetrics.width(self.text()) > textWidth) or (fontMetrics.height() > textHeight):
                    fontMetrics = QtGui.QFontMetricsF(font)
                    font.setPointSizeF(font.pointSizeF() - 1)
                    
                    if font.pointSizeF() < 1:
                        break
                
                painter.setFont(font)
                painter.setPen(QtGui.QPen(self.textColor().darker()))
                
                textRect = QtCore.QRectF(
                    (gaugeRect.width() / 2) - painter.fontMetrics().width(self.text()) / 2,
                    (textHeight / 2) - (painter.fontMetrics().height() / 2),
                    textWidth,
                    textHeight
                )
                painter.drawText(textRect, self.text(), QtGui.QTextOption())
        
        except Exception as e:
            traceback.print_exc()
    
    def sizeHint(self):
        return QtCore.QSize(20, 190)
    
    def minimumSizeHint(self):
        return QtCore.QSize(0, 0)
    
    def maximumSize(self):
        return QtCore.QSize(sys.maxsize, sys.maxsize)
    
    def minimumSize(self):
        return QtCore.QSize(0, 0)
    
    def text(self):
        return self.__text
    
    def setText(self, value: str):
        self.__text = value
    
    def gaugePadding(self):
        return self.__gaugePadding
    
    def setGaugePadding(self, value: float):
        self.__gaugePadding = value
    
    def gaugeColor(self):
        return self.__gaugeColor
    
    def setGaugeColor(self, color: QtGui.QColor):
        self.__gaugeColor = color
    
    def gaugeBackgroundColor(self):
        return self.__gaugeBackColor
    
    def setGaugeBackgroundColor(self, color: QtGui.QColor):
        self.__gaugeBackColor = color
    
    def basePlateColor(self):
        return self.__basePlateColor
    
    def setBasePlateColor(self, color: QtGui.QColor):
        self.__basePlateColor = color
    
    def textColor(self):
        return self.__textColor
    
    def setTextColor(self, color: QtGui.QColor):
        self.__textColor = color
    
    def value(self):
        return self.__value
    
    def setValue(self, value: float):
        if self.minimum() <= value <= self.maximum():
            self.__value = value
    
    def minimum(self):
        return self.__minimum
    
    def setMaximum(self, value: float):
        if self.maximum() >= self.minimum():
            self.__maximum = value
        
        if self.value() > self.maximum():
            self.setValue(self.maximum())
    
    def maximum(self):
        return self.__maximum
    
    def setMinimum(self, value: float):
        if self.minimum() <= self.maximum():
            self.__minimum = value
        
        if self.value() < self.minimum():
            self.setValue(self.minimum())
    
    def incrementValue(self):
        self.setValue(self.value() + 1)
    
    def decrementValue(self):
        self.setValue(self.value() - 1)
