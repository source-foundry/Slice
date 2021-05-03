from pathlib import Path

from fontTools.ttLib import TTFont
import pytest

from PyQt5.QtCore import pyqtBoundSignal

from slice.instanceworker import InstanceWorker, InstanceWorkerSignals
from slice.models import FontModel, FontBitFlagModel, DesignAxisModel, FontNameModel


def bit_is_set(int_type, offset):
    mask = 1 << offset
    return (int_type & mask) != 0


def get_font_model():
    # Values in this test font
    # {'axisTag': 'MONO', 'axisNameID': 269, 'flags': 0, 'minValue': 0.0, 'defaultValue': 0.0, 'maxValue': 1.0}
    # {'axisTag': 'CASL', 'axisNameID': 270, 'flags': 0, 'minValue': 0.0, 'defaultValue': 0.0, 'maxValue': 1.0}
    # {'axisTag': 'wght', 'axisNameID': 271, 'flags': 0, 'minValue': 300.0, 'defaultValue': 300.0, 'maxValue': 1000.0}
    # {'axisTag': 'slnt', 'axisNameID': 272, 'flags': 0, 'minValue': -15.0, 'defaultValue': 0.0, 'maxValue': 0.0}
    # {'axisTag': 'CRSV', 'axisNameID': 273, 'flags': 0, 'minValue': 0.0, 'defaultValue': 0.5, 'maxValue': 1.0}
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def get_font_model_woff():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff").resolve())


def get_font_model_woff2():
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.woff2").resolve())


def get_os2_default_dict_false():
    return {
        "bit0": False,
        "bit5": False,
        "bit6": False,
        "bit8": False,
    }


def get_os2_default_dict_true():
    return {
        "bit0": True,
        "bit5": True,
        "bit6": True,
        "bit8": True,
    }


def get_head_default_dict_false():
    return {
        "bit0": False,
        "bit1": False,
    }


def get_head_default_dict_true():
    return {
        "bit0": True,
        "bit1": True,
    }


def test_instanceworker_signals_instantiation():
    iws = InstanceWorkerSignals()
    assert type(iws.finished) is pyqtBoundSignal
    assert type(iws.error) is pyqtBoundSignal
    assert type(iws.result) is pyqtBoundSignal


def test_instanceworker_class_default(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw is not None
    # does not convert to Path type on instantiation
    assert type(iw.outpath) is str
    assert type(iw.font_model) is FontModel
    assert type(iw.name_model) is FontNameModel
    assert type(iw.axis_model) is DesignAxisModel
    assert type(iw.bit_model) is FontBitFlagModel
    # ttfont attribute is not instantiated until run() method execution
    assert iw.ttfont is None


def test_instanceworker_instantiate_ttfont_and_gen_with_no_user_axis_defs(tmpdir):
    # This should gen to the var font with the same axis ranges
    # Note that this route is not executed because the application validates
    # that at least one axis is defined, else there is nothing to do
    # since the request is the original var font if there are no axis value defs
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    # uses a default model that has no data entry
    # and should take default values for all axes
    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # confirm that all variable axes remain
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include all variable axis tags in the original
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" in axis_tags
    assert "slnt" in axis_tags
    assert "CRSV" in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_with_no_user_axis_defs_woff_format(
    tmpdir,
):
    # This should gen to the var font with the same axis ranges
    # Note that this route is not executed because the application validates
    # that at least one axis is defined, else there is nothing to do
    # since the request is the original var font if there are no axis value defs
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff()

    # uses a default model that has no data entry
    # and should take default values for all axes
    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # confirm that it remains a woff format object
    # following instantiation
    assert iw.ttfont.flavor == "woff"
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # confirm that all variable axes remain
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include all variable axis tags in the original
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" in axis_tags
    assert "slnt" in axis_tags
    assert "CRSV" in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_with_no_user_axis_defs_woff2_format(
    tmpdir,
):
    # This should gen to the var font with the same axis ranges
    # Note that this route is not executed because the application validates
    # that at least one axis is defined, else there is nothing to do
    # since the request is the original var font if there are no axis value defs
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff2()

    # uses a default model that has no data entry
    # and should take default values for all axes
    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # confirm that it remains a woff2 format file
    # following instantiation
    assert iw.ttfont.flavor == "woff2"
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # confirm that all variable axes remain
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include all variable axis tags in the original
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" in axis_tags
    assert "slnt" in axis_tags
    assert "CRSV" in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_one_axis(tmpdir):
    # When there are
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # "MONO" axis defined as variable (i.e., no user input)
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = "0"
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after instantiation of the partial, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # in the test font, the "MONO" axis should still be variable
    # with the variable setting that was used above
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO axis, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" not in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_one_axis_woff(tmpdir):
    # When there are
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # "MONO" axis defined as variable (i.e., no user input)
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = "0"
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after instantiation of the partial, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # confirm that it remains a woff format file
    assert iw.ttfont.flavor == "woff"
    # in the test font, the "MONO" axis should still be variable
    # with the variable setting that was used above
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO axis, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" not in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_one_axis_woff2(
    tmpdir,
):
    # When there are
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff2()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # "MONO" axis defined as variable (i.e., no user input)
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = "0"
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after instantiation of the partial, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # confirm that it remains a woff2 format file
    assert iw.ttfont.flavor == "woff2"
    # in the test font, the "MONO" axis should still be variable
    # with the variable setting that was used above
    # make list of axis tags
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO axis, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" not in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_multi_axis(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # the next step mocks lack of user entry in MONO and CASL axis fields
    # with values defined for other fields. This should lead to a sub-space
    # build with variable and wght var axes
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = ""
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after sub-space gen, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO and CASL axes, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_multi_axis_woff(
    tmpdir,
):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # the next step mocks lack of user entry in MONO and CASL axis fields
    # with values defined for other fields. This should lead to a sub-space
    # build with variable and wght var axes
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = ""
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after sub-space gen, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # should remain woff format file
    assert iw.ttfont.flavor == "woff"
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO and CASL axes, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_and_gen_subspace_multi_axis_woff2(
    tmpdir,
):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff2()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # the next step mocks lack of user entry in MONO and CASL axis fields
    # with values defined for other fields. This should lead to a sub-space
    # build with variable and wght var axes
    axis_model._data[0][1] = ""
    axis_model._data[1][1] = ""
    axis_model._data[2][1] = "300"
    axis_model._data[3][1] = "0"
    axis_model._data[4][1] = "0.5"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after sub-space gen, fvar should still be present
    iw.instantiate_variable_font()
    assert "fvar" in iw.ttfont
    # should remain woff format file
    assert iw.ttfont.flavor == "woff2"
    axis_tags = [axis.axisTag for axis in iw.ttfont["fvar"].axes]
    # the font should include a variable MONO and CASL axes, all others
    # should have been sliced
    assert "MONO" in axis_tags
    assert "CASL" in axis_tags
    assert "wght" not in axis_tags
    assert "slnt" not in axis_tags
    assert "CRSV" not in axis_tags


def test_instanceworker_instantiate_ttfont_raises_valueerror_on_invalid_data(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)
    # enters an invalid data entry string of "BOGUSVALUE"
    # this should raise a ValueError that propagates
    # to an execution error dialog.
    axis_model._data[0][1] = "BOGUSVALUE"

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # confirm that execution with an invalid value raises ValueError
    # during attempt to cast to float
    with pytest.raises(ValueError):
        iw.instantiate_variable_font()


def test_instanceworker_edit_name_table(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()

    # mock name table data for all fields
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        ["Sixteen"],  # nameID16
        ["Seventeen"],  # nameID17
        ["Twenty-one"],  # nameID21
        ["Twenty-two"],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang).toUnicode() == "Sixteen"
    assert name.getName(17, *name_record_plat_enc_lang).toUnicode() == "Seventeen"
    assert name.getName(21, *name_record_plat_enc_lang).toUnicode() == "Twenty-one"
    assert name.getName(22, *name_record_plat_enc_lang).toUnicode() == "Twenty-two"

    # mock name table data for mandatory fields only
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        [""],  # nameID16
        [""],  # nameID17
        [""],  # nameID21
        [""],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang) is None
    assert name.getName(17, *name_record_plat_enc_lang) is None
    assert name.getName(21, *name_record_plat_enc_lang) is None
    assert name.getName(22, *name_record_plat_enc_lang) is None


def test_instanceworker_edit_name_table_woff(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert iw.ttfont.flavor == "woff"

    # mock name table data for all fields
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        ["Sixteen"],  # nameID16
        ["Seventeen"],  # nameID17
        ["Twenty-one"],  # nameID21
        ["Twenty-two"],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang).toUnicode() == "Sixteen"
    assert name.getName(17, *name_record_plat_enc_lang).toUnicode() == "Seventeen"
    assert name.getName(21, *name_record_plat_enc_lang).toUnicode() == "Twenty-one"
    assert name.getName(22, *name_record_plat_enc_lang).toUnicode() == "Twenty-two"

    # mock name table data for mandatory fields only
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        [""],  # nameID16
        [""],  # nameID17
        [""],  # nameID21
        [""],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang) is None
    assert name.getName(17, *name_record_plat_enc_lang) is None
    assert name.getName(21, *name_record_plat_enc_lang) is None
    assert name.getName(22, *name_record_plat_enc_lang) is None


def test_instanceworker_edit_name_table_woff2(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff2()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert iw.ttfont.flavor == "woff2"

    # mock name table data for all fields
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        ["Sixteen"],  # nameID16
        ["Seventeen"],  # nameID17
        ["Twenty-one"],  # nameID21
        ["Twenty-two"],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang).toUnicode() == "Sixteen"
    assert name.getName(17, *name_record_plat_enc_lang).toUnicode() == "Seventeen"
    assert name.getName(21, *name_record_plat_enc_lang).toUnicode() == "Twenty-one"
    assert name.getName(22, *name_record_plat_enc_lang).toUnicode() == "Twenty-two"

    # mock name table data for mandatory fields only
    iw.name_model._data = [
        ["One"],  # nameID1
        ["Two"],  # nameID2
        ["Three"],  # nameID3
        ["Four"],  # nameID4
        ["Six"],  # nameID6
        [""],  # nameID16
        [""],  # nameID17
        [""],  # nameID21
        [""],  # nameID22
    ]
    iw.name_model.layoutChanged.emit()

    # edit the name tables
    iw.edit_name_table()
    name = iw.ttfont["name"]
    name_record_plat_enc_lang = (3, 1, 1033)
    assert name.getName(1, *name_record_plat_enc_lang).toUnicode() == "One"
    assert name.getName(2, *name_record_plat_enc_lang).toUnicode() == "Two"
    assert name.getName(3, *name_record_plat_enc_lang).toUnicode() == "Three"
    assert name.getName(4, *name_record_plat_enc_lang).toUnicode() == "Four"
    assert name.getName(6, *name_record_plat_enc_lang).toUnicode() == "Six"
    assert name.getName(16, *name_record_plat_enc_lang) is None
    assert name.getName(17, *name_record_plat_enc_lang) is None
    assert name.getName(21, *name_record_plat_enc_lang) is None
    assert name.getName(22, *name_record_plat_enc_lang) is None


def test_instanceworker_edit_bit_flags(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()

    # set the bits
    iw.edit_bit_flags()
    fs_sel = iw.ttfont["OS/2"].fsSelection
    head = iw.ttfont["head"].macStyle
    assert bit_is_set(fs_sel, 0) is True
    assert bit_is_set(fs_sel, 5) is True
    assert bit_is_set(fs_sel, 6) is True
    assert bit_is_set(fs_sel, 8) is True
    assert bit_is_set(head, 0) is True
    assert bit_is_set(head, 1) is True

    # now clear the bits and confirm that they are all cleared
    bit_model2 = FontBitFlagModel(
        get_os2_default_dict_false(), get_head_default_dict_false()
    )
    iw2 = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model2,
    )
    iw2.instantiate_ttfont()
    iw2.edit_bit_flags()
    fs_sel2 = iw2.ttfont["OS/2"].fsSelection
    head2 = iw2.ttfont["head"].macStyle
    assert bit_is_set(fs_sel2, 0) is False
    assert bit_is_set(fs_sel2, 5) is False
    assert bit_is_set(fs_sel2, 6) is False
    assert bit_is_set(fs_sel2, 8) is False
    assert bit_is_set(head2, 0) is False
    assert bit_is_set(head2, 1) is False


def test_instanceworker_edit_bit_flags_woff(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()

    # set the bits
    iw.edit_bit_flags()
    assert iw.ttfont.flavor == "woff"
    fs_sel = iw.ttfont["OS/2"].fsSelection
    head = iw.ttfont["head"].macStyle
    assert bit_is_set(fs_sel, 0) is True
    assert bit_is_set(fs_sel, 5) is True
    assert bit_is_set(fs_sel, 6) is True
    assert bit_is_set(fs_sel, 8) is True
    assert bit_is_set(head, 0) is True
    assert bit_is_set(head, 1) is True

    # now clear the bits and confirm that they are all cleared
    bit_model2 = FontBitFlagModel(
        get_os2_default_dict_false(), get_head_default_dict_false()
    )
    iw2 = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model2,
    )
    iw2.instantiate_ttfont()
    iw2.edit_bit_flags()
    assert iw2.ttfont.flavor == "woff"
    fs_sel2 = iw2.ttfont["OS/2"].fsSelection
    head2 = iw2.ttfont["head"].macStyle
    assert bit_is_set(fs_sel2, 0) is False
    assert bit_is_set(fs_sel2, 5) is False
    assert bit_is_set(fs_sel2, 6) is False
    assert bit_is_set(fs_sel2, 8) is False
    assert bit_is_set(head2, 0) is False
    assert bit_is_set(head2, 1) is False


def test_instanceworker_edit_bit_flags_woff2(tmpdir):
    outpath = str(tmpdir.join("test.ttf"))
    font_model = get_font_model_woff2()

    axis_model = DesignAxisModel()
    axis_model.load_font(font_model)

    name_model = FontNameModel()
    name_model.load_font(font_model)

    bit_model = FontBitFlagModel(
        get_os2_default_dict_true(), get_head_default_dict_true()
    )

    iw = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model,
    )

    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()

    # set the bits
    iw.edit_bit_flags()
    assert iw.ttfont.flavor == "woff2"
    fs_sel = iw.ttfont["OS/2"].fsSelection
    head = iw.ttfont["head"].macStyle
    assert bit_is_set(fs_sel, 0) is True
    assert bit_is_set(fs_sel, 5) is True
    assert bit_is_set(fs_sel, 6) is True
    assert bit_is_set(fs_sel, 8) is True
    assert bit_is_set(head, 0) is True
    assert bit_is_set(head, 1) is True

    # now clear the bits and confirm that they are all cleared
    bit_model2 = FontBitFlagModel(
        get_os2_default_dict_false(), get_head_default_dict_false()
    )
    iw2 = InstanceWorker(
        outpath,
        font_model,
        axis_model,
        name_model,
        bit_model2,
    )
    iw2.instantiate_ttfont()
    iw2.edit_bit_flags()
    assert iw2.ttfont.flavor == "woff2"
    fs_sel2 = iw2.ttfont["OS/2"].fsSelection
    head2 = iw2.ttfont["head"].macStyle
    assert bit_is_set(fs_sel2, 0) is False
    assert bit_is_set(fs_sel2, 5) is False
    assert bit_is_set(fs_sel2, 6) is False
    assert bit_is_set(fs_sel2, 8) is False
    assert bit_is_set(head2, 0) is False
    assert bit_is_set(head2, 1) is False
