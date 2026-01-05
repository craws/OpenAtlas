import re
from typing import Any

from flask import Response
from lxml import etree


def subunit_xml(result: dict[str, Any]) -> bytes:
    new_dict = {}
    for key, value in result.items():
        item_list = [{item['openatlasClassName']: item} for item in value]
        new_dict[key] = item_list
    root = dict_to_xml('root', new_dict)
    xml_bytes = etree.tostring(
        root,
        pretty_print=True,
        xml_declaration=True,
        encoding="utf-8")
    return xml_bytes


def dict_to_xml(tag: str, data: Any) -> etree.Element:
    elem = etree.Element(tag)
    if isinstance(data, dict):
        for key, val in data.items():
            elem.append(dict_to_xml(str(key), val))
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict) and len(item) == 1:
                key, val = next(iter(item.items()))
                elem.append(dict_to_xml(key, val))
            else:
                elem.append(dict_to_xml('item', item))
    else:
        elem.text = clean_text(data)
    return elem


def export_database_xml(tables: dict[str, Any], filename: str) -> Response:
    return Response(
        etree.tostring(
            dict_to_xml('root', tables),
            pretty_print=True,
            xml_declaration=True,
            encoding='utf-8'),
        mimetype='application/xml',
        headers={'Content-Disposition': f'attachment;filename={filename}.xml'})


def clean_text(text: Any) -> str:
    if text is None:
        return ''
    string_ = str(text)
    # Remove illegal XML control ASCII characters
    return re.compile(r'[\x00-\x08\x0B\x0C\x0E-\x1F]').sub('', string_)
