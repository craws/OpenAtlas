
-- Merge OpenAtlas classes Place and Object location (#2874)

---- Move links from object_location to corresponding place
UPDATE model.link l SET range_id = (
    SELECT l2.domain_id
    FROM model.link l2
    WHERE l2.range_id = l.range_id AND l2.property_code='P53')
WHERE
    l.property_code != 'P53' AND
    range_id IN (
       SELECT e.id
       FROM entity e
       WHERE e.openatlas_class_name = 'object_location');

UPDATE model.link l SET domain_id = (
    SELECT l2.domain_id
    FROM model.link l2
    WHERE l2.range_id = l.domain_id AND l2.property_code='P53')
WHERE
    l.property_code = 'P89' AND
    domain_id IN (
       SELECT e.id
       FROM entity e
       WHERE e.openatlas_class_name = 'object_location');

---- Update GIS data to use place instead of location
UPDATE model.gis SET entity_id = (
    SELECT domain_id
    FROM model.link
    WHERE range_id = entity_id AND property_code='P53');

---- Delete object_location
DELETE FROM openatlas_class WHERE name = 'object_location';
