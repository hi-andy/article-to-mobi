from PIL import Image, ImageDraw, ImageFont

img = Image.open('./cover/cover.jpg')
(img_w, img_h) = img.size

title_font = ImageFont.truetype('./fonts/Baoli.ttc', int(img_h / 16))
author_font = ImageFont.truetype('./fonts/Baoli.ttc', int(img_h / 25))

draw = ImageDraw.Draw(img)
title = '知乎 - 财务包子铺'
author = '整理发布：Andy'

title_w, title_h = draw.textsize(title, font=title_font)
author_w, author_h = draw.textsize(author, font=author_font)

draw.text(((img_w - title_w) / 2, (img_h - title_h) / 9), title, (255, 255, 255), font=title_font)
draw.text(((img_w - author_w) / 2, (img_h - author_h) / 1.15), author, (255, 255, 255), font=author_font)

img.save('./images/cover.jpg', 'jpeg')
