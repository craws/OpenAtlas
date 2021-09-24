-- Upgrade 6.5.0 to 6.6.0
-- Be sure to backup the database and read the upgrade notes before executing!

BEGIN;

-- #1563: OpenAtlas model to database
ALTER TABLE model.class RENAME TO cidoc_class;
ALTER TABLE model.class_i18n RENAME TO cidoc_class_i18n;
ALTER TABLE model.class_inheritance RENAME TO  cidoc_class_inheritance;

ALTER SEQUENCE model.class_id_seq RENAME TO cidoc_class_id_seq;
ALTER SEQUENCE model.class_i18n_id_seq RENAME to cidoc_class_i18n_id_seq;
ALTER SEQUENCE model.class_inheritance_id_seq RENAME TO cidoc_class_inheritance_id_seq;

END;
