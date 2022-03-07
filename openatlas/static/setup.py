from setuptools import setup

package_json = {
    "dependencies": {
        "jquery": "^3.6.0",
        "d3": "^5.12.0",
        "@fortawesome/fontawesome-free": "^5.11.2",
        "huebee": "^2.0.0",
        "jquery-ui-dist": "^1.13.1",
        "jquery-validation": "^1.19.3",
        "jstree": "^3.3.8",
        "datatables.net": "^1.11.5",
        "datatables.net-dt": "^1.11.5",
        "datatables.net-buttons": "^2.2.2",
        "datatables.net-buttons-dt": "^2.2.2",
        "datatables.net-bs4": "^1.11.5",
        "leaflet": "^1.5.1",
        "leaflet-imageoverlay-rotated": "^v0.2.1",
        "save-svg-as-png": "^1.4.14",
        "tinymce": "^6.0.0",
        "bootstrap": "^4.3.1",
        "popper.js": "^1.16.0",
        "bootstrap-autocomplete": "2.3.7"
    }
}

setup(
    name='openatlas',
    setup_requires=['calmjs'],
    package_json=package_json
)
