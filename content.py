def out_content(path, content_item):
    # 生成目录文件
    with open(path + 'toc.html', 'a', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n\
    <html xmlns="http://www.w3.org/1999/xhtml">\n\
    <head>\n\
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n\
    <title>目录</title>\n\
    </head>\n\
    <body>\n\
    <h1 id="toc">文章目录</h1>\n\
        <ul>\n\
            {0}\
        </ul>\n\
    </body>\n\
    </html>'.format(content_item))
