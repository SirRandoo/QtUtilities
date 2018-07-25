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
# File Date: 12/22/2017'
from PyQt5 import QtWidgets, QtGui


__all__ = ["QAnimatedSplash"]


class QAnimatedSplash(QtWidgets.QSplashScreen):
    """An animated splash screen widget."""
    
    def __init__(self, qmovie: QtGui.QMovie=None, parent: QtWidgets.QWidget=None):
        super(QAnimatedSplash, self).__init__(parent=parent)
        
        self._movie = qmovie
    
    def setMovie(self, movie: QtGui.QMovie):
        self._movie = movie
    
    def updateFrame(self):
        self.setPixmap(self._movie.currentPixmap())
        self.update()
    
    # Qt Events #
    def showEvent(self, a0: QtGui.QShowEvent):
        if self._movie is None:
            raise ValueError("No movie set!")
        
        self._movie.updated.connect(self.updateFrame)
        self._movie.start()
