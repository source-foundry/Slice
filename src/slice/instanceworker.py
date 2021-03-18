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

import datetime
import sys
import traceback

from fontTools.misc.textTools import num2binary
from fontTools.ttLib.ttFont import TTFont
from fontTools.varLib.mutator import instantiateVariableFont
from PyQt5.QtCore import QObject, QRunnable, pyqtSignal, pyqtSlot


class InstanceWorkerSignals(QObject):
    finished = pyqtSignal()  # no return type, only signal that complete
    error = pyqtSignal(str)  # returns the error message
    result = pyqtSignal(str)  # returns file path for the new file write


class InstanceWorker(QRunnable):
    def __init__(
        self,
        outpath=None,
        font_model=None,
        axis_model=None,
        name_model=None,
        bit_model=None,
    ):
        super().__init__()
        self.signals = InstanceWorkerSignals()
        self.outpath = outpath
        self.font_model = font_model
        self.axis_model = axis_model
        self.name_model = name_model
        self.bit_model = bit_model
        self.ttfont = None

    @pyqtSlot()
    def run(self):
        try:
            # Debugging in stdout
            print(f"\n\n{datetime.datetime.now()}")
            self.ttfont = TTFont(self.font_model.fontpath)
            # instantiate
            self.instantiate_variable_font()
            # edit name table records
            self.edit_name_table()
            # edit bit flags
            self.edit_bit_flags()
            # write to disk
            self.ttfont.save(self.outpath)
        except Exception as e:
            self.signals.error.emit(f"{e}")
            sys.stderr.write(f"{traceback.format_exc()}\n")
        else:
            # returns the file out file path on success
            self.signals.result.emit(self.outpath)
            self.signals.finished.emit()

    def instantiate_variable_font(self):
        axis_instance_data = self.axis_model.get_instance_data()
        instantiateVariableFont(self.ttfont, axis_instance_data, inplace=True)
        print("\nAXIS INSTANCE VALUES")
        print(
            f"Instantiated variable font with axis definitions:\n{axis_instance_data}"
        )

    def edit_name_table(self):
        # string, nameID, platformID, platEncID, langID
        name_record_plat_enc_lang = (3, 1, 1033)
        name_instance_data = self.name_model.get_instance_data()
        name_table = self.ttfont["name"]
        # set 3, 1, 1033 name records (only!)
        # mandatory writes
        name_table.setName(name_instance_data["nameID1"], 1, *name_record_plat_enc_lang)
        name_table.setName(name_instance_data["nameID2"], 2, *name_record_plat_enc_lang)
        name_table.setName(name_instance_data["nameID3"], 3, *name_record_plat_enc_lang)
        name_table.setName(name_instance_data["nameID4"], 4, *name_record_plat_enc_lang)
        name_table.setName(name_instance_data["nameID6"], 6, *name_record_plat_enc_lang)

        # optional writes
        # Approach:
        # (1) if user text data exists, write it
        # (2) if user text data does not exist but record does, delete it
        # (3) otherwise do nothing
        if name_instance_data["nameID16"] != "":
            name_table.setName(
                name_instance_data["nameID16"], 16, *name_record_plat_enc_lang
            )
        elif name_table.getName(16, *name_record_plat_enc_lang):
            name_table.removeNames(16, *name_record_plat_enc_lang)

        if name_instance_data["nameID17"] != "":
            name_table.setName(
                name_instance_data["nameID17"], 17, *name_record_plat_enc_lang
            )
        elif name_table.getName(17, *name_record_plat_enc_lang):
            name_table.removeNames(17, *name_record_plat_enc_lang)

        if name_instance_data["nameID21"] != "":
            name_table.setName(
                name_instance_data["nameID21"], 21, *name_record_plat_enc_lang
            )
        elif name_table.getName(21, *name_record_plat_enc_lang):
            name_table.removeNames(21, *name_record_plat_enc_lang)

        if name_instance_data["nameID22"] != "":
            name_table.setName(
                name_instance_data["nameID22"], 22, *name_record_plat_enc_lang
            )
        elif name_table.getName(22, *name_record_plat_enc_lang):
            name_table.removeNames(22, *name_record_plat_enc_lang)

        # update name table data
        self.ttfont["name"] = name_table

        # print name table report
        print("\nNAME TABLE EDITS")
        print("Name records at write time:\n")
        print(f"nameID1: {self.ttfont['name'].getName(1, *name_record_plat_enc_lang)}")
        print(f"nameID2: {self.ttfont['name'].getName(2, *name_record_plat_enc_lang)}")
        print(f"nameID3: {self.ttfont['name'].getName(3, *name_record_plat_enc_lang)}")
        print(f"nameID4: {self.ttfont['name'].getName(4, *name_record_plat_enc_lang)}")
        print(f"nameID6: {self.ttfont['name'].getName(6, *name_record_plat_enc_lang)}")
        print(
            f"nameID16: {self.ttfont['name'].getName(16, *name_record_plat_enc_lang)}"
        )
        print(
            f"nameID17: {self.ttfont['name'].getName(17, *name_record_plat_enc_lang)}"
        )
        print(
            f"nameID21: {self.ttfont['name'].getName(21, *name_record_plat_enc_lang)}"
        )
        print(
            f"nameID22: {self.ttfont['name'].getName(22, *name_record_plat_enc_lang)}"
        )

    def edit_bit_flags(self):
        # edit the OS/2.fsSelection bit flag
        pre_os2_fsselection_int = self.ttfont["OS/2"].fsSelection
        edited_os2_fsselection_int = self.bit_model.edit_os2_fsselection_bits(
            pre_os2_fsselection_int
        )
        # edit OS/2.fsSelection in the TTFont attribute
        self.ttfont["OS/2"].fsSelection = edited_os2_fsselection_int

        # edit head.macstyle bit flag
        pre_head_macstyle_int = self.ttfont["head"].macStyle
        edited_head_macstyle_int = self.bit_model.edit_head_macstyle_bits(
            pre_head_macstyle_int
        )
        self.ttfont["head"].macStyle = edited_head_macstyle_int

        # bit flag debugging stdout report
        print("\nBIT FLAGS")
        print(
            f"\nOS/2.fsSelection updated with the following data:\n"
            f"{self.bit_model.get_os2_instance_data()}"
        )
        print(f"Pre OS/2.fsSelection:  {num2binary(pre_os2_fsselection_int, bits=16)}")
        print(
            f"Post OS/2.fsSelection: {num2binary(self.ttfont['OS/2'].fsSelection, bits=16)}"
        )
        print(
            f"\nhead.macStyle bit flag updated with the following data:\n"
            f"{self.bit_model.get_head_instance_data()}"
        )
        print(f"Pre head.macStyle:  {num2binary(pre_head_macstyle_int, bits=16)}")
        print(
            f"Post head.macStyle: {num2binary(self.ttfont['head'].macStyle, bits=16)}"
        )
