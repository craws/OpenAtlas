-- Table: web.user_tokens

-- DROP TABLE IF EXISTS web.user_tokens;

CREATE TABLE IF NOT EXISTS web.user_tokens
(
    id integer NOT NULL,
    user_id integer,
    jit text COLLATE pg_catalog."default",
    valid_from timestamp without time zone,
    valid_until timestamp without time zone,
    created timestamp without time zone,
    modified timestamp without time zone,
    CONSTRAINT user_tokens_pkey PRIMARY KEY (id),
    CONSTRAINT user_tokens_user_id_fkey FOREIGN KEY (user_id)
        REFERENCES web."user" (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS web.user_tokens
    OWNER to openatlas;
