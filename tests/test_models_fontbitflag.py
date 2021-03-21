from slice.models import FontBitFlagModel

#
# Utilities
#


def get_os2_default_dict():
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


def get_head_default_dict():
    return {
        "bit0": False,
        "bit1": False,
    }


def get_head_default_dict_true():
    return {
        "bit0": True,
        "bit1": True,
    }


# ~~~~~~~~~~~~~~~
#
# Tests
#
# ~~~~~~~~~~~~~~~


def test_bitflag_model_default():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm._os2_dict == get_os2_default_dict()
    assert fm._head_dict == get_head_default_dict()


def test_bitflag_model_set_bit():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm._set_bit(0, 0) == 1


def test_bitflag_model_clear_bit():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm._clear_bit(1, 0) == 0


def test_bitflag_model_get_offset_from_key():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm._get_bit_offset_from_key("bit0") == 0
    assert fm._get_bit_offset_from_key("bit1") == 1
    assert fm._get_bit_offset_from_key("bit10") == 10


def test_bitflag_model_get_os2_instance_data():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm.get_os2_instance_data() == get_os2_default_dict()


def test_bitflag_model_get_head_instance_data():
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    assert fm.get_head_instance_data() == get_head_default_dict()


def test_bitflag_model_edit_os2_fsselection_bits():
    # set all bits that will be cleared
    test_int = 353
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    # confirm that they are all cleared
    assert fm.edit_os2_fsselection_bits(test_int) == 0

    # clear all bits that will be set
    test_int2 = 0
    fm2 = FontBitFlagModel(get_os2_default_dict_true(), get_head_default_dict())
    # confirm that they are all set
    assert fm2.edit_os2_fsselection_bits(test_int2) == 353


def test_bitflag_model_edit_head_macstyle_bits():
    # set all bits that will be cleared
    test_int = 3
    fm = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict())
    # confirm that they are all cleared
    assert fm.edit_head_macstyle_bits(test_int) == 0

    # clear all bits that will be set
    test_int2 = 0
    fm2 = FontBitFlagModel(get_os2_default_dict(), get_head_default_dict_true())
    # confirm that they are all set
    assert fm2.edit_head_macstyle_bits(test_int2) == 3
