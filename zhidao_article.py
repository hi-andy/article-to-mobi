import bs4
import requests

from article import Article


class ZhiDao(Article):

    def __init__(self, path):
        self.root_path = path

    def get_url(self):
        urls = []
        for num in range(18, 35):
            url = 'http://zhidao.agutong.com/entries?page=' + str(num)
            response = requests.get(url)
            soup = bs4.BeautifulSoup(response.text, "html5lib")
            for a in soup.select('div.terms a[href^=/entries/]'):
                link = a.attrs.get('href')
                urls.append(link)
            print(num)
            # break
        return urls

    def get_article(self):
        urls = self.get_url()
        # urls = ['http://zhidao.agutong.com/entries/56853188a2b470000df8a258']
        articles = []
        i = 0
        for url in urls:
            url = 'http://zhidao.agutong.com' + url

            i += 1
            print('文章{0}：{1}'.format(i, url))

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
                line = str(line).strip()
                if line == '':
                    continue
                desc_text.append(line)
            body = ''.join(desc_text).strip()

            # 处理文章主体。
            entry_explanation = soup.find("div", class_="entry-explanation")
            if entry_explanation:
                entry_explanation = entry_explanation.contents
                body = body + '\n' + Article().article_body(entry_explanation, self.root_path + '/images')

            articles.append([title, body, url])
            # break
        return articles
