from PyQt5.QtWidgets import QWidget
from PyQt5.QtTest import QTest

from slice.ui.widgets import DragDropLineEdit


def test_drag_drop_line_edit(qtbot):
    widget1 = QWidget()
    widget2 = DragDropLineEdit(widget1)
    qtbot.addWidget(widget1)
    qtbot.addWidget(widget2)
    # placeholder text
    assert (
        widget2.placeholderText() == "Drop a variable font here or click the Open button"
    )
    assert widget2.isEnabled() is True
    # accepts drops
    assert widget2.acceptDrops() is True
    # uses a clear button
    assert widget2.isClearButtonEnabled() is True
    # test text entry
    assert widget2.text() == ""
    QTest.keyClicks(widget2, "test")
    assert widget2.text() == "test"
