#!/usr/bin/env python3

import os
import platform
import shutil

from file import File
from image import Picture
from zhidao_article import ZhiDao

abs_path = os.getcwd() + os.sep
book_name = '投资知道（上部）'
author = '整理发布：Andy'
file_name = book_name + '.mobi'
temp_path = abs_path + os.sep + 'temp' + os.sep

img_dir = temp_path + 'images/'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

# 封面图片 标题 & 副标题
image = Picture()
image.cover(book_name, author, './images/cover.jpg', img_dir + 'cover.jpg')

# 复制默认图片（占位文章中图片链接失效获取不到的图片）
shutil.copyfile(abs_path + os.sep + 'images/0.png', img_dir + '0.png')

# 获取文章（文章模型）
articles = ZhiDao(temp_path).get_article()

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
