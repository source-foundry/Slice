# This file is part of Slice.
#
#    Slice is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Slice is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Slice.  If not, see <https://www.gnu.org/licenses/>.

from fontTools.ttLib import TTFont
from PyQt5.QtCore import QAbstractTableModel, Qt


class SliceBaseTableModel(QAbstractTableModel):
    def __init__(self, *args):
        QAbstractTableModel.__init__(self, *args)
        self._data = [[]]
        self._v_header = []

    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]

    def setData(self, index, value, role):
        if index.isValid() and role == Qt.EditRole:
            self._data[index.row()][index.column()] = value
            self.dataChanged.emit(index, index, [role])
            return True
        else:
            return False

    def rowCount(self, index):
        # the index validity check approach addresses the qabstractitemmodel.cpp check:
        # QtWarningMsg: FAIL! model->hasChildren(topIndex) () returned FALSE (qabstractitemmodeltester.cpp:366)
        # See https://stackoverflow.com/a/50988188/2848172
        if index.isValid():
            return 0
        else:
            return len(self._data)

    def columnCount(self, index):
        # the index validity check approach addresses the qabstractitemmodel.cpp check:
        # QtWarningMsg: FAIL! model->hasChildren(topIndex) () returned FALSE (qabstractitemmodeltester.cpp:366)
        # See https://stackoverflow.com/a/50988188/2848172
        if index.isValid():
            return 0
        else:
            return len(self._data[0])

    def get_data(self):
        return self._data


class FontNameModel(SliceBaseTableModel):
    def __init__(self, *args):
        SliceBaseTableModel.__init__(self, *args)
        self.font_version = None
        self.font_family_name = None
        self._data = [
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
        self._v_header = [
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

    def load_font(self, font_model):
        ttfont = TTFont(font_model.fontpath)
        name = ttfont["name"]
        plat_id = 3
        plat_enc_id = 1
        lang_id = 1033
        for record in name.names:
            if (
                record.nameID == 1
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self._data[0][0] = record.toUnicode()
                self.font_family_name = record.toUnicode()
            elif (
                record.nameID == 2
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self._data[1][0] = record.toUnicode()
            elif (
                record.nameID == 3
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self._data[2][0] = record.toUnicode()
            elif (
                record.nameID == 4
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self._data[3][0] = record.toUnicode()
            elif (
                record.nameID == 5
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self.font_version = record.toUnicode()
            elif (
                record.nameID == 6
                and record.platformID == plat_id
                and record.platEncID == plat_enc_id
                and record.langID == lang_id
            ):
                self._data[4][0] = record.toUnicode()

        self.layoutChanged.emit()
        return True

    def headerData(self, section, orientation, role):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._v_header[section]
        elif orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return "Instance Values"

    def flags(self, index):
        # Note: index validity checks in this block address qabstractitemmodeltester error:
        # QtWarningMsg: FAIL! flags == Qt::ItemIsDropEnabled || flags == 0 () returned FALSE (qabstractitemmodeltester.cpp:329)

        # all indices are editable in this table
        if index.isValid():
            return super().flags(index) | Qt.ItemIsEditable
        else:
            return super().flags(index)

    def get_version(self):
        return self.font_version.split(";")[0]

    def get_family_name(self):
        return self.font_family_name

    def get_instance_data(self):
        return {
            "nameID1": self._data[0][0],
            "nameID2": self._data[1][0],
            "nameID3": self._data[2][0],
            "nameID4": self._data[3][0],
            "nameID6": self._data[4][0],
            "nameID16": self._data[5][0],
            "nameID17": self._data[6][0],
            "nameID21": self._data[7][0],
            "nameID22": self._data[8][0],
        }


class DesignAxisModel(SliceBaseTableModel):
    def __init__(self, *args):
        SliceBaseTableModel.__init__(self, *args)
        self.fvar_axes = {}
        self.ordered_axis_tags = []
        self._data = [
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
            ["", ""],
        ]
        # temp fields on load
        self._v_header = [
            "Axis 1",
            "Axis 2",
            "Axis 3",
            "Axis 4",
            "Axis 5",
        ]
        self._h_header = ["(Min, Max) [Default]", "Instance Values"]

    def data(self, index, role):
        if role in (Qt.DisplayRole, Qt.EditRole):
            return self._data[index.row()][index.column()]

        if role == Qt.TextAlignmentRole:
            return Qt.AlignCenter

    def headerData(self, section, orientation, role):
        if orientation == Qt.Vertical and role == Qt.DisplayRole:
            return self._v_header[section]
        elif orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._h_header[section]

    def flags(self, index):
        # Note: index validity checks in this block address qabstractitemmodeltester error:
        # QtWarningMsg: FAIL! flags == Qt::ItemIsDropEnabled || flags == 0 () returned FALSE (qabstractitemmodeltester.cpp:329)

        # column 0 (axis value range and default) is set
        # to non-editable
        if index.isValid() and index.column() == 0:
            return super().flags(index) | Qt.ItemIsSelectable
        # column 1 (instance value) is set to editable
        elif index.isValid() and index.column() == 1:
            return super().flags(index) | Qt.ItemIsEditable
        else:
            return super().flags(index)

    def load_font(self, font_model):
        ttfont = TTFont(font_model.fontpath)
        fvar = ttfont["fvar"]
        # used to re-define the model data on each
        # new font load
        new_data = []
        # clear the axis tag list attribute
        self.ordered_axis_tags = []
        for axis in fvar.axes:
            self.ordered_axis_tags.append(axis.axisTag)
            self.fvar_axes[axis.axisTag] = [
                axis.minValue,
                axis.defaultValue,
                axis.maxValue,
            ]
            new_data.append(
                [f"({axis.minValue}, {axis.maxValue}) [{axis.defaultValue}]", ""]
            )

        # set header with ordered axis tags
        self._v_header = self.ordered_axis_tags
        self._data = new_data
        self.layoutChanged.emit()
        return True

    def get_number_of_axes(self):
        return len(self.ordered_axis_tags)

    def get_instance_data(self):
        instance_data = {}
        # return a dictionary with map "axis_tag": "value"
        # value is cast to a float from a str
        for x, axistag in enumerate(self._v_header):
            axis_value = self._data[x][1]
            # if user did not define the axis value, then
            # use the default axis value
            if axis_value == "":
                instance_data[axistag] = float(self.get_default_axis_value(axistag))
            else:
                instance_data[axistag] = float(self._data[x][1])

        return instance_data

    def get_default_axis_value(self, axistag):
        if axistag in self.fvar_axes:
            # field that contains the default axis value
            return self.fvar_axes[axistag][1]
        else:
            return None


class FontBitFlagModel(object):
    def __init__(self, os2_dict, head_dict):
        self._os2_dict = os2_dict
        self._head_dict = head_dict

    def _set_bit(self, int_type, offset):
        mask = 1 << offset
        return int_type | mask

    def _clear_bit(self, int_type, offset):
        mask = ~(1 << offset)
        return int_type & mask

    def _get_bit_offset_from_key(self, bitkey):
        # dict key formatted as e.g., `bit0`
        # grab the integer portion and cast to int
        return int(bitkey.replace("bit", ""))

    def _edit_bits(self, integer, bit_dict):
        for bitkey, is_set in bit_dict.items():
            offset = self._get_bit_offset_from_key(bitkey)
            if is_set:
                integer = self._set_bit(integer, offset)
            else:
                integer = self._clear_bit(integer, offset)
        return integer

    def get_os2_instance_data(self):
        return self._os2_dict

    def get_head_instance_data(self):
        return self._head_dict

    def edit_os2_fsselection_bits(self, integer):
        return self._edit_bits(integer, self._os2_dict)

    def edit_head_macstyle_bits(self, integer):
        return self._edit_bits(integer, self._head_dict)


class FontModel(object):
    def __init__(self, fontpath):
        self.fontpath = fontpath

    def is_variable_font(self):
        """Check for fvar table to validate that a TTFont is a variable font"""
        return "fvar" in TTFont(self.fontpath)
