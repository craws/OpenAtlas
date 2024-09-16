BEGIN;

-- #2079: Text annotation

-- Sync image annotation fields to text annotation fields
ALTER TABLE web.annotation_image RENAME COLUMN annotation TO text;
ALTER TABLE web.annotation_image ALTER COLUMN text DROP NOT NULL;
ALTER TABLE web.annotation_image ADD COLUMN modified timestamp without time zone;
CREATE TRIGGER update_modified BEFORE UPDATE ON web.annotation_image FOR EACH ROW EXECUTE FUNCTION model.update_modified();

-- Text annotation
ALTER TABLE IF EXISTS ONLY web.annotation_text DROP CONSTRAINT IF EXISTS annotation_text_user_id_fkey;
ALTER TABLE IF EXISTS ONLY web.annotation_text DROP CONSTRAINT IF EXISTS annotation_text_source_id_fkey;
ALTER TABLE IF EXISTS ONLY web.annotation_text DROP CONSTRAINT IF EXISTS annotation_text_entity_id_fkey;
DROP TRIGGER IF EXISTS update_modified ON web.annotation_text;
ALTER TABLE IF EXISTS ONLY web.annotation_text DROP CONSTRAINT IF EXISTS annotation_text_pkey;
DROP TABLE IF EXISTS web.annotation_text;
DROP SEQUENCE IF EXISTS web.annotation_text_id_seq;

CREATE SEQUENCE web.annotation_text_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE MAXVALUE 2147483647 CACHE 1;
ALTER TABLE web.annotation_text_id_seq OWNER TO openatlas;

CREATE TABLE web.annotation_text (
    id integer DEFAULT nextval('web.annotation_text_id_seq'::regclass) NOT NULL,
    source_id integer NOT NULL,
    entity_id integer,
    link_start integer NOT NULL,
    link_end integer NOT NULL,
    user_id integer,
    text integer,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);
ALTER TABLE web.annotation_text OWNER TO openatlas;

ALTER TABLE ONLY web.annotation_text ADD CONSTRAINT annotation_text_pkey PRIMARY KEY (id);
CREATE TRIGGER update_modified BEFORE UPDATE ON web.annotation_text FOR EACH ROW EXECUTE FUNCTION model.update_modified();
ALTER TABLE ONLY web.annotation_text ADD CONSTRAINT annotation_text_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.annotation_text ADD CONSTRAINT annotation_text_source_id_fkey FOREIGN KEY (source_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.annotation_text ADD CONSTRAINT annotation_text_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;

END;
