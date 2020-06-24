import os


class File(object):

    def out_files(self, path, book_name, articles):

        opf_item = []
        opf_itemref = []
        ncx_item = []
        content_item = []

        if not os.path.exists(path):
            os.makedirs(path)

        for key, article in enumerate(articles):
            index = key + 1
            file_name = 'article%s' % index
            full_file_name = 'article%s.html' % index

            # 使用文章标题（中文）作为文件名，考虑到索引性能可能不会太好，也暂时没有必要这样做。
            # file_name = article[0]
            # full_file_name = article[0] + '.html'

            title = article[0]
            body = article[1]

            self.out_html(path, full_file_name, title, body)

            # opf 列表
            opf_item.append('\t<item id="{0}" media-type="text/x-oeb1-document" href="{1}"></item>\n'.format(file_name,
                                                                                                             full_file_name))
            opf_itemref.append('\t<itemref idref="%s"/>\n' % file_name)

            # 目录列表
            content_item.append('\t\t<li><a href="{0}">{1}</a></li>\n'.format(full_file_name, title))

            # ncx 列表
            ncx_item.append('\t<navPoint id="navpoint-{0}" playOrder="{1}">\n'
                            '\t\t<navLabel>\n'
                            '\t\t\t<text>{2}</text>\n'
                            '\t\t</navLabel>\n'
                            '\t\t<content src="{3}"/>\n'
                            '\t</navPoint>\n'.format((index + 1), (index + 1), title, full_file_name))

        self.out_content(path, ''.join(content_item))
        self.out_ncx(path, book_name, ''.join(ncx_item))
        self.out_opf(path, book_name, ''.join(opf_item), ''.join(opf_itemref))

    # 生成 ncx
    def out_ncx(self, path, book_name, ncx_item):
        with open(path + 'toc.ncx', 'a', encoding='utf-8') as f:
            f.write('<?xml version="1.0"　encoding="UTF-8"?>\n'
                    '<!DOCTYPE ncx PUBLIC "-//NISO//DTD ncx 2005-1//EN" "http://www.daisy.org/z3986/2005/ncx-2005-1.dtd">\n'
                    '<ncx xmlns="http://www.daisy.org/z3986/2005/ncx/" version="2005-1">\n'
                    '<head>\n'
                    '</head>\n'
                    '<docTitle>\n'
                    '\t<text>{0}</text>\n'
                    '</docTitle>\n'
                    '<navMap>\n'
                    '\t<navPoint id="navpoint-1" playOrder="1">\n'
                    '\t\t<navLabel>\n'
                    '\t\t\t<text>目录</text>\n'
                    '\t\t</navLabel>\n'
                    '\t\t<content src="toc.html"/>\n'
                    '\t</navPoint>\n'
                    '{1}'
                    '</navMap >\n'
                    '</ncx>\n'.format(book_name, ncx_item))

    # 生成 opf 文件
    def out_opf(self, path, book_name, opf_item, opf_itemref):
        with open(path + book_name + '.opf', 'a', encoding='utf-8') as f:
            f.write('<?xml version="1.0" encoding="UTF-8"?>\n'
                    '<package unique-identifier="uid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:asd="http://www.idpf.org/asdfaf">\n'
                    '<metadata>\n'
                    '<dc-metadata xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">\n'
                    '\t<dc:Title>{0}</dc:Title>\n'
                    '\t<dc:Language>zh</dc:Language>\n'
                    '\t<dc:Creator>Andy</dc:Creator>\n'
                    '\t<dc:Copyrights>文章版权归原作者所有</dc:Copyrights>\n'
                    '\t<dc:Publisher>Andy</dc:Publisher>\n'
                    '\t<x-metadata>\n'
                    '\t\t<EmbeddedCover>images/cover.jpg</EmbeddedCover>\n'
                    '\t</x-metadata>\n'
                    '</dc-metadata>\n'
                    '</metadata>\n'
                    '<manifest>\n'
                    '\t<item id="content" media-type="text/x-oeb1-document" href="toc.html"></item>\n'
                    '\t<item id="ncx" media-type="application/x-dtbncx+xml" href="toc.ncx"/>\n'
                    '{1}'
                    '</manifest>\n'
                    '<spine toc="ncx">\n'
                    '\t<itemref idref="content"/>\n'
                    '{2}'
                    '</spine>\n'
                    '<guide>\n'
                    '\t<reference type="toc" title="目录" href="toc.html"/>\n'
                    '</guide>\n'
                    '</package>'.format(book_name, opf_item, opf_itemref))

    # 生成目录文件
    def out_content(self, path, content_item):
        with open(path + 'toc.html', 'a', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n'
                    '<html xmlns="http://www.w3.org/1999/xhtml">\n'
                    '<head>\n'
                    '\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
                    '\t<title>目录</title>\n'
                    '</head>\n'
                    '<body>\n'
                    '\t<h1>文章目录</h1>\n'
                    '\t<ul>\n'
                    '{0}'
                    '\t</ul>\n'
                    '</body>\n'
                    '</html>'.format(content_item))

    # 每篇文章，单独一个文件
    def out_html(self, path, full_file_name, title, body):
        with open(path + full_file_name, 'w', encoding='utf-8') as f:
            f.write('<!DOCTYPE html>\n'
                    '<html xmlns="http://www.w3.org/1999/xhtml">\n'
                    '<head>\n'
                    '\t<meta http-equiv="Content-Type" content="text/html; charset=utf-8">\n'
                    '\t<title>{0}</title>\n'
                    '</head>\n'
                    '<body>\n'
                    '\t<h2>{1}</h2>\n'
                    '\t{2}\n'
                    '</body>\n'
                    '</html>\n'.format(title, title, body))
