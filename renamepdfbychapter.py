#! /usr/bin/env python3
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

import os
import os.path
from subprocess import Popen, PIPE
import glob
import sys
import re
import shutil


def main(argv):
    fullpath = os.path.abspath(argv[1])
    print('Looking at %s' % fullpath)
    
    for fileName in glob.glob(os.path.join(fullpath, '*.pdf')):
        try:
            full_file_name = os.path.join(fullpath, fileName)
            print('Converting %s' % full_file_name)

            p_open_cls = Popen(('/usr/bin/pdftotext', full_file_name, "-"), stdout=PIPE)
            convert_out = p_open_cls.stdout
            
            title_content = b''

            for i in range(1, 6):
                title_content += convert_out.readline()

            title_content = title_content.replace(b'\n', b'')
            
            digit_search = re.search(b'\d+', title_content)
            
            if digit_search is not None:
                new_chapter_pdf = os.path.join(fullpath, digit_search.group(0).decode('utf-8') + '.pdf')

                while os.path.exists(new_chapter_pdf):
                    new_chapter_pdf += 'dup.pdf'
                
                shutil.move(full_file_name, new_chapter_pdf)

            else:
                print('File is not a chapter, checking if front or back')
                if fileName.find("front") != -1:
                    first_pdf = os.path.join(fullpath, '0.pdf')

                    while os.path.exists(first_pdf):
                        first_pdf += '0.pdf'
                    
                    shutil.move(full_file_name, first_pdf)

                elif fileName.find('back') != -1:
                    last_pdf = os.path.join(fullpath, '9999.pdf')

                    while os.path.exists(last_pdf):
                        last_pdf += '9.pdf'

                    shutil.move(full_file_name, last_pdf)

        except OSError as ex:
            print(ex)
            print('Failed', full_file_name)


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Supply directory as argument')
        sys.exit()
    main(sys.argv)
