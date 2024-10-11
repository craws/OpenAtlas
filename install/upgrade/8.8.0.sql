BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.8.0' WHERE name = 'database_version';

-- #2357: Wrong direction for external references with files
-- This is work in progress!


-- bibliography and edition should always be the domain for P67 - referenced by
UPDATE model.link
SET (domain_id, range_id) = (range_id, domain_id)
WHERE id IN (
	SELECT l.id
	FROM model.link l
	JOIN model.entity d ON l.domain_id = d.id
	JOIN model.entity r ON l.range_id = r.id AND r.openatlas_class_name IN ('bibliography', 'edition')
	WHERE l.property_code = 'P67');


-- check for bad --
SELECT l.id, property_code, domain_id, d.name, range_id, r.name
	FROM model.link l
	JOIN model.entity d ON l.domain_id = d.id
        JOIN model.entity r ON l.range_id = r.id AND r.openatlas_class_name  IN ('bibliography', 'edition')
	WHERE l.property_code = 'P67'

-- check for good --
SELECT l.id, property_code, domain_id, d.name, range_id, r.name
	FROM model.link l
	JOIN model.entity d ON l.domain_id = d.id AND d.openatlas_class_name IN ('bibliography', 'edition')
        JOIN model.entity r ON l.range_id = r.id
	WHERE l.property_code = 'P67'

END;
