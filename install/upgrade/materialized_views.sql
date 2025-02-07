-------------------------------
-- DROP EXISTING OBJECTS
-------------------------------

-- Drop triggers (if they exist)
DROP TRIGGER IF EXISTS trigger_refresh_types_views ON model.entity;
DROP TRIGGER IF EXISTS trigger_refresh_reference_systems_view_entity ON model.entity;
DROP TRIGGER IF EXISTS trigger_refresh_get_file_info_view ON model.entity;
DROP TRIGGER IF EXISTS trigger_refresh_reference_systems_view_web ON web.reference_system;

-- Drop functions (if they exist)
DROP FUNCTION IF EXISTS refresh_types_views() CASCADE;
DROP FUNCTION IF EXISTS refresh_reference_systems_view() CASCADE;
DROP FUNCTION IF EXISTS refresh_get_file_info_view() CASCADE;

-- Drop unique indexes (if they exist)
DROP INDEX IF EXISTS cidoc_properties_idx;
DROP INDEX IF EXISTS cidoc_classes_idx;
DROP INDEX IF EXISTS reference_systems_idx;
DROP INDEX IF EXISTS types_without_count_idx;
DROP INDEX IF EXISTS types_with_count_idx;
DROP INDEX IF EXISTS get_file_info_idx;

-- Drop materialized views in the proper order (CASCADE drops dependent objects)
DROP MATERIALIZED VIEW IF EXISTS model.get_file_info CASCADE;
DROP MATERIALIZED VIEW IF EXISTS model.types_with_count CASCADE;
DROP MATERIALIZED VIEW IF EXISTS model.types_without_count CASCADE;
DROP MATERIALIZED VIEW IF EXISTS model.reference_systems CASCADE;
DROP MATERIALIZED VIEW IF EXISTS model.cidoc_classes CASCADE;
DROP MATERIALIZED VIEW IF EXISTS model.cidoc_properties CASCADE;


-------------------------------
-- RECREATE MATERIALIZED VIEWS
-------------------------------

-- cidoc_properties
CREATE MATERIALIZED VIEW model.cidoc_properties AS
SELECT
    p.code,
    p.comment,
    p.domain_class_code,
    p.range_class_code,
    p.name,
    p.name_inverse,
    COUNT(l.id) AS count
FROM model.property p
LEFT JOIN model.link l ON p.code = l.property_code
GROUP BY
    p.code,
    p.comment,
    p.domain_class_code,
    p.range_class_code,
    p.name,
    p.name_inverse;

ALTER MATERIALIZED VIEW model.cidoc_properties OWNER TO openatlas;

-- cidoc_classes
CREATE MATERIALIZED VIEW model.cidoc_classes AS
SELECT
    c.code,
    c.name,
    c.comment,
    COUNT(e.id) AS count
FROM model.cidoc_class c
LEFT JOIN model.entity e ON c.code = e.cidoc_class_code
GROUP BY
    c.code,
    c.name,
    c.comment;

ALTER MATERIALIZED VIEW model.cidoc_classes OWNER TO openatlas;

-- reference_systems
CREATE MATERIALIZED VIEW model.reference_systems AS
SELECT
    e.id,
    e.name,
    e.cidoc_class_code,
    e.description,
    e.openatlas_class_name,
    e.created,
    e.modified,
    rs.website_url,
    rs.resolver_url,
    rs.identifier_example,
    rs.system,
    COUNT(l.id) AS count,
    array_to_json(
        array_agg((t.range_id, t.description))
        FILTER (WHERE t.range_id IS NOT NULL)
    ) AS types
FROM model.entity e
JOIN web.reference_system rs ON e.id = rs.entity_id
LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code = 'P67'
LEFT JOIN model.link t ON e.id = t.domain_id AND t.property_code = 'P2'
GROUP BY
    e.id,
    e.name,
    e.cidoc_class_code,
    e.description,
    e.openatlas_class_name,
    e.created,
    e.modified,
    rs.website_url,
    rs.resolver_url,
    rs.identifier_example,
    rs.system,
    rs.entity_id;

ALTER MATERIALIZED VIEW model.reference_systems OWNER TO openatlas;

-- types_without_count
CREATE MATERIALIZED VIEW model.types_without_count AS
SELECT
    e.id,
    e.name,
    e.cidoc_class_code,
    e.description,
    e.openatlas_class_name,
    e.created,
    e.modified,
    es.id AS super_id,
    0 AS count,
    0 AS count_property,
    COALESCE(to_char(e.begin_from, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS begin_from,
    COALESCE(to_char(e.begin_to, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS begin_to,
    COALESCE(to_char(e.end_from, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS end_from,
    COALESCE(to_char(e.end_to, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS end_to,
    e.begin_comment,
    e.end_comment,
    tns.entity_id AS non_selectable
FROM model.entity e
LEFT OUTER JOIN web.type_none_selectable tns ON e.id = tns.entity_id
LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code IN ('P127', 'P89')
LEFT JOIN model.entity es ON l.range_id = es.id
WHERE e.openatlas_class_name IN ('administrative_unit', 'type', 'type_tools')
GROUP BY e.id, es.id, tns.entity_id
ORDER BY e.name;

ALTER MATERIALIZED VIEW model.types_without_count OWNER TO openatlas;

-- types_with_count
CREATE MATERIALIZED VIEW model.types_with_count AS
SELECT
    e.id,
    e.name,
    e.cidoc_class_code,
    e.description,
    e.openatlas_class_name,
    e.created,
    e.modified,
    es.id AS super_id,
    COUNT(l2.id) AS count,
    COUNT(l3.id) AS count_property,
    COALESCE(to_char(e.begin_from, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS begin_from,
    COALESCE(to_char(e.begin_to, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS begin_to,
    COALESCE(to_char(e.end_from, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS end_from,
    COALESCE(to_char(e.end_to, 'YYYY-MM-DD HH24:MI:SS BC'), '') AS end_to,
    e.begin_comment,
    e.end_comment,
    tns.entity_id AS non_selectable
FROM model.entity e
LEFT OUTER JOIN web.type_none_selectable tns ON e.id = tns.entity_id
LEFT JOIN model.link l ON e.id = l.domain_id AND l.property_code IN ('P127', 'P89')
LEFT JOIN model.entity es ON l.range_id = es.id
LEFT JOIN model.link l2 ON e.id = l2.range_id AND l2.property_code IN ('P2', 'P89')
LEFT JOIN model.link l3 ON e.id = l3.type_id
WHERE e.openatlas_class_name IN ('administrative_unit', 'type', 'type_tools')
GROUP BY e.id, es.id, tns.entity_id
ORDER BY e.name;

ALTER MATERIALIZED VIEW model.types_with_count OWNER TO openatlas;

-- get_file_info
CREATE MATERIALIZED VIEW model.get_file_info AS
SELECT
    entity_id,
    public,
    creator,
    license_holder
FROM model.file_info;

ALTER MATERIALIZED VIEW model.get_file_info OWNER TO openatlas;


-------------------------------
-- CREATE UNIQUE INDEXES (Needed for CONCURRENT Refresh)
-------------------------------

CREATE UNIQUE INDEX cidoc_properties_idx ON model.cidoc_properties (code);
CREATE UNIQUE INDEX cidoc_classes_idx ON model.cidoc_classes (code);
CREATE UNIQUE INDEX reference_systems_idx ON model.reference_systems (id);
CREATE UNIQUE INDEX types_without_count_idx ON model.types_without_count (id);
CREATE UNIQUE INDEX types_with_count_idx ON model.types_with_count (id);
CREATE UNIQUE INDEX get_file_info_idx ON model.get_file_info (entity_id);


-------------------------------
-- INITIAL REFRESH OF ALL MATERIALIZED VIEWS
-------------------------------

REFRESH MATERIALIZED VIEW CONCURRENTLY model.cidoc_properties;
REFRESH MATERIALIZED VIEW CONCURRENTLY model.cidoc_classes;
REFRESH MATERIALIZED VIEW CONCURRENTLY model.reference_systems;
REFRESH MATERIALIZED VIEW CONCURRENTLY model.types_without_count;
REFRESH MATERIALIZED VIEW CONCURRENTLY model.types_with_count;
REFRESH MATERIALIZED VIEW CONCURRENTLY model.get_file_info;


-------------------------------
-- CREATE TRIGGER FUNCTIONS
-------------------------------

-- Function to refresh types_with_count and types_without_count
CREATE OR REPLACE FUNCTION refresh_types_views() RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY model.types_with_count;
    REFRESH MATERIALIZED VIEW CONCURRENTLY model.types_without_count;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to refresh reference_systems view
CREATE OR REPLACE FUNCTION refresh_reference_systems_view() RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY model.reference_systems;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- Function to refresh get_file_info view
CREATE OR REPLACE FUNCTION refresh_get_file_info_view() RETURNS TRIGGER AS $$
BEGIN
    REFRESH MATERIALIZED VIEW CONCURRENTLY model.get_file_info;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;


-------------------------------
-- CREATE TRIGGERS
-------------------------------

-- Trigger for types_with_count and types_without_count when model.entity is updated/inserted
CREATE TRIGGER trigger_refresh_types_views
AFTER INSERT OR UPDATE ON model.entity
FOR EACH ROW
WHEN (NEW.openatlas_class_name IN ('administrative_unit', 'type', 'type_tools'))
EXECUTE FUNCTION refresh_types_views();

-- Trigger for reference_systems when model.entity is updated/inserted
CREATE TRIGGER trigger_refresh_reference_systems_view_entity
AFTER INSERT OR UPDATE ON model.entity
FOR EACH ROW
WHEN (NEW.openatlas_class_name = 'reference_system')
EXECUTE FUNCTION refresh_reference_systems_view();

-- Trigger for reference_systems when web.reference_system is updated/inserted/deleted
CREATE TRIGGER trigger_refresh_reference_systems_view_web
AFTER INSERT OR UPDATE OR DELETE ON web.reference_system
FOR EACH ROW
EXECUTE FUNCTION refresh_reference_systems_view();

-- Trigger for get_file_info when model.entity is updated/inserted
CREATE TRIGGER trigger_refresh_get_file_info_view
AFTER INSERT OR UPDATE ON model.entity
FOR EACH ROW
WHEN (NEW.openatlas_class_name = 'file')
EXECUTE FUNCTION refresh_get_file_info_view();
