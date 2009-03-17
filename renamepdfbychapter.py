#! /usr/bin/python
import os
import os.path
from subprocess import Popen, PIPE
import glob
import sys
import re
import shutil

def main(argv):
    fullPath = os.path.abspath(argv[1])
    print "Looking at %s" % fullPath
    
    for fileName in glob.glob(os.path.join(fullPath, '*.pdf')):
        try:
            fullFileName = os.path.join(fullPath, fileName)
            print "Converting %s" % fullFileName

            pOpenCls = Popen(("/usr/bin/pdftotext", fullFileName, "-"), stdout=PIPE)
            convertOut = pOpenCls.stdout
            
            titleContent = ""

            for i in xrange(1, 6):
                titleContent += convertOut.readline()

            titleContent = titleContent.replace('\n', '')
            
            digitSearch = re.search('\d+', titleContent)
            
            if digitSearch != None:
                newChapterPdf = os.path.join(fullPath, digitSearch.group(0) + ".pdf")

                while os.path.exists(newChapterPdf):
                    newChapterPdf = newChapterPdf + "dup.pdf"
                
                shutil.move(fullFileName, newChapterPdf)

            else:
                print "File is not a chapter, checking if front or back"
                if fileName.find("front") != -1:
                    firstPdf = os.path.join(fullPath, "0.pdf")

                    while os.path.exists(firstPdf):
                        firstPdf = firstPdf + "0.pdf"
                    
                    shutil.move(fullFileName, firstPdf)

                elif fileName.find("back") != -1:
                    lastPdf = os.path.join(fullPath, "9999.pdf")

                    while os.path.exists(lastPdf):
                        lastPdf = lastPdf + "9.pdf"

                    shutil.move(fullFileName, lastPdf)

        except OSError, ex:
            print ex
            print 'Failed', fullFileName


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Supply directory as argument"
        sys.exit()
    main(sys.argv)
