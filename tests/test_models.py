from PyQt5.QtWidgets import QTableView

from slice.models import DesignAxisModel, FontModel, FontBitFlagModel, FontNameModel


def test_font_model():
    fm = FontModel("testpath")
    assert fm.fontpath == "testpath"


def test_designaxis_model_default(qtbot, qtmodeltester):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    # check model with default instantiation
    qtmodeltester.check(model)


def test_designaxis_model_filled(qtbot, qtmodeltester):
    pass
