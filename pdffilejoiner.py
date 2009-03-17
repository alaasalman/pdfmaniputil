#!/usr/bin/python
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
    print "Looking at %s" % fullPath
    
    outputPDF = PdfFileWriter()

    pdfList = glob.glob(os.path.join(fullPath, '*.pdf'))
    sortedPdfList = sorted(pdfList, compareByActualNumbers)

    pp = pprint.PrettyPrinter(indent=2)
    pp.pprint(sortedPdfList)

    for chapPdf in sortedPdfList:
        pdfInput = PdfFileReader(file(chapPdf, "rb"))
        for i in xrange(pdfInput.getNumPages()):
            outputPDF.addPage(pdfInput.getPage(i))

    # finally, write "output" to document-output.pdf
    outputStream = file(outputFileName, "wb")
    outputPDF.write(outputStream)
    outputStream.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Supply directory as argument"
        sys.exit()
    
    main(sys.argv)
