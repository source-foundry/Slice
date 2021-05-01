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
from PyQt5.QtGui import QFont, QFontDatabase, QIcon, QImage, QPixmap
from PyQt5.QtWidgets import (
    QDesktopWidget,
    QDialog,
    QDialogButtonBox,
    QFileDialog,
    QLabel,
    QMessageBox,
    QProgressBar,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

from ..imageresources import *


class SliceOpenFileDialog(QFileDialog):
    def __init__(self):
        QFileDialog.__init__(self)
        self.file_path = None
        self.root_directory = QDir.homePath()

        self.setWindowTitle("Open File")
        self.setWindowIcon(QIcon(":/img/slice-icon.svg"))
        # options |= QFileDialog.DontUseNativeDialog

        file_path, _ = self.getOpenFileName(
            self,
            "Open File",
            self.root_directory,
            "All Files (*);;ttf Files(*.ttf);;otf Files (*.otf);;"
            "woff Files (*.woff);;woff2 Files (*.woff2)",
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
        self.setWindowIcon(QIcon(":/img/slice-icon.svg"))

        if root_directory:
            self.root_directory = root_directory
        else:
            self.root_directory = QDir.homePath()

        file_path, _ = self.getSaveFileName(
            self,
            "Save File",
            self.root_directory,
            "All Files (*);;ttf Files(*.ttf);;otf Files (*.otf);;"
            "woff Files (*.woff);;woff2 Files (*.woff2)",
            options=self.Options(),
        )

        if file_path:
            self.file_path = file_path

    def get_file_path(self):
        return self.file_path


class SliceAboutDialog(QDialog):
    def __init__(self, version):
        QDialog.__init__(self)

        self.setGeometry(0, 0, 375, 425)
        rect = self.frameGeometry()
        centerCoord = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerCoord)
        self.move(rect.topLeft())

        self.setWindowTitle("About Slice")
        self.setWindowIcon(QIcon(":/img/slice-icon.svg"))

        QBtn = QDialogButtonBox.Ok
        self.buttonBox = QDialogButtonBox(QBtn)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        layout = QVBoxLayout()

        title = QLabel("Slice")

        recursive_id = QFontDatabase.addApplicationFont(":/font/RecursiveSans.ttf")
        font_family = QFontDatabase.applicationFontFamilies(recursive_id)[0]
        recursive = QFont(font_family)
        recursive.setPointSize(30)
        title.setFont(recursive)

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
            f"<li><p><a href='https://www.recursive.design'>Recursive Sans typeface</a> by Stephen Nixon</p></li>"
            f"<li><p><a href='https://github.com/IBM/plex'>IBM Plex Mono typeface</a> by IBM</p></li>"
            f"</ul>"
        )
        attributionTextField.setMaximumHeight(200)
        attributionTextField.setMinimumWidth(350)
        layout.addWidget(attributionTextField)

        for i in range(0, layout.count()):
            layout.itemAt(i).setAlignment(Qt.AlignHCenter)

        layout.addWidget(self.buttonBox)

        self.setLayout(layout)
        self.exec_()


class SliceProgressDialog(QWidget):
    def __init__(self, close_signal):
        QWidget.__init__(self)

        layout = QVBoxLayout()

        self.setGeometry(0, 0, 200, 75)
        rect = self.frameGeometry()
        centerCoord = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerCoord)
        self.move(rect.topLeft())

        self.message = QLabel("Slicing...")
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 0)

        layout.addWidget(self.message)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)
        close_signal.connect(self.close_progress_dialog)
        self.show()

    def close_progress_dialog(self):
        self.message.setText("Complete")
        self.progress_bar.setRange(0, 1)
        self.hide()


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
