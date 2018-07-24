## 说明：
    抓取微信公众号文章，生成 `mobi` 格式电子书。主要便于导入 Kindle 阅读查看。
    系统支持 macOS 和 windows。已测：windows 10 专业版 & macOS High Sierra 10.13.5
    images: 图书封面文件夹。要替换生成电子书封面，可替换此文件夹下同名文件。需注意图片宽高比。
## 使用 （修改 generate_mobi.py 文件）：
    修改 book_name：电子书名称，Kindle 阅读时显示。
    修改 from xxx_article import XXX 导入的文章模型
    修改 articles = XXX(temp_path).get_article() 获取文章的模型

    若要获取其它站点的信息，需依照实现 xxx_article.py 文章模型。在使用的时候也需要注意相应模型的内部实现，修改相应的 url 处理方式。

    示例 URL: https://mp.weixin.qq.com/s/cf1qc0qfeivEBPGIAmsaGA
