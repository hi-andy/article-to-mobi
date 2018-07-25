#!/usr/bin/env python3

import os
import platform
import shutil

from file import File
from zhihu_article import ZhiHu

abs_path = os.getcwd() + os.sep
book_name = '知乎-财务包子铺'
file_name = book_name + '.mobi'

temp_path = abs_path + os.sep + 'temp' + os.sep

# 复制图书封面
cover = abs_path + os.sep + 'cover'
booK_cover = temp_path + 'cover'
if not os.path.exists(booK_cover):
    shutil.copytree(cover, booK_cover)

# 复制默认图片（有的图片链接失效，获取不到）
default_img = abs_path + os.sep + 'images'
img_dir = temp_path + 'images'
if not os.path.exists(img_dir):
    shutil.copytree(default_img, img_dir)

# 获取文章（文章模型）
articles = ZhiHu(temp_path).get_article()

# 输出文件
File().out_mobi(temp_path, book_name, articles)

# 生成 mobi 文件
if 'Windows' == platform.system():
    os.system(abs_path + 'windows-kindlegen' + os.sep + 'kindlegen.exe ' + temp_path + book_name + '.opf')
elif 'Darwin' == platform.system():
    os.system(abs_path + 'macOS-kindlegen' + os.sep + 'kindlegen ' + temp_path + book_name + '.opf')
else:
    print('Not supported OS type.')

# 创建成功，移除临时文件，也可注释掉最后一行，保留临时文件。
if os.path.exists(temp_path + file_name):
    shutil.move(temp_path + file_name, abs_path)
    # shutil.rmtree(temp_path)
