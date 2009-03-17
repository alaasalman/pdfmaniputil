from pyPdf import PdfFileWriter, PdfFileReader
import os

for fileName in os.listdir('.'):
    try:
        if fileName.lower()[-3:] != "pdf": continue
        input1 = PdfFileReader(file(fileName, "rb"))
   
        pdfTitle = input1.getDocumentInfo().title

        if pdfTitle is not None and len(pdfTitle) > 2:
            print '##1', fileName, ': ', pdfTitle

        pdfText = input1.getPage(0).extractText()
        print fileName
        print pdfText[0:50]

    except:
        print 'Failed', fileName
