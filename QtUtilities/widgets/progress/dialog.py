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
import collections
import datetime
import logging
import typing

from PyQt5 import QtCore, QtGui, QtWidgets

from .widget import ProgressWidget

__all__ = {"Task", "ColorPair", "Progress"}

Task = collections.namedtuple("Task", ["display_text", "task"])
ColorPair = collections.namedtuple("ColorPair", ["text", "bar"])


class Progress(QtWidgets.QDialog):
    """An extendable progress dialog class."""
    logger = logging.getLogger("shovelbot.core.progress")
    
    tasks_finished = QtCore.pyqtSignal()  # Emitted when all tasks have been completed.
    
    # Below are signals for branched tasks.
    # Branched tasks are sub-tasks to the previous scope.
    branch_finished = QtCore.pyqtSignal()
    sub_branch_finished = QtCore.pyqtSignal()
    
    def __init__(self, *, parent: QtWidgets.QWidget = None):
        # Super Call #
        super(Progress, self).__init__(parent=parent, flags=QtCore.Qt.WindowTitleHint | QtCore.Qt.WindowSystemMenuHint)
        
        # "Private" Attributes #
        self._progresses = []  # type: typing.List[ProgressWidget]
        self._cache = collections.deque()
        self._thread = QtCore.QThread(parent=self)
        self._busy_color = ColorPair(bar=QtGui.QColor(255, 255, 0), text=QtGui.QColor(0, 0, 0))
        self._failed_color = ColorPair(bar=QtGui.QColor(255, 0, 0), text=QtGui.QColor(255, 255, 255))
        self._tasks = dict()  # type: typing.Dict[str, collections.deque[Task]]
        self._timestamp = datetime.datetime.now()
        
        # "Public" Attributes #
        
        # "Wrapper" Attributes #
        self.set_title = self.setWindowTitle
        
        # Internal Calls #
        self.setLayout(QtWidgets.QVBoxLayout())
        self._thread.started.connect(self.invoke_next_task)
    
    # Task Methods #
    @staticmethod
    def create_task(task: typing.Union[typing.Callable, Task, typing.List[Task]], display_text: str = None) -> Task:
        """Creates a task object this class can recognize."""
        if display_text is None:
            if hasattr(task, "__qualname__"):
                display_text = f'Processing task "{task.__qualname__}"...'
            
            elif hasattr(task, "__name__"):
                display_text = f'Processing task "{task.__name__}"...'
        
        return Task(display_text, task)
    
    def add_task(self, task: Task):
        """Adds a task to the progress dialog's internal task queue."""
        if "0" not in self._tasks:
            self._tasks["0"] = collections.deque()
        
        self._tasks["0"].append(task)
    
    def remove_task(self, task: Task):
        """Removes a task to the progress dialog's internal task queue."""
        if "0" in self._tasks:
            self._tasks["0"].remove(task)
    
    def add_tasks(self, *tasks: Task):
        """Bulk adds tasks to the progress dialog's internal task queue."""
        for task in tasks:
            self.add_task(task)
    
    def remove_tasks(self, *tasks: Task):
        """Bulk removes tasks from the progress dialog's internal task queue."""
        for task in tasks:
            self.remove_task(task)
    
    def prepare_next_task(self):
        """Prepares the next top-level task in the progress dialog."""
        if "0" in self._tasks:
            self._tasks = {"0": self._tasks["0"]}  # type: typing.Dict[str, collections.deque[Task]]
            
            index = 1
            task = self._tasks["0"].popleft()
            self._tasks["0"].append(task)
            
            while True:
                if isinstance(task.task, Task):
                    self._tasks[str(index)] = collections.deque(task.task)
                    index += 1
                    
                    task = task.task
                
                elif isinstance(task.task, list) and len(task.task) > 0:
                    self._tasks[str(index)] = collections.deque(task.task)
                    index += 1
                    
                    task = task.task[0]
                
                elif callable(task.task):
                    break
    
    def visualise_tasks(self):
        """Visualises the current line of tasks."""
        for task_index in self._tasks:
            index = int(task_index)
            task = self._tasks[task_index].popleft()
            current_max = len(self._tasks[task_index])
            
            self._tasks[task_index].appendleft(task)
            
            try:
                task_progress = self._progresses[index]
                task_progress.set_display_text(task.display_text)
                
                if current_max > task_progress.bar.maximum():
                    task_progress.set_range(0, current_max)
                
                else:
                    task_progress.bar.setValue(task_progress.bar.maximum() - current_max)
            
            except IndexError:
                task_progress = self.add_widget()
                task_progress.set_display_text(task.display_text)
                
                if current_max > task_progress.bar.maximum():
                    task_progress.set_range(0, current_max)
                
                else:
                    task_progress.bar.setValue(task_progress.bar.maximum() - current_max)
    
    def invoke_next_task(self):
        """Invokes the next logical task in queue."""
        next_task_index = len(self._tasks) - 1
        parent_task_index = next_task_index - 1
        
        if str(next_task_index) in self._tasks:
            next_task_queue = self._tasks[str(next_task_index)]
            next_task = next_task_queue.popleft()
            self._timestamp = datetime.datetime.now()
            
            # noinspection PyBroadException
            try:
                next_task.task()
            
            except Exception as e:
                self.set_failed()
                self.logger.warning("Task execution failed!")
                self.logger.warning("Cause: {}".format(str(e)))
            
            else:
                self.set_succeeded()
            
            finally:
                if not self._tasks[str(next_task_index)]:
                    self._tasks.pop(str(next_task_index))
                    
                    if str(parent_task_index) in self._tasks:
                        self._tasks[str(parent_task_index)].popleft()
    
    def process_tasks(self):
        """Processes all tasks in the progress dialog."""
        if "0" in self._tasks:
            self.logger.info("Processing tasks...")
            
            while self._tasks["0"]:
                self.prepare_next_task()
                self.visualise_tasks()
                
                self._thread.start()
                is_busy = False
                
                while self._thread.isRunning():
                    if self._timestamp and not is_busy:
                        difference = datetime.datetime.now() - self._timestamp
                        
                        if difference.seconds >= 5:
                            self.set_busy()
                            is_busy = True
                    
                    QtWidgets.qApp.processEvents()
        
        else:
            self.logger.warning("No tasks to processes!")
            self.logger.warning("Add tasks before invoking `process_tasks`!")
        
        self.hide()
        self.tasks_finished.emit()
    
    # Widget Methods #
    def add_widget(self) -> ProgressWidget:
        """Adds a ProgressWidget to the dialog's internal list of widgets."""
        widget = ProgressWidget(parent=self)
        self.layout().addWidget(widget, None, QtCore.Qt.AlignCenter)
        self._progresses.append(widget)
        
        return widget
    
    def remove_widget(self, widget: ProgressWidget):
        """Removes a ProgressWidget from the dialog's internal list of widgets."""
        self.layout().removeWidget(widget)
        self._progresses.remove(widget)
    
    # Status Methods #
    def set_busy(self, all_bars: bool = False):
        """Sets the progress dialog's status to busy.  If `all_bars` is true,
        all progress bars in the dialog will be set to busy."""
        palette = self.palette()  # type: QtGui.QPalette
        palette.setColor(palette.Highlight, self._busy_color.bar)
        palette.setColor(palette.HighlightedText, self._busy_color.text)
        
        self._decorate_bars(palette, only_current=all_bars)
    
    def set_failed(self, all_bars: bool = False):
        """Sets the progress dialog's status to failed.  If `all_bars` is true,
        all progress bars in the dialog will be set to failed."""
        palette = self.palette()  # type: QtGui.QPalette
        palette.setColor(palette.Highlight, self._failed_color.bar)
        palette.setColor(palette.HighlightedText, self._failed_color.text)
        
        self._decorate_bars(palette, only_current=all_bars)
    
    def set_succeeded(self, all_bars: bool = False):
        """Sets the progress dialog's status to succeeded.  If `all_bars` is true,
        all progress bars in the dialog will be set to succeeded."""
        self._decorate_bars(self.palette(), only_current=all_bars)
    
    def _decorate_bars(self, palette: QtGui.QPalette, *, only_current: bool = True):
        """Decorates the dialog's progress bars with the specified palette."""
        if not only_current:
            for widget in self._progresses:
                widget.bar.setPalette(palette)
        
        else:
            for widget in reversed(self._progresses):
                if widget.isVisible():
                    widget.setPalette(palette)
                    break
    
    # Qt Events #
    def showEvent(self, event: QtGui.QShowEvent):
        """An override of QDialog's show event."""
        self.logger.info("Prepping progress dialog...")
        first_processed = False
        
        for widget in self._progresses:
            if not first_processed:
                first_processed = True
                
                widget.setVisible(True)
                widget.set_range(0, 1)
                widget.reset()
            
            else:
                widget.setHidden(True)
                widget.bar.setRange(0, 1)
                widget.reset()
        
        self.set_succeeded(all_bars=True)
        # noinspection PyCallByClass,PyTypeChecker
        QtCore.QTimer.singleShot(1, self.process_tasks)
