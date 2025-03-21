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
ALTER TABLE ONLY web.reference_system ADD CONSTRAINT reference_system_reference_system_api_id_fkey
    FOREIGN KEY (reference_system_api_id) REFERENCES web.reference_system_api(id)
        ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;

END;
