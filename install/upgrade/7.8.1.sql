-- Upgrade 7.8.0 to 7.8.1
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

-- Raise database version
UPDATE web.settings SET value = '7.8.1' WHERE name = 'database_version';

-- #1911: Removing wrong data that may have been created because of membership bug
DELETE FROM model.link WHERE property_code = 'P2' AND range_id IN (
WITH RECURSIVE items AS (
  SELECT domain_id
  FROM model.link
  WHERE range_id = (SELECT id FROM model.entity WHERE name = 'Actor function' AND openatlas_class_name = 'type') AND property_code = 'P127'
  UNION SELECT l.domain_id FROM model.link l INNER JOIN items i ON l.range_id = i.domain_id AND l.property_code = 'P127'
  ) SELECT domain_id FROM items
);
DELETE FROM model.link WHERE property_code = 'P2' AND range_id IN (
WITH RECURSIVE items AS (
  SELECT domain_id
  FROM model.link
  WHERE range_id = (SELECT id FROM model.entity WHERE name = 'Actor relation' AND openatlas_class_name = 'type') AND property_code = 'P127'
  UNION SELECT l.domain_id FROM model.link l INNER JOIN items i ON l.range_id = i.domain_id AND l.property_code = 'P127'
  ) SELECT domain_id FROM items
);
DELETE FROM model.link WHERE property_code = 'P2' AND range_id IN (
WITH RECURSIVE items AS (
  SELECT domain_id
  FROM model.link
  WHERE range_id = (SELECT id FROM model.entity WHERE name = 'Involvement' AND openatlas_class_name = 'type') AND property_code = 'P127'
  UNION SELECT l.domain_id FROM model.link l INNER JOIN items i ON l.range_id = i.domain_id AND l.property_code = 'P127'
  ) SELECT domain_id FROM items
);

END;
