from typing import Any

from flask import url_for


def get_oa_ontology_uri() -> str:
    # TODO: In the future, host permanently at https://openatlas.eu/ontology/
    # or https://github.com/openatlas/ontology. For now, serve locally.
    try:
        return url_for('api_v1_lod.get_ontology', _external=True) + '#'
    except RuntimeError:
        return 'https://openatlas.eu/ontology/#'


def get_oa_ontology_graph():
    from rdflib import OWL, RDF, RDFS, Graph, Literal, Namespace, URIRef
    g = Graph()
    oa_base = get_oa_ontology_uri()
    oa = Namespace(oa_base)
    crm = Namespace('http://www.cidoc-crm.org/cidoc-crm/')
    g.bind('oa', oa)
    g.bind('crm', crm)
    g.bind('owl', OWL)

    ont_uri = URIRef(oa_base.rstrip('#'))
    g.add((ont_uri, RDF.type, OWL.Ontology))
    g.add((ont_uri, RDFS.label, Literal('OpenAtlas Extension Ontology', lang='en')))
    g.add((ont_uri, RDFS.comment, Literal(
        'Custom shortcuts and extensions for OpenAtlas CIDOC CRM / CRMarchaeo Linked Data. '
        'TODO: Host permanently at https://openatlas.eu/ontology/ or https://github.com/openatlas/ontology',
        lang='en')))

    # oa:has_relationship_to (E39 -> E39)
    p_rel = oa.has_relationship_to
    g.add((p_rel, RDF.type, OWL.ObjectProperty))
    g.add((p_rel, RDFS.label, Literal('has relationship to', lang='en')))
    g.add((p_rel, RDFS.domain, crm.E39_Actor))
    g.add((p_rel, RDFS.range, crm.E39_Actor))

    # oa:begins_in (E77 -> E53)
    p_b = oa.begins_in
    g.add((p_b, RDF.type, OWL.ObjectProperty))
    g.add((p_b, RDFS.label, Literal('begins in', lang='en')))
    g.add((p_b, RDFS.domain, crm.E77_Persistent_Item))
    g.add((p_b, RDFS.range, crm.E53_Place))

    # oa:ends_in (E77 -> E53)
    p_e = oa.ends_in
    g.add((p_e, RDF.type, OWL.ObjectProperty))
    g.add((p_e, RDFS.label, Literal('ends in', lang='en')))
    g.add((p_e, RDFS.domain, crm.E77_Persistent_Item))
    g.add((p_e, RDFS.range, crm.E53_Place))

    return g


def get_lod_context() -> dict[str, Any]:
    oa_uri = get_oa_ontology_uri()
    return {
        '@context': {
            '@version': 1.1,
            # Namespaces
            'crm': 'http://www.cidoc-crm.org/cidoc-crm/',
            'archaeo': 'http://www.cidoc-crm.org/cidoc-crm/CRMarchaeo/',
            'sci': 'http://www.ics.forth.gr/isl/CRMsci/',
            'geo': 'http://www.opengis.net/ont/geosparql#',
            'skos': 'http://www.w3.org/2004/02/skos/core#',
            'rdfs': 'http://www.w3.org/2000/01/rdf-schema#',
            'xsd': 'http://www.w3.org/2001/XMLSchema#',
            'as': 'https://www.w3.org/ns/activitystreams#',
            'oa': oa_uri,

            # Core JSON-LD aliases
            'id': '@id',
            'type': '@type',
            'label': 'rdfs:label',
            'description': 'crm:P3_has_note',

            # CIDOC CRM & CRMarchaeo Entity Classes
            'HumanMadeObject': 'crm:E22_Human-Made_Object',
            'BiologicalObject': 'crm:E20_Biological_Object',
            'Feature': 'archaeo:A6_Feature',
            'StratigraphicUnit': 'archaeo:A8_Stratigraphic_Unit',
            'Place': 'crm:E53_Place',
            'Person': 'crm:E21_Person',
            'Group': 'crm:E74_Group',
            'Activity': 'crm:E7_Activity',
            'Acquisition': 'crm:E8_Acquisition',
            'Production': 'crm:E12_Production',
            'Modification': 'crm:E11_Modification',
            'Move': 'crm:E9_Move',
            'Type': 'crm:E55_Type',
            'Document': 'crm:E31_Document',
            'LinguisticObject': 'crm:E33_Linguistic_Object',
            'Creation': 'crm:E65_Creation',
            'TimeSpan': 'crm:E52_Time-Span',
            'Dimension': 'crm:E54_Dimension',
            'Geometry': 'geo:Geometry',
            'Appellation': 'crm:E41_Appellation',

            # ActivityStreams Classes for Paging
            'OrderedCollectionPage': 'as:OrderedCollectionPage',
            'OrderedCollection': 'as:OrderedCollection',

            # Geometry & GIS (GeoSPARQL)
            'has_geometry': {'@id': 'geo:hasGeometry', '@type': '@id'},
            'as_wkt': {'@id': 'geo:asWKT', '@type': 'geo:wktLiteral'},

            # Chronology & Timespan
            'has_time_span': {'@id': 'crm:P4_has_time-span', '@type': '@id'},
            'begin_of_the_begin': {
                '@id': 'crm:P82a_begin_of_the_begin',
                '@type': 'xsd:dateTime'},
            'end_of_the_begin': {
                '@id': 'crm:P81a_end_of_the_begin',
                '@type': 'xsd:dateTime'},
            'begin_of_the_end': {
                '@id': 'crm:P81b_begin_of_the_end',
                '@type': 'xsd:dateTime'},
            'end_of_the_end': {
                '@id': 'crm:P82b_end_of_the_end',
                '@type': 'xsd:dateTime'},
            'begin_comment': {'@id': 'oa:begin_comment'},
            'end_comment': {'@id': 'oa:end_comment'},

            # Classification & Typology
            'has_type': {'@id': 'crm:P2_has_type', '@type': '@id'},
            'identified_by': {
                '@id': 'crm:P1_is_identified_by',
                '@type': '@id'},

            # Composition & Hierarchy
            'is_composed_of': {
                '@id': 'crm:P46_is_composed_of',
                '@type': '@id'},
            'forms_part_of': {
                '@id': 'crm:P46i_forms_part_of',
                '@type': '@id'},

            # Spatial Location
            'has_location': {
                '@id': 'crm:P53_has_former_or_current_location',
                '@type': '@id'},
            'is_location_of': {
                '@id': 'crm:P53i_is_former_or_current_location_of',
                '@type': '@id'},
            'falls_within': {'@id': 'crm:P89_falls_within', '@type': '@id'},
            'contains_place': {'@id': 'crm:P89i_contains', '@type': '@id'},

            # Events & Activities
            'took_place_at': {'@id': 'crm:P7_took_place_at', '@type': '@id'},
            'carried_out_by': {
                '@id': 'crm:P14_carried_out_by',
                '@type': '@id'},
            'performed': {'@id': 'crm:P14i_performed', '@type': '@id'},
            'had_participant': {
                '@id': 'crm:P11_had_participant',
                '@type': '@id'},
            'participated_in': {
                '@id': 'crm:P11i_participated_in',
                '@type': '@id'},
            'has_produced': {'@id': 'crm:P108_has_produced', '@type': '@id'},
            'was_produced_by': {
                '@id': 'crm:P108i_was_produced_by',
                '@type': '@id'},
            'has_modified': {'@id': 'crm:P31_has_modified', '@type': '@id'},
            'was_modified_by': {
                '@id': 'crm:P31i_was_modified_by',
                '@type': '@id'},
            'transferred_title_of': {
                '@id': 'crm:P24_transferred_title_of',
                '@type': '@id'},
            'title_transferred_through': {
                '@id': 'crm:P24i_changed_ownership_through',
                '@type': '@id'},
            'transferred_title_to': {
                '@id': 'crm:P22_transferred_title_to',
                '@type': '@id'},
            'title_transferred_to': {
                '@id': 'crm:P22i_acquired_title_through',
                '@type': '@id'},
            'transferred_title_from': {
                '@id': 'crm:P23_transferred_title_from',
                '@type': '@id'},
            'title_transferred_from': {
                '@id': 'crm:P23i_surrendered_title_through',
                '@type': '@id'},
            'current_owner': {
                '@id': 'crm:P52_has_current_owner',
                '@type': '@id'},
            'is_current_owner_of': {
                '@id': 'crm:P52i_is_current_owner_of',
                '@type': '@id'},
            'residence': {
                '@id': 'crm:P74_has_current_or_former_residence',
                '@type': '@id'},
            'residence_of': {
                '@id': 'crm:P74i_is_current_or_former_residence_of',
                '@type': '@id'},
            'has_member': {
                '@id': 'crm:P107_has_current_or_former_member',
                '@type': '@id'},
            'member_of': {
                '@id': 'crm:P107i_is_current_or_former_member_of',
                '@type': '@id'},
            'has_created': {'@id': 'crm:P94_has_created', '@type': '@id'},
            'was_created_by': {
                '@id': 'crm:P94i_was_created_by',
                '@type': '@id'},
            'moved': {'@id': 'crm:P25_moved', '@type': '@id'},
            'moved_from': {'@id': 'crm:P27_moved_from', '@type': '@id'},
            'moved_to': {'@id': 'crm:P26_moved_to', '@type': '@id'},
            'continued': {'@id': 'crm:P134_continued', '@type': '@id'},
            'was_continued_by': {
                '@id': 'crm:P134i_was_continued_by',
                '@type': '@id'},

            # Dimensions & Measurements
            'has_dimension': {'@id': 'crm:P43_has_dimension', '@type': '@id'},
            'value': {'@id': 'crm:P90_has_value', '@type': 'xsd:decimal'},
            'unit': {'@id': 'crm:P91_has_unit'},

            # Hierarchy of Types
            'has_broader_term': {
                '@id': 'crm:P127_has_broader_term',
                '@type': '@id'},
            'has_narrower_term': {
                '@id': 'crm:P127i_has_narrower_term',
                '@type': '@id'},

            # Texts, Inscriptions & Translations
            'carries': {'@id': 'crm:P128_carries', '@type': '@id'},
            'is_carried_by': {'@id': 'crm:P128i_is_carried_by', '@type': '@id'},
            'has_translation': {
                '@id': 'crm:P73_has_translation',
                '@type': '@id'},
            'is_translation_of': {
                '@id': 'crm:P73i_is_translation_of',
                '@type': '@id'},

            # References & Media
            'refers_to': {'@id': 'crm:P67_refers_to', '@type': '@id'},
            'is_referred_to_by': {
                '@id': 'crm:P67i_is_referred_to_by',
                '@type': '@id'},

            # OpenAtlas Custom Shortcuts
            'has_relationship_to': {
                '@id': 'oa:has_relationship_to',
                '@type': '@id'},
            'begins_in': {'@id': 'oa:begins_in', '@type': '@id'},
            'ends_in': {'@id': 'oa:ends_in', '@type': '@id'},

            # ActivityStreams Paging Properties
            'partOf': {'@id': 'as:partOf', '@type': '@id'},
            'first': {'@id': 'as:first', '@type': '@id'},
            'last': {'@id': 'as:last', '@type': '@id'},
            'prev': {'@id': 'as:prev', '@type': '@id'},
            'next': {'@id': 'as:next', '@type': '@id'},
            'startIndex': {'@id': 'as:startIndex', '@type': 'xsd:nonNegativeInteger'},
            'totalItems': {'@id': 'as:totalItems', '@type': 'xsd:nonNegativeInteger'},
            'orderedItems': {'@id': 'as:items', '@container': '@list'}
        }
    }
