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
    return FontModel(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


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


def test_instanceworker_instantiate_ttfont_and_gen_static_instance(tmpdir):
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

    assert iw.ttfont is None
    # the ttfont attribute is set with this method
    iw.instantiate_ttfont()
    assert type(iw.ttfont) is TTFont
    # it is a variable font and should have an fvar table
    assert "fvar" in iw.ttfont

    # after instantiation of the static, fvar should be gone
    iw.instantiate_variable_font()
    assert "fvar" not in iw.ttfont


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
