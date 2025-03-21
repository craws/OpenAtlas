BEGIN;

-- Raise database version

UPDATE web.settings SET value = '8.11.0' WHERE name = 'database_version';

-- #2319 APIS interface

CREATE TABLE web.reference_system_api (
    id integer NOT NULL,
    name text NOT NULL
);
ALTER TABLE web.reference_system_api OWNER TO openatlas;

CREATE SEQUENCE web.reference_system_api_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER TABLE web.reference_system_api_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.reference_system_api_id_seq OWNED BY web.reference_system_api.id;
ALTER TABLE ONLY web.reference_system_api ALTER COLUMN id
    SET DEFAULT nextval('web.reference_system_api_id_seq'::regclass);
ALTER TABLE ONLY web.reference_system_api ADD CONSTRAINT reference_system_api_pkey PRIMARY KEY (id);
ALTER TABLE ONLY web.reference_system_api ADD CONSTRAINT reference_system_api_name_key UNIQUE (name);
ALTER TABLE ONLY web.reference_system ADD CONSTRAINT reference_system_reference_system_api_name_fkey
    FOREIGN KEY (reference_system_api_name) REFERENCES web.reference_system_api(name)
        ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;

INSERT INTO web.reference_system_api(name) VALUES
 ('Wikidata'), ('GeoNames'), ('GND'), ('APIS');

UPDATE web.reference_system SET reference_system_api_name = 'Wikidata' WHERE name = 'Wikidata';
UPDATE web.reference_system SET reference_system_api_name = 'GeoNames' WHERE name = 'GeoNames';
UPDATE web.reference_system SET reference_system_api_name = 'GND' WHERE name = 'GND';

END;
