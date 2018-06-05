import re

import bs4
import requests


class Article(object):
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.62 Safari/537.36"
    }

    def __init__(self, url):
        self.main_url = url

    def get_url(self, main_url):
        response = requests.get(main_url)
        soup = bs4.BeautifulSoup(response.text, "html5lib")
        urls = [a.attrs.get('href') for a in soup.select('ul.list-paddingleft-2 a[href^=http://mp.weixin.qq.com/s?]')]
        if not urls:
            urls = [main_url]
        return urls

    def get_article(self):
        urls = self.get_url(self.main_url)
        articles = []
        for url in urls:
            response = requests.get(url)
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
            articles.append([title, body, author, publish_time, url])
            # break
        return articles
