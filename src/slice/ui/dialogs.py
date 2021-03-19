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

from fontTools import __version__ as fonttools_version
from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QTextBrowser,
    QVBoxLayout,
)

from ..imageresources import *


class SliceOpenFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.file_path = None
        self.root_directory = QDir.homePath()

        self.setWindowTitle("Open File")
        # options |= QFileDialog.DontUseNativeDialog

        file_path, _ = self.getOpenFileName(
            self,
            "Open File",
            self.root_directory,
            "All Files (*);;ttf Files(*.ttf);;otf Files (*.otf)",
            options=self.Options(),
        )

        if file_path:
            self.file_path = file_path

    def get_file_path(self):
        return self.file_path


class SliceSaveFileDialog(QFileDialog):
    def __init__(self, root_directory=None):
        QFileDialog.__init__(self)
        self.file_path = None
        self.root_directory = None

        self.setWindowTitle("Save File")

        if root_directory:
            self.root_directory = root_directory
        else:
            self.root_directory = QDir.homePath()

        file_path, _ = self.getSaveFileName(
            self,
            "Save File",
            self.root_directory,
            "All Files (*);;ttf Files(*.ttf);;otf Files (*.otf)",
            options=self.Options(),
        )

        if file_path:
            self.file_path = file_path

    def get_file_path(self):
        return self.file_path


class SliceAboutDialog(QDialog):
    def __init__(self, version):
        QDialog.__init__(self)

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Slice")
        font = title.font()
        font.setPointSize(30)
        title.setFont(font)

        layout.addWidget(title)

        logoLabel = QLabel()
        qimage = QImage(":/img/slice-icon.svg")
        pixmap = QPixmap.fromImage(qimage)
        logoLabel.setPixmap(pixmap)
        logoLabel.setFixedHeight(60)
        logoLabel.setFixedWidth(75)

        layout.addWidget(logoLabel)

        layout.addWidget(QLabel(f"Version {version}"))
        layout.addWidget(QLabel("Copyright 2021 Christopher Simpkins"))
        licenseLink = QLabel(
            "<p><a href='https://github.com/source-foundry/Slice/blob/main/LICENSE'>GPLv3 License</a></p>"
        )
        licenseLink.setOpenExternalLinks(True)
        layout.addWidget(licenseLink)
        sourceLink = QLabel(
            "<p><a href='https://github.com/source-foundry/Slice'>Source</a></p>"
        )
        sourceLink.setOpenExternalLinks(True)
        layout.addWidget(sourceLink)
        layout.addWidget(QLabel("❤️ Built with these fine tools ❤️"))

        attributionTextField = QTextBrowser()
        attributionTextField.setOpenExternalLinks(True)

        attributionTextField.setHtml(
            f"<ul>"
            f"<li><p><a href='https://www.riverbankcomputing.com/software/pyqt/'>PyQt5</a> GUI framework</p></li>"
            f"<li><p><a href='https://github.com/fonttools/fonttools'>fontTools</a> library (v{fonttools_version})</p></li>"
            f"<li><p><a href='https://fonts.google.com/specimen/Monoton'>Monoton typeface</a> by Vernon Adams</p></li>"
            f"</ul>"
        )
        attributionTextField.setMaximumHeight(100)
        layout.addWidget(attributionTextField)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.exec_()


class SliceErrorDialog(QMessageBox):
    def __init__(self, inform_text, detailed_text=None):
        QMessageBox.__init__(self)
        self.setIcon(QMessageBox.Critical)
        self.setText("Error")
        self.setWindowTitle("Error")
        self.setInformativeText(f"{inform_text}")
        if detailed_text:
            self.setDetailedText(f"{detailed_text}")
        self.setStandardButtons(QMessageBox.Ok)
        self.exec_()
