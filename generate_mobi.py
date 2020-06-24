#!/usr/bin/env python3

import os
import platform
import shutil

from file import File
from image import Picture
from wechat_article import WeChat


# 生成 mobi 文件
def create_mobi():
    if 'Windows' == platform.system():
        os.system(abs_path + 'windows-kindlegen' + os.sep + 'kindlegen.exe ' + temp_path + book_name + '.opf')
    elif 'Darwin' == platform.system():
        os.system(abs_path + 'macOS-kindlegen' + os.sep + 'kindlegen64 ' + temp_path + book_name + '.opf')
    else:
        print('Not supported OS type.')

    # 创建成功，移除临时文件，也可注释掉最后一行，保留临时文件。
    if os.path.exists(temp_path + file_name):
        shutil.move(temp_path + file_name, abs_path)
        shutil.rmtree(temp_path)


# ################################## 定义图书信息
book_name = '架构师之路16年精选50篇'  # 书名
author = '整理发布：Andy'  # 作者
file_name = book_name + '.mobi'  # 图书文件名

abs_path = os.getcwd() + os.sep
temp_path = abs_path + 'temp' + os.sep

img_dir = temp_path + 'images/'
if not os.path.exists(img_dir):
    os.makedirs(img_dir)

# 图书封面图片，并添加标题 & 副标题到封面图片
image = Picture()
image.cover(book_name, author, './images/cover.jpg', img_dir + 'cover.jpg')

# 复制默认图片（占位文章中插图，链接失效获取不到的插图）
shutil.copyfile(abs_path + os.sep + 'images/0.png', img_dir + '0.png')

# 获取文章（文章模型）
url = 'https://mp.weixin.qq.com/s?__biz=MjM5ODYxMDA5OQ==&mid=2651959886&idx=1&sn=03e45a5014053607eff5e55ed2c660d7&chksm=bd2d07928a5a8e8454d395e176fa9d346682abfe9dfbf3244f1dead83ee4508aa25121f9b811&scene=21#wechat_redirect'

url1 = 'https://mp.weixin.qq.com/s/cf1qc0qfeivEBPGIAmsaGA'

articles = WeChat(url, temp_path).get_article()

# 输出文件
File().out_files(temp_path, book_name, articles)

# 创建电子书
create_mobi()
