from typing import Any, Union

import dicttoxml


def subunit_xml(out: dict[str, Any]) -> bytes:
    item_list = []
    new_dict = {}
    for key, value in out.items():
        item_list.append({item['openatlasClassName']: item} for item in value)
        new_dict[key] = item_list
    xml = dicttoxml.dicttoxml(
        new_dict,
        root=False,
        attr_type=False)
    xml = xml.replace(b'<item >', b'')
    xml = xml.replace(b'<item>', b'')
    xml = xml.replace(b'</item>', b'')
    return xml


