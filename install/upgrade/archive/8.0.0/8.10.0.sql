BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.10.0' WHERE name = 'database_version';

-- #1233: API: External Authentication
CREATE TABLE IF NOT EXISTS web.user_tokens (
    id integer NOT NULL,
    user_id integer NOT NULL,
    creator_id integer NOT NULL,
    name text,
    jti text,
    valid_from timestamp without time zone,
    valid_until timestamp without time zone,
    created timestamp without time zone NOT NULL DEFAULT now(),
    modified timestamp without time zone,
    revoked boolean NOT NULL DEFAULT false,
    CONSTRAINT user_tokens_pkey PRIMARY KEY (id),
    CONSTRAINT user_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user" (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE NO ACTION,
    CONSTRAINT user_tokens_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES web."user" (id) MATCH SIMPLE ON UPDATE CASCADE ON DELETE NO ACTION
);

ALTER TABLE IF EXISTS web.user_tokens OWNER to openatlas;
CREATE SEQUENCE web.user_tokens_id_seq START WITH 1 INCREMENT BY 1 NO MINVALUE NO MAXVALUE CACHE 1;
ALTER TABLE web.user_tokens_id_seq OWNER TO openatlas;
ALTER SEQUENCE web.user_tokens_id_seq OWNED BY web.user_tokens.id;
ALTER TABLE ONLY web.user_tokens ALTER COLUMN id SET DEFAULT nextval('web.user_tokens_id_seq'::regclass);

END;
