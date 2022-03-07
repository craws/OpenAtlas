from setuptools import setup

package_json = {
    "dependencies": {
        "@fortawesome/fontawesome-free": "^5.15.4",
        "bootstrap-autocomplete": "2.3.7",
        "bootstrap": "^4.6.1",
        "d3": "^5.16.0",
        "datatables.net-bs4": "^1.11.5",
        "datatables.net-buttons-dt": "^1.7.1",
        "datatables.net-buttons": "^1.7.1",
        "datatables.net-dt": "^1.11.5",
        "datatables.net": "^1.11.5",
        "huebee": "^2.1.1",
        "jquery-ui-dist": "^1.13.1",
        "jquery-validation": "^1.19.3",
        "jquery": "^3.6.0",
        "jstree": "^3.3.12",
        "leaflet-imageoverlay-rotated": "^v0.2.1",
        "leaflet.markercluster": "^1.5.3",
        "leaflet-draw": "^1.0.4",
        "leaflet-easybutton": "^2.4.0",
        "leaflet-groupedlayercontrol": "^0.6.1",
        "leaflet": "^1.7.1",
        "popper.js": "^1.16.1",
        "save-svg-as-png": "^1.4.17",
        "tinymce": "^5.10.3",
    }
}

setup(
    name='openatlas',
    setup_requires=['calmjs'],
    package_json=package_json
)
