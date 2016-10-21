#!/usr/bin/env python
""" 
    Copyright 2010 Alaa Salman <alaa@codedemigod.com>
    
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
from pyPdf import PdfFileWriter, PdfFileReader

def compareByActualNumbers(x, y):
    strippedX = os.path.basename(x)[:-4]
    strippedY = os.path.basename(y)[:-4]

    if not (strippedX.isdigit() and strippedY.isdigit()):
        return 0

    xInt = int(strippedX)
    yInt = int(strippedY)

    if xInt < yInt:
        return -1
    elif xInt == yInt:
        return 0
    elif xInt > yInt:
        return 1

def main(argv):
    fullPath = os.path.abspath(argv[1])
    outputFileName = os.path.join(fullPath, "fullBook.pdf")
    print("Looking at %s" % fullPath)
    
    outputPDF = PdfFileWriter()

    pdfList = glob.glob(os.path.join(fullPath, '*.pdf'))
    sortedPdfList = sorted(pdfList, compareByActualNumbers)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(sortedPdfList)

    for chapPdf in sortedPdfList:
        pdfInput = PdfFileReader(open(chapPdf, "rb"))
        for i in range(pdfInput.getNumPages()):
            outputPDF.addPage(pdfInput.getPage(i))

    # finally, write "output" to document-output.pdf
    outputStream = open(outputFileName, "wb")
    outputPDF.write(outputStream)
    outputStream.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Supply directory as argument")
        sys.exit()
    
    main(sys.argv)
