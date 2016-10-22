#!/usr/bin/env python3
"""
    Copyright 2016 Alaa Salman <alaa@codedemigod.com>
    
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""

import sys
import glob
import os
import os.path
import pprint

from PyPDF2 import PdfFileWriter, PdfFileReader


def main(argv):
    full_path = os.path.abspath(argv[1])
    output_file_name = os.path.join(full_path, 'fullBook.pdf')
    print('Looking at %s' % full_path)
    
    output_pdf = PdfFileWriter()

    pdf_list = glob.glob(os.path.join(full_path, '*.pdf'))
    sorted_pdf_list = sorted(pdf_list, key=lambda fname: fname[:-4])

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(sorted_pdf_list)

    for chapPdf in sorted_pdf_list:
        pdf_input = PdfFileReader(open(chapPdf, 'rb'))
        for i in range(pdf_input.getNumPages()):
            output_pdf.addPage(pdf_input.getPage(i))

    # finally, write 'output' to document-output.pdf
    output_stream = open(output_file_name, 'wb')
    output_pdf.write(output_stream)
    output_stream.close()


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Supply directory as argument')
        sys.exit()
    
    main(sys.argv)
