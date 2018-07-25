# This file is part of QtUtilities.
#
# QtUtilities is free software: you can
# redistribute it and/or modify it under the
# terms of the GNU Lesser General Public
# License as published by the Free Software
# Foundation, either version 3 of the License,
# or (at your option) any later version.
#
# QtUtilities is distributed in the hope
# that it will be useful, but WITHOUT ANY
# WARRANTY; without even the implied warranty
# of MERCHANTABILITY or FITNESS FOR A PARTICULAR
# PURPOSE.  See the GNU Lesser General Public
# License for more details.
#
# You should have received a copy of the GNU
# Lesser General Public License along with
# QtUtilities.  If not,
# see <http://www.gnu.org/licenses/>.
#
# Author: RandomShovel
# File Date: 12/25/2017
from PyQt5 import QtWidgets


# Table Functions #
def clear_table(table: QtWidgets.QTableWidget, headers: list = None):
    """Clears ALL data from the passed table, including headers.

    :param table is a QTableWidget object
    :param headers is a list of strings representing the new headers to fill the table with. This should be in
    order from left to right."""
    
    table.clear()
    
    if headers:
        set_table_headers(table, headers)
    
    else:
        set_table_headers(table, ["Key", "Value"])


def safe_clear_table(table: QtWidgets.QTableWidget, headers: list = None):
    """Clears the contents from the passed table while preserving its current headers.

    :param table is a QTableWidget object
    :param headers is a list of strings representing the new headers to fill the table with. This should be in
    order from left to right."""
    
    if headers is None:
        headers = list()
    
    _current_headers = [table.horizontalHeaderItem(column).text() for column in range(table.columnCount())]
    
    for header in headers:
        if header not in _current_headers:
            _current_headers.append(header)
    
    for index, header in enumerate(_current_headers):
        table.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))


def set_table_headers(table: QtWidgets.QTableWidget, headers: list):
    """Sets the passed table's horizontal headers to the strings provided.

    :param table is a QTableWidget object
    :param headers is a list of headers to set

    'headers' should be a list of strings representing header titles. This list should be in order from
    left to right."""
    for index, header in enumerate(headers):
        table.setHorizontalHeaderItem(index, QtWidgets.QTableWidgetItem(str(header)))


def append_table(table: QtWidgets.QTableWidget, data: dict):
    """Appends the supplied data to the table.

    :param table is the QTableWidget to modify
    :param data is a dict object of the data to insert into the table

    'data' should be formatted as follows:
    {
        'horizontal_header' : 'item1',
        'horizontal_header_2' : 'item2'
    }"""
    table.setRowCount(table.rowCount() + 1)
    
    for column_index in range(table.columnCount()):
        _column_header = table.horizontalHeaderItem(column_index).text()
        
        if data.get(_column_header):
            table.setItem(table.rowCount() - 1, column_index,
                          QtWidgets.QTableWidgetItem(str(data.get(_column_header))))


def populate_table(table: QtWidgets.QTableWidget, data: dict):
    """Populates a QTableWidget with the data provided

    :param table: The QTableWidget to modify
    :param data: The dictionary data to put in the table

    'data' should be formatted as follows:
    {
        'horizontal_header' : [
            'item1',
            'item2',
            'item3'
        ],
        'horizontal_header2' : [
            'item1',
            'item2',
            'item3'
        ]
    }

    :raises ValueError if there isn't any data to populate the table with"""
    _columns = len(data)
    
    if _columns > 0:
        table.setColumnCount(_columns)
        _current_column = 0
        _row_count = 0
        
        for key, value in data.items():
            _current_row = 0
            table.setHorizontalHeaderItem(_current_column, QtWidgets.QTableWidgetItem(str(key)))
            
            if len(value) > _row_count:
                table.setRowCount(len(value))
                _row_count = value
            
            for item in value:
                table.setItem(_current_row, _current_column, QtWidgets.QTableWidgetItem(str(item)))
                _current_row += 1
            
            _current_column += 1
    
    else:
        raise ValueError
