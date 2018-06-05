## 说明
    抓取微信公众号文章，生成 `mobi` 格式电子书。主要便于导入 Kindle 阅读查看。
    images: 图书封面文件夹。要替换生成电子书封面，可替换此文件夹下同名文件。注意图片宽高比。
## 使用:
    依次传递相关参数：
        电子书名称：Kindle 阅读时显示
        URL: 要抓取的文章 url 地址,　可以是一个文章 URL 列表.　示例 URL: https://mp.weixin.qq.com/s/cf1qc0qfeivEBPGIAmsaGA
    
    运行：python3 generate_mobi.py 电子书名称　文章URL
        执行成功会在当前目录生成　`book.mobi` 文件。