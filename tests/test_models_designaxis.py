from pathlib import Path

from PyQt5.QtWidgets import QTableView

from slice.models import DesignAxisModel, FontModel


def get_font_model():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def test_designaxis_model_default(qtbot, qtmodeltester):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    # check model with default instantiation
    qtmodeltester.check(model)


def test_designaxis_model_filled(qtbot, qtmodeltester):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    assert model._h_header == ["(Min, Max) [Default]", "Instance Values"]
    assert model.ordered_axis_tags == ["MONO", "CASL", "wght", "slnt", "CRSV"]
    assert model._v_header == ["MONO", "CASL", "wght", "slnt", "CRSV"]
    assert model.fvar_axes == {
        "MONO": [0.0, 0.0, 1.0],
        "CASL": [0.0, 0.0, 1.0],
        "wght": [300.0, 300.0, 1000.0],
        "slnt": [-15.0, 0.0, 0.0],
        "CRSV": [0.0, 0.5, 1.0],
    }
    assert model._data == [
        ["(0.0, 1.0) [0.0]", ""],
        ["(0.0, 1.0) [0.0]", ""],
        ["(300.0, 1000.0) [300.0]", ""],
        ["(-15.0, 0.0) [0.0]", ""],
        ["(0.0, 1.0) [0.5]", ""],
    ]


def test_designaxis_model_get_instance_data(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # without user entered definitions, we should get default
    # axis values
    assert model.get_instance_data() == {
        "MONO": 0.0,
        "CASL": 0.0,
        "wght": 300.0,
        "slnt": 0.0,
        "CRSV": 0.5,
    }

    # simulate update of model data with user input
    # and check again to confirm that it is present
    model._data[0][1] = "1.0"
    model._data[1][1] = "1.0"
    model._data[2][1] = "1000.0"
    model._data[3][1] = "-15.0"
    model._data[4][1] = "1.0"
    model.layoutChanged.emit()

    assert model.get_instance_data() == {
        "MONO": 1.0,
        "CASL": 1.0,
        "wght": 1000.0,
        "slnt": -15.0,
        "CRSV": 1.0,
    }


def test_designaxis_model_get_number_of_axes(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_number_of_axes() == 5


def test_designaxis_model_get_default_axis_value(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_default_axis_value("MONO") == 0.0
    assert model.get_default_axis_value("CASL") == 0.0
    assert model.get_default_axis_value("wght") == 300.0
    assert model.get_default_axis_value("slnt") == 0.0
    assert model.get_default_axis_value("CRSV") == 0.5


def test_designaxis_model_get_registered_axis_string(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    assert model.get_registered_axis_string("ital") == "Italic"
    assert model.get_registered_axis_string("opsz") == "Optical size"
    assert model.get_registered_axis_string("slnt") == "Slant"
    assert model.get_registered_axis_string("wdth") == "Width"
    assert model.get_registered_axis_string("wght") == "Weight"
    assert model.get_registered_axis_string("BOGUS") is None
