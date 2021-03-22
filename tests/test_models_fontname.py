from pathlib import Path

from PyQt5.QtWidgets import QTableView

from slice.models import FontNameModel, FontModel


def get_font_model():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def test_fontname_model_default(qtbot, qtmodeltester):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    # check model with default instantiation
    qtmodeltester.check(model)
