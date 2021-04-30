from pathlib import Path

from PyQt5.QtWidgets import QTableView

from slice.models import FontNameModel, FontModel


def get_font_model():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def get_font_model_woff():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff").resolve())


def get_font_model_woff2():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff2").resolve())


def test_fontname_model_default(qtbot, qtmodeltester):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    # check model with default instantiation
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    assert model._v_header == [
        "01 Family",
        "02 Subfamily",
        "03 Unique",
        "04 Full",
        "06 Postscript",
        "16 Typo Family",
        "17 Typo Subfamily",
        "21 WWS Family",
        "22 WWS Subfamily",
    ]
    assert model._data == [
        [""],  # nameID 1   (index 0)
        [""],  # nameID 2   (index 1)
        [""],  # nameID 3   (index 2)
        [""],  # nameID 4   (index 3)
        [""],  # nameID 6   (index 4)
        [""],  # nameID 16  (index 5)
        [""],  # nameID 17  (index 6)
        [""],  # nameID 21  (index 7)
        [""],  # nameID 22  (index 8)
    ]


def test_fontname_model_filled(qtbot, qtmodeltester):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    # The vertical headers should not change
    assert model._v_header == [
        "01 Family",
        "02 Subfamily",
        "03 Unique",
        "04 Full",
        "06 Postscript",
        "16 Typo Family",
        "17 Typo Subfamily",
        "21 WWS Family",
        "22 WWS Subfamily",
    ]
    # default name table data from test font
    assert model._data == [
        ["Recursive Sans Linear Light"],  # nameID 1   (index 0)
        ["Regular"],  # nameID 2   (index 1)
        ["1.077;ARRW;Recursive-SansLinearLight"],  # nameID 3   (index 2)
        ["Recursive Sans Linear Light"],  # nameID 4   (index 3)
        ["Recursive-SansLinearLight"],  # nameID 6   (index 4)
        [""],  # nameID 16  (index 5)
        [""],  # nameID 17  (index 6)
        [""],  # nameID 21  (index 7)
        [""],  # nameID 22  (index 8)
    ]


def test_fontname_model_filled_woff(qtbot, qtmodeltester):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model_woff())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    # The vertical headers should not change
    assert model._v_header == [
        "01 Family",
        "02 Subfamily",
        "03 Unique",
        "04 Full",
        "06 Postscript",
        "16 Typo Family",
        "17 Typo Subfamily",
        "21 WWS Family",
        "22 WWS Subfamily",
    ]
    # default name table data from test font
    assert model._data == [
        ["Recursive Sans Linear Light"],  # nameID 1   (index 0)
        ["Regular"],  # nameID 2   (index 1)
        ["1.077;ARRW;Recursive-SansLinearLight"],  # nameID 3   (index 2)
        ["Recursive Sans Linear Light"],  # nameID 4   (index 3)
        ["Recursive-SansLinearLight"],  # nameID 6   (index 4)
        [""],  # nameID 16  (index 5)
        [""],  # nameID 17  (index 6)
        [""],  # nameID 21  (index 7)
        [""],  # nameID 22  (index 8)
    ]


def test_fontname_model_filled_woff2(qtbot, qtmodeltester):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model_woff2())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    # The vertical headers should not change
    assert model._v_header == [
        "01 Family",
        "02 Subfamily",
        "03 Unique",
        "04 Full",
        "06 Postscript",
        "16 Typo Family",
        "17 Typo Subfamily",
        "21 WWS Family",
        "22 WWS Subfamily",
    ]
    # default name table data from test font
    assert model._data == [
        ["Recursive Sans Linear Light"],  # nameID 1   (index 0)
        ["Regular"],  # nameID 2   (index 1)
        ["1.077;ARRW;Recursive-SansLinearLight"],  # nameID 3   (index 2)
        ["Recursive Sans Linear Light"],  # nameID 4   (index 3)
        ["Recursive-SansLinearLight"],  # nameID 6   (index 4)
        [""],  # nameID 16  (index 5)
        [""],  # nameID 17  (index 6)
        [""],  # nameID 21  (index 7)
        [""],  # nameID 22  (index 8)
    ]


def test_fontname_model_get_version(qtbot):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_version() == "Version 1.077"


def test_fontname_model_get_family_name(qtbot):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_family_name() == "Recursive Sans Linear Light"


def test_fontname_model_get_instance_data(qtbot):
    tableview = QTableView()
    model = FontNameModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_instance_data() == {
        "nameID1": "Recursive Sans Linear Light",
        "nameID2": "Regular",
        "nameID3": "1.077;ARRW;Recursive-SansLinearLight",
        "nameID4": "Recursive Sans Linear Light",
        "nameID6": "Recursive-SansLinearLight",
        "nameID16": "",
        "nameID17": "",
        "nameID21": "",
        "nameID22": "",
    }

    # simulate update of model data with user input
    # and check again to confirm that it is present
    model._data = [
        ["One"],
        ["Two"],
        ["Three"],
        ["Four"],
        ["Six"],
        ["Sixteen"],
        ["Seventeen"],
        ["Twenty-one"],
        ["Twenty-two"],
    ]
    model.layoutChanged.emit()

    assert model.get_instance_data() == {
        "nameID1": "One",
        "nameID2": "Two",
        "nameID3": "Three",
        "nameID4": "Four",
        "nameID6": "Six",
        "nameID16": "Sixteen",
        "nameID17": "Seventeen",
        "nameID21": "Twenty-one",
        "nameID22": "Twenty-two",
    }
