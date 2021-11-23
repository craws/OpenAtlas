from typing import Any, Dict
from xml.dom.minidom import parseString

import dicttoxml


def subunit_xml(out: Dict[str, Any], parser: Dict[str, Any]):
    # https://stackoverflow.com/questions/5236296/how-to-convert-list-of-dict-to-dict
    # https://github.com/quandyfactory/dicttoxml

    #print(out)
    out = transform_output(out)

    xml = dicttoxml.dicttoxml(
        out,
        root=False,
        attr_type=False,
    )
    # print(xml)
    # dom = parseString(xml)
    # print(dom.toprettyxml())

    xml = xml.replace(b'<item >', b'')
    xml = xml.replace(b'<item>', b'')
    xml = xml.replace(b'</item>', b'')
    return xml


def transform_output(out: Dict[str, Any]) -> Dict[str, Any]:
    new_dict = {}
    for k, v in out.items():
        subunits = {f"n{item['id']}":item for item in v}
        new_dict[k] = subunits

    return new_dict
