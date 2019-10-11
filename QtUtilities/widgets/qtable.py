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
import typing

from PyQt5 import QtWidgets

__all__ = ['QTable']


class QTable(QtWidgets.QTableWidget):
    """A custom QTableWidget that adds convenience methods."""
    
    def horizontal_headers(self) -> typing.List[QtWidgets.QTableWidgetItem]:
        """Returns the current horizontal headers in the QTableWidget."""
        return [self.horizontalHeaderItem(c) for c in range(self.columnCount())]
    
    def vertical_headers(self) -> typing.List[QtWidgets.QTableWidgetItem]:
        """Returns the current vertical headers in the QTableWidget."""
        return [self.verticalHeaderItem(r) for r in range(self.rowCount())]
    
    def preserved_clear(self):
        """Clears the contents of the table while preserving the
        existing horizontal headers."""
        # Preservation
        horizontal_headers = [QtWidgets.QTableWidgetItem(h) for h in self.horizontal_headers()]
        
        # Purging
        self.clear()
        self.setRowCount(0)
        
        # Repopulation
        for index, header in enumerate(horizontal_headers):
            self.setHorizontalHeaderItem(index, header)
    
    def set_horizontal_headers(self, *headers: typing.Union[str, QtWidgets.QTableWidgetItem]):
        """Sets the horizontal headers for the QTableWidget."""
        self.setColumnCount(len(headers))
        
        for index, header in enumerate(headers):
            if isinstance(headers, QtWidgets.QTableWidgetItem):
                self.setHorizontalHeaderItem(index, header)
            
            else:
                self.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))
    
    def set_vertical_headers(self, *headers: typing.Union[str, QtWidgets.QTableWidgetItem]):
        """Sets the vertical headers for the QTableWidget."""
        for index, header in enumerate(headers):
            if isinstance(headers, QtWidgets.QTableWidgetItem):
                self.setVerticalHeaderItem(index, header)
            
            else:
                self.setVerticalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))
    
    def append(self, *args, **kwargs):
        """Appends the supplied data to the table.
        
        If data is passed through *args, it will be appended from
        left to right, or right to left depending on the current locale.
        
        If data is passed through **kwargs, the column in the new row will be
        set to the passed value.  If a header contains spaces, an underscore
        can be passed in place of it."""
        # Expand the row count by one
        self.setRowCount(self.rowCount() + 1)
        
        if args:
            if len(args) > self.columnCount():
                raise IndexError
            
            for column, arg in enumerate(args):
                if isinstance(arg, QtWidgets.QTableWidgetItem):
                    self.setItem(self.rowCount() - 1, column, arg)
                
                else:
                    self.setItem(self.rowCount() - 1, column, QtWidgets.QTableWidgetItem(str(arg)))
        
        elif kwargs:
            for column in range(self.columnCount()):
                header: QtWidgets.QTableWidgetItem = self.horizontalHeaderItem(column)
                value = kwargs[header.text().replace(' ', '_')]
                
                if isinstance(value, QtWidgets.QTableWidgetItem):
                    self.setItem(self.rowCount() - 1, column, value)
                
                else:
                    self.setItem(self.rowCount() - 1, column, QtWidgets.QTableWidgetItem(str(value)))
    
    def set_row(self, row: int, *args, **kwargs):
        """Modifies the specified row in the table.
        
        If data is passed through *args, the row will be modified from left to
        right, or right to left depending on the current locale.
        
        If data is passed through **kwargs, the column in `row` will be set to
        the passed value.  If a header contains spaces, an underscore can be
        passed in place of it."""
        # if row > self.rowCount() or row < 0:
        #     raise IndexError
        
        if args:
            if len(args) > self.columnCount():
                raise IndexError

            for column, arg in enumerate(args):
                if isinstance(arg, QtWidgets.QTableWidgetItem):
                    self.setItem(row, column, arg)
                
                else:
                    self.setItem(row, column, QtWidgets.QTableWidgetItem(str(arg)))
        
        elif kwargs:
            for column in range(self.columnCount()):
                header: QtWidgets.QTableWidgetItem = self.horizontalHeaderItem(column)
                value = kwargs.get(header.text().replace(' ', '_'))
                
                if value is None:
                    continue  # The column wasn't specified
                
                if isinstance(value, QtWidgets.QTableWidgetItem):
                    self.setItem(row, column, value)
                
                else:
                    self.setItem(row, column, QtWidgets.QTableWidgetItem(str(value)))
    
    def row_from_data(self, **data) -> int:
        """Returns the first row that matches the specified data."""
        for row in range(self.rowCount()):
            # Declarations
            row_contents = {}
            
            # Populate row contents
            for column in range(self.columnCount()):
                header: QtWidgets.QTableWidgetItem = self.horizontalHeaderItem(column)
                item: QtWidgets.QTableWidgetItem = self.item(row, column)

                row_contents[header.text().replace(' ', '_')] = item.text()
            
            # Check if the contents add up
            if all([data[k] == row_contents[k] for k in data]):
                return row
        
        raise LookupError
    
    def row_from_header(self, header: str) -> typing.Tuple[int, QtWidgets.QTableWidgetItem]:
        """Returns the first row that matches the specified vertical header."""
        for row in range(self.rowCount()):
            row_header: QtWidgets.QTableWidgetItem = self.verticalHeaderItem(row)
            
            if row_header.text().replace(' ', '_') == header:
                return row, row_header
        
        raise LookupError
    
    def set_row_header(self, row: int, header: typing.Union[str, QtWidgets.QTableWidgetItem]):
        """Sets the vertical header for `row` to `header`."""
        if row > self.rowCount() or row < 0:
            raise IndexError
        
        if isinstance(header, QtWidgets.QTableWidgetItem):
            self.setVerticalHeaderItem(row, header)
        
        else:
            self.setVerticalHeaderItem(row, QtWidgets.QTableWidgetItem(str(header)))
    
    def set_column_header(self, column: int, header: typing.Union[str, QtWidgets.QTableWidgetItem]):
        """Sets the horizontal header for `column` to `header`."""
        if column > self.columnCount() or column < 0:
            raise IndexError
        
        if isinstance(header, QtWidgets.QTableWidgetItem):
            self.setHorizontalHeaderItem(column, header)
        
        else:
            self.setHorizontalHeaderItem(column, QtWidgets.QTableWidgetItem(str(header)))
