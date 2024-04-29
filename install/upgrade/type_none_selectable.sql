
BEGIN;


-- #2261 Option to prevent selection of a type
DROP TABLE IF EXISTS "type_none_selectable";
DROP SEQUENCE IF EXISTS type_none_selectable_id_seq;
CREATE SEQUENCE type_none_selectable_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE "web"."type_none_selectable" (
    "id" integer DEFAULT nextval('type_none_selectable_id_seq') NOT NULL,
    "entity_id" integer NOT NULL,
    "created" timestamp DEFAULT now() NOT NULL,
    CONSTRAINT "type_none_selectable_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

COMMENT ON TABLE "web"."type_none_selectable" IS 'IDs of types that are not meant to be selected, e.g. a category';


ALTER TABLE ONLY "web"."type_none_selectable" ADD CONSTRAINT "type_none_selectable_entity_id_fkey"
FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE NOT DEFERRABLE;

END;
