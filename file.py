import os
import re

import bs4
import requests

import content
import htmlo
import ncx
import opf

headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
}


def get_url(main_url):
    response = requests.get(main_url)
    soup = bs4.BeautifulSoup(response.text, "html5lib")
    return [a.attrs.get('href') for a in soup.select('ul.list-paddingleft-2 a[href^=http://mp.weixin.qq.com/s?]')]


def get_article(article_url):
    response = requests.get(article_url)
    soup = bs4.BeautifulSoup(response.text, "html5lib")

    # 删除看似无用的标签：section img
    [s.extract() for s in soup('section')]
    [s.extract() for s in soup('img')]

    # 匹配标题，去除首尾空白
    rough_title = soup.select('h2.rich_media_title')[0].get_text()
    js_title = re.sub('\s+', '', rough_title)
    title = re.match(r'.*document\.write\("(.*)"\);}$', js_title).group(1)
    # 匹配作者
    author = re.sub('\s+', '', soup.select('span#profileBt a')[0].get_text())
    # 发布时间
    publish_time = 000
    # body = soup.select('div.rich_media_content ')[0].get_text().strip()
    # body = soup.find_all("div", attrs={"class": "rich_media_content"}) # get list

    misc_body = soup.find_all("div", class_="rich_media_content")[0].contents

    # 文章主题. 去除空白行，并且拼接。
    body = ''
    for line in misc_body:
        tag = re.match('<p\s*.*?>(.*)?</p>', str(line))
        if str(tag) != 'None':
            if tag.group(1) == '<br/>' or tag.group(1) == '':
                continue
            else:
                tag2 = re.match('<span\s*.+?>(.*)?</span>', str(tag.group(1)))
                if str(tag2) != 'None':
                    if tag2.group(1) == '<br/>' or tag2.group(1) == '':
                        continue

        # 去除所有内联样式，原有样式在 Kindle 表现不佳。
        line = re.sub('\s*?style="\s*.+?"', '', str(line))
        body += str(line) + '\n'

    body = body.strip()

    article = (title, body, author, publish_time, article_url)
    return article


def out_file(urls, path, book_name):
    opf_item = ''
    opf_itemref = ''
    ncx_item = ''
    content_item = ''

    if not os.path.exists(path):
        os.makedirs(path)

    for key, url in enumerate(urls):
        article = get_article(url)
        index = key + 1
        file_name = 'article%s' % index
        full_file_name = 'article%s.html' % index
        title = article[0]
        body = article[1]

        htmlo.out_html(path, full_file_name, title, body)

        # opf 列表
        opf_item += '\t<item id="{0}" media-type="text/x-oeb1-document" href="{1}"></item>'.format(file_name, full_file_name) + '\n'
        opf_itemref += '\t<itemref idref="%s"/>' % file_name + '\n'

        # 目录列表
        content_item += '\t\t<li><a href="{0}">{1}</a></li>'.format(full_file_name, title) + '\n'

        # ncx 列表
        ncx_item += '\t\t\t<navPoint id="navpoint-{0}" playOrder="{1}">\n\
                <navLabel>\n\
                    <text>{2}</text>\n\
                </navLabel>\n\
                <content src="{3}"/>\n\
            </navPoint>'.format((index + 1), (index + 1), title, full_file_name) + '\n'

    content.out_content(path, content_item)
    ncx.out_ncx(path, book_name, ncx_item)
    opf.out_opf(path, book_name, opf_item, opf_itemref)
