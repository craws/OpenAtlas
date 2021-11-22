from xml.dom.minidom import parseString

import dicttoxml


def subunit_xml(out, parser, file_name):
    print(out)
    xml = dicttoxml.dicttoxml(
        out,
        root=False,
        attr_type=False,
    )
    # print(xml)
    # dom = parseString(xml)
    # print(dom.toprettyxml())
    return xml
