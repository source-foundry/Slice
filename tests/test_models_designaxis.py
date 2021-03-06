from pathlib import Path

import pytest

from PyQt5.QtWidgets import QTableView

from slice.models import DesignAxisModel, FontModel


def get_font_model():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def get_font_model_woff():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff").resolve())


def get_font_model_woff2():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff2").resolve())


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
    assert model._h_header == ["Min : Max [Default]", "Edit Values"]
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
        ["0.0 : 1.0 [0.0]", ""],
        ["0.0 : 1.0 [0.0]", ""],
        ["300.0 : 1000.0 [300.0]", ""],
        ["-15.0 : 0.0 [0.0]", ""],
        ["0.0 : 1.0 [0.5]", ""],
    ]


def test_designaxis_model_filled_woff(qtbot, qtmodeltester):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model_woff())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    assert model._h_header == ["Min : Max [Default]", "Edit Values"]
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
        ["0.0 : 1.0 [0.0]", ""],
        ["0.0 : 1.0 [0.0]", ""],
        ["300.0 : 1000.0 [300.0]", ""],
        ["-15.0 : 0.0 [0.0]", ""],
        ["0.0 : 1.0 [0.5]", ""],
    ]


def test_designaxis_model_filled_woff2(qtbot, qtmodeltester):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model_woff2())

    # test with qtmodeltester
    qtmodeltester.check(model)

    # confirm that font data loaded appropriately
    assert model._h_header == ["Min : Max [Default]", "Edit Values"]
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
        ["0.0 : 1.0 [0.0]", ""],
        ["0.0 : 1.0 [0.0]", ""],
        ["300.0 : 1000.0 [300.0]", ""],
        ["-15.0 : 0.0 [0.0]", ""],
        ["0.0 : 1.0 [0.5]", ""],
    ]


def test_designaxis_model_get_instance_data(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # without user entered definitions, we should get
    # an empty axis tag / value dict
    # this is intentional so that these axes remain
    # variable
    assert model.get_instance_data() == {}

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


def test_designaxis_model_get_partial_instance_data(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # without user entered definitions, we should get
    # empty set
    assert model.get_instance_data() == {}

    # simulate update of model data with user input
    # that requests sub-space that maintains
    # variable "MONO" and "slnt" axes
    # (i.e. these fields are empty)
    model._data[0][1] = ""
    model._data[1][1] = "1.0"
    model._data[2][1] = "1000.0"
    model._data[3][1] = ""
    model._data[4][1] = "1.0"
    model.layoutChanged.emit()

    # should not include instance values for: "MONO", "slnt"
    # the instantiation function maintains variable
    # axes for any axis tag that is present in font
    # and not included in this dict
    assert model.get_instance_data() == {
        "CASL": 1.0,
        "wght": 1000.0,
        "CRSV": 1.0,
    }


def test_designaxis_model_instance_data_validates_missing_data(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # without user entered definitions, we should get
    # an empty axis tag / value dict
    # this is intentional so that these axes remain
    # variable
    assert model.get_instance_data() == {}

    assert model.instance_data_validates_missing_data() is False

    # fill model and try again
    # this requires at least one axis to have a value
    model._data[0][1] = ""
    model._data[1][1] = "1.0"
    model._data[2][1] = ""
    model._data[3][1] = ""
    model._data[4][1] = ""
    model.layoutChanged.emit()

    assert model.instance_data_validates_missing_data() is True


def test_designaxis_model_instance_data_validates_invalid_data(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # without user entered definitions, we should get
    # an empty axis tag / value dict
    # this is intentional so that these axes remain
    # variable
    assert model.get_instance_data() == {}

    assert model.instance_data_validates_missing_data() is False

    # fill model and try again
    # but this time add invalid data
    # this should prompt a ValueError exception
    model._data[0][1] = ""
    model._data[1][1] = "BOGUSVALUE"
    model._data[2][1] = ""
    model._data[3][1] = ""
    model._data[4][1] = ""
    model.layoutChanged.emit()

    with pytest.raises(ValueError):
        model.instance_data_validates_missing_data()


def test_designaxis_model_subspace_data_validates_includes_default(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # all values include the default axis value (300) in range
    passing_values = (
        [100, 300],
        [200, 400],
        [300, 700],
        [100.0, 300.0],
        [200.0, 400.0],
        [300.0, 700.0],
    )

    # these should not raise exception
    for passing_value in passing_values:
        model.subspace_data_validates_includes_default_value(passing_value, "wght")

    failing_values = [
        [100, 200],
        [400, 700],
        [100.0, 299.9],
        [300.1, 400.0],
        [100, 299.9],
        [300.1, 700],
    ]

    # these should raise exceptions because default value is not included in range
    for failing_value in failing_values:
        with pytest.raises(ValueError):
            model.subspace_data_validates_includes_default_value(failing_value, "wght")


def test_designaxis_model_parse_subspace_range_pass(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # The following list includes valid, supported axis range
    # restriction values for the requested syntax `min_val:max_val [default_val]`
    # the test font includes wght axis range with 300 default value
    # this must be included in the range until L4 sub-spacing support
    # is added
    passing_values = [
        ("100:300", (100.0, 300.0), None),
        ("100 : 300", (100.0, 300.0), None),
        (" 100 : 300 ", (100.0, 300.0), None),
        ("300:100", (100.0, 300.0), None),
        ("300 : 100", (100.0, 300.0), None),
        (" 300 : 100 ", (100.0, 300.0), None),
        ("100.0:300.0", (100.0, 300.0), None),
        ("100.0 : 300.0", (100.0, 300.0), None),
        (" 100.0 : 300.0 ", (100.0, 300.0), None),
        ("100:300 [300]", (100.0, 300.0), "300"),
        ("100 : 300 [300]", (100.0, 300.0), "300"),
        (" 100 : 300 [ 300 ]", (100.0, 300.0), "300"),
        ("100.0:300.0 [300.0]", (100.0, 300.0), "300.0"),
        ("100.0 : 300.0 [300.0]", (100.0, 300.0), "300.0"),
        (" 100.0 : 300.0 [300.0]", (100.0, 300.0), "300.0"),
        ("100.0:300.0 [ 300.0 ]", (100.0, 300.0), "300.0"),
        ("300.0:100.0 [ 300.0 ]", (100.0, 300.0), "300.0"),
        ("300:100 [ 300 ]", (100.0, 300.0), "300"),
        # the following is not recommended because default will not match in the future
        ("(100:300)", (100.0, 300.0), None),
    ]

    for passing_value in passing_values:
        match = model.parse_subspace_range(passing_value[0], "wght")
        # range should match tuple
        assert match[0] == passing_value[1]
        # default value should match string
        assert match[1] == passing_value[2]

    negative_values = [
        # negative values on slnt axis
        ("-10:0", (-10.0, 0.0), None),
        ("-10.0:0", (-10.0, 0.0), None),
        ("-10 : 0", (-10.0, 0.0), None),
        # mock negative max end using signed zero
        ("-10:-0", (-10.0, -0.0), None),
        ("-10.0:-0.0", (-10.0, -0.0), None),
        ("-10.0 : -0.0", (-10.0, -0.0), None),
        # test negative default
        ("-10:-0 [-5]", (-10.0, -0.0), "-5"),
        ("-10:-0 [ -5 ]", (-10.0, -0.0), "-5"),
        ("-10.0 : -0.0 [ -5.0 ]", (-10.0, -0.0), "-5.0"),
    ]

    for negative_value in negative_values:
        # switch to slnt axis for these tests
        match = model.parse_subspace_range(negative_value[0], "slnt")
        # range should match tuple
        assert match[0] == negative_value[1]
        # default value should match string
        assert match[1] == negative_value[2]


def test_designaxis_model_parse_subspace_range_fail_invalid_syntax(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # The following list includes invalid values that
    # raise errors during execution
    failing_values = [
        # invalid syntax
        "100,300",
        "(100,300)",
        "100,300 [300]",
        "(100,300) [300]",
        # invalid types
        "100:bogus",
        "bogus:100",
    ]

    for failing_value in failing_values:
        with pytest.raises(ValueError):
            model.parse_subspace_range(failing_value, "wght")


def test_designaxis_model_parse_subspace_range_fail_invalid_range_without_default(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # The following list includes invalid values that
    # raise errors during execution b/c axis default not in range
    # this applies until L4 support is available
    failing_values = [
        "100:200",
        "400:700",
        "100.0:299.9",
        "300.1:400.0",
        "100:299.9",
        "300.1:700",
        "200:100",
        "299.9 : 100.0",
    ]

    for failing_value in failing_values:
        with pytest.raises(ValueError):
            model.parse_subspace_range(failing_value, "wght")


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


def test_designaxis_model_get_axis_name_string(qtbot):
    tableview = QTableView()
    model = DesignAxisModel()
    tableview.setModel(model)
    qtbot.addWidget(tableview)
    model.load_font(get_font_model())

    # registered axes
    assert model.get_axis_name_string("ital") == "Italic"
    assert model.get_axis_name_string("opsz") == "Optical size"
    assert model.get_axis_name_string("slnt") == "Slant"
    assert model.get_axis_name_string("wdth") == "Width"
    assert model.get_axis_name_string("wght") == "Weight"

    # unregistered axes
    assert model.get_axis_name_string("CASL") == "Casual"
    assert model.get_axis_name_string("CRSV") == "Cursive"
    assert model.get_axis_name_string("XPRN") == "Expression"
    assert model.get_axis_name_string("GRAD") == "Grade"
    assert model.get_axis_name_string("MONO") == "Monospace"
    assert model.get_axis_name_string("SOFT") == "Softness"
    assert model.get_axis_name_string("WONK") == "Wonky"

    # not a known (to this application) axis tag
    assert model.get_axis_name_string("ZXYJ") is None
