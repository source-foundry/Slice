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

import sys
import traceback
from pathlib import Path

from PyQt5.QtCore import Qt, QThreadPool, QUrl
from PyQt5.QtGui import (
    QDesktopServices,
    QFont,
    QFontDatabase,
    QImage,
    QKeySequence,
    QPixmap,
)
from PyQt5.QtWidgets import (
    QAction,
    QApplication,
    QCheckBox,
    QDesktopWidget,
    QFormLayout,
    QGridLayout,
    QGroupBox,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QSizePolicy,
    QTableView,
    QVBoxLayout,
    QWidget,
)

from .fontresources import *
from .imageresources import *
from .instanceworker import InstanceWorker
from .models import DesignAxisModel, FontBitFlagModel, FontModel, FontNameModel
from .ui.dialogs import (
    SliceAboutDialog,
    SliceErrorDialog,
    SliceOpenFileDialog,
    SliceSaveFileDialog,
)
from .ui.widgets import DragDropLineEdit

__VERSION__ = "0.2.1"


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

        # default FontModel
        self.font_model = FontModel(None)

        # defined with axis widgets used in the
        # axis editor view
        self.axis_data_dict = {}

        # set up thread pool
        self.setupThreadPool()

        # set up the UI
        self.setUIMenuBar()
        self.setUIMainWindow()
        self.setUIMainLayout()
        self.setUIAppIconTitle()
        self.setUIFontPathDataEntry()
        self.setUIAxisValueDataEntry()
        self.setUINameTableDataEntry()
        self.setUIBitSettingsDataEntry()
        self.setUISliceButton()
        # self.addStretch()
        self.setUIStatusBar()

        # Define main layout on central widget
        w = QWidget()
        w.setLayout(self.main_layout)
        self.setCentralWidget(w)
        # adjust to center position on view
        self.setWindowCenterPosition()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # Thread Pool
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    def setupThreadPool(self):
        self.threadpool = QThreadPool()

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # UI definitions
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #
    # Menus
    #

    def setUIMenuBar(self):
        menuBar = self.menuBar()

        #
        # File menu
        #
        fileMenu = menuBar.addMenu("File")

        # Open
        self.openAction = QAction("&Open Font...", self)
        self.openAction.setShortcut(QKeySequence.Open)
        self.openAction.triggered.connect(self.menu_clicked_open)
        fileMenu.addAction(self.openAction)

        fileMenu.addSeparator()

        # Quit
        self.quitAction = QAction("&Quit", self)
        self.quitAction.setShortcut(QKeySequence.Quit)
        self.quitAction.triggered.connect(self.menu_clicked_quit)
        fileMenu.addAction(self.quitAction)

        #
        # Resources menu
        #
        resourcesMenu = menuBar.addMenu("References")

        openTypeSpecMenu = resourcesMenu.addMenu("OpenType Specification")

        # fvar table spec link
        self.fvarReferenceAction = QAction("fvar Table")
        self.fvarReferenceAction.triggered.connect(self.menu_clicked_fvar)
        openTypeSpecMenu.addAction(self.fvarReferenceAction)

        # head table spec link
        self.headReferenceAction = QAction("head Table")
        self.headReferenceAction.triggered.connect(self.menu_clicked_head)
        openTypeSpecMenu.addAction(self.headReferenceAction)

        # name table spec link
        self.nameReferenceAction = QAction("name Table")
        self.nameReferenceAction.triggered.connect(self.menu_clicked_name)
        openTypeSpecMenu.addAction(self.nameReferenceAction)

        # OS/2 table spec link
        self.os2ReferenceAction = QAction("OS/2 Table")
        self.os2ReferenceAction.triggered.connect(self.menu_clicked_os2)
        openTypeSpecMenu.addAction(self.os2ReferenceAction)

        #
        # Help menu
        #
        helpMenu = menuBar.addMenu("Help")

        # About
        self.aboutAction = QAction("&About...", self)
        self.aboutAction.triggered.connect(self.menu_clicked_about)
        helpMenu.addAction(self.aboutAction)

        # Check for updates
        self.updateCheckAction = QAction("Check for Updates", self)
        self.updateCheckAction.triggered.connect(self.menu_clicked_updatecheck)
        helpMenu.addAction(self.updateCheckAction)

        # Release notes
        self.releaseNotesAction = QAction("Release Notes", self)
        self.releaseNotesAction.triggered.connect(self.menu_clicked_releasenotes)
        helpMenu.addAction(self.releaseNotesAction)

        helpMenu.addSeparator()

        # Documentation
        self.documentationAction = QAction("Documentation", self)
        self.documentationAction.triggered.connect(self.menu_clicked_documentation)
        helpMenu.addAction(self.documentationAction)

        helpMenu.addSeparator()

        # License
        self.licenseAction = QAction("View &License", self)
        self.licenseAction.triggered.connect(self.menu_clicked_license)
        helpMenu.addAction(self.licenseAction)

        # Source
        self.sourceAction = QAction("View Source", self)
        self.sourceAction.triggered.connect(self.menu_clicked_source)
        helpMenu.addAction(self.sourceAction)

        helpMenu.addSeparator()

        # Issue Tracker
        self.issueTrackerAction = QAction("Issue Tracker", self)
        self.issueTrackerAction.triggered.connect(self.menu_clicked_issuetracker)
        helpMenu.addAction(self.issueTrackerAction)

        # Report a Bug
        self.bugReportAction = QAction("Report a Bug", self)
        self.bugReportAction.triggered.connect(self.menu_clicked_bugreport)
        helpMenu.addAction(self.bugReportAction)

    #
    # Main window and main layout
    #

    def setUIMainWindow(self):
        self.setWindowTitle("Slice")
        self.resize(850, 950)

    def setUIMainLayout(self):
        self.main_layout = QVBoxLayout()

    #
    # Application icon and title row
    #

    def setUIAppIconTitle(self):
        monoton_id = QFontDatabase.addApplicationFont(":/font/Monoton-Regular.subset.ttf")
        font_family = QFontDatabase.applicationFontFamilies(monoton_id)[0]
        monoton = QFont(font_family)
        outerHBox = QHBoxLayout()
        titleLabel = QLabel("<h1>slice</h1>")
        titleLabel.setStyleSheet("QLabel { font-size: 36px;}")
        titleLabel.setFont(monoton)
        titleLabel.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        iconLabel = QLabel()
        # note: commented block below shows how to use
        #       svg embedded as a Python string literal
        #       for QImage instantiation. The current
        #       approach is better
        # svg_bytes = bytearray(svg_icon, encoding="utf-8")
        # qimage = QImage.fromData(svg_bytes)
        qimage = QImage(":/img/slice-icon.svg")
        pixmap = QPixmap.fromImage(qimage)
        iconLabel.setPixmap(pixmap)
        iconLabel.setFixedHeight(60)
        iconLabel.setFixedWidth(75)
        outerHBox.addWidget(iconLabel)
        outerHBox.addWidget(titleLabel)

        # add widget to main layout
        self.main_layout.addLayout(outerHBox)

    #
    # Font path free text entry field view (with DnD support)
    #

    def setUIFontPathDataEntry(self):
        self.fontpathLineEdit = DragDropLineEdit(self)
        self.fontpathLineEdit.returnPressed.connect(
            self.key_pressed_return_fontpath_data_entry
        )
        dataEntryForm = QFormLayout()
        dataEntryForm.setAlignment(Qt.AlignLeft)
        dataEntryForm.addRow(QLabel("<h3>Font Path:</h3> "), self.fontpathLineEdit)
        dataEntryForm.setContentsMargins(0, 0, 0, 0)

        self.openFontPathButton = QPushButton("Open", self)
        self.openFontPathButton.pressed.connect(self.btn_clicked_open_fontpath)
        row_layout = QHBoxLayout()
        row_layout.addLayout(dataEntryForm)
        row_layout.addWidget(self.openFontPathButton)
        row_layout.addStretch()

        # add the widgets and layout to a QGroupBox
        fontpathGroupBox = QGroupBox("")  # empty string param = no group box title
        fontpathGroupBox.setLayout(row_layout)
        # add widget to main layout
        self.main_layout.addWidget(fontpathGroupBox)

    #
    # Axis instance value editor table view
    #

    def setUIAxisValueDataEntry(self):
        outerVBox = QVBoxLayout()
        axisEditLabel = QLabel("<h4>Axis Definitions</h4>")
        axisEditLabel.setStyleSheet("QLabel { padding-left: 5px;}")
        axisEditGroupBox = QGroupBox("")
        axisEditGroupBox.setMinimumHeight(200)
        axisEditGroupBox.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
        )

        self.fvar_table_view = QTableView()
        self.fvar_table_model = DesignAxisModel()
        self.fvar_table_view.setModel(self.fvar_table_model)
        self.fvar_table_view.horizontalHeader().setStretchLastSection(True)
        self.fvar_table_view.resizeColumnToContents(0)
        self.fvar_table_view.setAlternatingRowColors(True)
        axisEditGroupBox.setLayout(QVBoxLayout())
        axisEditGroupBox.layout().addWidget(self.fvar_table_view)
        axisEditGroupBox.setMinimumHeight(205)

        outerVBox.addWidget(axisEditLabel)
        outerVBox.addWidget(axisEditGroupBox)
        # add to main layout
        # self.main_layout.addSpacing(10)
        self.main_layout.addLayout(outerVBox)

    #
    # Name table record editor table view
    #

    def setUINameTableDataEntry(self):
        outerVBox = QVBoxLayout()
        nameTableLabel = QLabel("<h4>Name Table Definitions</h4>")
        nameTableLabel.setStyleSheet("QLabel { padding-left: 5px;}")
        nameTableGroupBox = QGroupBox("")
        self.nameTableView = QTableView()
        self.name_table_model = FontNameModel()
        self.nameTableView.setModel(self.name_table_model)
        self.nameTableView.horizontalHeader().setStretchLastSection(True)
        self.nameTableView.setAlternatingRowColors(True)
        nameTableGroupBox.setLayout(QVBoxLayout())
        nameTableGroupBox.layout().addWidget(self.nameTableView)
        nameTableGroupBox.setMinimumHeight(210)

        outerVBox.addWidget(nameTableLabel)
        outerVBox.addWidget(nameTableGroupBox)
        # self.main_layout.addSpacing(10)
        self.main_layout.addLayout(outerVBox)

    #
    # Bit flag settings editor table view
    #

    def setUIBitSettingsDataEntry(self):
        outerVBox = QVBoxLayout()
        outerHBox = QHBoxLayout()
        bitSettingsLabel = QLabel("<h4>Bit Flag Settings</h4>")
        bitSettingsLabel.setStyleSheet("QLabel { padding-left: 5px;}")

        bitSettingsOuterGroupBox = QGroupBox("")
        bitSettingsOS2GroupBox = QGroupBox("OS/2.fsSelection")
        bitSettingsHeadGroupBox = QGroupBox("head.macStyle")

        # OS/2.fsSelection bit check boxes
        self.os2_fsselection_bit_0_checkbox = QCheckBox("bit 0 (ITALIC)")
        self.os2_fsselection_bit_5_checkbox = QCheckBox("bit 5 (BOLD)")
        self.os2_fsselection_bit_6_checkbox = QCheckBox("bit 6 (REGULAR)")
        self.os2_fsselection_bit_8_checkbox = QCheckBox("bit 8 (WWS)")

        # head.macStyle bit check boxes
        self.head_macstyle_bit_0_checkbox = QCheckBox("bit 0 (BOLD)")
        self.head_macstyle_bit_1_checkbox = QCheckBox("bit 1 (ITALIC)")

        # add check boxes to OS/2 grid layout
        bitSettingsOS2GridLayout = QGridLayout()
        bitSettingsOS2GridLayout.addWidget(self.os2_fsselection_bit_0_checkbox, 0, 0)
        bitSettingsOS2GridLayout.addWidget(self.os2_fsselection_bit_5_checkbox, 0, 1)
        bitSettingsOS2GridLayout.addWidget(self.os2_fsselection_bit_6_checkbox, 1, 0)
        bitSettingsOS2GridLayout.addWidget(self.os2_fsselection_bit_8_checkbox, 1, 1)

        # add check boxes to head grid layout
        bitSettingsHeadGridLayout = QGridLayout()
        bitSettingsHeadGridLayout.addWidget(self.head_macstyle_bit_0_checkbox, 0, 0)
        bitSettingsHeadGridLayout.addWidget(self.head_macstyle_bit_1_checkbox, 0, 1)

        # add OS/2 and head grid layouts to table group boxes
        bitSettingsOS2GroupBox.setLayout(bitSettingsOS2GridLayout)
        bitSettingsHeadGroupBox.setLayout(bitSettingsHeadGridLayout)

        # add table group boxes to outer H box layout
        outerHBox.addWidget(bitSettingsOS2GroupBox)
        outerHBox.addWidget(bitSettingsHeadGroupBox)

        # add outer H box layout to outer group box layout
        bitSettingsOuterGroupBox.setLayout(outerHBox)

        outerVBox.addWidget(bitSettingsLabel)
        outerVBox.addWidget(bitSettingsOuterGroupBox)

        # self.main_layout.addSpacing(10)
        self.main_layout.addLayout(outerVBox)

    #
    # Slice execution button
    #

    def setUISliceButton(self):
        self.sliceButton = QPushButton("Slice", self)
        self.sliceButton.setMaximumWidth(250)
        self.sliceButton.setMinimumWidth(200)
        # add to main layout
        # self.main_layout.addSpacing(3)
        self.main_layout.addWidget(self.sliceButton, alignment=Qt.AlignCenter)
        # self.main_layout.addSpacing(3)
        # add slot to clicked event
        self.sliceButton.clicked.connect(self.btn_clicked_slice)

    #
    # Status bar view
    #

    def setUIStatusBar(self):
        # messages are managed with
        # .clearMessage() and .showMessage()
        self.statusbar = self.statusBar()
        self.statusbar.showMessage("Ready")

        # Version info
        status_version_label = QLabel(f"v{__VERSION__}")
        self.statusbar.addPermanentWidget(status_version_label)
        self.statusbar.update()

    #
    # UI utilities
    #

    def addStretch(self):
        self.main_layout.addStretch()

    def setWindowCenterPosition(self):
        rect = self.frameGeometry()
        centerLoc = QDesktopWidget().availableGeometry().center()
        rect.moveCenter(centerLoc)
        self.move(rect.topLeft())

    #
    # Data control
    #

    def collect_os2_bit_checkbox_fields(self):
        return {
            "bit0": self.os2_fsselection_bit_0_checkbox.isChecked(),
            "bit5": self.os2_fsselection_bit_5_checkbox.isChecked(),
            "bit6": self.os2_fsselection_bit_6_checkbox.isChecked(),
            "bit8": self.os2_fsselection_bit_8_checkbox.isChecked(),
        }

    def collect_head_bit_checkbox_fields(self):
        return {
            "bit0": self.head_macstyle_bit_0_checkbox.isChecked(),
            "bit1": self.head_macstyle_bit_1_checkbox.isChecked(),
        }

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # Event slots
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~

    #
    # Menu click events
    #

    def menu_clicked_about(self):
        SliceAboutDialog(f"{__VERSION__}")

    def menu_clicked_bugreport(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/source-foundry/Slice/issues/new")
        )

    def menu_clicked_documentation(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/source-foundry/Slice/blob/main/README.md")
        )

    def menu_clicked_fvar(self):
        QDesktopServices.openUrl(
            QUrl("https://docs.microsoft.com/en-us/typography/opentype/spec/fvar")
        )

    def menu_clicked_head(self):
        QDesktopServices.openUrl(
            QUrl("https://docs.microsoft.com/en-us/typography/opentype/spec/head")
        )

    def menu_clicked_issuetracker(self):
        QDesktopServices.openUrl(QUrl("https://github.com/source-foundry/Slice/issues"))

    def menu_clicked_license(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/source-foundry/Slice/blob/main/LICENSE")
        )

    def menu_clicked_name(self):
        QDesktopServices.openUrl(
            QUrl("https://docs.microsoft.com/en-us/typography/opentype/spec/name")
        )

    def menu_clicked_open(self):
        self.openFontPathButton.setEnabled(False)
        self._open_font_file_action()

    def menu_clicked_os2(self):
        QDesktopServices.openUrl(
            QUrl("https://docs.microsoft.com/en-us/typography/opentype/spec/os2")
        )

    def menu_clicked_quit(self):
        self.close()

    def menu_clicked_releasenotes(self):
        QDesktopServices.openUrl(
            QUrl("https://github.com/source-foundry/Slice/blob/main/CHANGELOG.md")
        )

    def menu_clicked_source(self):
        QDesktopServices.openUrl(QUrl("https://github.com/source-foundry/Slice"))

    def menu_clicked_updatecheck(self):
        QDesktopServices.openUrl(QUrl("https://github.com/source-foundry/Slice/releases"))

    #
    # Button click events
    #

    def btn_clicked_open_fontpath(self):
        self.openFontPathButton.setEnabled(False)
        self._open_font_file_action()

    def btn_clicked_slice(self):
        # user did not load font data
        if not self.font_model.fontpath:
            self.statusbar.showMessage("Requires a font path")
            self.statusbar.update()
            # must keep this return statement to abort execution!
            return
        else:
            # validation: confirm that the user did not edit the
            # file path in the text edit field without initiation
            # of a font re-load (e.g., manual edit of text without
            # clicking Return button)
            if self.fontpathLineEdit.text() != self.font_model.fontpath:
                SliceErrorDialog(
                    "The file path in the font path field does not match the "
                    "loaded font path.  Please load your font again."
                )
            else:
                outpath = SliceSaveFileDialog(
                    root_directory=str(Path(self.font_model.fontpath).parent)
                ).get_file_path()

                # the user did not select a save path
                # abort instantiation
                if not outpath:
                    self.statusbar.showMessage("Canceled")
                    self.statusbar.update()
                    return

                # Define the FontBitFlagModel
                bit_model = FontBitFlagModel(
                    self.collect_os2_bit_checkbox_fields(),
                    self.collect_head_bit_checkbox_fields(),
                )
                try:
                    instance_worker = InstanceWorker(
                        outpath,
                        self.font_model,
                        self.fvar_table_model,
                        self.name_table_model,
                        bit_model,
                    )

                    # attach InstanceWorker signals / slots
                    instance_worker.signals.result.connect(self._instance_worker_output)
                    instance_worker.signals.finished.connect(
                        self._instance_worker_complete
                    )
                    instance_worker.signals.error.connect(self._instance_worker_error)

                    # start the worker thread
                    self.threadpool.start(instance_worker)
                    self.statusbar.showMessage("Slicing instance...")
                    self.sliceButton.setDisabled(True)

                except Exception as e:
                    SliceErrorDialog(
                        "Font processing failed with an error.  See details below.",
                        detailed_text=str(e),
                    )
                    self.statusbar.showMessage("Error")
                    self.statusbar.update()
                    # print trace to std error
                    sys.stderr.write(f"{traceback.format_exc()}\n")

        # enable the Slice button at end of instantiation
        # attempt irrespective of the error/success outcome
        self.sliceButton.setEnabled(True)

    #
    # Keyboard input press events
    #

    def key_pressed_return_fontpath_data_entry(self):
        self.load_font(self.fontpathLineEdit.text())

    #
    # Event private methods
    #

    def _open_font_file_action(self):
        self.statusbar.showMessage("Select variable font file path")
        filepath_dialog = SliceOpenFileDialog()
        filepath = filepath_dialog.get_file_path()
        if filepath:
            self.fontpathLineEdit.setText(filepath)
            self.load_font(filepath)

        self.openFontPathButton.setEnabled(True)

    #
    # Instance worker thread events
    #

    def _instance_worker_output(self, result_string):
        # InstanceWorker successfully completed file write
        # prints the out file path to stdout stream on success
        print(f"Write path: {result_string}")

    def _instance_worker_complete(self):
        # Instance worker ended execution
        self.sliceButton.setEnabled(True)
        self.statusbar.showMessage("Complete")

    def _instance_worker_error(self, error_string):
        # Instance worker errored
        # Propagate the exception to an error dialog
        SliceErrorDialog(
            "Font processing failed with an error. See details below.",
            detailed_text=error_string,
        )
        self.sliceButton.setEnabled(True)
        self.statusbar.showMessage("Failed")

    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    #
    # Font load
    #
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~
    def load_font(self, filepath):
        """Instantiates default data model values and writes font data to UI."""
        try:
            self.font_model = FontModel(filepath)
            if not self.font_model.is_variable_font():
                SliceErrorDialog(
                    "The file does not appear to be a variable font. See details below.",
                    "The font is missing the OpenType fvar table and is not recognized "
                    "as a variable font. Please try again with a font that includes the "
                    "fvar table.",
                )
                return False
        except Exception as e:
            SliceErrorDialog(
                "An error was encountered during the attempt to load your font. "
                "See details below.",
                detailed_text=str(e),
            )
            return False

        name_table_was_set = self.name_table_model.load_font(self.font_model)
        axis_value_table_was_set = self.fvar_table_model.load_font(self.font_model)
        self.fvar_table_view.resizeColumnToContents(0)

        # uncheck all bit flag setting check boxes
        self.os2_fsselection_bit_0_checkbox.setChecked(False)
        self.os2_fsselection_bit_5_checkbox.setChecked(False)
        self.os2_fsselection_bit_6_checkbox.setChecked(False)
        self.os2_fsselection_bit_8_checkbox.setChecked(False)
        self.head_macstyle_bit_0_checkbox.setChecked(False)
        self.head_macstyle_bit_1_checkbox.setChecked(False)

        if name_table_was_set and axis_value_table_was_set:
            # Update status bar with font family name,
            # version, and number of axes
            self.statusbar.showMessage(
                f"{self.name_table_model.get_family_name()} "
                f"{self.name_table_model.get_version()} "
                f"loaded ({self.fvar_table_model.get_number_of_axes()} axes)"
            )


def main():
    app = QApplication(sys.argv)
    # fusion_style = QStyleFactory.create("Fusion")
    # app.setStyle(fusion_style)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
