import re

import bs4
import requests

from article import Article


class WeChat(Article):

    def __init__(self, url, path):
        self.main_url = url
        self.root_path = path

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
            title = soup.select('h2.rich_media_title')[0].get_text()
            title = re.sub('\s+', '', title)
            # 如果标题出问题打开下面一条注释，多匹配一次。
            # title = re.match(r'.*document\.write\("(.*)"\);}$', js_title).group(1)

            # 匹配作者
            author = re.sub('\s+', '', soup.select('span#profileBt a')[0].get_text())

            # 发布时间
            publish_time = 000
            # body = soup.select('div.rich_media_content ')[0].get_text().strip()
            # body = soup.find_all("div", attrs={"class": "rich_media_content"}) # get list

            misc_body = soup.find_all("div", class_="rich_media_content")[0].contents

            # 文章主题
            body = Article.article_body(misc_body, self.root_path + '/images')

            articles.append([title, body, author, publish_time, url])
            # break
        return articles
