import logging
from typing import Any

import dicttoxml
from flask import Response

dicttoxml.set_debug(debug=False)
dicttoxml.LOG.setLevel(logging.ERROR)


def subunit_xml(result: dict[str, Any]) -> bytes:
    item_list = []
    new_dict = {}
    for key, value in result.items():
        item_list.append({item['openatlasClassName']: item} for item in value)
        new_dict[key] = item_list
    xml = dicttoxml.dicttoxml(new_dict, root=False, attr_type=False)
    xml = xml.replace(b'<item >', b'')
    xml = xml.replace(b'<item>', b'')
    xml = xml.replace(b'</item>', b'')
    return xml


def export_database_xml(tables: dict[str, Any], filename: str) -> Response:
    return Response(
        dicttoxml.dicttoxml(tables, root=False, attr_type=False),
        mimetype='application/xml',
        headers={
            'Content-Disposition': f'attachment;filename={filename}.xml'})
