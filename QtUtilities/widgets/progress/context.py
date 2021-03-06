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
import functools
import typing

from PyQt5 import QtCore, QtWidgets, sip

from QtUtilities import signals


class Context(QtWidgets.QDialog):
    """A special progress dialog that works as a context manager."""
    
    def __init__(self, maximum: int = None, reverse: bool = None):
        # Super Call #
        super(Context, self).__init__(flags=QtCore.Qt.WindowSystemMenuHint)
        
        # "Internal" Attributes #
        self._progress = QtWidgets.QProgressBar(parent=self)
        self._label = QtWidgets.QLabel("Loading...", parent=self)
        self._layout = QtWidgets.QVBoxLayout(self)
        self._reversed = bool(reverse)
        
        # Internal Calls #
        self._layout.addWidget(self._label)
        self._layout.addWidget(self._progress)
        
        self._progress.setRange(0, maximum if maximum is not None else 0)
        self._label.setAlignment(QtCore.Qt.AlignCenter)
        self._label.setWordWrap(True)
        self.setModal(True)
        
        if maximum is not None:
            self._progress.setValue(maximum if self._reversed else 0)
    
    # Progress Bar Methods #
    def increment(self):
        """Increments the progress' value."""
        if not self._reversed:
            if self._progress.value() < self._progress.maximum():
                self._progress.setValue(self._progress.value() + 1)
        
        else:
            if self._progress.value() > self._progress.minimum():
                self._progress.setValue(self._progress.value() - 1)
    
    def decrement(self):
        """Decrements the progress' value."""
        if not self._reversed:
            if self._progress.value() > self._progress.minimum():
                self._progress.setValue(self._progress.value() - 1)
        
        else:
            if self._progress.value() < self._progress.maximum():
                self._progress.setValue(self._progress.value() + 1)
    
    # Label Methods #
    def set_text(self, text: str):
        """Sets the label's text to `text`."""
        self._label.setText(text)
        self.adjustSize()
    
    # Utility Methods #
    def threaded_task(self, label: str, func: callable, *args, **kwargs):
        """Executes a callable in a thread, while updating the dialog.
        
        :param label: The text to display when this task is executing
        :param func: The callable to execute"""
        self.set_text(label)
    
        thread = QtCore.QThread()
        thread.run = functools.partial(func, *args, **kwargs)
    
        thread.start()
        signals.wait_for_signal(thread.finished)
    
        self.increment()

    def task(self, label: str, func: callable, *args, **kwargs):
        """Executes a callable while updating the dialog.
        
        :param label: The text to display when this task is executing
        :param func: The callable to execute"""
        self.set_text(label)
        func(*args, **kwargs)
        self.increment()

    def wait_for_task(self, label: str, signal: typing.Union[QtCore.pyqtSignal, QtCore.pyqtBoundSignal], *,
                      timeout: int = None, before: callable = None, threaded: bool = None):
        """Waits for a signal to be emitted before normal execution will proceed.
        
        :param label: The text to display when this task is executing
        :param signal: The signal to wait for
        :param timeout: The amount of seconds to wait before forcibly ending
        :param before: The callable to execute before waiting
        :param threaded: Whether or not the callable will be executed in a thread"""
        loop = QtCore.QEventLoop()
        self.set_text(label)
    
        signal.connect(loop.quit)
    
        if before is not None:
            if threaded:
                thread = QtCore.QThread()
                thread.run = before
            
                QtCore.QTimer.singleShot(1, thread.start)
        
            else:
                QtCore.QTimer.singleShot(1, before)
    
        if timeout:
            QtCore.QTimer.singleShot(timeout * 1000, loop.quit)
    
        loop.exec()
    
    @staticmethod
    def wait_for(signal, *, timeout: int = None, initiator: callable = None):
        """Waits for a signal to be emitted before continuing.  `timeout` is
        the amount of seconds to wait for.  `initiator` is the callable that
        will eventually emit `signal`."""
        loop = QtCore.QEventLoop()
        signal.connect(loop.quit)
        
        if timeout:
            # noinspection PyCallByClass,PyTypeChecker
            QtCore.QTimer.singleShot(timeout * 1000, loop.quit)
        
        if initiator:
            # noinspection PyCallByClass,PyTypeChecker
            QtCore.QTimer.singleShot(1, initiator)
        
        loop.exec()
    
    @staticmethod
    def delay(milliseconds: int = None):
        """A sleep-like method for the progress dialog."""
        if milliseconds is None:
            milliseconds = 1000  # 1 second
        
        loop = QtCore.QEventLoop()
        # noinspection PyTypeChecker,PyCallByClass
        QtCore.QTimer.singleShot(milliseconds, loop.quit)
        loop.exec()
    
    # Context Methods #
    def __enter__(self):
        self.show()
        
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.done(0)
        
        if not sip.isdeleted(self):
            self.deleteLater()
