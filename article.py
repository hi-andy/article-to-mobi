import re

from image import Picture


class Article(object):

    def article_body(self, body, image_path):
        image = Picture()
        list_body = []
        for line in body:

            line = str(line).strip()

            # 先把 img 标签的 src 取出。然后去除所有标签属性、内联样式
            # 因为原有样式在 Kindle 表现不佳，并且生成电子书的时候可能会有警告（line-height)。
            # 若要改变书的排版布局，也可以在此为指定的标签添加自己的样式：class,id。然后再定义自己的 css 文件即可。
            src = re.search('<img\s+?.*?src="(\s*.+?)?"', line)
            line = re.sub('(\s+?[\w\-*\w*]+?=".+?")+?', '', line)

            # 保存插图到本地
            if src is not None:
                print('原始图片：' + src.group(1))
                print('本地图片地址：' + image.save(src.group(1), image_path))
                local_src = './images/' + image.save(src.group(1), image_path)  # 返回保存的文件名
                line = re.sub('<img.*?>', '<img src="' + local_src + '" style="display:block;"/>', line)

            # 去除空的 img 标签。
            line = re.sub('<img/?>', '', line)

            # 去除空的 strong 标签。
            line = re.sub('<strong>\s*</strong>', '', line)

            # 去除空的 b 标签。
            line = re.sub('<b>\s*</b>', '', line)

            # 去除空的 span 标签。
            line = re.sub('<span>\s*</span>', '', line)

            # 去除空的 p 标签。
            line = re.sub('<p>\s*</p>', '', line)

            # 去除空的 div 标签。
            line = re.sub('<div>\s*</div>', '', line)

            if line == '':
                continue

            list_body.append(line + '\n')
        return ''.join(list_body).strip()
