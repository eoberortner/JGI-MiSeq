# file openpyxl/tests/test_style.py

# Copyright (c) 2010-2011 openpyxl
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
#
# @license: http://www.opensource.org/licenses/mit-license.php
# @author: see AUTHORS file

# Python stdlib imports
import os.path
import datetime

# 3rd party imports
from nose.tools import eq_, assert_false, ok_

# package imports
from openpyxl.reader.excel import load_workbook
from openpyxl.tests.helper import DATADIR, assert_equals_file_content, get_xml
from openpyxl.reader.style import read_style_table
from openpyxl.workbook import Workbook
from openpyxl.style import NumberFormat
from openpyxl.writer.styles import StyleWriter
from openpyxl.style import NumberFormat, Border, Color, Font


class TestCreateStyle(object):

    @classmethod
    def setup_class(cls):
        now = datetime.datetime.now()
        cls.workbook = Workbook()
        cls.worksheet = cls.workbook.create_sheet()
        cls.worksheet.cell(coordinate='A1').value = '12.34%'
        cls.worksheet.cell(coordinate='B4').value = now
        cls.worksheet.cell(coordinate='B5').value = now
        cls.worksheet.cell(coordinate='C14').value = 'This is a test'
        cls.worksheet.cell(coordinate='D9').value = '31.31415'
        cls.worksheet.cell(coordinate='D9').style.number_format.format_code = \
                NumberFormat.FORMAT_NUMBER_00
        cls.writer = StyleWriter(cls.workbook)

    def test_create_style_table(self):
        eq_(3, len(self.writer.style_table))

    def test_write_style_table(self):
        reference_file = os.path.join(DATADIR, 'writer', 'expected', 'simple-styles.xml')
        assert_equals_file_content(reference_file, self.writer.write_table())

class TestStyleWriter(object):

    def setUp(self):

        self.workbook = Workbook()
        self.worksheet = self.workbook.create_sheet()

    def test_no_style(self):

        w = StyleWriter(self.workbook)
        eq_(0, len(w.style_table))

    def test_nb_style(self):

        for i in range(1, 6):
            self.worksheet.cell(row=1, column=i).style.font.size += i
        w = StyleWriter(self.workbook)
        eq_(5, len(w.style_table))

        self.worksheet.cell('A10').style.borders.top = Border.BORDER_THIN
        w = StyleWriter(self.workbook)
        eq_(6, len(w.style_table))

    def test_style_unicity(self):

        for i in range(1, 6):
            self.worksheet.cell(row=1, column=i).style.font.bold = True
        w = StyleWriter(self.workbook)
        eq_(1, len(w.style_table))

    def test_fonts(self):

        self.worksheet.cell('A1').style.font.size = 12
        self.worksheet.cell('A1').style.font.bold = True
        w = StyleWriter(self.workbook)
        w._write_fonts()
        eq_(get_xml(w._root), '<?xml version=\'1.0\' encoding=\'UTF-8\'?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11" /><color theme="1" /><name val="Calibri" /><family val="2" /><scheme val="minor" /></font><font><sz val="12" /><color rgb="FF000000" /><name val="Calibri" /><family val="2" /><b /></font></fonts></styleSheet>')

    def test_fonts_with_underline(self):
        self.worksheet.cell('A1').style.font.size = 12
        self.worksheet.cell('A1').style.font.bold = True
        self.worksheet.cell('A1').style.font.underline = Font.UNDERLINE_SINGLE
        w = StyleWriter(self.workbook)
        w._write_fonts()
        eq_(get_xml(w._root), '<?xml version=\'1.0\' encoding=\'UTF-8\'?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fonts count="2"><font><sz val="11" /><color theme="1" /><name val="Calibri" /><family val="2" /><scheme val="minor" /></font><font><sz val="12" /><color rgb="FF000000" /><name val="Calibri" /><family val="2" /><b /><u /></font></fonts></styleSheet>')

    def test_fills(self):

        self.worksheet.cell('A1').style.fill.fill_type = 'solid'
        self.worksheet.cell('A1').style.fill.start_color.index = Color.DARKYELLOW
        w = StyleWriter(self.workbook)
        w._write_fills()
        eq_(get_xml(w._root), '<?xml version=\'1.0\' encoding=\'UTF-8\'?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><fills count="3"><fill><patternFill patternType="none" /></fill><fill><patternFill patternType="gray125" /></fill><fill><patternFill patternType="solid"><fgColor rgb="FF808000" /></patternFill></fill></fills></styleSheet>')

    def test_borders(self):

        self.worksheet.cell('A1').style.borders.top.border_style = Border.BORDER_THIN
        self.worksheet.cell('A1').style.borders.top.color.index = Color.DARKYELLOW
        w = StyleWriter(self.workbook)
        w._write_borders()
        eq_(get_xml(w._root), '<?xml version=\'1.0\' encoding=\'UTF-8\'?><styleSheet xmlns="http://schemas.openxmlformats.org/spreadsheetml/2006/main"><borders count="2"><border><left /><right /><top /><bottom /><diagonal /></border><border><left /><right /><top style="thin"><color rgb="FF808000" /></top><bottom /><diagonal /></border></borders></styleSheet>')

    def test_write_cell_xfs_1(self):

        self.worksheet.cell('A1').style.font.size = 12
        w = StyleWriter(self.workbook)
        ft = w._write_fonts()
        nft = w._write_number_formats()
        w._write_cell_xfs(nft, ft, {}, {})
        xml = get_xml(w._root)
        ok_('applyFont="1"' in xml)
        ok_('applyFill="1"' not in xml)
        ok_('applyBorder="1"' not in xml)
        ok_('applyAlignment="1"' not in xml)

    def test_alignment(self):
        self.worksheet.cell('A1').style.alignment.horizontal = 'center'
        self.worksheet.cell('A1').style.alignment.vertical = 'center'
        w = StyleWriter(self.workbook)
        nft = w._write_number_formats()
        w._write_cell_xfs(nft, {}, {}, {})
        xml = get_xml(w._root)
        ok_('applyAlignment="1"' in xml)
        ok_('horizontal="center"' in xml)
        ok_('vertical="center"' in xml)

    def test_alignment_rotation(self):
        self.worksheet.cell('A1').style.alignment.vertical = 'center'
        self.worksheet.cell('A1').style.alignment.text_rotation = 90
        self.worksheet.cell('A2').style.alignment.vertical = 'center'
        self.worksheet.cell('A2').style.alignment.text_rotation = 135
        self.worksheet.cell('A3').style.alignment.text_rotation = -34
        w = StyleWriter(self.workbook)
        nft = w._write_number_formats()
        w._write_cell_xfs(nft, {}, {}, {})
        xml = get_xml(w._root)
        ok_('textRotation="90"' in xml)
        ok_('textRotation="135"' in xml)
        ok_('textRotation="124"' in xml)

    def test_alignment_indent(self):
        self.worksheet.cell('A1').style.alignment.indent = 1
        self.worksheet.cell('A2').style.alignment.indent = 4
        self.worksheet.cell('A3').style.alignment.indent = 0
        self.worksheet.cell('A3').style.alignment.indent = -1
        w = StyleWriter(self.workbook)
        nft = w._write_number_formats()
        w._write_cell_xfs(nft, {}, {}, {})
        xml = get_xml(w._root)
        ok_('indent="1"' in xml)
        ok_('indent="4"' in xml)
        #Indents not greater than zero are ignored when writing
        ok_('indent="0"' not in xml)
        ok_('indent="-1"' not in xml)


#def test_format_comparisions():
#    format1 = NumberFormat()
#    format2 = NumberFormat()
#    format3 = NumberFormat()
#    format1.format_code = 'm/d/yyyy'
#    format2.format_code = 'm/d/yyyy'
#    format3.format_code = 'mm/dd/yyyy'
#    assert not format1 < format2
#    assert format1 < format3
#    assert format1 == format2
#    assert format1 != format3


def test_builtin_format():
    format = NumberFormat()
    format.format_code = '0.00'
    eq_(format.builtin_format_code(2), format._format_code)


def test_read_style():
    reference_file = os.path.join(DATADIR, 'reader', 'simple-styles.xml')

    handle = open(reference_file, 'r')
    try:
        content = handle.read()
    finally:
        handle.close()
    style_table = read_style_table(content)
    eq_(4, len(style_table))
    eq_(NumberFormat._BUILTIN_FORMATS[9],
            style_table[1].number_format.format_code)
    eq_('yyyy-mm-dd', style_table[2].number_format.format_code)


def test_read_complex_style():
    reference_file = os.path.join(DATADIR, 'reader', 'complex-styles.xlsx')
    wb = load_workbook(reference_file)
    ws = wb.get_active_sheet()
    eq_(ws.column_dimensions['A'].width, 31.1640625)
    eq_(ws.cell('A2').style.font.name, 'Arial')
    eq_(ws.cell('A2').style.font.size, '10')
    eq_(ws.cell('A2').style.font.bold, False)
    eq_(ws.cell('A2').style.font.italic, False)
    eq_(ws.cell('A3').style.font.name, 'Arial')
    eq_(ws.cell('A3').style.font.size, '12')
    eq_(ws.cell('A3').style.font.bold, True)
    eq_(ws.cell('A3').style.font.italic, False)
    eq_(ws.cell('A4').style.font.name, 'Arial')
    eq_(ws.cell('A4').style.font.size, '14')
    eq_(ws.cell('A4').style.font.bold, False)
    eq_(ws.cell('A4').style.font.italic, True)
    eq_(ws.cell('A5').style.font.color.index, 'FF3300FF')
    eq_(ws.cell('A6').style.font.color.index, 'theme:9:')
    eq_(ws.cell('A7').style.fill.start_color.index, 'FFFFFF66')
    eq_(ws.cell('A8').style.fill.start_color.index, 'theme:8:')
    eq_(ws.cell('A9').style.alignment.horizontal,'left')
    eq_(ws.cell('A10').style.alignment.horizontal,'right')
    eq_(ws.cell('A11').style.alignment.horizontal,'center')
    eq_(ws.cell('A12').style.alignment.vertical,'top')
    eq_(ws.cell('A13').style.alignment.vertical,'center')
    eq_(ws.cell('A14').style.alignment.vertical,'bottom')
    eq_(ws.cell('A15').style.number_format._format_code,'0.00')
    eq_(ws.cell('A16').style.number_format._format_code,'mm-dd-yy')
    eq_(ws.cell('A17').style.number_format._format_code,'0.00%')
    eq_('A18:B18' in ws._merged_cells, True)
    eq_(ws.cell('B18').merged,True)
    eq_(ws.cell('A19').style.borders.top.color.index,'FF006600')
    eq_(ws.cell('A19').style.borders.bottom.color.index,'FF006600')
    eq_(ws.cell('A19').style.borders.left.color.index,'FF006600')
    eq_(ws.cell('A19').style.borders.right.color.index,'FF006600')
    eq_(ws.cell('A21').style.borders.top.color.index,'theme:7:')
    eq_(ws.cell('A21').style.borders.bottom.color.index,'theme:7:')
    eq_(ws.cell('A21').style.borders.left.color.index,'theme:7:')
    eq_(ws.cell('A21').style.borders.right.color.index,'theme:7:')
    eq_(ws.cell('A23').style.fill.start_color.index,'FFCCCCFF')
    eq_(ws.cell('A23').style.borders.top.color.index,'theme:6:')
    eq_('A23:B24' in ws._merged_cells, True)
    eq_(ws.cell('A24').merged,True)
    eq_(ws.cell('B23').merged,True)
    eq_(ws.cell('B24').merged,True)
    eq_(ws.cell('A25').style.alignment.wrap_text,True)
    eq_(ws.cell('A26').style.alignment.shrink_to_fit,True)

def test_read_cell_style():
    reference_file = os.path.join(
            DATADIR, 'reader', 'empty-workbook-styles.xml')
    handle = open(reference_file, 'r')
    try:
        content = handle.read()
    finally:
        handle.close()
    style_table = read_style_table(content)
    eq_(2, len(style_table))
