import json
import shutil

from flask import g, request

from openatlas import app


def write_openapi_instance() -> None:
    openapi = app.config['OPENAPI_FILE']
    openapi_instance = app.config['OPENAPI_INSTANCE_FILE']
    if not openapi_instance.exists():
        shutil.copy(openapi, openapi_instance)
    with openapi_instance.open(mode='r+') as i, openapi.open(mode='r') as f:
        original = json.load(f)
        instance = json.load(i)
        if original['info']['version'] != instance['info']['version']:
            shutil.copy(openapi, openapi_instance)
        server = {
            'url': request.host_url + 'api/{basePath}',
            'description': f'{g.settings['site_name']} Server',
            'variables': {'basePath': {'default': '0.4', 'enum': ['0.4']}}}
        modified = False
        if len(instance['servers']) == 2:
            instance['servers'].insert(0, server)
            modified = True
        elif instance['servers'][0]['description'] != server['description']:
            instance['servers'][0] = server
            modified = True
        if modified:
            i.seek(0)
            json.dump(instance, i, indent=4)
            i.truncate()
