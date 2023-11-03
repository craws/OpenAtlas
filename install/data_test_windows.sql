-- IIIF activation
UPDATE web.settings SET value = 'c:\iiif' WHERE name = 'iiif_path';
UPDATE web.settings SET value = 'http://localhost:8182/iiif/2/' WHERE name = 'iiif_url';
