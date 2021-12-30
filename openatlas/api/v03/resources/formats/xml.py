from typing import Any, Dict, List, Union

import dicttoxml


def subunit_xml(
        out: Union[List[Dict[str, Any]], Dict[str, Any]]) -> bytes:
    out = transform_output(out)
    xml = dicttoxml.dicttoxml(
        out,
        root=False,
        attr_type=False)
    xml = xml.replace(b'<item >', b'')
    xml = xml.replace(b'<item>', b'')
    xml = xml.replace(b'</item>', b'')
    return xml


def transform_output(out: Dict[str, Any]) -> Dict[str, Any]:
    item_list = []
    new_dict = {}
    for key, value in out.items():
        item_list.append({item['openatlasClassName']: item} for item in value)
        new_dict[key] = item_list
    return new_dict
