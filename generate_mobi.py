import os
import platform
import shutil

import file

abs_path = os.getcwd()
main_url = 'https://mp.weixin.qq.com/s/cf1qc0qfeivEBPGIAmsaGA'
book_name = 'L先生说'

book_path = abs_path + os.sep + 'book' + os.sep
images = abs_path + os.sep + 'images'
book_images = book_path + 'images'

urls = file.get_url(main_url)
file.out_file(urls, book_path, book_name)

shutil.copytree(images, book_images)

if 'Windows' in platform.platform():
    os.system(abs_path + '/windows-kindlegen/kindlegen.exe ' + path + 'book.opf')
