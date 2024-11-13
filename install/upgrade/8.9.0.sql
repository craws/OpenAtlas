-- Upgrade 8.8.x to 8.9.0
-- Be sure to backup the database and read the upgrade notes before executing.

BEGIN;

UPDATE web.settings SET value = '8.9.0' WHERE name = 'database_version';


CREATE TABLE IF NOT EXISTS web.user_tokens
(
    id integer NOT NULL,
    user_id integer NOT NULL,
    name text COLLATE pg_catalog."default",
    jit text COLLATE pg_catalog."default",
    valid_from timestamp without time zone,
    valid_until timestamp without time zone,
    created timestamp without time zone NOT NULL DEFAULT now(),
    modified timestamp without time zone,
    CONSTRAINT user_tokens_pkey PRIMARY KEY (id),
    CONSTRAINT user_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user" (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE SET NULL NOT VALID
);


ALTER TABLE IF EXISTS web.user_tokens OWNER to openatlas;
CREATE SEQUENCE web.user_tokens_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE web.user_tokens_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.user_tokens_id_seq OWNED BY web.user_tokens.id;
ALTER TABLE ONLY web.user_tokens ALTER COLUMN id SET DEFAULT nextval('web.user_tokens_id_seq'::regclass);


END;
