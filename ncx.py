def out_ncx(path, book_name, ncx_item):
    # 生成 ncx
    with open(path + 'toc.ncx', 'a', encoding='utf-8') as f:
        f.write('<?xml version="1.0"　encoding="UTF-8"?>\n\
    <!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n\
    <ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n\
    <head>\n\
    </head>\n\
    <docTitle>\n\
        <text>{0}</text>\n\
    </docTitle>\n\
    <navMap>\n\
        <navPoint id="navpoint-1" playOrder="1">\n\
            <navLabel>\n\
                <text>Content</text>\n\
            </navLabel>\n\
            <content src="toc.html#toc"/>\n\
        </navPoint>\n\
        {1}\
    </navMap >\n\
    </ncx>\n'.format(book_name, ncx_item))
