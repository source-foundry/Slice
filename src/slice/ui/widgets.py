# This file is part of Slice.
#
#    Slice is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Slice is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Slice.  If not, see <https://www.gnu.org/licenses/>.

from PyQt5.QtWidgets import QLineEdit, QSizePolicy


class DragDropLineEdit(QLineEdit):
    def __init__(self, parent, *args):
        QLineEdit.__init__(self, *args)
        # sets widget to accept drag and drop
        self.parent = parent
        self.setAcceptDrops(True)
        self.setClearButtonEnabled(True)
        self.setTextMargins(5, 5, 5, 5)
        self.setMinimumWidth(625)
        self.setMaximumWidth(2500)
        self.setMinimumHeight(35)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Minimum)
        self.setPlaceholderText("Drop a variable font here or click the Open button")

    def dragEnterEvent(self, e):
        # mime data types are defined in
        # https://www.tutorialspoint.com/pyqt5/pyqt5_drag_and_drop.htm
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        cleaned_text = self.clean_file_path(e.mimeData().text())
        # set the text entry area
        self.setText(cleaned_text)
        # call the parent method to load font on UI
        self.parent.load_font(cleaned_text)

    def clean_file_path(self, text):
        return text.replace("file://", "")
