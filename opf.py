def out_opf(path, book_name, opf_item, opf_itemref):
    # 生成 opf 文件
    with open(path + 'book.opf', 'a', encoding='utf-8') as f:
        f.write('<?xml version="1.0" encoding="UTF-8"?>\n\
    <package unique-identifier="uid" xmlns:opf="http://www.idpf.org/2007/opf" xmlns:asd="http://www.idpf.org/asdfaf">\n\
    <metadata>\n\
        <dc-metadata  xmlns:dc="http://purl.org/metadata/dublin_core" xmlns:oebpackage="http://openebook.org/namespaces/oeb-package/1.0/">\n\
            <dc:Title>{0}</dc:Title>\n\
            <dc:Language>zh</dc:Language>\n\
            <dc:Creator>Andy</dc:Creator>\n\
            <dc:Copyrights>文章版权归原作者所有</dc:Copyrights>\n\
            <dc:Publisher>Andy</dc:Publisher>\n\
            <x-metadata>\n\
                <EmbeddedCover>images/cover.jpg</EmbeddedCover>\n\
            </x-metadata>\n\
        </dc-metadata>\n\
    </metadata>\n\
    <manifest>\n\
        <item id="content" media-type="text/x-oeb1-document" href="toc.html"></item>\n\
        <item id="ncx" media-type="application/x-dtbncx+xml" href="toc.ncx"/>\n\
        {1}\n\
    </manifest>\n\
    <spine toc="ncx">\n\
        <itemref idref="content"/>\n\
        {2}\n\
    </spine>\n\
    <guide>\n\
        <reference type="toc" title="目录" href="toc.html"/>\n\
    </guide>\n\
    </package>'.format(book_name, opf_item, opf_itemref))
