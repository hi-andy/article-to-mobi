import bs4
import requests

from article import Article


class ZhiHu(Article):

    def __init__(self, path):
        self.root_path = path
        self.headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Safari/537.36'
        }

    def get_url(self):

        urls = []
        # 文章列表页页码范围：此处共 2 页
        for num in range(1, 3):
            url = 'https://www.zhihu.com/collection/30519333?page=' + str(num)
            response = requests.get(url, headers=self.headers)
            soup = bs4.BeautifulSoup(response.text, "html5lib")
            for a in soup.select('h2.zm-item-title a[href^=/question/]'):
                link = a.attrs.get('href')
                urls.append(link)
            print(num)
            # break
        return urls

    def get_article(self):
        urls = self.get_url()
        articles = []
        i = 0
        for url in urls:
            url = 'https://www.zhihu.com' + url

            i += 1
            print('文章{0}：{1}'.format(i, url))

            response = requests.get(url, headers=self.headers)
            response.encoding = 'utf-8'
            soup = bs4.BeautifulSoup(response.text, "html5lib")

            # 删除无用标签：br。有的文章排版此标签不可删除。
            # [s.extract() for s in soup('br')]

            # 匹配标题，去除首尾空白
            title = soup.select('h1.QuestionHeader-title')[0].get_text().strip()

            # 处理文章主体。
            body = ''
            div = soup.find_all("div", class_="RichContent-inner")
            if div:
                article = div[0].contents
                body = Article().article_body(article, self.root_path + '/images')

            articles.append([title, body, url])

            # break
        return articles
