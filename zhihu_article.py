import bs4
import requests

from article import Article


class ZhiHu(Article):

    def __init__(self, path):
        self.root_path = path

    def get_url(self):
        urls = []
        for num in range(1, 3):
            url = 'https://www.zhihu.com/collection/30519333?page=' + str(num)
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, "html5lib")
            for a in soup.select('div.terms a[href^=/question/]'):
                link = a.attrs.get('href')
                urls.append(link)
            print(num)
            break
        return urls

    def get_article(self):
        urls = self.get_url()
        articles = []
        i = 0
        for url in urls:
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, "html5lib")

            # 删除无用标签：br
            [s.extract() for s in soup('br')]

            # 匹配标题，去除首尾空白
            title = soup.select('div.entry-name span')[0].get_text().strip()

            # 文章简述
            entry_desc = soup.find("div", class_="entry-desc").contents
            desc_text = []
            for line in entry_desc:
                if str(line.string) == 'None':
                    continue
                desc_text.append(str(line))
            body = ''.join(desc_text).strip()

            # 处理文章主体。
            entry_explanation = soup.find("div", class_="entry-explanation")
            if entry_explanation:
                entry_explanation = entry_explanation.contents
                body = body + '\n' + Article().article_body(entry_explanation, self.root_path + '/images')

            articles.append([title, body, url])
            i += 1
            print(i)
            print(url)
            # break
        return articles
