from pathlib import Path

from slice.models import FontModel

#
# Utilities
#


def get_font_path_vf():
    return Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve()


def get_font_path_vf_woff():
    return Path("tests/assets/fonts/Recursive-VF.subset.woff").resolve()


def get_font_path_vf_woff2():
    return Path("tests/assets/fonts/Recursive-VF.subset.woff2").resolve()


def get_font_string_vf():
    return str(Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve())


def get_font_path_static():
    return Path("tests/assets/fonts/Recursive-Sliced.subset.ttf").resolve()


def get_font_string_static():
    return str(Path("tests/assets/fonts/Recursive-Sliced.subset.ttf").resolve())


# ~~~~~~~~~~~
#
# Tests
#
# ~~~~~~~~~~~


def test_font_model_default_with_path():
    fm = FontModel(get_font_path_vf())
    assert fm.fontpath == Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve()


def test_font_model_default_with_string():
    fm = FontModel(get_font_string_vf())
    assert fm.fontpath == str(
        Path("tests/assets/fonts/Recursive-VF.subset.ttf").resolve()
    )


def test_font_model_is_variable_font_true_with_path():
    fm = FontModel(get_font_path_vf())
    assert fm.is_variable_font() is True


def test_font_model_is_variable_font_true_with_path_woff():
    fm = FontModel(get_font_path_vf_woff())
    assert fm.is_variable_font() is True


def test_font_model_is_variable_font_true_with_path_woff2():
    fm = FontModel(get_font_path_vf_woff2())
    assert fm.is_variable_font() is True


def test_font_model_is_variable_font_false_with_path():
    fm = FontModel(get_font_path_static())
    assert fm.is_variable_font() is False


def test_font_model_is_variable_font_true_with_string():
    fm = FontModel(get_font_string_vf())
    assert fm.is_variable_font() is True


def test_font_model_is_variable_font_false_with_string():
    fm = FontModel(get_font_string_static())
    assert fm.is_variable_font() is False
