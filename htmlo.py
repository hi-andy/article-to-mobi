def out_html(path, full_file_name, title, body):
    # 每篇文章，单独一个文件
    with open(path + full_file_name, 'w', encoding='utf-8') as f:
        f.write('<!DOCTYPE html>\n\
    <html xmlns="http://www.w3.org/1999/xhtml">\n\
    <head>\n\
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n\
    <title>{0}</title>\n\
    </head>\n\
    <body>\n\
        <h2>{1}</h2>\n\
        {2}\n\
    </body>\n\
    </html>\n'.format(title, title, body))
