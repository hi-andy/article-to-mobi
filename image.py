import imghdr
import os
import random
import re

import cairosvg
import requests
from PIL import Image, ImageDraw, ImageFont
from requests import exceptions


class Picture(object):

    # 保存插图
    def save(self, img_url, path='./images'):

        if not os.path.exists(path):
            os.makedirs(path)

        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

        try:
            r = requests.get(img_url, stream=True, headers=headers)
            if r.status_code != 200:
                return '0.png'

            match = re.search('.*/(\.(png|jpg|gif|jpeg|bmp))', img_url)  # 原始图片文件名
            if match is not None:
                file_name = self.random_string(25) + match.group(1)
            else:
                if r.headers['content-type'] == 'image/svg+xml':  # svg 转 png 保存
                    file_name = self.random_string(25) + '.png'
                    file_path = re.sub('/|\\\\', os.sep, path) + '/' + file_name
                    cairosvg.svg2png(bytestring=r.text, write_to=file_path)
                    return file_name
                else:
                    file_name = self.random_string(25) + '.' + imghdr.what(img_url, r.content)  # 生成文件名 + 探测到的文件扩展名。

            file_path = re.sub('/|\\\\', os.sep, path) + '/' + file_name

            try:
                with open(file_path, "wb") as file:
                    file.write(r.content)
                return file_name
            except IOError as e:
                print('保存图片失败：', e)
            except Exception as e:
                print('错误 ：', e)

        except exceptions.HTTPError as e:
            return '0.png'
        except exceptions.ConnectionError as e:
            return '0.png'

    # 封面图片添加标题 & 副标题。
    def cover(self, title, subtitle, source, distination):
        img = Image.open(source)
        (img_w, img_h) = img.size

        title_font = ImageFont.truetype('./fonts/Baoli.ttc', int(img_h / 16))
        subtitle_font = ImageFont.truetype('./fonts/Baoli.ttc', int(img_h / 25))

        draw = ImageDraw.Draw(img)

        title_w, title_h = draw.textsize(title, font=title_font)
        subtitle_w, subtitle_h = draw.textsize(subtitle, font=subtitle_font)

        draw.text(((img_w - title_w) / 2, (img_h - title_h) / 9), title, (255, 255, 255), font=title_font)
        draw.text(((img_w - subtitle_w) / 2, (img_h - subtitle_h) / 1.15), subtitle, (255, 255, 255), font=subtitle_font)

        img.save(distination, 'jpeg')

    def random_string(self, length=8):

        # seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!@#$%^&*()_+=-"
        seed = "1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ_-"
        sa = []
        for i in range(length):
            sa.append(random.choice(seed))
        return ''.join(sa)
