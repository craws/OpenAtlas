-- Upgrade 7.0.x to 7.0.3
-- Be sure to backup the database and read the upgrade notes before executing!

-- Deletes possible wrong links created because of bug #1634
-- In case you are running 7.1.0.sql later it isn't needed because included there too

DELETE FROM model.link WHERE id in (
    SELECT l.id FROM model.link l
    JOIN model.entity d ON l.domain_id = d.id AND d.openatlas_class_name = 'type'
    JOIN model.entity r ON l.range_id = r.id AND r.openatlas_class_name = 'type'
    WHERE l.property_code = 'P2'
);
