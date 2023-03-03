import itertools
import json
import pathlib
from typing import Any, Union

from flask import Response, jsonify, request
from flask_restful import marshal

from openatlas import app
from openatlas.api.formats.csv import (
    export_csv_for_network_analysis, export_entities_csv)
from openatlas.api.formats.geojson import get_geojson, get_geojson_v2
from openatlas.api.formats.linked_places import get_linked_places_entity
from openatlas.api.formats.loud import get_loud_entities
from openatlas.api.formats.rdf import rdf_output
from openatlas.api.formats.xml import subunit_xml
from openatlas.api.resources.error import (
    EntityDoesNotExistError, LastEntityError, NoEntityAvailable, TypeIDError)
from openatlas.api.resources.model_mapper import (
    get_all_links_of_entities, get_all_links_of_entities_inverse)
from openatlas.api.resources.search import search
from openatlas.api.resources.search_validation import (
    iterate_validation)
from openatlas.api.resources.templates import (
    geojson_collection_template, geojson_pagination, linked_place_pagination,
    linked_places_template, subunit_template, loud_pagination, loud_template)
from openatlas.api.resources.util import (
    get_entities_by_type, get_key, link_parser_check,
    link_parser_check_inverse, parser_str_to_dict, remove_duplicate_entities)
from openatlas.models.entity import Entity


def resolve_entities(
        entities: list[Entity],
        parser: dict[str, Any],
        file_name: Union[int, str]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['type_id'] and not (
            entities := get_entities_by_type(entities, parser)
    ):  # pylint: disable=superfluous-parens
        # check disabled because of pylint bug, fixed in pylint 2.10.0
        raise TypeIDError
    if parser['search']:
        search_parser = parser_str_to_dict(parser['search'])
        if iterate_validation(search_parser):
            entities = search(entities, search_parser)
    if parser['export'] == 'csv':
        return export_entities_csv(entities, file_name)
    if parser['export'] == 'csvNetwork':
        return export_csv_for_network_analysis(entities, parser)
    if not entities:
        raise NoEntityAvailable
    result = get_json_output(
        sorting(
            remove_duplicate_entities(entities),
            parser),
        parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result['results'], parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['count'] == 'true':
        return jsonify(result['pagination']['entities'])
    if parser['download'] == 'true':
        return download(result, get_entities_template(parser), file_name)
    return marshal(result, get_entities_template(parser)), 200


def get_entities_template(parser: dict[str, str]) -> dict[str, Any]:
    if parser['format'] in ['geojson', 'geojson-v2']:
        return geojson_pagination()
    return linked_place_pagination(parser)


def sorting(entities: list[Entity], parser: dict[str, Any]) -> list[Entity]:
    if 'latest' in request.path:
        return entities
    return sorted(
        entities,
        key=lambda entity: get_key(entity, parser),
        reverse=bool(parser['sort'] == 'desc'))


def get_entity_formatted(
        entity: Entity,
        parser: dict[str, Any]) -> dict[str, Any]:
    if parser['format'] == 'geojson':
        return get_geojson([entity], parser)
    if parser['format'] == 'geojson-v2':
        return get_geojson_v2([entity], parser)
    return get_linked_places_entity(
        entity,
        get_all_links_of_entities(entity.id),
        get_all_links_of_entities_inverse(entity.id),
        parser)


def resolve_entity(
        entity: Entity,
        parser: dict[str, Any]) \
        -> Union[Response, dict[str, Any], tuple[Any, int]]:
    if parser['export'] == 'csv':
        export_entities_csv(entity, entity.name)
    if parser['export'] == 'csvNetwork':
        export_csv_for_network_analysis([entity], parser)
    result = get_entity_formatted(entity, parser)
    if parser['format'] in app.config['RDF_FORMATS']:
        return Response(
            rdf_output(result, parser),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    template = geojson_collection_template() \
        if parser['format'] in ['geojson', 'geojson-v2'] \
        else linked_places_template(parser['show'])
    if parser['download']:
        download(result, template, entity.id)
    return marshal(result, template), 200


def resolve_subunits(
        subunit: list[dict[str, Any]],
        parser: dict[str, Any],
        name: str) -> Union[Response, dict[str, Any], tuple[Any, int]]:
    out = {'collection' if parser['format'] == 'xml' else name: subunit}
    if parser['count']:
        return jsonify(len(out[name]))
    if parser['format'] == 'xml':
        if parser['download']:
            return Response(
                subunit_xml(out),
                mimetype='application/xml',
                headers={
                    'Content-Disposition': f'attachment;filename={name}.xml'})
        return Response(
            subunit_xml(out),
            mimetype=app.config['RDF_FORMATS'][parser['format']])
    if parser['download']:
        download(out, subunit_template(name), name)
    return marshal(out, subunit_template(name)), 200


def get_json_output(
        entities: list[Entity],
        parser: dict[str, Any]) -> dict[str, Any]:
    total = [e.id for e in entities]
    count = len(total)
    parser['limit'] = count if parser['limit'] == 0 else parser['limit']
    e_list = list(itertools.islice(total, 0, None, int(parser['limit'])))
    index = [{'page': num + 1, 'startId': i} for num, i in enumerate(e_list)]
    parser['first'] = get_by_page(index, parser) \
        if parser['page'] else parser['first']
    total = get_start_entity(total, parser) \
        if parser['last'] or parser['first'] else total
    j = [i for i, x in enumerate(entities) if x.id == total[0]]
    new_entities = [e for idx, e in enumerate(entities[j[0]:])]
    return {
        "results": get_entities_formatted(new_entities, parser),
        "pagination": {
            'entitiesPerPage': int(parser['limit']),
            'entities': count,
            'index': index,
            'totalPages': len(index)}}


def get_entities_formatted(
        entities_all: list[Entity],
        parser: dict[str, Any]) -> list[dict[str, Any]]:
    entities = entities_all[:int(parser['limit'])]
    if parser['format'] == 'geojson':
        return [get_geojson(entities, parser)]
    if parser['format'] == 'geojson-v2':
        return [get_geojson_v2(entities, parser)]
    entities_dict: dict[str, Any] = {}
    for entity in entities:
        entities_dict[entity.id] = {
            'entity': entity,
            'links': [],
            'links_inverse': []}
    for link_ in link_parser_check(entities, parser):
        entities_dict[link_.domain.id]['links'].append(link_)
    for link_ in link_parser_check_inverse(entities, parser):
        entities_dict[link_.range.id]['links_inverse'].append(link_)
    result = []
    for item in entities_dict.values():
        result.append(
            get_linked_places_entity(
                item['entity'],
                item['links'],
                item['links_inverse'],
                parser))
    return result



# def parse_loud_context() -> dict[str, str]:
#     file_path = pathlib.Path(app.root_path) / 'api' / 'linked-art.json'
#     with open(file_path) as f:
#         output = {}
#         for key, value in json.load(f)['@context'].items():
#             if isinstance(value, dict):
#                 output[value['@id']] = key
#                 if '@context' in value.keys():
#                     for key2, value2 in value['@context'].items():
#                         if isinstance(value2, dict):
#                             output[value2['@id']] = key2
#     return output


def get_start_entity(total: list[int], parser: dict[str, Any]) -> list[Any]:
    if parser['first'] and int(parser['first']) in total:
        return list(itertools.islice(
            total,
            total.index(int(parser['first'])),
            None))
    if parser['last'] and int(parser['last']) in total:
        if not (out := list(itertools.islice(
                total,
                total.index(int(parser['last'])) + 1,
                None))):
            raise LastEntityError
        return out
    raise EntityDoesNotExistError


def get_by_page(
        index: list[dict[str, Any]],
        parser: dict[str, Any]) -> dict[str, Any]:
    page = parser['page'] \
        if parser['page'] < index[-1]['page'] else index[-1]['page']
    return [entry['startId'] for entry in index if entry['page'] == page][0]


def download(
        data: Union[list[Any], dict[Any, Any]],
        template: dict[Any, Any],
        name: Union[str, int]) -> Response:
    return Response(
        json.dumps(marshal(data, template)),
        mimetype='application/json',
        headers={'Content-Disposition': f'attachment;filename={name}.json'})


parse_loud_context = {"crm:E1_CRM_Entity": "CRMEntity", "crm:E2_Temporal_Entity": "TemporalEntity", "crm:E3_Condition_State": "ConditionState", "crm:E4_Period": "Period", "crm:P9_consists_of": "part", "crm:P9i_forms_part_of": "part_of", "la:member_of": "member_of", "crm:E5_Event": "Event", "crm:E6_Destruction": "Destruction", "crm:E7_Activity": "Activity", "crm:E8_Acquisition": "Acquisition", "crm:E9_Move": "Move", "crm:E10_Transfer_of_Custody": "TransferOfCustody", "crm:E11_Modification": "Modification", "crm:E12_Production": "Production", "crm:E13_Attribute_Assignment": "AttributeAssignment", "crm:E14_Condition_Assessment": "ConditionAssessment", "crm:E15_Identifier_Assignment": "IdentifierAssignment", "crm:E16_Measurement": "Measurement", "crm:E17_Type_Assignment": "TypeAssignment", "crm:E18_Physical_Thing": "PhysicalThing", "crm:P46_is_composed_of": "part", "crm:P46i_forms_part_of": "part_of", "crm:E19_Physical_Object": "PhysicalObject", "crm:E20_Biological_Object": "BiologicalObject", "crm:E21_Person": "Person", "crm:P107_has_current_or_former_member": "member", "crm:P107i_is_current_or_former_member_of": "member_of", "crm:E22_Human-Made_Object": "HumanMadeObject", "crm:E24_Physical_Human-Made_Thing": "PhysicalHumanMadeThing", "crm:E25_Human-Made_Feature": "HumanMadeFeature", "crm:E26_Physical_Feature": "PhysicalFeature", "crm:E27_Site": "Site", "crm:E28_Conceptual_Object": "ConceptualObject", "crm:E29_Design_or_Procedure": "DesignOrProcedure", "crm:E30_Right": "Right", "crm:P148_has_component": "c_part", "crm:P148i_is_component_of": "c_part_of", "crm:E31_Document": "Document", "crm:E32_Authority_Document": "AuthorityDocument", "crm:E33_Linguistic_Object": "LinguisticObject", "crm:P106_is_composed_of": "part", "crm:P106i_forms_part_of": "part_of", "crm:E34_Inscription": "Inscription", "crm:E35_Title": "Title", "crm:E36_Visual_Item": "VisualItem", "crm:E37_Mark": "Mark", "crm:E39_Actor": "Actor", "crm:E41_Appellation": "Appellation", "crm:E42_Identifier": "Identifier", "crm:E52_Time-Span": "TimeSpan", "crm:P86i_contains": "part", "crm:P86_falls_within": "part_of", "crm:E53_Place": "Place", "crm:P89i_contains": "part", "crm:P89_falls_within": "part_of", "crm:E54_Dimension": "Dimension", "crm:E55_Type": "Type", "skos:narrower": "narrower", "skos:broader": "broader", "crm:E56_Language": "Language", "crm:E57_Material": "Material", "crm:E58_Measurement_Unit": "MeasurementUnit", "crm:E63_Beginning_of_Existence": "BeginningOfExistence", "crm:E64_End_of_Existence": "EndOfExistence", "crm:E65_Creation": "Creation", "crm:E66_Formation": "Formation", "crm:E67_Birth": "Birth", "crm:E68_Dissolution": "Dissolution", "crm:E69_Death": "Death", "crm:E70_Thing": "Thing", "crm:E71_Human-Made_Thing": "HumanMadeThing", "crm:E72_Legal_Object": "LegalObject", "crm:E73_Information_Object": "InformationObject", "crm:E74_Group": "Group", "crm:E77_Persistent_Item": "PersistentItem", "crm:E78_Curated_Holding": "CuratedHolding", "crm:E79_Part_Addition": "PartAddition", "crm:E80_Part_Removal": "PartRemoval", "crm:E81_Transformation": "Transformation", "crm:E83_Type_Creation": "TypeCreation", "crm:E85_Joining": "Joining", "crm:E86_Leaving": "Leaving", "crm:E87_Curation_Activity": "CurationActivity", "crm:E89_Propositional_Object": "PropositionalObject", "crm:E90_Symbolic_Object": "SymbolicObject", "crm:E92_Spacetime_Volume": "SpacetimeVolume", "crm:E93_Presence": "Presence", "crm:E96_Purchase": "Purchase", "crm:E97_Monetary_Amount": "MonetaryAmount", "crm:E98_Currency": "Currency", "crm:E99_Product_Type": "ProductType", "crm:E33_E41_Linguistic_Appellation": "Name", "crm:P1_is_identified_by": "identified_by", "crm:P1i_identifies": "identifies", "crm:P2_has_type": "classified_as", "crm:P2i_is_type_of": "type_of", "crm:P3_has_note": "note", "crm:P4_has_time-span": "timespan", "crm:P4i_is_time-span_of": "timespan_of", "crm:P5_consists_of": "subState", "crm:P5i_forms_part_of": "subState_of", "crm:P7_took_place_at": "took_place_at", "crm:P7i_witnessed": "location_of", "crm:P8_took_place_on_or_within": "took_place_on_or_within", "crm:P8i_witnessed": "witnessed", "crm:P10_falls_within": "falls_within", "crm:P10i_contains": "contains", "crm:P11_had_participant": "participant", "crm:P11i_participated_in": "participated_in", "crm:P12_occurred_in_the_presence_of": "involved", "crm:P12i_was_present_at": "present_at", "crm:P13_destroyed": "destroyed", "crm:P13i_was_destroyed_by": "destroyed_by", "crm:P14_carried_out_by": "carried_out_by", "crm:P14i_performed": "carried_out", "crm:P15_was_influenced_by": "influenced_by", "crm:P15i_influenced": "influenced", "crm:P16_used_specific_object": "used_specific_object", "crm:P16i_was_used_for": "used_for", "crm:P17_was_motivated_by": "motivated_by", "crm:P17i_motivated": "motivated", "crm:P19_was_intended_use_of": "intended_use_of", "crm:P19i_was_made_for": "made_for", "crm:P20_had_specific_purpose": "specific_purpose", "crm:P20i_was_purpose_of": "specific_purpose_of", "crm:P21_had_general_purpose": "general_purpose", "crm:P21i_was_purpose_of": "purpose_of", "crm:P22_transferred_title_to": "transferred_title_to", "crm:P22i_acquired_title_through": "acquired_title_through", "crm:P23_transferred_title_from": "transferred_title_from", "crm:P23i_surrendered_title_through": "surrendered_title_through", "crm:P24_transferred_title_of": "transferred_title_of", "crm:P24i_changed_ownership_through": "changed_ownership_through", "crm:P25_moved": "moved", "crm:P25i_moved_by": "moved_by", "crm:P26_moved_to": "moved_to", "crm:P26i_was_destination_of": "destination_of", "crm:P27_moved_from": "moved_from", "crm:P27i_was_origin_of": "origin_of", "crm:P28_custody_surrendered_by": "transferred_custody_from", "crm:P28i_surrendered_custody_through": "surrendered_custody_through", "crm:P29_custody_received_by": "transferred_custody_to", "crm:P29i_received_custody_through": "acquired_custody_through", "crm:P30_transferred_custody_of": "transferred_custody_of", "crm:P30i_custody_transferred_through": "custody_transferred_through", "crm:P31_has_modified": "modified", "crm:P31i_was_modified_by": "modified_by", "crm:P32_used_general_technique": "technique", "crm:P32i_was_technique_of": "technique_of", "crm:P33_used_specific_technique": "specific_technique", "crm:P33i_was_used_by": "used_by", "crm:P34_concerned": "concerned", "crm:P34i_was_assessed_by": "assessed_by", "crm:P35_has_identified": "identified", "crm:P35i_was_identified_by": "condition_identified_by", "crm:P37_assigned": "assigned_identifier", "crm:P37i_was_assigned_by": "identifier_assigned_by", "crm:P38_deassigned": "deassigned", "crm:P38i_was_deassigned_by": "deassigned_by", "crm:P39_measured": "measured", "crm:P39i_was_measured_by": "measured_by", "crm:P40_observed_dimension": "observed_dimension", "crm:P40i_was_observed_in": "observed_in", "crm:P41_classified": "classified", "crm:P41i_was_classified_by": "classified_by", "crm:P42_assigned": "assigned_type", "crm:P42i_was_assigned_by": "type_assigned_by", "crm:P43_has_dimension": "dimension", "crm:P43i_is_dimension_of": "dimension_of", "crm:P44_has_condition": "condition", "crm:P44i_is_condition_of": "condition_of", "crm:P45_consists_of": "made_of", "crm:P45i_is_incorporated_in": "incorporated_in", "crm:P48_has_preferred_identifier": "preferred_identifier", "crm:P48i_is_preferred_identifier_of": "preferred_identifier_of", "crm:P49_has_former_or_current_keeper": "former_or_current_keeper", "crm:P49i_is_former_or_current_keeper_of": "former_or_current_keeper_of", "crm:P50_has_current_keeper": "current_custodian", "crm:P50i_is_current_keeper_of": "current_custodian_of", "crm:P51_has_former_or_current_owner": "former_or_current_owner", "crm:P51i_is_former_or_current_owner_of": "former_or_current_owner_of", "crm:P52_has_current_owner": "current_owner", "crm:P52i_is_current_owner_of": "current_owner_of", "crm:P53_has_former_or_current_location": "former_or_current_location", "crm:P53i_is_former_or_current_location_of": "former_or_current_location_of", "crm:P54_has_current_permanent_location": "current_permanent_location", "crm:P54i_is_current_permanent_location_of": "current_permanent_location_of", "crm:P55_has_current_location": "current_location", "crm:P55i_currently_holds": "currently_holds", "crm:P56_bears_feature": "bears", "crm:P56i_is_found_on": "found_on", "crm:P57_has_number_of_parts": "number_of_parts", "crm:P59_has_section": "section", "crm:P59i_is_located_on_or_within": "located_on_or_within", "crm:P62_depicts": "depicts", "crm:P62i_is_depicted_by": "depicted_by", "crm:P65_shows_visual_item": "shows", "crm:P65i_is_shown_by": "shown_by", "crm:P67_refers_to": "refers_to", "crm:P67i_is_referred_to_by": "referred_to_by", "crm:P68_foresees_use_of": "foresees_use_of", "crm:P68i_use_foreseen_by": "use_foreseen_by", "crm:P69_is_associated_with": "associated_with", "crm:P70_documents": "documents", "crm:P70i_is_documented_in": "documented_in", "crm:P71_lists": "lists", "crm:P71i_is_listed_in": "listed_in", "crm:P72_has_language": "language", "crm:P72i_is_language_of": "language_of", "crm:P73_has_translation": "translation", "crm:P73i_is_translation_of": "translation_of", "crm:P74_has_current_or_former_residence": "residence", "crm:P74i_is_current_or_former_residence_of": "current_or_former_residence_of", "crm:P75_possesses": "possesses", "crm:P75i_is_possessed_by": "possessed_by", "crm:P76_has_contact_point": "contact_point", "crm:P76i_provides_access_to": "provides_access_to", "crm:P79_beginning_is_qualified_by": "beginning_is_qualified_by", "crm:P80_end_is_qualified_by": "end_is_qualified_by", "crm:P81_ongoing_throughout": "ongoing_throughout", "crm:P82_at_some_time_within": "at_some_time_within", "crm:P90_has_value": "value", "crm:P91_has_unit": "unit", "crm:P91i_is_unit_of": "unit_of", "crm:P92_brought_into_existence": "brought_into_existence", "crm:P92i_was_brought_into_existence_by": "brought_into_existence_by", "crm:P93_took_out_of_existence": "took_out_of_existence", "crm:P93i_was_taken_out_of_existence_by": "taken_out_of_existence_by", "crm:P94_has_created": "created", "crm:P94i_was_created_by": "created_by", "crm:P95_has_formed": "formed", "crm:P95i_was_formed_by": "formed_by", "crm:P96_by_mother": "by_mother", "crm:P96i_gave_birth": "gave_birth", "crm:P97_from_father": "from_father", "crm:P97i_was_father_for": "father_for", "crm:P98_brought_into_life": "brought_into_life", "crm:P98i_was_born": "born", "crm:P99_dissolved": "dissolved", "crm:P99i_was_dissolved_by": "dissolved_by", "crm:P100_was_death_of": "death_of", "crm:P100i_died_in": "died", "crm:P101_had_as_general_use": "general_use", "crm:P101i_was_use_of": "use_of", "crm:P102_has_title": "title", "crm:P102i_is_title_of": "title_of", "crm:P103_was_intended_for": "intended_for", "crm:P103i_was_intention_of": "intention_of", "crm:P104_is_subject_to": "subject_to", "crm:P104i_applies_to": "applies_to", "crm:P105_right_held_by": "right_held_by", "crm:P105i_has_right_on": "right_on", "crm:P108_has_produced": "produced", "crm:P108i_was_produced_by": "produced_by", "crm:P109_has_current_or_former_curator": "current_or_former_curator", "crm:P109i_is_current_or_former_curator_of": "current_or_former_curator_of", "crm:P110_augmented": "augmented", "crm:P110i_was_augmented_by": "augmented_by", "crm:P111_added": "added", "crm:P111i_was_added_by": "added_by", "crm:P112_diminished": "diminished", "crm:P112i_was_diminished_by": "diminished_by", "crm:P113_removed": "removed", "crm:P113i_was_removed_by": "removed_by", "crm:P121_overlaps_with": "overlaps_with", "crm:P122_borders_with": "borders_with", "crm:P123_resulted_in": "resulted_in", "crm:P123i_resulted_from": "resulted_from", "crm:P124_transformed": "transformed", "crm:P124i_was_transformed_by": "transformed_by", "crm:P125_used_object_of_type": "used_object_of_type", "crm:P125i_was_type_of_object_used_in": "type_of_object_used_in", "crm:P126_employed": "employed", "crm:P126i_was_employed_in": "employed_in", "crm:P128_carries": "carries", "crm:P128i_is_carried_by": "carried_by", "crm:P129_is_about": "about", "crm:P129i_is_subject_of": "subject_of", "crm:P130_shows_features_of": "shows_features_of", "crm:P130i_features_are_also_found_on": "features_are_also_found_on", "crm:P132_overlaps_with": "volume_overlaps_with", "crm:P133_is_separated_from": "distinct_from", "crm:P134_continued": "continued", "crm:P134i_was_continued_by": "continued_by", "crm:P135_created_type": "created_type", "crm:P135i_was_created_by": "type_created_by", "crm:P136_was_based_on": "based_on", "crm:P136i_supported_type_creation": "supported_type_creation", "crm:P137_exemplifies": "exemplifies", "crm:P137i_is_exemplified_by": "exemplified_by", "crm:P138_represents": "represents", "crm:P138i_has_representation": "representation", "crm:P139_has_alternative_form": "alternative", "crm:P140_assigned_attribute_to": "assigned_to", "crm:P140i_was_attributed_by": "attributed_by", "crm:P141_assigned": "assigned", "crm:P141i_was_assigned_by": "assigned_by", "crm:P142_used_constituent": "used_constituent", "crm:P142i_was_used_in": "used_in", "crm:P143_joined": "joined", "crm:P143i_was_joined_by": "joined_by", "crm:P144_joined_with": "joined_with", "crm:P144i_gained_member_by": "gained_member_by", "crm:P145_separated": "separated", "crm:P145i_left_by": "left_by", "crm:P146_separated_from": "separated_from", "crm:P146i_lost_member_by": "lost_member_by", "crm:P147_curated": "curated", "crm:P147i_was_curated_by": "curated_by", "crm:P150_defines_typical_parts_of": "defines_typical_parts_of", "crm:P150i_defines_typical_wholes_for": "defines_typical_wholes_for", "crm:P151_was_formed_from": "formed_from", "crm:P151i_participated_in": "participated_in_formation", "crm:P152_has_parent": "parent", "crm:P152i_is_parent_of": "parent_of", "crm:P156_occupies": "occupies", "crm:P156i_is_occupied_by": "occupied_by", "crm:P157_is_at_rest_relative_to": "at_rest_relative_to", "crm:P157i_provides_reference_space_for": "provides_reference_space_for", "crm:P160_has_temporal_projection": "temporal_projection", "crm:P161_has_spatial_projection": "spatial_projection", "crm:P164_during": "during", "crm:P164i_was_time-span_of": "timespan_of_presence", "crm:P165_incorporates": "presence_of", "crm:P165i_is_incorporated_in": "incorporated_by", "crm:P166_was_a_presence_of": "a_presence_of", "crm:P166i_had_presence": "presence", "crm:P167_at": "at", "crm:P167i_was_place_of": "place_of", "crm:P168_place_is_defined_by": "defined_by", "crm:P169i_spacetime_volume_is_defined_by": "spacetime_volume_is_defined_by", "crm:P170i_time_is_defined_by": "time_is_defined_by", "crm:P171_at_some_place_within": "at_some_place_within", "crm:P172_contains": "spatially_contains", "crm:P173_starts_before_or_with_the_end_of": "starts_before_or_with_the_end_of", "crm:P173i_ends_after_or_with_the_start_of": "ends_after_or_with_the_start_of", "crm:P174_starts_before_the_end_of": "starts_before_the_end_of", "crm:P174i_ends_after_the_start_of": "ends_after_the_start_of", "crm:P175_starts_before_or_with_the_start_of": "starts_before_or_with_the_start_of", "crm:P175i_starts_with_or_after_the_start_of": "starts_with_or_after_the_start_of", "crm:P176_starts_before_the_start_of": "starts_before_the_start_of", "crm:P176i_starts_after_the_start_of": "starts_after_the_start_of", "crm:P177_assigned_property_of_type": "assigned_property", "crm:P179_had_sales_price": "sales_price", "crm:P179i_was_sales_price_of": "sales_price_of", "crm:P180_has_currency": "currency", "crm:P180i_was_currency_of": "currency_of", "crm:P182_ends_before_or_with_the_start_of": "ends_before_or_with_the_start_of", "crm:P182i_starts_after_or_with_the_end_of": "starts_after_or_with_the_end_of", "crm:P183_ends_before_the_start_of": "ends_before_the_start_of", "crm:P183i_starts_after_the_end_of": "starts_after_the_end_of", "crm:P184_ends_before_or_with_the_end_of": "ends_before_or_with_the_end_of", "crm:P184i_ends_with_or_after_the_end_of": "ends_with_or_after_the_end_of", "crm:P185_ends_before_the_end_of": "ends_before_the_end_of", "crm:P185i_ends_after_the_end_of": "ends_after_the_end_of", "crm:P186_produced_thing_of_product_type": "produced_thing_of_product_type", "crm:P186i_is_produced_by": "type_produced_by", "crm:P187_has_production_plan": "production_plan", "crm:P187i_is_production_plan_for": "production_plan_for", "crm:P188_requires_production_tool": "requires_production_tool", "crm:P188i_is_production_tool_for": "production_tool_for", "crm:P189_approximates": "approximates", "crm:P189i_is_approximated_by": "approximated_by", "crm:P190_has_symbolic_content": "content", "crm:P191_had_duration": "duration", "crm:P191i_was_duration_of": "duration_of", "crm:P195_was_a_presence_of": "presence_of_thing", "crm:P195i_had_presence": "thing_presence", "crm:P196_defines": "defines", "crm:P196i_is_defined_by": "thing_defined_by", "crm:P197_covered_parts_of": "covered_parts_of", "crm:P197i_was_partially_covered_by": "partially_covered_by", "crm:P198_holds_or_supports": "holds_or_supports", "crm:P198i_is_held_or_supported_by": "held_or_supported_by", "crm:P199_represents_instance_of_type": "represents_instance_of_type", "crm:P199i_has_instance_represented_by": "instance_represented_by", "crm:P81a_end_of_the_begin": "end_of_the_begin", "crm:P81b_begin_of_the_end": "begin_of_the_end", "crm:P82a_begin_of_the_begin": "begin_of_the_begin", "crm:P82b_end_of_the_end": "end_of_the_end", "crm:P90a_has_lower_value_limit": "lower_value_limit", "crm:P90b_has_upper_value_limit": "upper_value_limit", "dig:D1_Digital_Object": "DigitalObject", "sci:S19_Encounter_Event": "Encounter", "sci:O13_triggers": "caused", "sci:O13i_is_triggered_by": "caused_by", "sci:O19_encountered_object": "encountered", "sci:O19i_was_object_encountered_at": "encountered_by", "archaeo:AP25_occurs_during": "AP25_occurs_during", "rdfs:label": "_label", "skos:exactMatch": "exact_match", "skos:closeMatch": "close_match", "skos:hasTopConcept": "hasTopConcept", "skos:topConceptOf": "topConceptOf", "skos:inScheme": "inScheme", "rdfs:seeAlso": "see_also", "dcterms:conformsTo": "conforms_to", "dc:format": "format", "la:Payment": "Payment", "la:RightAcquisition": "RightAcquisition", "la:Phase": "Phase", "la:Set": "Set", "la:has_member": "member", "la:Addition": "Addition", "la:Removal": "Removal", "la:DigitalService": "DigitalService", "la:property_classified_as": "property_classified_as", "la:current_permanent_custodian": "current_permanent_custodian", "la:current_permanent_custodian_of": "current_permanent_custodian_of", "la:equivalent": "equivalent", "la:paid_amount": "paid_amount", "la:paid_from": "paid_from", "la:paid_to": "paid_to", "la:establishes": "establishes", "la:established_by": "established_by", "la:invalidates": "invalidates", "la:invalidated_by": "invalidated_by", "la:initiated": "initiated", "la:initiated_by": "initiated_by", "la:terminated": "terminated", "la:terminated_by": "terminated_by", "la:has_phase": "has_phase", "la:phase_of": "phase_of", "la:related_entity": "related_entity", "la:related_entity_of": "related_entity_of", "la:relationship": "relationship", "la:added_to": "added_to", "la:added_to_by": "added_to_by", "la:added_member": "added_member", "la:added_member_by": "added_member_by", "la:removed_from": "removed_from", "la:removed_from_by": "removed_from_by", "la:removed_member": "removed_member", "la:removed_member_by": "removed_member_by", "la:digitally_carries": "digitally_carries", "la:digitally_carried_by": "digitally_carried_by", "la:digitally_shows": "digitally_shows", "la:digitally_shown_by": "digitally_shown_by", "la:access_point": "access_point", "la:digitally_available_via": "digitally_available_via", "la:digitally_makes_available": "digitally_makes_available"}