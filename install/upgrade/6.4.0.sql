-- Upgrade 6.3.0 to 6.4.0
-- Be sure to backup the database and read the upgrade notes before executing!

BEGIN;

-- Activate image processing (#1492)
INSERT INTO web.settings (name, value) VALUES ('image_processing', 'True');

-- Clean up data after type link bug (#1554)
DELETE FROM model.link WHERE id IN (
    SELECT l.id FROM model.link l
    JOIN model.entity d ON l.domain_id = d.id AND d.system_class = 'type'
    JOIN model.entity r ON l.range_id = r.id AND d.system_class = 'type'
    WHERE l.property_code = 'P2');

END;
