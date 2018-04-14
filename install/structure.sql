--
-- PostgreSQL database dump
--

-- Dumped from database version 9.6.6
-- Dumped by pg_dump version 9.6.6

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;
SET search_path = web, pg_catalog;

ALTER TABLE IF EXISTS ONLY web.user_settings DROP CONSTRAINT IF EXISTS user_settings_user_id_fkey;
ALTER TABLE IF EXISTS ONLY web."user" DROP CONSTRAINT IF EXISTS user_group_id_fkey;
ALTER TABLE IF EXISTS ONLY web.user_bookmarks DROP CONSTRAINT IF EXISTS user_bookmarks_user_id_fkey;
ALTER TABLE IF EXISTS ONLY web.user_bookmarks DROP CONSTRAINT IF EXISTS user_bookmarks_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY web.hierarchy DROP CONSTRAINT IF EXISTS hierarchy_id_fkey;
ALTER TABLE IF EXISTS ONLY web.hierarchy_form DROP CONSTRAINT IF EXISTS hierarchy_form_hierarchy_id_fkey;
ALTER TABLE IF EXISTS ONLY web.hierarchy_form DROP CONSTRAINT IF EXISTS hierarchy_form_form_id_fkey;
SET search_path = model, pg_catalog;

ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_range_class_code_fkey;
ALTER TABLE IF EXISTS ONLY model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_super_code_fkey;
ALTER TABLE IF EXISTS ONLY model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_sub_code_fkey;
ALTER TABLE IF EXISTS ONLY model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_property_code_fkey;
ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_domain_class_code_fkey;
ALTER TABLE IF EXISTS ONLY model.link DROP CONSTRAINT IF EXISTS link_range_id_fkey;
ALTER TABLE IF EXISTS ONLY model.link_property DROP CONSTRAINT IF EXISTS link_property_range_id_fkey;
ALTER TABLE IF EXISTS ONLY model.link_property DROP CONSTRAINT IF EXISTS link_property_property_code_fkey;
ALTER TABLE IF EXISTS ONLY model.link_property DROP CONSTRAINT IF EXISTS link_property_domain_id_fkey;
ALTER TABLE IF EXISTS ONLY model.link DROP CONSTRAINT IF EXISTS link_property_code_fkey;
ALTER TABLE IF EXISTS ONLY model.link DROP CONSTRAINT IF EXISTS link_domain_id_fkey;
ALTER TABLE IF EXISTS ONLY model.entity DROP CONSTRAINT IF EXISTS entity_class_code_fkey;
ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_super_code_fkey;
ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_sub_code_fkey;
ALTER TABLE IF EXISTS ONLY model.class_i18n DROP CONSTRAINT IF EXISTS class_i18n_class_code_fkey;
SET search_path = gis, pg_catalog;

ALTER TABLE IF EXISTS ONLY gis.polygon DROP CONSTRAINT IF EXISTS polygon_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY gis.point DROP CONSTRAINT IF EXISTS point_entity_id_fkey;
ALTER TABLE IF EXISTS ONLY gis.linestring DROP CONSTRAINT IF EXISTS linestring_entity_id_fkey;
SET search_path = web, pg_catalog;

DROP TRIGGER IF EXISTS update_modified ON web.i18n;
DROP TRIGGER IF EXISTS update_modified ON web.hierarchy_form;
DROP TRIGGER IF EXISTS update_modified ON web.form;
DROP TRIGGER IF EXISTS update_modified ON web.hierarchy;
DROP TRIGGER IF EXISTS update_modified ON web.user_bookmarks;
DROP TRIGGER IF EXISTS update_modified ON web.user_settings;
DROP TRIGGER IF EXISTS update_modified ON web."group";
DROP TRIGGER IF EXISTS update_modified ON web."user";
SET search_path = model, pg_catalog;

DROP TRIGGER IF EXISTS update_modified ON model.property_i18n;
DROP TRIGGER IF EXISTS update_modified ON model.class_i18n;
DROP TRIGGER IF EXISTS update_modified ON model.link_property;
DROP TRIGGER IF EXISTS update_modified ON model.property_inheritance;
DROP TRIGGER IF EXISTS update_modified ON model.link;
DROP TRIGGER IF EXISTS update_modified ON model.entity;
DROP TRIGGER IF EXISTS update_modified ON model.property;
DROP TRIGGER IF EXISTS update_modified ON model.class_inheritance;
DROP TRIGGER IF EXISTS update_modified ON model.class;
DROP TRIGGER IF EXISTS on_delete_link_property ON model.link_property;
DROP TRIGGER IF EXISTS on_delete_entity ON model.entity;
SET search_path = gis, pg_catalog;

DROP TRIGGER IF EXISTS update_modified ON gis.polygon;
DROP TRIGGER IF EXISTS update_modified ON gis.linestring;
DROP TRIGGER IF EXISTS update_modified ON gis.point;
SET search_path = web, pg_catalog;

ALTER TABLE IF EXISTS ONLY web."user" DROP CONSTRAINT IF EXISTS user_username_key;
ALTER TABLE IF EXISTS ONLY web.user_settings DROP CONSTRAINT IF EXISTS user_settings_user_id_name_key;
ALTER TABLE IF EXISTS ONLY web.user_settings DROP CONSTRAINT IF EXISTS user_settings_pkey;
ALTER TABLE IF EXISTS ONLY web."user" DROP CONSTRAINT IF EXISTS user_pkey;
ALTER TABLE IF EXISTS ONLY web.user_log DROP CONSTRAINT IF EXISTS user_log_pkey;
ALTER TABLE IF EXISTS ONLY web."user" DROP CONSTRAINT IF EXISTS user_email_key;
ALTER TABLE IF EXISTS ONLY web.user_bookmarks DROP CONSTRAINT IF EXISTS user_bookmarks_user_id_entity_id_key;
ALTER TABLE IF EXISTS ONLY web.user_bookmarks DROP CONSTRAINT IF EXISTS user_bookmarks_pkey;
ALTER TABLE IF EXISTS ONLY web."user" DROP CONSTRAINT IF EXISTS unsubscribe_code_key;
ALTER TABLE IF EXISTS ONLY web.settings DROP CONSTRAINT IF EXISTS settings_pkey;
ALTER TABLE IF EXISTS ONLY web.system_log DROP CONSTRAINT IF EXISTS log_pkey;
ALTER TABLE IF EXISTS ONLY web.i18n DROP CONSTRAINT IF EXISTS i18n_pkey;
ALTER TABLE IF EXISTS ONLY web.i18n DROP CONSTRAINT IF EXISTS i18n_name_language_key;
ALTER TABLE IF EXISTS ONLY web.hierarchy DROP CONSTRAINT IF EXISTS hierarchy_pkey;
ALTER TABLE IF EXISTS ONLY web.hierarchy DROP CONSTRAINT IF EXISTS hierarchy_name_key;
ALTER TABLE IF EXISTS ONLY web.hierarchy_form DROP CONSTRAINT IF EXISTS hierarchy_form_pkey;
ALTER TABLE IF EXISTS ONLY web."group" DROP CONSTRAINT IF EXISTS group_pkey;
ALTER TABLE IF EXISTS ONLY web.form DROP CONSTRAINT IF EXISTS form_pkey;
ALTER TABLE IF EXISTS ONLY web.form DROP CONSTRAINT IF EXISTS form_name_key;
SET search_path = model, pg_catalog;

ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_pkey;
ALTER TABLE IF EXISTS ONLY model.property_inheritance DROP CONSTRAINT IF EXISTS property_inheritance_pkey;
ALTER TABLE IF EXISTS ONLY model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_property_code_language_code_attribute_key;
ALTER TABLE IF EXISTS ONLY model.property_i18n DROP CONSTRAINT IF EXISTS property_i18n_pkey;
ALTER TABLE IF EXISTS ONLY model.property DROP CONSTRAINT IF EXISTS property_code_key;
ALTER TABLE IF EXISTS ONLY model.link_property DROP CONSTRAINT IF EXISTS link_property_pkey;
ALTER TABLE IF EXISTS ONLY model.link DROP CONSTRAINT IF EXISTS link_pkey;
ALTER TABLE IF EXISTS ONLY model.entity DROP CONSTRAINT IF EXISTS entity_pkey;
ALTER TABLE IF EXISTS ONLY model.class DROP CONSTRAINT IF EXISTS class_pkey;
ALTER TABLE IF EXISTS ONLY model.class DROP CONSTRAINT IF EXISTS class_name_key;
ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_super_id_sub_id_key;
ALTER TABLE IF EXISTS ONLY model.class_inheritance DROP CONSTRAINT IF EXISTS class_inheritance_pkey;
ALTER TABLE IF EXISTS ONLY model.class_i18n DROP CONSTRAINT IF EXISTS class_i18n_pkey;
ALTER TABLE IF EXISTS ONLY model.class_i18n DROP CONSTRAINT IF EXISTS class_i18n_class_code_language_code_attribute_key;
ALTER TABLE IF EXISTS ONLY model.class DROP CONSTRAINT IF EXISTS class_code_key;
SET search_path = gis, pg_catalog;

ALTER TABLE IF EXISTS ONLY gis.polygon DROP CONSTRAINT IF EXISTS polygon_pkey;
ALTER TABLE IF EXISTS ONLY gis.point DROP CONSTRAINT IF EXISTS point_pkey;
ALTER TABLE IF EXISTS ONLY gis.linestring DROP CONSTRAINT IF EXISTS linestring_pkey;
SET search_path = web, pg_catalog;

ALTER TABLE IF EXISTS web.user_settings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.user_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.user_bookmarks ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web."user" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.system_log ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.settings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.i18n ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.hierarchy_form ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.hierarchy ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web."group" ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS web.form ALTER COLUMN id DROP DEFAULT;
SET search_path = model, pg_catalog;

ALTER TABLE IF EXISTS model.property_inheritance ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.property_i18n ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.property ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.link_property ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.link ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.entity ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.class_inheritance ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.class_i18n ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS model.class ALTER COLUMN id DROP DEFAULT;
SET search_path = gis, pg_catalog;

ALTER TABLE IF EXISTS gis.polygon ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS gis.point ALTER COLUMN id DROP DEFAULT;
ALTER TABLE IF EXISTS gis.linestring ALTER COLUMN id DROP DEFAULT;
SET search_path = web, pg_catalog;

DROP SEQUENCE IF EXISTS web.user_settings_id_seq;
DROP TABLE IF EXISTS web.user_settings;
DROP SEQUENCE IF EXISTS web.user_log_id_seq;
DROP TABLE IF EXISTS web.user_log;
DROP SEQUENCE IF EXISTS web.user_id_seq;
DROP SEQUENCE IF EXISTS web.user_bookmarks_id_seq;
DROP TABLE IF EXISTS web.user_bookmarks;
DROP TABLE IF EXISTS web."user";
DROP SEQUENCE IF EXISTS web.settings_id_seq;
DROP TABLE IF EXISTS web.settings;
DROP SEQUENCE IF EXISTS web.log_id_seq;
DROP TABLE IF EXISTS web.system_log;
DROP SEQUENCE IF EXISTS web.i18n_id_seq;
DROP TABLE IF EXISTS web.i18n;
DROP SEQUENCE IF EXISTS web.hierarchy_id_seq;
DROP SEQUENCE IF EXISTS web.hierarchy_form_id_seq;
DROP TABLE IF EXISTS web.hierarchy_form;
DROP TABLE IF EXISTS web.hierarchy;
DROP SEQUENCE IF EXISTS web.group_id_seq;
DROP TABLE IF EXISTS web."group";
DROP SEQUENCE IF EXISTS web.form_id_seq;
DROP TABLE IF EXISTS web.form;
SET search_path = model, pg_catalog;

DROP SEQUENCE IF EXISTS model.property_inheritance_id_seq;
DROP TABLE IF EXISTS model.property_inheritance;
DROP SEQUENCE IF EXISTS model.property_id_seq;
DROP SEQUENCE IF EXISTS model.property_i18n_id_seq;
DROP TABLE IF EXISTS model.property_i18n;
DROP TABLE IF EXISTS model.property;
DROP SEQUENCE IF EXISTS model.link_property_id_seq;
DROP TABLE IF EXISTS model.link_property;
DROP SEQUENCE IF EXISTS model.link_id_seq;
DROP TABLE IF EXISTS model.link;
DROP SEQUENCE IF EXISTS model.entity_id_seq;
DROP TABLE IF EXISTS model.entity;
DROP SEQUENCE IF EXISTS model.class_inheritance_id_seq;
DROP TABLE IF EXISTS model.class_inheritance;
DROP SEQUENCE IF EXISTS model.class_id_seq;
DROP SEQUENCE IF EXISTS model.class_i18n_id_seq;
DROP TABLE IF EXISTS model.class_i18n;
DROP TABLE IF EXISTS model.class;
SET search_path = gis, pg_catalog;

DROP SEQUENCE IF EXISTS gis.polygon_id_seq;
DROP TABLE IF EXISTS gis.polygon;
DROP SEQUENCE IF EXISTS gis.point_id_seq;
DROP TABLE IF EXISTS gis.point;
DROP SEQUENCE IF EXISTS gis.linestring_id_seq;
DROP TABLE IF EXISTS gis.linestring;
SET search_path = model, pg_catalog;

DROP FUNCTION IF EXISTS model.update_modified();
DROP FUNCTION IF EXISTS model.delete_link_dates();
DROP FUNCTION IF EXISTS model.delete_entity_related();
DROP SCHEMA IF EXISTS web;
DROP SCHEMA IF EXISTS model;
DROP SCHEMA IF EXISTS gis;
--
-- Name: gis; Type: SCHEMA; Schema: -; Owner: openatlas
--

CREATE SCHEMA gis;


ALTER SCHEMA gis OWNER TO openatlas;

--
-- Name: model; Type: SCHEMA; Schema: -; Owner: openatlas
--

CREATE SCHEMA model;


ALTER SCHEMA model OWNER TO openatlas;

--
-- Name: web; Type: SCHEMA; Schema: -; Owner: openatlas
--

CREATE SCHEMA web;


ALTER SCHEMA web OWNER TO openatlas;

SET search_path = model, pg_catalog;

--
-- Name: delete_entity_related(); Type: FUNCTION; Schema: model; Owner: openatlas
--

CREATE FUNCTION delete_entity_related() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            -- Delete dates (E61) and aliases (E41, E82)
            IF OLD.class_code IN ('E6', 'E7', 'E8', 'E12', 'E21', 'E40', 'E74', 'E18', 'E22') THEN
                DELETE FROM model.entity WHERE id IN (
                    SELECT range_id FROM model.link WHERE domain_id = OLD.id AND class_code IN ('E41', 'E61', 'E82'));
            END IF;

            -- Delete the location (E53)
            IF OLD.class_code IN ('E18', 'E22') THEN
                DELETE FROM model.entity WHERE id = (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P53');
            END IF;

            -- If it is a document (E33) delete the translations (E33)
            IF OLD.class_code = 'E33' THEN
                DELETE FROM model.entity WHERE id = (SELECT range_id FROM model.link WHERE domain_id = OLD.id AND property_code = 'P73');
            END IF;

            RETURN OLD;
        END;
    $$;


ALTER FUNCTION model.delete_entity_related() OWNER TO openatlas;

--
-- Name: delete_link_dates(); Type: FUNCTION; Schema: model; Owner: openatlas
--

CREATE FUNCTION delete_link_dates() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
        BEGIN
            IF OLD.property_code IN ('OA5', 'OA6') THEN
                DELETE FROM model.entity WHERE id = OLD.range_id AND class_code = 'E61';
            END IF;
            RETURN OLD;
        END;
    $$;


ALTER FUNCTION model.delete_link_dates() OWNER TO openatlas;

--
-- Name: update_modified(); Type: FUNCTION; Schema: model; Owner: openatlas
--

CREATE FUNCTION update_modified() RETURNS trigger
    LANGUAGE plpgsql
    AS $$
BEGIN

   NEW.modified = now();

   RETURN NEW;

END;

$$;


ALTER FUNCTION model.update_modified() OWNER TO openatlas;

SET search_path = gis, pg_catalog;

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: linestring; Type: TABLE; Schema: gis; Owner: openatlas
--

CREATE TABLE linestring (
    id integer NOT NULL,
    entity_id integer NOT NULL,
    name text,
    description text,
    type text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    geom public.geometry(LineString,4326)
);


ALTER TABLE linestring OWNER TO openatlas;

--
-- Name: linestring_id_seq; Type: SEQUENCE; Schema: gis; Owner: openatlas
--

CREATE SEQUENCE linestring_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE linestring_id_seq OWNER TO openatlas;

--
-- Name: linestring_id_seq; Type: SEQUENCE OWNED BY; Schema: gis; Owner: openatlas
--

ALTER SEQUENCE linestring_id_seq OWNED BY linestring.id;


--
-- Name: point; Type: TABLE; Schema: gis; Owner: openatlas
--

CREATE TABLE point (
    id integer NOT NULL,
    entity_id integer NOT NULL,
    name text,
    description text,
    type text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    geom public.geometry(Point,4326)
);


ALTER TABLE point OWNER TO openatlas;

--
-- Name: point_id_seq; Type: SEQUENCE; Schema: gis; Owner: openatlas
--

CREATE SEQUENCE point_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE point_id_seq OWNER TO openatlas;

--
-- Name: point_id_seq; Type: SEQUENCE OWNED BY; Schema: gis; Owner: openatlas
--

ALTER SEQUENCE point_id_seq OWNED BY point.id;


--
-- Name: polygon; Type: TABLE; Schema: gis; Owner: openatlas
--

CREATE TABLE polygon (
    id integer NOT NULL,
    entity_id integer NOT NULL,
    name text,
    description text,
    type text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    geom public.geometry(Polygon,4326)
);


ALTER TABLE polygon OWNER TO openatlas;

--
-- Name: polygon_id_seq; Type: SEQUENCE; Schema: gis; Owner: openatlas
--

CREATE SEQUENCE polygon_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE polygon_id_seq OWNER TO openatlas;

--
-- Name: polygon_id_seq; Type: SEQUENCE OWNED BY; Schema: gis; Owner: openatlas
--

ALTER SEQUENCE polygon_id_seq OWNED BY polygon.id;


SET search_path = model, pg_catalog;

--
-- Name: class; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE class (
    id integer NOT NULL,
    code text NOT NULL,
    name text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE class OWNER TO openatlas;

--
-- Name: COLUMN class.code; Type: COMMENT; Schema: model; Owner: openatlas
--

COMMENT ON COLUMN class.code IS 'e.g. E21';


--
-- Name: COLUMN class.name; Type: COMMENT; Schema: model; Owner: openatlas
--

COMMENT ON COLUMN class.name IS 'e.g. Person';


--
-- Name: class_i18n; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE class_i18n (
    id integer NOT NULL,
    class_code text NOT NULL,
    language_code text NOT NULL,
    attribute text NOT NULL,
    text text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified time without time zone
);


ALTER TABLE class_i18n OWNER TO openatlas;

--
-- Name: class_i18n_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE class_i18n_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE class_i18n_id_seq OWNER TO openatlas;

--
-- Name: class_i18n_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE class_i18n_id_seq OWNED BY class_i18n.id;


--
-- Name: class_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE class_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE class_id_seq OWNER TO openatlas;

--
-- Name: class_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE class_id_seq OWNED BY class.id;


--
-- Name: class_inheritance; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE class_inheritance (
    id integer NOT NULL,
    super_code text NOT NULL,
    sub_code text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE class_inheritance OWNER TO openatlas;

--
-- Name: class_inheritance_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE class_inheritance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE class_inheritance_id_seq OWNER TO openatlas;

--
-- Name: class_inheritance_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE class_inheritance_id_seq OWNED BY class_inheritance.id;


--
-- Name: entity; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE entity (
    id integer NOT NULL,
    class_code text NOT NULL,
    name text NOT NULL,
    description text,
    value_integer integer,
    value_timestamp timestamp without time zone,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    system_type text
);


ALTER TABLE entity OWNER TO openatlas;

--
-- Name: entity_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE entity_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE entity_id_seq OWNER TO openatlas;

--
-- Name: entity_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE entity_id_seq OWNED BY entity.id;


--
-- Name: link; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE link (
    id integer NOT NULL,
    property_code text NOT NULL,
    domain_id integer NOT NULL,
    range_id integer NOT NULL,
    description text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE link OWNER TO openatlas;

--
-- Name: link_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE link_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE link_id_seq OWNER TO openatlas;

--
-- Name: link_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE link_id_seq OWNED BY link.id;


--
-- Name: link_property; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE link_property (
    id integer NOT NULL,
    property_code text NOT NULL,
    domain_id integer NOT NULL,
    range_id integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE link_property OWNER TO openatlas;

--
-- Name: link_property_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE link_property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE link_property_id_seq OWNER TO openatlas;

--
-- Name: link_property_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE link_property_id_seq OWNED BY link_property.id;


--
-- Name: property; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE property (
    id integer NOT NULL,
    code text NOT NULL,
    range_class_code text NOT NULL,
    domain_class_code text NOT NULL,
    name text NOT NULL,
    name_inverse text,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE property OWNER TO openatlas;

--
-- Name: property_i18n; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE property_i18n (
    id integer NOT NULL,
    property_code text NOT NULL,
    language_code text NOT NULL,
    attribute text NOT NULL,
    text text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE property_i18n OWNER TO openatlas;

--
-- Name: property_i18n_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE property_i18n_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE property_i18n_id_seq OWNER TO openatlas;

--
-- Name: property_i18n_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE property_i18n_id_seq OWNED BY property_i18n.id;


--
-- Name: property_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE property_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE property_id_seq OWNER TO openatlas;

--
-- Name: property_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE property_id_seq OWNED BY property.id;


SET default_with_oids = true;

--
-- Name: property_inheritance; Type: TABLE; Schema: model; Owner: openatlas
--

CREATE TABLE property_inheritance (
    id integer NOT NULL,
    super_code text NOT NULL,
    sub_code text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE property_inheritance OWNER TO openatlas;

--
-- Name: property_inheritance_id_seq; Type: SEQUENCE; Schema: model; Owner: openatlas
--

CREATE SEQUENCE property_inheritance_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE property_inheritance_id_seq OWNER TO openatlas;

--
-- Name: property_inheritance_id_seq; Type: SEQUENCE OWNED BY; Schema: model; Owner: openatlas
--

ALTER SEQUENCE property_inheritance_id_seq OWNED BY property_inheritance.id;


SET search_path = web, pg_catalog;

SET default_with_oids = false;

--
-- Name: form; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE form (
    id integer NOT NULL,
    name text NOT NULL,
    extendable boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE form OWNER TO openatlas;

--
-- Name: form_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE form_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE form_id_seq OWNER TO openatlas;

--
-- Name: form_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE form_id_seq OWNED BY form.id;


--
-- Name: group; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE "group" (
    id integer NOT NULL,
    name text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE "group" OWNER TO openatlas;

--
-- Name: group_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE group_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE group_id_seq OWNER TO openatlas;

--
-- Name: group_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE group_id_seq OWNED BY "group".id;


--
-- Name: hierarchy; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE hierarchy (
    id integer NOT NULL,
    name text NOT NULL,
    multiple boolean DEFAULT false NOT NULL,
    system boolean DEFAULT false NOT NULL,
    directional boolean DEFAULT false NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE hierarchy OWNER TO openatlas;

--
-- Name: COLUMN hierarchy.id; Type: COMMENT; Schema: web; Owner: openatlas
--

COMMENT ON COLUMN hierarchy.id IS 'same as model.entity.id';


--
-- Name: COLUMN hierarchy.name; Type: COMMENT; Schema: web; Owner: openatlas
--

COMMENT ON COLUMN hierarchy.name IS 'same as model.entity.name, to ensure unique root type names';


--
-- Name: hierarchy_form; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE hierarchy_form (
    id integer NOT NULL,
    hierarchy_id integer NOT NULL,
    form_id integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE hierarchy_form OWNER TO openatlas;

--
-- Name: hierarchy_form_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE hierarchy_form_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hierarchy_form_id_seq OWNER TO openatlas;

--
-- Name: hierarchy_form_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE hierarchy_form_id_seq OWNED BY hierarchy_form.id;


--
-- Name: hierarchy_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE hierarchy_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE hierarchy_id_seq OWNER TO openatlas;

--
-- Name: hierarchy_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE hierarchy_id_seq OWNED BY hierarchy.id;


--
-- Name: i18n; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE i18n (
    id integer NOT NULL,
    name text NOT NULL,
    language text NOT NULL,
    text text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE i18n OWNER TO openatlas;

--
-- Name: i18n_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE i18n_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE i18n_id_seq OWNER TO openatlas;

--
-- Name: i18n_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE i18n_id_seq OWNED BY i18n.id;


--
-- Name: system_log; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE system_log (
    id integer NOT NULL,
    priority integer NOT NULL,
    type text,
    message text NOT NULL,
    user_id integer,
    ip text,
    info text,
    created timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE system_log OWNER TO openatlas;

--
-- Name: log_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE log_id_seq OWNER TO openatlas;

--
-- Name: log_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE log_id_seq OWNED BY system_log.id;


--
-- Name: settings; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE settings (
    id integer NOT NULL,
    name text NOT NULL,
    value text NOT NULL
);


ALTER TABLE settings OWNER TO openatlas;

--
-- Name: settings_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE settings_id_seq OWNER TO openatlas;

--
-- Name: settings_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE settings_id_seq OWNED BY settings.id;


--
-- Name: user; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE "user" (
    id integer NOT NULL,
    group_id integer NOT NULL,
    username text NOT NULL,
    password text NOT NULL,
    active boolean DEFAULT false NOT NULL,
    real_name text DEFAULT ''::text NOT NULL,
    email text,
    info text DEFAULT ''::text NOT NULL,
    login_last_success timestamp without time zone,
    login_last_failure timestamp without time zone,
    login_failed_count integer DEFAULT 0 NOT NULL,
    password_reset_code text,
    password_reset_date timestamp without time zone,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone,
    unsubscribe_code text
);


ALTER TABLE "user" OWNER TO openatlas;

--
-- Name: user_bookmarks; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE user_bookmarks (
    id integer NOT NULL,
    user_id integer NOT NULL,
    entity_id integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE user_bookmarks OWNER TO openatlas;

--
-- Name: user_bookmarks_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE user_bookmarks_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_bookmarks_id_seq OWNER TO openatlas;

--
-- Name: user_bookmarks_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE user_bookmarks_id_seq OWNED BY user_bookmarks.id;


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE user_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_id_seq OWNER TO openatlas;

--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: user_log; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE user_log (
    id integer NOT NULL,
    user_id integer NOT NULL,
    entity_id integer NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    action text NOT NULL
);


ALTER TABLE user_log OWNER TO openatlas;

--
-- Name: user_log_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE user_log_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_log_id_seq OWNER TO openatlas;

--
-- Name: user_log_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE user_log_id_seq OWNED BY user_log.id;


--
-- Name: user_settings; Type: TABLE; Schema: web; Owner: openatlas
--

CREATE TABLE user_settings (
    id integer NOT NULL,
    user_id integer NOT NULL,
    name text NOT NULL,
    value text NOT NULL,
    created timestamp without time zone DEFAULT now() NOT NULL,
    modified timestamp without time zone
);


ALTER TABLE user_settings OWNER TO openatlas;

--
-- Name: user_settings_id_seq; Type: SEQUENCE; Schema: web; Owner: openatlas
--

CREATE SEQUENCE user_settings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE user_settings_id_seq OWNER TO openatlas;

--
-- Name: user_settings_id_seq; Type: SEQUENCE OWNED BY; Schema: web; Owner: openatlas
--

ALTER SEQUENCE user_settings_id_seq OWNED BY user_settings.id;


SET search_path = gis, pg_catalog;

--
-- Name: linestring id; Type: DEFAULT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY linestring ALTER COLUMN id SET DEFAULT nextval('linestring_id_seq'::regclass);


--
-- Name: point id; Type: DEFAULT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY point ALTER COLUMN id SET DEFAULT nextval('point_id_seq'::regclass);


--
-- Name: polygon id; Type: DEFAULT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY polygon ALTER COLUMN id SET DEFAULT nextval('polygon_id_seq'::regclass);


SET search_path = model, pg_catalog;

--
-- Name: class id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class ALTER COLUMN id SET DEFAULT nextval('class_id_seq'::regclass);


--
-- Name: class_i18n id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_i18n ALTER COLUMN id SET DEFAULT nextval('class_i18n_id_seq'::regclass);


--
-- Name: class_inheritance id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_inheritance ALTER COLUMN id SET DEFAULT nextval('class_inheritance_id_seq'::regclass);


--
-- Name: entity id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY entity ALTER COLUMN id SET DEFAULT nextval('entity_id_seq'::regclass);


--
-- Name: link id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link ALTER COLUMN id SET DEFAULT nextval('link_id_seq'::regclass);


--
-- Name: link_property id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link_property ALTER COLUMN id SET DEFAULT nextval('link_property_id_seq'::regclass);


--
-- Name: property id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property ALTER COLUMN id SET DEFAULT nextval('property_id_seq'::regclass);


--
-- Name: property_i18n id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_i18n ALTER COLUMN id SET DEFAULT nextval('property_i18n_id_seq'::regclass);


--
-- Name: property_inheritance id; Type: DEFAULT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_inheritance ALTER COLUMN id SET DEFAULT nextval('property_inheritance_id_seq'::regclass);


SET search_path = web, pg_catalog;

--
-- Name: form id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY form ALTER COLUMN id SET DEFAULT nextval('form_id_seq'::regclass);


--
-- Name: group id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "group" ALTER COLUMN id SET DEFAULT nextval('group_id_seq'::regclass);


--
-- Name: hierarchy id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy ALTER COLUMN id SET DEFAULT nextval('hierarchy_id_seq'::regclass);


--
-- Name: hierarchy_form id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy_form ALTER COLUMN id SET DEFAULT nextval('hierarchy_form_id_seq'::regclass);


--
-- Name: i18n id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY i18n ALTER COLUMN id SET DEFAULT nextval('i18n_id_seq'::regclass);


--
-- Name: settings id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY settings ALTER COLUMN id SET DEFAULT nextval('settings_id_seq'::regclass);


--
-- Name: system_log id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY system_log ALTER COLUMN id SET DEFAULT nextval('log_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: user_bookmarks id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_bookmarks ALTER COLUMN id SET DEFAULT nextval('user_bookmarks_id_seq'::regclass);


--
-- Name: user_log id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_log ALTER COLUMN id SET DEFAULT nextval('user_log_id_seq'::regclass);


--
-- Name: user_settings id; Type: DEFAULT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_settings ALTER COLUMN id SET DEFAULT nextval('user_settings_id_seq'::regclass);


SET search_path = gis, pg_catalog;

--
-- Name: linestring linestring_pkey; Type: CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY linestring
    ADD CONSTRAINT linestring_pkey PRIMARY KEY (id);


--
-- Name: point point_pkey; Type: CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY point
    ADD CONSTRAINT point_pkey PRIMARY KEY (id);


--
-- Name: polygon polygon_pkey; Type: CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY polygon
    ADD CONSTRAINT polygon_pkey PRIMARY KEY (id);


SET search_path = model, pg_catalog;

--
-- Name: class class_code_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class
    ADD CONSTRAINT class_code_key UNIQUE (code);


--
-- Name: class_i18n class_i18n_class_code_language_code_attribute_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_i18n
    ADD CONSTRAINT class_i18n_class_code_language_code_attribute_key UNIQUE (class_code, language_code, attribute);


--
-- Name: class_i18n class_i18n_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_i18n
    ADD CONSTRAINT class_i18n_pkey PRIMARY KEY (id);


--
-- Name: class_inheritance class_inheritance_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_inheritance
    ADD CONSTRAINT class_inheritance_pkey PRIMARY KEY (id);


--
-- Name: class_inheritance class_inheritance_super_id_sub_id_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_inheritance
    ADD CONSTRAINT class_inheritance_super_id_sub_id_key UNIQUE (super_code, sub_code);


--
-- Name: class class_name_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class
    ADD CONSTRAINT class_name_key UNIQUE (name);


--
-- Name: class class_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class
    ADD CONSTRAINT class_pkey PRIMARY KEY (id);


--
-- Name: entity entity_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY entity
    ADD CONSTRAINT entity_pkey PRIMARY KEY (id);


--
-- Name: link link_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_pkey PRIMARY KEY (id);


--
-- Name: link_property link_property_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link_property
    ADD CONSTRAINT link_property_pkey PRIMARY KEY (id);


--
-- Name: property property_code_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_code_key UNIQUE (code);


--
-- Name: property_i18n property_i18n_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_i18n
    ADD CONSTRAINT property_i18n_pkey PRIMARY KEY (id);


--
-- Name: property_i18n property_i18n_property_code_language_code_attribute_key; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_i18n
    ADD CONSTRAINT property_i18n_property_code_language_code_attribute_key UNIQUE (property_code, language_code, attribute);


--
-- Name: property_inheritance property_inheritance_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_inheritance
    ADD CONSTRAINT property_inheritance_pkey PRIMARY KEY (id);


--
-- Name: property property_pkey; Type: CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_pkey PRIMARY KEY (id);


SET search_path = web, pg_catalog;

--
-- Name: form form_name_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY form
    ADD CONSTRAINT form_name_key UNIQUE (name);


--
-- Name: form form_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY form
    ADD CONSTRAINT form_pkey PRIMARY KEY (id);


--
-- Name: group group_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "group"
    ADD CONSTRAINT group_pkey PRIMARY KEY (id);


--
-- Name: hierarchy_form hierarchy_form_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy_form
    ADD CONSTRAINT hierarchy_form_pkey PRIMARY KEY (id);


--
-- Name: hierarchy hierarchy_name_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy
    ADD CONSTRAINT hierarchy_name_key UNIQUE (name);


--
-- Name: hierarchy hierarchy_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy
    ADD CONSTRAINT hierarchy_pkey PRIMARY KEY (id);


--
-- Name: i18n i18n_name_language_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY i18n
    ADD CONSTRAINT i18n_name_language_key UNIQUE (name, language);


--
-- Name: i18n i18n_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY i18n
    ADD CONSTRAINT i18n_pkey PRIMARY KEY (id);


--
-- Name: system_log log_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY system_log
    ADD CONSTRAINT log_pkey PRIMARY KEY (id);


--
-- Name: settings settings_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY settings
    ADD CONSTRAINT settings_pkey PRIMARY KEY (id);


--
-- Name: user unsubscribe_code_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT unsubscribe_code_key UNIQUE (unsubscribe_code);


--
-- Name: user_bookmarks user_bookmarks_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_bookmarks
    ADD CONSTRAINT user_bookmarks_pkey PRIMARY KEY (id);


--
-- Name: user_bookmarks user_bookmarks_user_id_entity_id_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_bookmarks
    ADD CONSTRAINT user_bookmarks_user_id_entity_id_key UNIQUE (user_id, entity_id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user_log user_log_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_log
    ADD CONSTRAINT user_log_pkey PRIMARY KEY (id);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_settings user_settings_pkey; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT user_settings_pkey PRIMARY KEY (id);


--
-- Name: user_settings user_settings_user_id_name_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT user_settings_user_id_name_key UNIQUE (user_id, name);


--
-- Name: user user_username_key; Type: CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_username_key UNIQUE (username);


SET search_path = gis, pg_catalog;

--
-- Name: point update_modified; Type: TRIGGER; Schema: gis; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON point FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: linestring update_modified; Type: TRIGGER; Schema: gis; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON linestring FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: polygon update_modified; Type: TRIGGER; Schema: gis; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON polygon FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


SET search_path = model, pg_catalog;

--
-- Name: entity on_delete_entity; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER on_delete_entity BEFORE DELETE ON entity FOR EACH ROW EXECUTE PROCEDURE delete_entity_related();


--
-- Name: link_property on_delete_link_property; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER on_delete_link_property AFTER DELETE ON link_property FOR EACH ROW EXECUTE PROCEDURE delete_link_dates();


--
-- Name: class update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON class FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: class_inheritance update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON class_inheritance FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: property update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON property FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: entity update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON entity FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: link update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON link FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: property_inheritance update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON property_inheritance FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: link_property update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON link_property FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: class_i18n update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON class_i18n FOR EACH ROW EXECUTE PROCEDURE update_modified();


--
-- Name: property_i18n update_modified; Type: TRIGGER; Schema: model; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON property_i18n FOR EACH ROW EXECUTE PROCEDURE update_modified();


SET search_path = web, pg_catalog;

--
-- Name: user update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON "user" FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: group update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON "group" FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: user_settings update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON user_settings FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: user_bookmarks update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON user_bookmarks FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: hierarchy update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON hierarchy FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: form update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON form FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: hierarchy_form update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON hierarchy_form FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


--
-- Name: i18n update_modified; Type: TRIGGER; Schema: web; Owner: openatlas
--

CREATE TRIGGER update_modified BEFORE UPDATE ON i18n FOR EACH ROW EXECUTE PROCEDURE model.update_modified();


SET search_path = gis, pg_catalog;

--
-- Name: linestring linestring_entity_id_fkey; Type: FK CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY linestring
    ADD CONSTRAINT linestring_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: point point_entity_id_fkey; Type: FK CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY point
    ADD CONSTRAINT point_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: polygon polygon_entity_id_fkey; Type: FK CONSTRAINT; Schema: gis; Owner: openatlas
--

ALTER TABLE ONLY polygon
    ADD CONSTRAINT polygon_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


SET search_path = model, pg_catalog;

--
-- Name: class_i18n class_i18n_class_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_i18n
    ADD CONSTRAINT class_i18n_class_code_fkey FOREIGN KEY (class_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: class_inheritance class_inheritance_sub_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_inheritance
    ADD CONSTRAINT class_inheritance_sub_code_fkey FOREIGN KEY (sub_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: class_inheritance class_inheritance_super_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY class_inheritance
    ADD CONSTRAINT class_inheritance_super_code_fkey FOREIGN KEY (super_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: entity entity_class_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY entity
    ADD CONSTRAINT entity_class_code_fkey FOREIGN KEY (class_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link link_domain_id_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link link_property_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_property_code_fkey FOREIGN KEY (property_code) REFERENCES property(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link_property link_property_domain_id_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link_property
    ADD CONSTRAINT link_property_domain_id_fkey FOREIGN KEY (domain_id) REFERENCES link(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link_property link_property_property_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link_property
    ADD CONSTRAINT link_property_property_code_fkey FOREIGN KEY (property_code) REFERENCES property(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link_property link_property_range_id_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link_property
    ADD CONSTRAINT link_property_range_id_fkey FOREIGN KEY (range_id) REFERENCES entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: link link_range_id_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY link
    ADD CONSTRAINT link_range_id_fkey FOREIGN KEY (range_id) REFERENCES entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property property_domain_class_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_domain_class_code_fkey FOREIGN KEY (domain_class_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property_i18n property_i18n_property_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_i18n
    ADD CONSTRAINT property_i18n_property_code_fkey FOREIGN KEY (property_code) REFERENCES property(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property_inheritance property_inheritance_sub_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_inheritance
    ADD CONSTRAINT property_inheritance_sub_code_fkey FOREIGN KEY (sub_code) REFERENCES property(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property_inheritance property_inheritance_super_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property_inheritance
    ADD CONSTRAINT property_inheritance_super_code_fkey FOREIGN KEY (super_code) REFERENCES property(code) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: property property_range_class_code_fkey; Type: FK CONSTRAINT; Schema: model; Owner: openatlas
--

ALTER TABLE ONLY property
    ADD CONSTRAINT property_range_class_code_fkey FOREIGN KEY (range_class_code) REFERENCES class(code) ON UPDATE CASCADE ON DELETE CASCADE;


SET search_path = web, pg_catalog;

--
-- Name: hierarchy_form hierarchy_form_form_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy_form
    ADD CONSTRAINT hierarchy_form_form_id_fkey FOREIGN KEY (form_id) REFERENCES form(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: hierarchy_form hierarchy_form_hierarchy_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy_form
    ADD CONSTRAINT hierarchy_form_hierarchy_id_fkey FOREIGN KEY (hierarchy_id) REFERENCES hierarchy(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: hierarchy hierarchy_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY hierarchy
    ADD CONSTRAINT hierarchy_id_fkey FOREIGN KEY (id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_bookmarks user_bookmarks_entity_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_bookmarks
    ADD CONSTRAINT user_bookmarks_entity_id_fkey FOREIGN KEY (entity_id) REFERENCES model.entity(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user_bookmarks user_bookmarks_user_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_bookmarks
    ADD CONSTRAINT user_bookmarks_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- Name: user user_group_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY "user"
    ADD CONSTRAINT user_group_id_fkey FOREIGN KEY (group_id) REFERENCES "group"(id) ON UPDATE CASCADE;


--
-- Name: user_settings user_settings_user_id_fkey; Type: FK CONSTRAINT; Schema: web; Owner: openatlas
--

ALTER TABLE ONLY user_settings
    ADD CONSTRAINT user_settings_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id) ON UPDATE CASCADE ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

