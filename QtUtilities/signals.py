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
import logging

from PyQt5 import QtCore

__all__ = {"wait_for_signal", "wait_for_signal_or", "wait_for_signal_and"}

logger = logging.getLogger(__name__)


def wait_for_signal(signal, *, timeout: int = None):
    """Waits for `signal`.  If `timeout is specified,
    this method will stop after `timeout` milliseconds.
    :param signal: The signal to wait for.
    :param timeout: The amount of milliseconds to wait
    before timing out."""
    loop = QtCore.QEventLoop()
    timer = QtCore.QTimer()
    emitted = False
    returnables = None

    def on_emit(*args):
        emitted = True
        returnables = args
    
    try:
        signal.connect(on_emit)
        signal.connect(loop.quit)
        
        if timeout is not None:
            if timeout > 0:
                timer.singleShot(timeout, loop.quit)
        
        loop.exec()
    
    except Exception as e:
        logger.warning("`wait_for_signal` ended abruptly! ({})".format(str(e)))
    
    finally:
        if loop.isRunning():
            loop.quit()
        
        if timer.isActive():
            timer.stop()
        
        loop.deleteLater()
        timer.deleteLater()

    return emitted, returnables


def wait_for_signal_and(*signals, timeout: int = None):
    """Waits for all of the signals passed to be emitted.
    If `timeout` is specified, this method will stop after
    `timeout` milliseconds.
    :param timeout: The amount of milliseconds to wait
    before timing out.
    
    :returns bool: Whether or not the signal emitted."""
    loop = QtCore.QEventLoop()
    timer = QtCore.QTimer()
    emitted = {str(i): dict() for i, _ in enumerate(signals)}
    
    try:
        for signal in signals:
            if hasattr(signal, "connect"):
                signal.connect(lambda: emitted.__setitem__(str(signals.index(signal)), True))
                signal.connect(loop.quit)
        
        if timeout is not None:
            if timeout > 0:
                timer.singleShot(timeout, loop.quit)
        
        loop.exec()
    
    except Exception as e:
        logger.warning("`wait_for_signal_and` ended abruptly! ({})".format(str(e)))
    
    finally:
        if loop.isRunning():
            loop.quit()
        
        if timer.isActive():
            timer.stop()
        
        timer.deleteLater()
        loop.deleteLater()
    
    return all(emitted.values())


def wait_for_signal_or(*signals, timeout: int = None):
    """Waits for one of the signals passed to be emitted.
    If `timeout` is specified, this method will stop after
    `timeout` milliseconds.
    :param timeout: The amount of milliseconds to wait
    before timing out.
    
    :returns bool: Whether or not the signal emitted."""
    loop = QtCore.QEventLoop()
    timer = QtCore.QTimer()
    emitted = False
    
    def on_emit():
        emitted = True
    
    try:
        for signal in signals:
            if hasattr(signal, "connect"):
                signal.connect(on_emit)
                signal.connect(loop.quit)
        
        if timeout is not None:
            if timeout > 0:
                timer.singleShot(timeout, loop.quit)
        
        loop.exec()
    
    except Exception as e:
        logger.warning("`wait_for_signal_or` ended abruptly! ({})".format(str(e)))
    
    finally:
        if loop.isRunning():
            loop.quit()
        
        if timer.isActive():
            timer.stop()
        
        timer.deleteLater()
        loop.deleteLater()
    
    return emitted
