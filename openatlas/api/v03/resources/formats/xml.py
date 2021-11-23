from typing import Any, Dict

import dicttoxml


def subunit_xml(out: Dict[str, Any]):
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
    new_dict = {}
    for k, v in out.items():
        subunits = {f"n{item['id']}": item for item in v}
        new_dict[k] = subunits
    return new_dict
