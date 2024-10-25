BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.8.0' WHERE name = 'database_version';

-- #2357: Fix possible wrong direction for references with files
UPDATE model.link
SET (domain_id, range_id) = (range_id, domain_id)
WHERE id IN (
	SELECT l.id
	FROM model.link l
	JOIN model.entity d ON l.domain_id = d.id AND d.openatlas_class_name = 'file'
	JOIN model.entity r ON l.range_id = r.id AND r.openatlas_class_name IN ('bibliography', 'edition', 'external_reference')
	WHERE l.property_code = 'P67');

END;
