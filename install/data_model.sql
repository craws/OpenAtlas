--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET lock_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;

SET search_path = model, pg_catalog;

--
-- Data for Name: class; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO class VALUES (1, 'E1', 'CRM Entity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (2, 'E2', 'Temporal Entity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (3, 'E3', 'Condition State', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (4, 'E4', 'Period', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (5, 'E5', 'Event', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (6, 'E6', 'Destruction', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (7, 'E7', 'Activity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (8, 'E8', 'Acquisition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (9, 'E9', 'Move', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (10, 'E10', 'Transfer of Custody', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (11, 'E11', 'Modification', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (12, 'E12', 'Production', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (13, 'E13', 'Attribute Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (14, 'E14', 'Condition Assessment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (15, 'E15', 'Identifier Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (16, 'E16', 'Measurement', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (17, 'E17', 'Type Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (18, 'E18', 'Physical Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (19, 'E19', 'Physical Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (20, 'E20', 'Biological Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (21, 'E21', 'Person', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (22, 'E22', 'Man-Made Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (23, 'E24', 'Physical Man-Made Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (24, 'E25', 'Man-Made Feature', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (25, 'E26', 'Physical Feature', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (26, 'E27', 'Site', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (27, 'E28', 'Conceptual Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (28, 'E29', 'Design or Procedure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (29, 'E30', 'Right', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (30, 'E31', 'Document', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (31, 'E32', 'Authority Document', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (32, 'E33', 'Linguistic Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (33, 'E34', 'Inscription', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (34, 'E35', 'Title', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (35, 'E36', 'Visual Item', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (36, 'E37', 'Mark', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (37, 'E38', 'Image', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (38, 'E39', 'Actor', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (39, 'E40', 'Legal Body', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (40, 'E41', 'Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (41, 'E42', 'Identifier', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (42, 'E44', 'Place Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (43, 'E45', 'Address', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (44, 'E46', 'Section Definition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (45, 'E47', 'Spatial Coordinates', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (46, 'E48', 'Place Name', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (47, 'E49', 'Time Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (48, 'E50', 'Date', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (49, 'E51', 'Contact Point', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (50, 'E52', 'Time-Span', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (51, 'E53', 'Place', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (52, 'E54', 'Dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (53, 'E55', 'Type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (54, 'E56', 'Language', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (55, 'E57', 'Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (56, 'E58', 'Measurement Unit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (57, 'E63', 'Beginning of Existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (58, 'E64', 'End of Existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (59, 'E65', 'Creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (60, 'E66', 'Formation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (61, 'E67', 'Birth', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (62, 'E68', 'Dissolution', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (63, 'E69', 'Death', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (64, 'E70', 'Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (65, 'E71', 'Man-Made Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (66, 'E72', 'Legal Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (67, 'E73', 'Information Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (68, 'E74', 'Group', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (69, 'E75', 'Conceptual Object Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (70, 'E77', 'Persistent Item', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (71, 'E78', 'Collection', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (72, 'E79', 'Part Addition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (73, 'E80', 'Part Removal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (74, 'E81', 'Transformation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (75, 'E82', 'Actor Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (76, 'E83', 'Type Creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (77, 'E84', 'Information Carrier', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (78, 'E85', 'Joining', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (79, 'E86', 'Leaving', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (80, 'E87', 'Curation Activity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (81, 'E89', 'Propositional Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (82, 'E90', 'Symbolic Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (83, 'E59', 'Primitive Value', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (84, 'E60', 'Number', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (85, 'E61', 'Time Primitive', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class VALUES (86, 'E62', 'String', '2015-06-11 19:26:28.25822', NULL);


--
-- Name: class_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('class_id_seq', 86, true);


--
-- Data for Name: class_inheritance; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO class_inheritance VALUES (1, 1, 2, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (2, 2, 3, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (3, 2, 4, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (4, 4, 5, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (5, 58, 6, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (6, 5, 7, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (7, 7, 8, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (8, 7, 9, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (9, 7, 10, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (10, 7, 11, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (11, 11, 12, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (12, 57, 12, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (13, 7, 13, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (14, 13, 14, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (15, 13, 15, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (16, 13, 16, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (17, 13, 17, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (18, 66, 18, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (19, 18, 19, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (20, 19, 20, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (21, 20, 21, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (22, 38, 21, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (23, 19, 22, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (24, 23, 22, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (25, 18, 23, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (26, 65, 23, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (27, 23, 24, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (28, 25, 24, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (29, 18, 25, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (30, 25, 26, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (31, 65, 27, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (32, 67, 28, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (33, 81, 29, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (34, 67, 30, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (35, 30, 31, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (36, 67, 32, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (37, 32, 33, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (38, 36, 33, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (39, 32, 34, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (40, 40, 34, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (41, 67, 35, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (42, 35, 36, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (43, 35, 37, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (44, 70, 38, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (45, 68, 39, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (46, 82, 40, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (47, 40, 41, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (48, 40, 42, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (49, 42, 43, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (50, 49, 43, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (51, 42, 44, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (52, 42, 45, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (53, 42, 46, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (54, 40, 47, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (55, 47, 48, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (56, 40, 49, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (57, 1, 50, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (58, 1, 51, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (59, 1, 52, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (60, 27, 53, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (61, 53, 54, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (62, 53, 55, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (63, 53, 56, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (64, 5, 57, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (65, 5, 58, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (66, 7, 59, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (67, 57, 59, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (68, 7, 60, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (69, 57, 60, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (70, 57, 61, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (71, 58, 62, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (72, 58, 63, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (73, 70, 64, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (74, 64, 65, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (75, 64, 66, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (76, 81, 67, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (77, 82, 67, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (78, 38, 68, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (79, 40, 69, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (80, 1, 70, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (81, 23, 71, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (82, 11, 72, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (83, 11, 73, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (84, 57, 74, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (85, 58, 74, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (86, 40, 75, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (87, 59, 76, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (88, 22, 77, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (89, 7, 78, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (90, 7, 79, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (91, 7, 80, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (92, 27, 81, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (93, 27, 82, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (94, 66, 82, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (95, 83, 84, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (96, 83, 85, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO class_inheritance VALUES (97, 83, 86, '2015-06-11 19:26:28.25822', NULL);


--
-- Name: class_inheritance_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('class_inheritance_id_seq', 97, true);


--
-- Data for Name: entity; Type: TABLE DATA; Schema: model; Owner: openatlas
--



--
-- Name: entity_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('entity_id_seq', 1, false);


--
-- Data for Name: i18n; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO i18n VALUES (1, 'class', 'name', 1, 'el', 'Οντότητα CIDOC CRM', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2, 'class', 'name', 1, 'en', 'CRM Entity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (3, 'class', 'name', 1, 'de', 'CRM Entität', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (4, 'class', 'name', 1, 'ru', 'CRM Сущность', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (5, 'class', 'name', 1, 'fr', 'Entité CRM', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (6, 'class', 'name', 1, 'pt', 'Entidade CRM', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (7, 'class', 'name', 1, 'cn', 'CRM实体', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (8, 'class', 'comment', 1, 'en', 'This class comprises all things in the universe of discourse of the CIDOC Conceptual Reference Model.
It is an abstract concept providing for three general properties:
1.	Identification by name or appellation, and in particular by a preferred identifier
2.	Classification by type, allowing further refinement of the specific subclass an instance belongs to
3.	Attachment of free text for the expression of anything not captured by formal properties
With the exception of E59 Primitive Value, all other classes within the CRM are directly or indirectly specialisations of E1 CRM Entity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (9, 'class', 'name', 2, 'fr', 'Entité temporelle', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (10, 'class', 'name', 2, 'en', 'Temporal Entity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (11, 'class', 'name', 2, 'ru', 'Временная Сущность', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (12, 'class', 'name', 2, 'el', 'Έγχρονη  Οντότητα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (13, 'class', 'name', 2, 'de', 'Geschehendes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (14, 'class', 'name', 2, 'pt', 'Entidade Temporal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (15, 'class', 'name', 2, 'cn', '时间实体', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (16, 'class', 'comment', 2, 'en', 'This class comprises all phenomena, such as the instances of E4 Periods, E5 Events and states, which happen over a limited extent in time.
	In some contexts, these are also called perdurants. This class is disjoint from E77 Persistent Item. This is an abstract class and has no direct instances. E2 Temporal Entity is specialized into E4 Period, which applies to a particular geographic area (defined with a greater or lesser degree of precision), and E3 Condition State, which applies to instances of E18 Physical Thing.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (17, 'class', 'name', 3, 'ru', 'Состояние', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (18, 'class', 'name', 3, 'en', 'Condition State', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (19, 'class', 'name', 3, 'de', 'Zustandsphase', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (20, 'class', 'name', 3, 'fr', 'État matériel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (21, 'class', 'name', 3, 'el', 'Κατάσταση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (22, 'class', 'name', 3, 'pt', 'Estado Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (23, 'class', 'name', 3, 'cn', '状态', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (24, 'class', 'comment', 3, 'en', 'This class comprises the states of objects characterised by a certain condition over a time-span.
An instance of this class describes the prevailing physical condition of any material object or feature during a specific E52 Time Span. In general, the time-span for which a certain condition can be asserted may be shorter than the real time-span, for which this condition held.
 The nature of that condition can be described using P2 has type. For example, the E3 Condition State “condition of the SS Great Britain between 22 September 1846 and 27 August 1847” can be characterized as E55 Type “wrecked”.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (25, 'class', 'name', 4, 'de', 'Phase', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (26, 'class', 'name', 4, 'en', 'Period', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (27, 'class', 'name', 4, 'fr', 'Période', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (28, 'class', 'name', 4, 'ru', 'Период', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (29, 'class', 'name', 4, 'el', 'Περίοδος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (30, 'class', 'name', 4, 'pt', 'Período', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (31, 'class', 'name', 4, 'cn', '期间', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (32, 'class', 'comment', 4, 'en', '	This class comprises sets of coherent phenomena or cultural manifestations bounded in time and space.
It is the social or physical coherence of these phenomena that identify an E4 Period and not the associated spatio-temporal bounds. These bounds are a mere approximation of the actual process of growth, spread and retreat. Consequently, different periods can overlap and coexist in time and space, such as when a nomadic culture exists in the same area as a sedentary culture.
Typically this class is used to describe prehistoric or historic periods such as the “Neolithic Period”, the “Ming Dynasty” or the “McCarthy Era”. There are however no assumptions about the scale of the associated phenomena. In particular all events are seen as synthetic processes consisting of coherent phenomena. Therefore E4 Period is a superclass of E5 Event. For example, a modern clinical E67 Birth can be seen as both an atomic E5 Event and as an E4 Period that consists of multiple activities performed by multiple instances of E39 Actor.
There are two different conceptualisations of ‘artistic style’, defined either by physical features or by historical context. For example, “Impressionism” can be viewed as a period lasting from approximately 1870 to 1905 during which paintings with particular characteristics were produced by a group of artists that included (among others) Monet, Renoir, Pissarro, Sisley and Degas. Alternatively, it can be regarded as a style applicable to all paintings sharing the characteristics of the works produced by the Impressionist painters, regardless of historical context. The first interpretation is an E4 Period, and the second defines morphological object types that fall under E55 Type.
Another specific case of an E4 Period is the set of activities and phenomena associated with a settlement, such as the populated period of Nineveh.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (33, 'class', 'name', 5, 'el', 'Συμβάν', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (34, 'class', 'name', 5, 'fr', 'Événement', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (35, 'class', 'name', 5, 'ru', 'Событие', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (36, 'class', 'name', 5, 'en', 'Event', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (37, 'class', 'name', 5, 'de', 'Ereignis', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (38, 'class', 'name', 5, 'pt', 'Evento', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (39, 'class', 'name', 5, 'cn', '事件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (40, 'class', 'comment', 5, 'en', 'This class comprises changes of states in cultural, social or physical systems, regardless of scale, brought about by a series or group of coherent physical, cultural, technological or legal phenomena. Such changes of state will affect instances of E77 Persistent Item or its subclasses.
The distinction between an E5 Event and an E4 Period is partly a question of the scale of observation. Viewed at a coarse level of detail, an E5 Event is an ‘instantaneous’ change of state. At a fine level, the E5 Event can be analysed into its component phenomena within a space and time frame, and as such can be seen as an E4 Period. The reverse is not necessarily the case: not all instances of E4 Period give rise to a noteworthy change of state.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (41, 'class', 'name', 6, 'ru', 'Разрушение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (42, 'class', 'name', 6, 'en', 'Destruction', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (43, 'class', 'name', 6, 'fr', 'Destruction', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (44, 'class', 'name', 6, 'de', 'Zerstörung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (45, 'class', 'name', 6, 'el', 'Καταστροφή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (46, 'class', 'name', 6, 'pt', 'Destruição', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (47, 'class', 'name', 6, 'cn', '摧毁', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (123, 'class', 'name', 16, 'de', 'Messung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (124, 'class', 'name', 16, 'fr', 'Mesurage', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (125, 'class', 'name', 16, 'en', 'Measurement', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (48, 'class', 'comment', 6, 'en', 'This class comprises events that destroy one or more instances of E18 Physical Thing such that they lose their identity as the subjects of documentation.
Some destruction events are intentional, while others are independent of human activity. Intentional destruction may be documented by classifying the event as both an E6 Destruction and E7 Activity.
The decision to document an object as destroyed, transformed or modified is context sensitive:
1.  If the matter remaining from the destruction is not documented, the event is modelled solely as E6 Destruction.
2. An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the original. In this case, the new items have separate identities. Matter is preserved, but identity is not.
3. When the initial identity of the changed instance of E18 Physical Thing is preserved, the event should be documented as E11 Modification.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (49, 'class', 'name', 7, 'en', 'Activity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (50, 'class', 'name', 7, 'fr', 'Activité', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (51, 'class', 'name', 7, 'de', 'Handlung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (52, 'class', 'name', 7, 'ru', 'Деятельность', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (53, 'class', 'name', 7, 'el', 'Δράση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (54, 'class', 'name', 7, 'pt', 'Atividade', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (55, 'class', 'name', 7, 'cn', '活动', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (56, 'class', 'comment', 7, 'en', 'This class comprises actions intentionally carried out by instances of E39 Actor that result in changes of state in the cultural, social, or physical systems documented.
This notion includes complex, composite and long-lasting actions such as the building of a settlement or a war, as well as simple, short-lived actions such as the opening of a door.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (57, 'class', 'name', 8, 'fr', 'Acquisition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (58, 'class', 'name', 8, 'el', 'Απόκτηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (59, 'class', 'name', 8, 'ru', 'Событие Приобретения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (60, 'class', 'name', 8, 'en', 'Acquisition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (61, 'class', 'name', 8, 'de', 'Erwerb', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (62, 'class', 'name', 8, 'pt', 'Aquisição', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (63, 'class', 'name', 8, 'cn', '征集取得', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (64, 'class', 'comment', 8, 'en', 'This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor.
The class also applies to the establishment or loss of ownership of instances of E18 Physical Thing. It does not, however, imply changes of any other kinds of right. The recording of the donor and/or recipient is optional. It is possible that in an instance of E8 Acquisition there is either no donor or no recipient. Depending on the circumstances, it may describe:
1.	the beginning of ownership
2.	the end of ownership
3.	the transfer of ownership
4.	the acquisition from an unknown source
5.	the loss of title due to destruction of the item
It may also describe events where a collector appropriates legal title, for example by annexation or field collection. The interpretation of the museum notion of "accession" differs between institutions. The CRM therefore models legal ownership (E8 Acquisition) and physical custody (E10 Transfer of Custody) separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (65, 'class', 'name', 9, 'en', 'Move', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (66, 'class', 'name', 9, 'el', 'Μετακίνηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (67, 'class', 'name', 9, 'de', 'Objektbewegung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (68, 'class', 'name', 9, 'ru', 'Перемещение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (69, 'class', 'name', 9, 'fr', 'Déplacement', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (70, 'class', 'name', 9, 'pt', 'Locomoção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (71, 'class', 'name', 9, 'cn', '移动', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (72, 'class', 'comment', 9, 'en', 'This class comprises changes of the physical location of the instances of E19 Physical Object.
Note, that the class E9 Move inherits the property P7 took place at (witnessed): E53 Place. This property should be used to describe the trajectory or a larger area within which a move takes place, whereas the properties P26 moved to (was destination of), P27 moved from (was origin of) describe the start and end points only. Moves may also be documented to consist of other moves (via P9 consists of (forms part of)), in order to describe intermediate stages on a trajectory. In that case, start and end points of the partial moves should match appropriately between each other and with the overall event.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (73, 'class', 'name', 10, 'fr', 'Changement de détenteur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (74, 'class', 'name', 10, 'en', 'Transfer of Custody', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (75, 'class', 'name', 10, 'de', 'Übertragung des Gewahrsams', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (76, 'class', 'name', 10, 'el', 'Μεταβίβαση  Κατοχής', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (77, 'class', 'name', 10, 'ru', 'Передача Опеки', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (78, 'class', 'name', 10, 'pt', 'Transferência de Custódia', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (79, 'class', 'name', 10, 'cn', '保管作业转移', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (80, 'class', 'comment', 10, 'en', 'This class comprises transfers of physical custody of objects between instances of E39 Actor.
The recording of the donor and/or recipient is optional. It is possible that in an instance of E10 Transfer of Custody there is either no donor or no recipient. Depending on the circumstances it may describe:
1.	the beginning of custody
2.	the end of custody
3.	the transfer of custody
4.	the receipt of custody from an unknown source
5.	the declared loss of an object
The distinction between the legal responsibility for custody and the actual physical possession of the object should be expressed using the property P2 has type (is type of). A specific case of transfer of custody is theft.
The interpretation of the museum notion of "accession" differs between institutions. The CRM therefore models legal ownership and physical custody separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (81, 'class', 'name', 11, 'ru', 'Событие Изменения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (82, 'class', 'name', 11, 'en', 'Modification', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (83, 'class', 'name', 11, 'el', 'Τροποποίηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (84, 'class', 'name', 11, 'fr', 'Modification', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (85, 'class', 'name', 11, 'de', 'Bearbeitung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (86, 'class', 'name', 11, 'pt', 'Modificação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (87, 'class', 'name', 11, 'cn', '修改', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (126, 'class', 'name', 16, 'pt', 'Medição', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (127, 'class', 'name', 16, 'cn', '测量', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (182, 'class', 'name', 23, 'pt', 'Coisa Material Fabricada', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (183, 'class', 'name', 23, 'cn', '人造实体物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (184, 'class', 'comment', 23, 'en', 'This class comprises all persistent physical items that are purposely created by human activity.
This class comprises man-made objects, such as a swords, and man-made features, such as rock art. No assumptions are made as to the extent of modification required to justify regarding an object as man-made. For example, a “cup and ring” carving on bedrock is regarded as instance of E24 Physical Man-Made Thing.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (185, 'class', 'name', 24, 'fr', 'Caractéristique fabriquée', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (88, 'class', 'comment', 11, 'en', 'This class comprises all instances of E7 Activity that create, alter or change E24 Physical Man-Made Thing.
This class includes the production of an item from raw materials, and other so far undocumented objects, and the preventive treatment or restoration of an object for conservation.
Since the distinction between modification and production is not always clear, modification is regarded as the more generally applicable concept. This implies that some items may be consumed or destroyed in a Modification, and that others may be produced as a result of it. An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities.
If the instance of the E29 Design or Procedure utilized for the modification prescribes the use of specific materials, they should be documented using property P68 foresees use of (use foreseen by): E57 Material of E29 Design or Procedure, rather than via P126 employed (was employed in): E57 Material.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (89, 'class', 'name', 12, 'fr', 'Production', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (90, 'class', 'name', 12, 'el', 'Παραγωγή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (91, 'class', 'name', 12, 'de', 'Herstellung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (92, 'class', 'name', 12, 'ru', 'Событие Производства', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (93, 'class', 'name', 12, 'en', 'Production', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (94, 'class', 'name', 12, 'pt', 'Produção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (95, 'class', 'name', 12, 'cn', '生产', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (96, 'class', 'comment', 12, 'en', 'This class comprises activities that are designed to, and succeed in, creating one or more new items.
It specializes the notion of modification into production. The decision as to whether or not an object is regarded as new is context sensitive. Normally, items are considered “new” if there is no obvious overall similarity between them and the consumed items and material used in their production. In other cases, an item is considered “new” because it becomes relevant to documentation by a modification. For example, the scribbling of a name on a potsherd may make it a voting token. The original potsherd may not be worth documenting, in contrast to the inscribed one.
This entity can be collective: the printing of a thousand books, for example, would normally be considered a single event.
An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities and matter is preserved, but identity is not.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (97, 'class', 'name', 13, 'ru', 'Присвоение Атрибута', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (98, 'class', 'name', 13, 'fr', 'Affectation d''attribut', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (99, 'class', 'name', 13, 'de', 'Merkmalszuweisung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (100, 'class', 'name', 13, 'en', 'Attribute Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (101, 'class', 'name', 13, 'el', 'Απόδοση Ιδιοτήτων', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (102, 'class', 'name', 13, 'pt', 'Atribuição de Característica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (103, 'class', 'name', 13, 'cn', '屬性指定', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (104, 'class', 'comment', 13, 'en', 'This class comprises the actions of making assertions about properties of an object or any relation between two items or concepts.
This class allows the documentation of how the respective assignment came about, and whose opinion it was. All the attributes or properties assigned in such an action can also be seen as directly attached to the respective item or concept, possibly as a collection of contradictory values. All cases of properties in this model that are also described indirectly through an action are characterised as "short cuts" of this action. This redundant modelling of two alternative views is preferred because many implementations may have good reasons to model either the action or the short cut, and the relation between both alternatives can be captured by simple rules.
In particular, the class describes the actions of people making propositions and statements during certain museum procedures, e.g. the person and date when a condition statement was made, an identifier was assigned, the museum object was measured, etc. Which kinds of such assignments and statements need to be documented explicitly in structures of a schema rather than free text, depends on if this information should be accessible by structured queries.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (105, 'class', 'name', 14, 'el', 'Εκτίμηση Κατάστασης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (106, 'class', 'name', 14, 'ru', 'Оценка Состояния', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (107, 'class', 'name', 14, 'fr', 'Expertise de l''état matériel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (108, 'class', 'name', 14, 'de', 'Zustandsfeststellung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (109, 'class', 'name', 14, 'en', 'Condition Assessment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (110, 'class', 'name', 14, 'pt', 'Avaliação do Estado Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (111, 'class', 'name', 14, 'cn', '状态评估', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (112, 'class', 'comment', 14, 'en', 'This class describes the act of assessing the state of preservation of an object during a particular period.
The condition assessment may be carried out by inspection, measurement or through historical research. This class is used to document circumstances of the respective assessment that may be relevant to interpret its quality at a later stage, or to continue research on related documents.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (113, 'class', 'name', 15, 'el', 'Απόδοση Αναγνωριστικού', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (114, 'class', 'name', 15, 'ru', 'Назначение Идентификатора', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (115, 'class', 'name', 15, 'en', 'Identifier Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (116, 'class', 'name', 15, 'de', 'Kennzeichenzuweisung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (117, 'class', 'name', 15, 'fr', 'Attribution d’identificateur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (118, 'class', 'name', 15, 'pt', 'Atribuição de Identificador', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (119, 'class', 'name', 15, 'cn', '标识符指定', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (120, 'class', 'comment', 15, 'en', 'This class comprises activities that result in the allocation of an identifier to an instance of E1 CRM Entity. An E15 Identifier Assignment may include the creation of the identifier from multiple constituents, which themselves may be instances of E41 Appellation. The syntax and kinds of constituents to be used may be declared in a rule constituting an instance of E29 Design or Procedure.
Examples of such identifiers include Find Numbers, Inventory Numbers, uniform titles in the sense of librarianship and Digital Object Identifiers (DOI). Documenting the act of identifier assignment and deassignment is especially useful when objects change custody or the identification system of an organization is changed. In order to keep track of the identity of things in such cases, it is important to document by whom, when and for what purpose an identifier is assigned to an item.
The fact that an identifier is a preferred one for an organisation can be expressed by using the property E1 CRM Entity. P48 has preferred identifier (is preferred identifier of): E42 Identifier. It can better be expressed in a context independent form by assigning a suitable E55 Type, such as “preferred identifier assignment”, to the respective instance of E15 Identifier Assignment via the P2 has type property.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (121, 'class', 'name', 16, 'ru', 'Событие Измерения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (122, 'class', 'name', 16, 'el', 'Μέτρηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (128, 'class', 'comment', 16, 'en', 'This class comprises actions measuring physical properties and other values that can be determined by a systematic procedure.
Examples include measuring the monetary value of a collection of coins or the running time of a specific video cassette.
The E16 Measurement may use simple counting or tools, such as yardsticks or radiation detection devices. The interest is in the method and care applied, so that the reliability of the result may be judged at a later stage, or research continued on the associated documents. The date of the event is important for dimensions, which may change value over time, such as the length of an object subject to shrinkage. Details of methods and devices are best handled as free text, whereas basic techniques such as "carbon 14 dating" should be encoded using P2 has type (is type of:) E55 Type.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (129, 'class', 'name', 17, 'de', 'Typuszuweisung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (130, 'class', 'name', 17, 'ru', 'Присвоение Типа', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (131, 'class', 'name', 17, 'fr', 'Attribution de type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (132, 'class', 'name', 17, 'en', 'Type Assignment', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (133, 'class', 'name', 17, 'el', 'Απόδοση Τύπου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (134, 'class', 'name', 17, 'pt', 'Atribuição de Tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (135, 'class', 'name', 17, 'cn', '类型指定', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (136, 'class', 'comment', 17, 'en', 'This class comprises the actions of classifying items of whatever kind. Such items include objects, specimens, people, actions and concepts.
This class allows for the documentation of the context of classification acts in cases where the value of the classification depends on the personal opinion of the classifier, and the date that the classification was made. This class also encompasses the notion of "determination," i.e. the systematic and molecular identification of a specimen in biology.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (137, 'class', 'name', 18, 'de', 'Materielles', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (138, 'class', 'name', 18, 'el', 'Υλικό Πράγμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (139, 'class', 'name', 18, 'en', 'Physical Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (140, 'class', 'name', 18, 'fr', 'Chose matérielle', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (141, 'class', 'name', 18, 'ru', 'Физическая Вещь', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (142, 'class', 'name', 18, 'pt', 'Coisa Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (143, 'class', 'name', 18, 'cn', '实体物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (144, 'class', 'comment', 18, 'en', 'This class comprises all persistent physical items with a relatively stable form, man-made or natural.
Depending on the existence of natural boundaries of such things, the CRM distinguishes the instances of E19 Physical Object from instances of E26 Physical Feature, such as holes, rivers, pieces of land etc. Most instances of E19 Physical Object can be moved (if not too heavy), whereas features are integral to the surrounding matter.
The CRM is generally not concerned with amounts of matter in fluid or gaseous states.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (145, 'class', 'name', 19, 'ru', 'Физический Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (146, 'class', 'name', 19, 'fr', 'Objet matériel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (147, 'class', 'name', 19, 'en', 'Physical Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (148, 'class', 'name', 19, 'el', 'Υλικό Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (149, 'class', 'name', 19, 'de', 'Materieller Gegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (150, 'class', 'name', 19, 'pt', 'Objeto Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (151, 'class', 'name', 19, 'cn', '实体物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (152, 'class', 'comment', 19, 'en', 'This class comprises items of a material nature that are units for documentation and have physical boundaries that separate them completely in an objective way from other objects.
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen. Typically, instances of E19 Physical Object can be moved (if not too heavy).
In some contexts, such objects, except for aggregates, are also called “bona fide objects” (Smith & Varzi, 2000, pp.401-420), i.e. naturally defined objects.
The decision as to what is documented as a complete item, rather than by its parts or components, may be a purely administrative decision or may be a result of the order in which the item was acquired.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (153, 'class', 'name', 20, 'ru', 'Биологический Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (154, 'class', 'name', 20, 'en', 'Biological Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (155, 'class', 'name', 20, 'el', 'Βιολογικό Ακτικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (156, 'class', 'name', 20, 'fr', 'Objet biologique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (157, 'class', 'name', 20, 'de', 'Biologischer Gegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (158, 'class', 'name', 20, 'pt', 'Objeto Biológico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (159, 'class', 'name', 20, 'cn', '生物体', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (160, 'class', 'comment', 20, 'en', 'This class comprises individual items of a material nature, which live, have lived or are natural products of or from living organisms.
Artificial objects that incorporate biological elements, such as Victorian butterfly frames, can be documented as both instances of E20 Biological Object and E22 Man-Made Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (161, 'class', 'name', 21, 'de', 'Person', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (162, 'class', 'name', 21, 'fr', 'Personne', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (163, 'class', 'name', 21, 'en', 'Person', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (164, 'class', 'name', 21, 'ru', 'Личность', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (165, 'class', 'name', 21, 'el', 'Πρόσωπο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (166, 'class', 'name', 21, 'pt', 'Pessoa', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (167, 'class', 'name', 21, 'cn', '人物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (168, 'class', 'comment', 21, 'en', 'This class comprises real persons who live or are assumed to have lived.
Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures. In cases where doubt exists as to whether several persons are in fact identical, multiple instances can be created and linked to indicate their relationship. The CRM does not propose a specific form to support reasoning about possible identity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (169, 'class', 'name', 22, 'fr', 'Objet fabriqué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (170, 'class', 'name', 22, 'el', 'Ανθρωπογενές Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (171, 'class', 'name', 22, 'de', 'Künstlicher Gegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (172, 'class', 'name', 22, 'ru', 'Рукотворный Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (173, 'class', 'name', 22, 'en', 'Man-Made Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (174, 'class', 'name', 22, 'pt', 'Objeto Fabricado', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (175, 'class', 'name', 22, 'cn', '人造物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (176, 'class', 'comment', 22, 'en', 'This class comprises physical objects purposely created by human activity.
No assumptions are made as to the extent of modification required to justify regarding an object as man-made. For example, an inscribed piece of rock or a preserved butterfly are both regarded as instances of E22 Man-Made Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (177, 'class', 'name', 23, 'ru', 'Физическая Рукотворная Вещь', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (178, 'class', 'name', 23, 'en', 'Physical Man-Made Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (179, 'class', 'name', 23, 'el', 'Ανθρωπογενές Υλικό Πράγμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (180, 'class', 'name', 23, 'de', 'Hergestelltes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (181, 'class', 'name', 23, 'fr', 'Chose matérielle fabriquée', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (186, 'class', 'name', 24, 'en', 'Man-Made Feature', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (187, 'class', 'name', 24, 'ru', 'Искусственный Признак', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (188, 'class', 'name', 24, 'el', 'Ανθρωπογενές Μόρφωμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (189, 'class', 'name', 24, 'de', 'Hergestelltes Merkmal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (190, 'class', 'name', 24, 'pt', 'Característica Fabricada', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (191, 'class', 'name', 24, 'cn', '人造外貌表征', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (192, 'class', 'comment', 24, 'en', 'This class comprises physical features that are purposely created by human activity, such as scratches, artificial caves, artificial water channels, etc.
No assumptions are made as to the extent of modification required to justify regarding a feature as man-made. For example, rock art or even “cup and ring” carvings on bedrock a regarded as types of E25 Man-Made Feature.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (193, 'class', 'name', 25, 'el', 'Υλικό Μόρφωμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (194, 'class', 'name', 25, 'en', 'Physical Feature', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (195, 'class', 'name', 25, 'ru', 'Физический Признак', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (196, 'class', 'name', 25, 'de', 'Materielles Merkmal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (197, 'class', 'name', 25, 'fr', 'Caractéristique matérielle', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (198, 'class', 'name', 25, 'pt', 'Característica Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (199, 'class', 'name', 25, 'cn', '实体外貌表征', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (200, 'class', 'comment', 25, 'en', 'This class comprises identifiable features that are physically attached in an integral way to particular physical objects.
Instances of E26 Physical Feature share many of the attributes of instances of E19 Physical Object. They may have a one-, two- or three-dimensional geometric extent, but there are no natural borders that separate them completely in an objective way from the carrier objects. For example, a doorway is a feature but the door itself, being attached by hinges, is not.
Instances of E26 Physical Feature can be features in a narrower sense, such as scratches, holes, reliefs, surface colours, reflection zones in an opal crystal or a density change in a piece of wood. In the wider sense, they are portions of particular objects with partially imaginary borders, such as the core of the Earth, an area of property on the surface of the Earth, a landscape or the head of a contiguous marble statue. They can be measured and dated, and it is sometimes possible to state who or what is or was responsible for them. They cannot be separated from the carrier object, but a segment of the carrier object may be identified (or sometimes removed) carrying the complete feature.
This definition coincides with the definition of "fiat objects" (Smith & Varzi, 2000, pp.401-420), with the exception of aggregates of “bona fide objects”.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (201, 'class', 'name', 26, 'el', 'Φυσικός Χώρος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (202, 'class', 'name', 26, 'en', 'Site', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (203, 'class', 'name', 26, 'fr', 'Site', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (204, 'class', 'name', 26, 'ru', 'Участок', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (205, 'class', 'name', 26, 'de', 'Gelände', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (206, 'class', 'name', 26, 'pt', 'Lugar', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (207, 'class', 'name', 26, 'cn', '场地', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (208, 'class', 'comment', 26, 'en', 'This class comprises pieces of land or sea floor.
In contrast to the purely geometric notion of E53 Place, this class describes constellations of matter on the surface of the Earth or other celestial body, which can be represented by photographs, paintings and maps.
 Instances of E27 Site are composed of relatively immobile material items and features in a particular configuration at a particular location', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (209, 'class', 'name', 27, 'fr', 'Objet conceptuel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (210, 'class', 'name', 27, 'de', 'Begrifflicher Gegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (211, 'class', 'name', 27, 'ru', 'Концептуальный Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (212, 'class', 'name', 27, 'en', 'Conceptual Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (213, 'class', 'name', 27, 'el', 'Νοητικό Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (214, 'class', 'name', 27, 'pt', 'Objeto Conceitual', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (215, 'class', 'name', 27, 'cn', '概念物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (216, 'class', 'comment', 27, 'en', 'This class comprises non-material products of our minds and other human produced data that 		have become objects of a discourse about their identity, circumstances of creation or historical 		implication. The production of such information may have been supported by the use of    		technical devices such as cameras or computers.
Characteristically, instances of this class are created, invented or thought by someone, and then may be documented or communicated between persons. Instances of E28 Conceptual Object have the ability to exist on more than one particular carrier at the same time, such as paper, electronic signals, marks, audio media, paintings, photos, human memories, etc.
They cannot be destroyed. They exist as long as they can be found on at least one carrier or in at least one human memory. Their existence ends when the last carrier and the last memory are lost.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (217, 'class', 'name', 28, 'el', 'Σχέδιο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (218, 'class', 'name', 28, 'de', 'Entwurf oder Verfahren', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (219, 'class', 'name', 28, 'fr', 'Conception ou procédure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (220, 'class', 'name', 28, 'ru', 'Проект или Процедура', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (221, 'class', 'name', 28, 'en', 'Design or Procedure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (222, 'class', 'name', 28, 'pt', 'Projeto ou Procedimento', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (223, 'class', 'name', 28, 'cn', '设计或程序', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (224, 'class', 'comment', 28, 'en', 'This class comprises documented plans for the execution of actions in order to achieve a result of a specific quality, form or contents. In particular it comprises plans for deliberate human activities that may result in the modification or production of instances of E24 Physical Thing.
Instances of E29 Design or Procedure can be structured in parts and sequences or depend on others. This is modelled using P69 has association with (is associated with).
Designs or procedures can be seen as one of the following:
1.	A schema for the activities it describes
2.	A schema of the products that result from their application.
3.	An independent intellectual product that may have never been applied, such as Leonardo da Vinci’s famous plans for flying machines.
Because designs or procedures may never be applied or only partially executed, the CRM models a loose relationship between the plan and the respective product.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (225, 'class', 'name', 29, 'ru', 'Право', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (226, 'class', 'name', 29, 'el', 'Δικαίωμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (227, 'class', 'name', 29, 'fr', 'Droit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (228, 'class', 'name', 29, 'en', 'Right', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (229, 'class', 'name', 29, 'de', 'Recht', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (230, 'class', 'name', 29, 'pt', 'Direitos', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (231, 'class', 'name', 29, 'cn', '权限', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (232, 'class', 'comment', 29, 'en', 'This class comprises legal privileges concerning material and immaterial things or their derivatives.
These include reproduction and property rights', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (233, 'class', 'name', 30, 'fr', 'Document', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (234, 'class', 'name', 30, 'en', 'Document', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (235, 'class', 'name', 30, 'de', 'Dokument', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (236, 'class', 'name', 30, 'ru', 'Документ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (237, 'class', 'name', 30, 'el', 'Τεκμήριο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (238, 'class', 'name', 30, 'pt', 'Documento', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (239, 'class', 'name', 30, 'cn', '文献', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (240, 'class', 'comment', 30, 'en', 'This class comprises identifiable immaterial items that make propositions about reality.
These propositions may be expressed in text, graphics, images, audiograms, videograms or by other similar means. Documentation databases are regarded as a special case of E31 Document. This class should not be confused with the term “document” in Information Technology, which is compatible with E73 Information Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (241, 'class', 'name', 31, 'de', 'Referenzdokument', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (242, 'class', 'name', 31, 'ru', 'Официальный Документ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (243, 'class', 'name', 31, 'fr', 'Document de référence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (244, 'class', 'name', 31, 'el', 'Πηγή Καθιερωμένων Όρων', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (245, 'class', 'name', 31, 'en', 'Authority Document', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (246, 'class', 'name', 31, 'pt', 'Documento de Referência', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (247, 'class', 'name', 31, 'cn', '权威文献', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (248, 'class', 'comment', 31, 'en', 'This class comprises encyclopaedia, thesauri, authority lists and other documents that define terminology or conceptual systems for consistent use.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (249, 'class', 'name', 32, 'ru', 'Линвистический Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (250, 'class', 'name', 32, 'en', 'Linguistic Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (251, 'class', 'name', 32, 'el', 'Γλωσσικό Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (252, 'class', 'name', 32, 'fr', 'Objet linguistique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (253, 'class', 'name', 32, 'de', 'Sprachlicher Gegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (254, 'class', 'name', 32, 'pt', 'Objeto Lingüístico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (255, 'class', 'name', 32, 'cn', '语言物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (256, 'class', 'comment', 32, 'en', 'This class comprises identifiable expressions in natural language or languages.
Instances of E33 Linguistic Object can be expressed in many ways: e.g. as written texts, recorded speech or sign language. However, the CRM treats instances of E33 Linguistic Object independently from the medium or method by which they are expressed. Expressions in formal languages, such as computer code or mathematical formulae, are not treated as instances of E33 Linguistic Object by the CRM. These should be modelled as instances of E73 Information Object.
The text of an instance of E33 Linguistic Object can be documented in a note by P3 has note: E62 String
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (257, 'class', 'name', 33, 'el', 'Επιγραφή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (258, 'class', 'name', 33, 'en', 'Inscription', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (259, 'class', 'name', 33, 'fr', 'Inscription', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (260, 'class', 'name', 33, 'ru', 'Надпись', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (261, 'class', 'name', 33, 'de', 'Inschrift', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (262, 'class', 'name', 33, 'pt', 'Inscrição', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (263, 'class', 'name', 33, 'cn', '题字', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (264, 'class', 'comment', 33, 'en', 'This class comprises recognisable, short texts attached to instances of E24 Physical Man-Made Thing.
The transcription of the text can be documented in a note by P3 has note: E62 String. The alphabet used can be documented by P2 has type: E55 Type. This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of an inscription, but the underlying prototype. The physical embodiment is modelled in the CRM as E24 Physical Man-Made Thing.
The relationship of a physical copy of a book to the text it contains is modelled using E84 Information Carrier. P128 carries (is carried by): E33 Linguistic Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (265, 'class', 'name', 34, 'ru', 'Заголовок', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (266, 'class', 'name', 34, 'fr', 'Titre', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (267, 'class', 'name', 34, 'de', 'Titel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (268, 'class', 'name', 34, 'en', 'Title', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (269, 'class', 'name', 34, 'el', ' Τίτλος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (270, 'class', 'name', 34, 'pt', 'Título', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (271, 'class', 'name', 34, 'cn', '题目', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (272, 'class', 'comment', 34, 'en', 'This class comprises the names assigned to works, such as texts, artworks or pieces of music.
Titles are proper noun phrases or verbal phrases, and should not be confused with generic object names such as “chair”, “painting” or “book” (the latter are common nouns that stand for instances of E55 Type). Titles may be assigned by the creator of the work itself, or by a social group.
This class also comprises the translations of titles that are used as surrogates for the original titles in different social contexts.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (273, 'class', 'name', 35, 'ru', 'Визуальный Предмет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (274, 'class', 'name', 35, 'fr', 'Item visuel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (275, 'class', 'name', 35, 'el', 'Οπτικό Στοιχείο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (276, 'class', 'name', 35, 'en', 'Visual Item', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (277, 'class', 'name', 35, 'de', 'Bildliches', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (278, 'class', 'name', 35, 'pt', 'Item Visual', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (279, 'class', 'name', 35, 'cn', '视觉项目', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (280, 'class', 'comment', 35, 'en', 'This class comprises the intellectual or conceptual aspects of recognisable marks and images.
This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of a visual item, but the underlying prototype. For example, a mark such as the ICOM logo is generally considered to be the same logo when used on any number of publications. The size, orientation and colour may change, but the logo remains uniquely identifiable. The same is true of images that are reproduced many times. This means that visual items are independent of their physical support.
The class E36 Visual Item provides a means of identifying and linking together instances of E24 Physical Man-Made Thing that carry the same visual symbols, marks or images etc. The property P62 depicts (is depicted by) between E24 Physical Man-Made Thing and depicted subjects (E1 CRM Entity) can be regarded as a short-cut of the more fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1CRM Entity, which in addition captures the optical features of the depiction.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (281, 'class', 'name', 36, 'ru', 'Пометка', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (282, 'class', 'name', 36, 'fr', 'Marque', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (283, 'class', 'name', 36, 'el', 'Σήμανση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (284, 'class', 'name', 36, 'en', 'Mark', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (285, 'class', 'name', 36, 'de', 'Marke', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (286, 'class', 'name', 36, 'pt', 'Marca', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (287, 'class', 'name', 36, 'cn', '标志', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (288, 'class', 'comment', 36, 'en', 'This class comprises symbols, signs, signatures or short texts applied to instances of E24 Physical Man-Made Thing by arbitrary techniques in order to indicate the creator, owner, dedications, purpose, etc.
This class specifically excludes features that have no semantic significance, such as scratches or tool marks. These should be documented as instances of E25 Man-Made Feature.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (289, 'class', 'name', 37, 'ru', 'Изображение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (290, 'class', 'name', 37, 'el', 'Εικόνα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (291, 'class', 'name', 37, 'de', 'Bild', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (292, 'class', 'name', 37, 'fr', 'Image', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (293, 'class', 'name', 37, 'en', 'Image', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (294, 'class', 'name', 37, 'pt', 'Imagem', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (295, 'class', 'name', 37, 'cn', '图像', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (296, 'class', 'comment', 37, 'en', 'This class comprises distributions of form, tone and colour that may be found on surfaces such as photos, paintings, prints and sculptures or directly on electronic media.
The degree to which variations in the distribution of form and colour affect the identity of an instance of E38 Image depends on a given purpose. The original painting of the Mona Lisa in the Louvre may be said to bear the same instance of E38 Image as reproductions in the form of transparencies, postcards, posters or T-shirts, even though they may differ in size and carrier and may vary in tone and colour. The images in a “spot the difference” competition are not the same with respect to their context, however similar they may at first appear.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (297, 'class', 'name', 38, 'de', 'Akteur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (298, 'class', 'name', 38, 'ru', 'Агент', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (299, 'class', 'name', 38, 'fr', 'Agent', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (300, 'class', 'name', 38, 'el', 'Δράστης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (301, 'class', 'name', 38, 'en', 'Actor', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (302, 'class', 'name', 38, 'pt', 'Agente', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (303, 'class', 'name', 38, 'cn', '角色', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (304, 'class', 'comment', 38, 'en', 'This class comprises people, either individually or in groups, who have the potential to perform intentional actions for which they can be held responsible.
The CRM does not attempt to model the inadvertent actions of such actors. Individual people should be documented as instances of E21 Person, whereas groups should be documented as instances of either E74 Group or its subclass E40 Legal Body.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (305, 'class', 'name', 39, 'fr', 'Collectivité', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (306, 'class', 'name', 39, 'de', 'Juristische Person', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (307, 'class', 'name', 39, 'el', 'Νομικό Πρόσωπο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (308, 'class', 'name', 39, 'ru', 'Юридическое Лицо', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (309, 'class', 'name', 39, 'en', 'Legal Body', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (310, 'class', 'name', 39, 'pt', 'Pessoa Jurídica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (311, 'class', 'name', 39, 'cn', '法律组织', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (312, 'class', 'comment', 39, 'en', 'This class comprises institutions or groups of people that have obtained a legal recognition as a group and can act collectively as agents.
This means that they can perform actions, own property, create or destroy things and can be held collectively responsible for their actions like individual people. The term ''personne morale'' is often used for this in French.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (313, 'class', 'name', 40, 'de', 'Benennung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (314, 'class', 'name', 40, 'ru', 'Обозначение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (315, 'class', 'name', 40, 'en', 'Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (316, 'class', 'name', 40, 'fr', 'Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (317, 'class', 'name', 40, 'el', 'Ονομασία', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (318, 'class', 'name', 40, 'pt', 'Designação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (319, 'class', 'name', 40, 'cn', '称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (320, 'class', 'comment', 40, 'en', 'This class comprises signs, either meaningful or not, or arrangements of signs following a specific syntax, that are used or can be used to refer to and identify a specific instance of some class or category within a certain context.
Instances of E41 Appellation do not identify things by their meaning, even if they happen to have one, but instead by convention, tradition, or agreement. Instances of E41 Appellation are cultural constructs; as such, they have a context, a history, and a use in time and space by some group of users. A given instance of E41 Appellation can have alternative forms, i.e., other instances of E41 Appellation that are always regarded as equivalent independent from the thing it denotes.
Specific subclasses of E41 Appellation should be used when instances of E41 Appellation of a characteristic form are used for particular objects. Instances of E49 Time Appellation, for example, which take the form of instances of E50 Date, can be easily recognised.
E41 Appellation should not be confused with the act of naming something. Cf. E15 Identifier Assignment
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (321, 'class', 'name', 41, 'fr', 'Identificateur d''objet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (322, 'class', 'name', 41, 'el', 'Κωδικός Αναγνώρισης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (323, 'class', 'name', 41, 'ru', 'Идентификатор Объекта', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (324, 'class', 'name', 41, 'de', 'Kennung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (325, 'class', 'name', 41, 'en', 'Identifier', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (326, 'class', 'name', 41, 'pt', 'Identificador de Objeto', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (327, 'class', 'name', 41, 'cn', '标识符', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (328, 'class', 'comment', 41, 'en', 'This class comprises strings or codes assigned to instances of E1 CRM Entity in order to identify them uniquely and permanently within the context of one or more organisations. Such codes are often known as inventory numbers, registration codes, etc. and are typically composed of alphanumeric sequences. The class E42 Identifier is not normally used for machine-generated identifiers used for automated processing unless these are also used by human agents.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (329, 'class', 'name', 42, 'ru', 'Обозначение Места', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (330, 'class', 'name', 42, 'en', 'Place Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (331, 'class', 'name', 42, 'fr', 'Appellation de lieu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (332, 'class', 'name', 42, 'de', 'Ortsbenennung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (333, 'class', 'name', 42, 'el', 'Ονομασία Τόπου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (334, 'class', 'name', 42, 'pt', 'Designação de Local', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (335, 'class', 'name', 42, 'cn', '地点称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (336, 'class', 'comment', 42, 'en', 'This class comprises any sort of identifier characteristically used to refer to an E53 Place.
Instances of E44 Place Appellation may vary in their degree of precision and their meaning may vary over time - the same instance of E44 Place Appellation may be used to refer to several places, either because of cultural shifts, or because objects used as reference points have moved around. Instances of E44 Place Appellation can be extremely varied in form: postal addresses, instances of E47 Spatial Coordinate, and parts of buildings can all be considered as instances of E44 Place Appellation.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (337, 'class', 'name', 43, 'fr', 'Adresse', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (338, 'class', 'name', 43, 'de', 'Adresse', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (339, 'class', 'name', 43, 'el', 'Διεύθυνση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (340, 'class', 'name', 43, 'ru', 'Адрес', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (341, 'class', 'name', 43, 'en', 'Address', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (342, 'class', 'name', 43, 'pt', 'Endereço', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (343, 'class', 'name', 43, 'cn', '地址', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (496, 'class', 'comment', 62, 'en', 'This class comprises the events that result in the formal or informal termination of an E74 Group of people.
If the dissolution was deliberate, the Dissolution event should also be instantiated as an E7 Activity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (497, 'class', 'name', 63, 'ru', 'Смерть', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (344, 'class', 'comment', 43, 'en', 'This class comprises identifiers expressed in coding systems for places, such as postal addresses used for mailing.
An E45 Address can be considered both as the name of an E53 Place and as an E51 Contact Point for an E39 Actor. This dual aspect is reflected in the multiple inheritance. However, some forms of mailing addresses, such as a postal box, are only instances of E51 Contact Point, since they do not identify any particular Place. These should not be documented as instances of E45 Address.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (345, 'class', 'name', 44, 'fr', 'Désignation de section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (346, 'class', 'name', 44, 'ru', 'Определение Района', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (347, 'class', 'name', 44, 'en', 'Section Definition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (348, 'class', 'name', 44, 'de', 'Abschnittsdefinition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (349, 'class', 'name', 44, 'el', 'Ονομασία Τμήματος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (350, 'class', 'name', 44, 'pt', 'Designação de Seção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (351, 'class', 'name', 44, 'cn', '区域定义', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (352, 'class', 'comment', 44, 'en', 'This class comprises areas of objects referred to in terms specific to the general geometry or structure of its kind.
The ''prow'' of the boat, the ''frame'' of the picture, the ''front'' of the building are all instances of E46 Section Definition. The class highlights the fact that parts of objects can be treated as locations. This holds in particular for features without natural boundaries, such as the “head” of a marble statue made out of one block (cf. E53 Place). In answer to the question ''where is the signature?'' one might reply ''on the lower left corner''. (Section Definition is closely related to the term “segment” in Gerstl, P.& Pribbenow, S, 1996 “ A conceptual theory of part – whole relations and its applications”, Data & Knowledge 	Engineering 20 305-322, North Holland- Elsevier ).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (353, 'class', 'name', 45, 'fr', 'Coordonnées spatiales', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (354, 'class', 'name', 45, 'ru', 'Пространственные Координаты', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (355, 'class', 'name', 45, 'el', 'Χωρικές Συντεταγμένες', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (356, 'class', 'name', 45, 'de', 'Raumkoordinaten', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (357, 'class', 'name', 45, 'en', 'Spatial Coordinates', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (358, 'class', 'name', 45, 'pt', 'Coordenadas Espaciais', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (359, 'class', 'name', 45, 'cn', '空间坐标', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (360, 'class', 'comment', 45, 'en', 'This class comprises the textual or numeric information required to locate specific instances of E53 Place within schemes of spatial identification.

Coordinates are a specific form of E44 Place Appellation, that is, a means of referring to a particular E53 Place. Coordinates are not restricted to longitude, latitude and altitude. Any regular system of reference that maps onto an E19 Physical Object can be used to generate coordinates.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (361, 'class', 'name', 46, 'ru', 'Название Места', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (362, 'class', 'name', 46, 'fr', 'Toponyme', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (363, 'class', 'name', 46, 'el', 'Τοπωνύμιο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (364, 'class', 'name', 46, 'en', 'Place Name', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (365, 'class', 'name', 46, 'de', 'Orts- oder Flurname', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (366, 'class', 'name', 46, 'pt', 'Nome de Local', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (367, 'class', 'name', 46, 'cn', '地名', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (368, 'class', 'comment', 46, 'en', 'This class comprises particular and common forms of E44 Place Appellation.
Place Names may change their application over time: the name of an E53 Place may change, and a name may be reused for a different E53 Place. Instances of E48 Place Name are typically subject to place name gazetteers.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (369, 'class', 'name', 47, 'ru', 'Обозначение Времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (370, 'class', 'name', 47, 'el', 'Ονομασία Χρόνου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (371, 'class', 'name', 47, 'de', 'Zeitbenennung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (372, 'class', 'name', 47, 'en', 'Time Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (373, 'class', 'name', 47, 'fr', 'Appellation temporelle', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (374, 'class', 'name', 47, 'pt', 'Designação de Tempo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (375, 'class', 'name', 47, 'cn', '时间称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (376, 'class', 'comment', 47, 'en', 'This class comprises all forms of names or codes, such as historical periods, and dates, which are characteristically used to refer to a specific E52 Time-Span.
The instances of E49 Time Appellation may vary in their degree of precision, and they may be relative to other time frames, “Before Christ” for example. Instances of E52 Time-Span are often defined by reference to a cultural period or an event e.g. ‘the duration of the Ming Dynasty’.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (377, 'class', 'name', 48, 'de', 'Datum', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (378, 'class', 'name', 48, 'el', 'Ημερομηνία', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (379, 'class', 'name', 48, 'ru', 'Дата', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (380, 'class', 'name', 48, 'fr', 'Date', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (381, 'class', 'name', 48, 'en', 'Date', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (382, 'class', 'name', 48, 'pt', 'Data', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (383, 'class', 'name', 48, 'cn', '日期', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (384, 'class', 'comment', 48, 'en', 'This class comprises specific forms of E49 Time Appellation.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (385, 'class', 'name', 49, 'de', 'Kontaktpunkt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (386, 'class', 'name', 49, 'el', 'Στοιχείο Επικοινωνίας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (387, 'class', 'name', 49, 'fr', 'Coordonnées individuelles', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (388, 'class', 'name', 49, 'en', 'Contact Point', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (389, 'class', 'name', 49, 'ru', 'Контакт', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (390, 'class', 'name', 49, 'pt', 'Ponto de Contato', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (391, 'class', 'name', 49, 'cn', '联系方式', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (392, 'class', 'comment', 49, 'en', 'This class comprises identifiers employed, or understood, by communication services to direct communications to an instance of E39 Actor. These include E-mail addresses, telephone numbers, post office boxes, Fax numbers, URLs etc. Most postal addresses can be considered both as instances of E44 Place Appellation and E51 Contact Point. In such cases the subclass E45 Address should be used.
URLs are addresses used by machines to access another machine through an http request. Since the accessed machine acts on behalf of the E39 Actor providing the machine, URLs are considered as instances of E51 Contact Point to that E39 Actor.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (393, 'class', 'name', 50, 'fr', 'Durée', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (394, 'class', 'name', 50, 'de', 'Zeitspanne', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (395, 'class', 'name', 50, 'ru', 'Интервал Времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (396, 'class', 'name', 50, 'el', 'Χρονικό Διάστημα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (397, 'class', 'name', 50, 'en', 'Time-Span', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (398, 'class', 'name', 50, 'pt', 'Período de Tempo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (399, 'class', 'name', 50, 'cn', '时段', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (498, 'class', 'name', 63, 'en', 'Death', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (499, 'class', 'name', 63, 'de', 'Tod', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (500, 'class', 'name', 63, 'fr', 'Mort', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (501, 'class', 'name', 63, 'el', 'Θάνατος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (502, 'class', 'name', 63, 'pt', 'Morte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (503, 'class', 'name', 63, 'cn', '死亡', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (400, 'class', 'comment', 50, 'en', 'This class comprises abstract temporal extents, in the sense of Galilean physics, having a beginning, an end and a duration.
Time Span has no other semantic connotations. Time-Spans are used to define the temporal extent of instances of E4 Period, E5 Event and any other phenomena valid for a certain time. An E52 Time-Span may be identified by one or more instances of E49 Time Appellation.
Since our knowledge of history is imperfect, instances of E52 Time-Span can best be considered as approximations of the actual Time-Spans of temporal entities. The properties of E52 Time-Span are intended to allow these approximations to be expressed precisely.  An extreme case of approximation, might, for example, define an E52 Time-Span having unknown beginning, end and duration. Used as a common E52 Time-Span for two events, it would nevertheless define them as being simultaneous, even if nothing else was known.
	Automatic processing and querying of instances of E52 Time-Span is facilitated if data can be parsed into an E61 Time Primitive.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (401, 'class', 'name', 51, 'fr', 'Lieu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (402, 'class', 'name', 51, 'en', 'Place', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (403, 'class', 'name', 51, 'el', 'Τόπος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (404, 'class', 'name', 51, 'ru', 'Место', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (405, 'class', 'name', 51, 'de', 'Ort', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (406, 'class', 'name', 51, 'pt', 'Local', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (407, 'class', 'name', 51, 'cn', '地点', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (408, 'class', 'comment', 51, 'en', 'This class comprises extents in space, in particular on the surface of the earth, in the pure sense of physics: independent from temporal phenomena and matter.
The instances of E53 Place are usually determined by reference to the position of “immobile” objects such as buildings, cities, mountains, rivers, or dedicated geodetic marks. A Place can be determined by combining a frame of reference and a location with respect to this frame. It may be identified by one or more instances of E44 Place Appellation.
 It is sometimes argued that instances of E53 Place are best identified by global coordinates or absolute reference systems. However, relative references are often more relevant in the context of cultural documentation and tend to be more precise. In particular, we are often interested in position in relation to large, mobile objects, such as ships. For example, the Place at which Nelson died is known with reference to a large mobile object – H.M.S Victory. A resolution of this Place in terms of absolute coordinates would require knowledge of the movements of the vessel and the precise time of death, either of which may be revised, and the result would lack historical and cultural relevance.
Any object can serve as a frame of reference for E53 Place determination. The model foresees the notion of a "section" of an E19 Physical Object as a valid E53 Place determination.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (409, 'class', 'name', 52, 'en', 'Dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (410, 'class', 'name', 52, 'fr', 'Dimensions', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (411, 'class', 'name', 52, 'el', 'Μέγεθος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (412, 'class', 'name', 52, 'ru', 'Величина', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (413, 'class', 'name', 52, 'de', 'Maß', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (414, 'class', 'name', 52, 'pt', 'Dimensão', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (415, 'class', 'name', 52, 'cn', '规模数量', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (416, 'class', 'comment', 52, 'en', 'This class comprises quantifiable properties that can be measured by some calibrated means and can be approximated by values, i.e. points or regions in a mathematical or conceptual space, such as natural or real numbers, RGB values etc.
An instance of E54 Dimension represents the true quantity, independent from its numerical approximation, e.g. in inches or in cm. The properties of the class E54 Dimension allow for expressing the numerical approximation of the values of an instance of E54 Dimension. If the true values belong to a non-discrete space, such as spatial distances, it is recommended to record them as approximations by intervals or regions of indeterminacy enclosing the assumed true values. For instance, a length of 5 cm may be recorded as 4.5-5.5 cm, according to the precision of the respective observation. Note, that interoperability of values described in different units depends critically on the representation as value regions.
Numerical approximations in archaic instances of E58 Measurement Unit used in historical records should be preserved. Equivalents corresponding to current knowledge should be recorded as additional instances of E54 Dimension as appropriate.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (417, 'class', 'name', 53, 'el', 'Τύπος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (418, 'class', 'name', 53, 'en', 'Type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (419, 'class', 'name', 53, 'fr', 'Type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (420, 'class', 'name', 53, 'ru', 'Тип', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (421, 'class', 'name', 53, 'de', 'Typus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (422, 'class', 'name', 53, 'pt', 'Tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (423, 'class', 'name', 53, 'cn', '类型', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (424, 'class', 'comment', 53, 'en', 'This class comprises concepts denoted by terms from thesauri and controlled vocabularies used to characterize and classify instances of CRM classes. Instances of E55 Type represent concepts  in contrast to instances of E41 Appellation which are used to name instances of CRM classes.
E55 Type is the CRM’s interface to domain specific ontologies and thesauri. These can be represented in the CRM as subclasses of E55 Type, forming hierarchies of terms, i.e. instances of E55 Type linked via P127 has broader  term (has narrower term). Such hierarchies may be extended with additional properties.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (425, 'class', 'name', 54, 'fr', 'Langue', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (426, 'class', 'name', 54, 'ru', 'Язык', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (427, 'class', 'name', 54, 'en', 'Language', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (428, 'class', 'name', 54, 'el', 'Γλώσσα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (429, 'class', 'name', 54, 'de', 'Sprache', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (430, 'class', 'name', 54, 'pt', 'Língua', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (431, 'class', 'name', 54, 'cn', '语言', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (432, 'class', 'comment', 54, 'en', 'This class is a specialization of E55 Type and comprises the natural languages in the sense of concepts.
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E56 Language, e.g.: “instances of  Mandarin Chinese”.
It is recommended that internationally or nationally agreed codes and terminology are used to denote instances of E56 Language, such as those defined in ISO 639:1988.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (433, 'class', 'name', 55, 'fr', 'Matériau', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (434, 'class', 'name', 55, 'el', 'Υλικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (435, 'class', 'name', 55, 'ru', 'Материал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (436, 'class', 'name', 55, 'en', 'Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (437, 'class', 'name', 55, 'de', 'Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (438, 'class', 'name', 55, 'pt', 'Material', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (439, 'class', 'name', 55, 'cn', '材料', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (504, 'class', 'comment', 63, 'en', 'This class comprises the deaths of human beings.
If a person is killed, their death should be instantiated as E69 Death and as E7 Activity. The death or perishing of other living beings should be documented using E64 End of Existence.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (505, 'class', 'name', 64, 'ru', '', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (506, 'class', 'name', 64, 'fr', 'Chose', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (507, 'class', 'name', 64, 'en', 'Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (508, 'class', 'name', 64, 'el', 'Πράγμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (440, 'class', 'comment', 55, 'en', 'This class is a specialization of E55 Type and comprises the concepts of materials.
Instances of E57 Material may denote properties of matter before its use, during its use, and as incorporated in an object, such as ultramarine powder, tempera paste, reinforced concrete. Discrete pieces of raw-materials kept in museums, such as bricks, sheets of fabric, pieces of metal, should be modelled individually in the same way as other objects. Discrete used or processed pieces, such as the stones from Nefer Titi''s temple, should be modelled as parts (cf. P46 is composed of).
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E57 Material, e.g.: “instances of  gold”.
It is recommended that internationally or nationally agreed codes and terminology are used.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (441, 'class', 'name', 56, 'fr', 'Unité de mesure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (442, 'class', 'name', 56, 'en', 'Measurement Unit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (443, 'class', 'name', 56, 'el', 'Μονάδα Μέτρησης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (444, 'class', 'name', 56, 'de', 'Maßeinheit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (445, 'class', 'name', 56, 'ru', 'Единица Измерения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (446, 'class', 'name', 56, 'pt', 'Unidade de Medida', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (447, 'class', 'name', 56, 'cn', '测量单位', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (448, 'class', 'comment', 56, 'en', 'This class is a specialization of E55 Type and comprises the types of measurement units: feet, inches, centimetres, litres, lumens, etc.
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E58 Measurement Unit, e.g.: “instances of cm”.
Syst?me International (SI) units or internationally recognized non-SI terms should be used whenever possible. (ISO 1000:1992). Archaic Measurement Units used in historical records should be preserved.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (449, 'class', 'name', 57, 'fr', 'Début d''existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (450, 'class', 'name', 57, 'en', 'Beginning of Existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (451, 'class', 'name', 57, 'de', 'Daseinsbeginn', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (452, 'class', 'name', 57, 'el', 'Αρχή Ύπαρξης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (453, 'class', 'name', 57, 'ru', 'Начало Существования', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (454, 'class', 'name', 57, 'pt', 'Início da Existência', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (455, 'class', 'name', 57, 'cn', '存在开始', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (456, 'class', 'comment', 57, 'en', 'This class comprises events that bring into existence any E77 Persistent Item.
It may be used for temporal reasoning about things (intellectual products, physical items, groups of people, living beings) beginning to exist; it serves as a hook for determination of a terminus post quem and ante quem. ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (457, 'class', 'name', 58, 'de', 'Daseinsende', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (458, 'class', 'name', 58, 'ru', 'Конец Существования', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (459, 'class', 'name', 58, 'el', 'Τέλος Ύπαρξης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (460, 'class', 'name', 58, 'fr', 'Fin d''existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (461, 'class', 'name', 58, 'en', 'End of Existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (462, 'class', 'name', 58, 'pt', 'Fim da Existência', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (463, 'class', 'name', 58, 'cn', '存在结束', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (464, 'class', 'comment', 58, 'en', 'This class comprises events that end the existence of any E77 Persistent Item.
It may be used for temporal reasoning about things (physical items, groups of people, living beings) ceasing to exist; it serves as a hook for determination of a terminus postquem and antequem. In cases where substance from a Persistent Item continues to exist in a new form, the process would be documented by E81 Transformation.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (465, 'class', 'name', 59, 'el', 'Δημιουργία', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (466, 'class', 'name', 59, 'ru', 'Событие Творения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (467, 'class', 'name', 59, 'fr', 'Création', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (468, 'class', 'name', 59, 'de', 'Begriffliche Schöpfung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (469, 'class', 'name', 59, 'en', 'Creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (470, 'class', 'name', 59, 'pt', 'Criação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (471, 'class', 'name', 59, 'cn', '创造', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (472, 'class', 'comment', 59, 'en', 'This class comprises events that result in the creation of conceptual items or immaterial products, such as legends, poems, texts, music, images, movies, laws, types etc.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (473, 'class', 'name', 60, 'en', 'Formation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (474, 'class', 'name', 60, 'ru', 'Событие Формирования', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (475, 'class', 'name', 60, 'fr', 'Formation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (476, 'class', 'name', 60, 'de', 'Gruppenbildung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (477, 'class', 'name', 60, 'el', 'Συγκρότηση Ομάδας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (478, 'class', 'name', 60, 'pt', 'Formação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (479, 'class', 'name', 60, 'cn', '组成', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (480, 'class', 'comment', 60, 'en', 'This class comprises events that result in the formation of a formal or informal E74 Group of people, such as a club, society, association, corporation or nation.
E66 Formation does not include the arbitrary aggregation of people who do not act as a collective.
The formation of an instance of E74 Group does not mean that the group is populated with members at the time of formation. In order to express the joining of members at the time of formation, the respective activity should be simultaneously an instance of both E66 Formation and E85 Joining.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (481, 'class', 'name', 61, 'en', 'Birth', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (482, 'class', 'name', 61, 'ru', 'Рождение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (483, 'class', 'name', 61, 'fr', 'Naissance', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (484, 'class', 'name', 61, 'de', 'Geburt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (485, 'class', 'name', 61, 'el', 'Γέννηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (486, 'class', 'name', 61, 'pt', 'Nascimento', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (487, 'class', 'name', 61, 'cn', '诞生', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (488, 'class', 'comment', 61, 'en', 'This class comprises the births of human beings. E67 Birth is a biological event focussing on the context of people coming into life. (E63 Beginning of Existence comprises the coming into life of any living beings).
Twins, triplets etc. are brought into life by the same E67 Birth event. The introduction of the E67 Birth event as a documentation element allows the description of a range of family relationships in a simple model. Suitable extensions may describe more details and the complexity of motherhood with the intervention of modern medicine. In this model, the biological father is not seen as a necessary participant in the E67 Birth event.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (489, 'class', 'name', 62, 'ru', 'Роспуск', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (490, 'class', 'name', 62, 'de', 'Gruppenauflösung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (491, 'class', 'name', 62, 'el', 'Διάλυση Ομάδας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (492, 'class', 'name', 62, 'en', 'Dissolution', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (493, 'class', 'name', 62, 'fr', 'Dissolution', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (494, 'class', 'name', 62, 'pt', 'Dissolução', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (495, 'class', 'name', 62, 'cn', '解散', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (509, 'class', 'name', 64, 'de', 'Sache', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (510, 'class', 'name', 64, 'pt', 'Coisa', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (511, 'class', 'name', 64, 'cn', '万物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (512, 'class', 'comment', 64, 'en', 'This general class comprises usable discrete, identifiable, instances of E77 Persistent Item that are documented as single units.

They can be either intellectual products or physical things, and are characterized by relative stability. They may for instance either have a solid physical form, an electronic encoding, or they may be logical concept or structure.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (513, 'class', 'name', 65, 'de', 'Künstliches', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (514, 'class', 'name', 65, 'fr', 'Chose fabriquée', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (515, 'class', 'name', 65, 'ru', 'Рукотворная Вещь', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (516, 'class', 'name', 65, 'en', 'Man-Made Thing', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (517, 'class', 'name', 65, 'el', 'Ανθρώπινο Δημιούργημα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (518, 'class', 'name', 65, 'pt', 'Coisa Fabricada', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (519, 'class', 'name', 65, 'cn', '人造物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (520, 'class', 'comment', 65, 'en', 'This class comprises discrete, identifiable man-made items that are documented as single units.
These items are either intellectual products or man-made physical things, and are characterized by relative stability. They may for instance have a solid physical form, an electronic encoding, or they may be logical concepts or structures.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (521, 'class', 'name', 66, 'fr', 'Objet juridique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (522, 'class', 'name', 66, 'ru', 'Объект Права', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (523, 'class', 'name', 66, 'el', 'Νομικό Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (524, 'class', 'name', 66, 'en', 'Legal Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (525, 'class', 'name', 66, 'de', 'Rechtsobjekt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (526, 'class', 'name', 66, 'pt', 'Objeto Jurídico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (527, 'class', 'name', 66, 'cn', '法律物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (528, 'class', 'comment', 66, 'en', 'This class comprises those material or immaterial items to which instances of E30 Right, such as the right of ownership or use, can be applied.
This is true for all E18 Physical Thing. In the case of instances of E28 Conceptual Object, however, the identity of the E28 Conceptual Object or the method of its use may be too ambiguous to reliably establish instances of E30 Right, as in the case of taxa and inspirations. Ownership of corporations is currently regarded as out of scope of the CRM.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (529, 'class', 'name', 67, 'de', 'Informationsgegenstand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (530, 'class', 'name', 67, 'en', 'Information Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (531, 'class', 'name', 67, 'el', 'Πληροφοριακό Αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (532, 'class', 'name', 67, 'fr', 'Objet d''information', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (533, 'class', 'name', 67, 'ru', 'Информационный Объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (534, 'class', 'name', 67, 'pt', 'Objeto de Informação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (535, 'class', 'name', 67, 'cn', '信息物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (536, 'class', 'comment', 67, 'en', 'This class comprises identifiable immaterial items, such as a poems, jokes, data sets, images, texts, multimedia objects, procedural prescriptions, computer program code, algorithm or mathematical formulae, that have an objectively recognizable structure and are documented as single units.
An E73 Information Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously.
Instances of E73 Information Object of a linguistic nature should be declared as instances of the E33 Linguistic Object subclass. Instances of E73 Information Object of a documentary nature should be declared as instances of the E31 Document subclass. Conceptual items such as types and classes are not instances of E73 Information Object, nor are ideas without a reproducible expression.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (537, 'class', 'name', 68, 'ru', 'Группа', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (538, 'class', 'name', 68, 'en', 'Group', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (539, 'class', 'name', 68, 'el', 'Ομάδα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (540, 'class', 'name', 68, 'de', 'Menschliche Gruppe', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (541, 'class', 'name', 68, 'fr', 'Groupe', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (542, 'class', 'name', 68, 'pt', 'Grupo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (543, 'class', 'name', 68, 'cn', '群组', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (544, 'class', 'comment', 68, 'en', 'This class comprises any gatherings or organizations of two or more people that act collectively or in a similar way due to any form of unifying relationship. In the wider sense this class also comprises official positions which used to be regarded in certain contexts as one actor, independent of the current holder of the office, such as the president of a country.
A gathering of people becomes an E74 Group when it exhibits organizational characteristics usually typified by a set of ideas or beliefs held in common, or actions performed together. These might be communication, creating some common artifact, a common purpose such as study, worship, business, sports, etc. Nationality can be modeled as membership in an E74 Group (cf. HumanML markup). Married couples and other concepts of family are regarded as particular examples of E74 Group.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (545, 'class', 'name', 69, 'fr', 'Appellation d''objet conceptuel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (546, 'class', 'name', 69, 'ru', 'Обозначение Концептуального Объекта', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (547, 'class', 'name', 69, 'de', 'Begriff- oder Konzeptbenennung ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (548, 'class', 'name', 69, 'en', 'Conceptual Object Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (549, 'class', 'name', 69, 'el', 'Ονομασία Νοητικού Αντικειμένου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (550, 'class', 'name', 69, 'pt', 'Designação de Objeto Conceitual', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (551, 'class', 'name', 69, 'cn', '概念物件称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (552, 'class', 'comment', 69, 'en', 'This class comprises all appellations specific to intellectual products or standardized patterns.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (553, 'class', 'name', 70, 'en', 'Persistent Item', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (554, 'class', 'name', 70, 'ru', 'Постоянная Сущность', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (555, 'class', 'name', 70, 'de', 'Seiendes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (556, 'class', 'name', 70, 'el', 'Ον', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (557, 'class', 'name', 70, 'fr', 'Entité persistante', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (558, 'class', 'name', 70, 'pt', 'Entidade Persistente', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (559, 'class', 'name', 70, 'cn', '持续性项目', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (592, 'class', 'comment', 74, 'en', 'This class comprises the events that result in the simultaneous destruction of one or more than one E77 Persistent Item and the creation of one or more than one E77 Persistent Item that preserves recognizable substance from the first one(s) but has fundamentally different nature and identity.
Although the old and the new instances of E77 Persistent Item are treated as discrete entities having separate, unique identities, they are causally connected through the E81 Transformation; the destruction of the old E77 Persistent Item(s) directly causes the creation of the new one(s) using or preserving some relevant substance. Instances of E81 Transformation are therefore distinct from re-classifications (documented using E17 Type Assignment) or modifications (documented using E11 Modification) of objects that do not fundamentally change their nature or identity. Characteristic cases are reconstructions and repurposing of historical buildings or ruins, fires leaving buildings in ruins, taxidermy of specimen in natural history and the reorganization of a corporate body into a new one.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (560, 'class', 'comment', 70, 'en', 'This class comprises items that have a persistent identity, sometimes known as “endurants” in philosophy.
They can be repeatedly recognized within the duration of their existence by identity criteria rather than by continuity or observation. Persistent Items can be either physical entities, such as people, animals or things, or conceptual entities such as ideas, concepts, products of the imagination or common names.
The criteria that determine the identity of an item are often difficult to establish -; the decision depends largely on the judgement of the observer. For example, a building is regarded as no longer existing if it is dismantled and the materials reused in a different configuration. On the other hand, human beings go through radical and profound changes during their life-span, affecting both material composition and form, yet preserve their identity by other criteria. Similarly, inanimate objects may be subject to exchange of parts and matter. The class E77 Persistent Item does not take any position about the nature of the applicable identity criteria and if actual knowledge about identity of an instance of this class exists. There may be cases, where the identity of an E77 Persistent Item is not decidable by a certain state of knowledge.
The main classes of objects that fall outside the scope the E77 Persistent Item class are temporal objects such as periods, events and acts, and descriptive properties. ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (561, 'class', 'name', 71, 'ru', 'Коллекция', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (562, 'class', 'name', 71, 'el', 'Συλλογή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (563, 'class', 'name', 71, 'fr', 'Collection', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (564, 'class', 'name', 71, 'en', 'Collection', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (565, 'class', 'name', 71, 'de', 'Sammlung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (566, 'class', 'name', 71, 'pt', 'Coleção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (567, 'class', 'name', 71, 'cn', '收藏', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (568, 'class', 'comment', 71, 'en', 'This class comprises aggregations of instances of E18 Physical Thing that are assembled and maintained (“curated” and “preserved,” in museological terminology) by one or more instances of E39 Actor over time for a specific purpose and audience, and according to a particular collection development plan.
Items may be added or removed from an E78 Collection in pursuit of this plan. This class should not be confused with the E39 Actor maintaining the E78 Collection often referred to with the name of the E78 Collection (e.g. “The Wallace Collection decided…”).
Collective objects in the general sense, like a tomb full of gifts, a folder with stamps or a set of chessmen, should be documented as instances of E19 Physical Object, and not as instances of E78 Collection. This is because they form wholes either because they are physically bound together or because they are kept together for their functionality.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (569, 'class', 'name', 72, 'fr', 'Addition d''élément', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (570, 'class', 'name', 72, 'en', 'Part Addition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (571, 'class', 'name', 72, 'de', 'Teilhinzufügung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (572, 'class', 'name', 72, 'ru', 'Добавление Части', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (573, 'class', 'name', 72, 'el', 'Προσθήκη Μερών', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (574, 'class', 'name', 72, 'pt', 'Adição de Parte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (575, 'class', 'name', 72, 'cn', '部件增加', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (576, 'class', 'comment', 72, 'en', 'This class comprises activities that result in an instance of E24 Physical Man-Made Thing being increased, enlarged or augmented by the addition of a part.
Typical scenarios include the attachment of an accessory, the integration of a component, the addition of an element to an aggregate object, or the accessioning of an object into a curated E78 Collection. Objects to which parts are added are, by definition, man-made, since the addition of a part implies a human activity. Following the addition of parts, the resulting man-made assemblages are treated objectively as single identifiable wholes, made up of constituent or component parts bound together either physically (for example the engine becoming a part of the car), or by sharing a common purpose (such as the 32 chess pieces that make up a chess set). This class of activities forms a basis for reasoning about the history and continuity of identity of objects that are integrated into other objects over time, such as precious gemstones being repeatedly incorporated into different items of jewellery, or cultural artifacts being added to different museum instances of E78 Collection over their lifespan.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (577, 'class', 'name', 73, 'de', 'Teilentfernung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (578, 'class', 'name', 73, 'fr', 'Soustraction d''élément', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (579, 'class', 'name', 73, 'en', 'Part Removal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (580, 'class', 'name', 73, 'ru', 'Удаление Части', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (581, 'class', 'name', 73, 'el', 'Αφαίρεση Μερών', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (582, 'class', 'name', 73, 'pt', 'Remoção de Parte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (583, 'class', 'name', 73, 'cn', '部件删除', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (584, 'class', 'comment', 73, 'en', 'This class comprises the activities that result in an instance of E18 Physical Thing being decreased by the removal of a part.
Typical scenarios include the detachment of an accessory, the removal of a component or part of a composite object, or the deaccessioning of an object from a curated E78 Collection. If the E80 Part Removal results in the total decomposition of the original object into pieces, such that the whole ceases to exist, the activity should instead be modelled as an E81 Transformation, i.e. a simultaneous destruction and production. In cases where the part removed has no discernible identity prior to its removal but does have an identity subsequent to its removal, the activity should be regarded as both E80 Part Removal and E12 Production. This class of activities forms a basis for reasoning about the history, and continuity of identity over time, of objects that are removed from other objects, such as precious gemstones being extracted from different items of jewelry, or cultural artifacts being deaccessioned from different museum collections over their lifespan.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (585, 'class', 'name', 74, 'ru', 'Трансформация', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (586, 'class', 'name', 74, 'en', 'Transformation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (587, 'class', 'name', 74, 'fr', 'Transformation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (588, 'class', 'name', 74, 'de', 'Umwandlung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (589, 'class', 'name', 74, 'el', 'Μετατροπή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (590, 'class', 'name', 74, 'pt', 'Transformação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (591, 'class', 'name', 74, 'cn', '转变', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (593, 'class', 'name', 75, 'en', 'Actor Appellation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (594, 'class', 'name', 75, 'ru', 'Обозначение Агента', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (595, 'class', 'name', 75, 'el', 'Ονομασία Δράστη', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (596, 'class', 'name', 75, 'fr', 'Appellation d''agent', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (597, 'class', 'name', 75, 'de', 'Akteurbenennung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (598, 'class', 'name', 75, 'pt', 'Designação de Agente', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (599, 'class', 'name', 75, 'cn', '角色称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (638, 'class', 'name', 83, 'de', 'Primitiver Wert', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (688, 'property', 'name', 4, 'en', 'has time-span', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (689, 'property', 'name', 4, 'de', 'hat Zeitspanne', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (690, 'property', 'name', 4, 'el', 'βρισκόταν σε εξέλιξη', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (600, 'class', 'comment', 75, 'en', 'This class comprises any sort of name, number, code or symbol characteristically used to identify an E39 Actor.
An E39 Actor will typically have more than one E82 Actor Appellation, and instances of E82 Actor Appellation in turn may have alternative representations. The distinction between corporate and personal names, which is particularly important in library applications, should be made by explicitly linking the E82 Actor Appellation to an instance of either E21 Person or E74 Group/E40 Legal Body. If this is not possible, the distinction can be made through the use of the P2 has type mechanism.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (601, 'class', 'name', 76, 'de', 'Typuserfindung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (602, 'class', 'name', 76, 'ru', 'Создание Типа', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (603, 'class', 'name', 76, 'en', 'Type Creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (604, 'class', 'name', 76, 'fr', 'Création de type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (605, 'class', 'name', 76, 'el', 'Δημιουργία Τύπου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (606, 'class', 'name', 76, 'pt', 'Criação de Tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (607, 'class', 'name', 76, 'cn', '类型创造', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (608, 'class', 'comment', 76, 'en', 'This class comprises activities formally defining new types of items.
It is typically a rigorous scholarly or scientific process that ensures a type is exhaustively described and appropriately named. In some cases, particularly in archaeology and the life sciences, E83 Type Creation requires the identification of an exemplary specimen and the publication of the type definition in an appropriate scholarly forum. The activity of E83 Type Creation is central to research in the life sciences, where a type would be referred to as a “taxon,” the type description as a “protologue,” and the exemplary specimens as “orgininal element” or “holotype”.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (609, 'class', 'name', 77, 'el', 'Φορέας Πληροφορίας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (610, 'class', 'name', 77, 'en', 'Information Carrier', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (611, 'class', 'name', 77, 'ru', 'Носитель Информации', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (612, 'class', 'name', 77, 'fr', 'Support d''information', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (613, 'class', 'name', 77, 'de', 'Informationsträger', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (614, 'class', 'name', 77, 'pt', 'Suporte de Informação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (615, 'class', 'name', 77, 'cn', '信息载体', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (616, 'class', 'comment', 77, 'en', 'This class comprises all instances of E22 Man-Made Object that are explicitly designed to act as persistent physical carriers for instances of E73 Information Object.
This allows a relationship to be asserted between an E19 Physical Object and its immaterial information contents. An E84 Information Carrier may or may not contain information, e.g., a diskette. Note that any E18 Physical Thing may carry information, such as an E34 Inscription. However, unless it was specifically designed for this purpose, it is not an Information Carrier. Therefore the property P128 carries (is carried by) applies to E18 Physical Thing in general.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (617, 'class', 'name', 78, 'de', 'Beitritt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (618, 'class', 'name', 78, 'en', 'Joining', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (619, 'class', 'name', 78, 'cn', '加入', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (620, 'class', 'comment', 78, 'en', 'This class comprises the activities that result in an instance of E39 Actor becoming a member of an instance of E74 Group. This class does not imply initiative by either party.
Typical scenarios include becoming a member of a social organisation, becoming employee of a company, marriage, the adoption of a child by a family and the inauguration of somebody into an official position.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (621, 'class', 'name', 79, 'de', 'Austritt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (622, 'class', 'name', 79, 'en', 'Leaving', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (623, 'class', 'name', 79, 'cn', '脱离', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (624, 'class', 'comment', 79, 'en', 'This class comprises the activities that result in an instance of E39 Actor to be disassociated from an instance of E74 Group. This class does not imply initiative by either party.
Typical scenarios include the termination of membership in a social organisation, ending the employment at a company, divorce, and the end of tenure of somebody in an official position.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (625, 'class', 'name', 80, 'de', 'Kuratorische Tätigkeit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (626, 'class', 'name', 80, 'en', 'Curation Activity', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (627, 'class', 'name', 80, 'cn', '典藏管理', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (628, 'class', 'comment', 80, 'en', 'This class comprises the activities that result in the continuity of management and the preservation and evolution of instances of E78 Collection, following an implicit or explicit curation plan.
It specializes the notion of activity into the curation of a collection and allows the history of curation to be recorded.
Items are accumulated and organized following criteria like subject, chronological period, material type, style of art etc. and can be added or removed from an E78 Collection for a specific purpose and/or audience. The initial aggregation of items of a collection is regarded as an instance of E12 Production Event while the activity of evolving, preserving and promoting a collection is regarded as an instance of E87 Curation Activity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (629, 'class', 'name', 81, 'de', 'Aussagenobjekt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (630, 'class', 'name', 81, 'en', 'Propositional Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (631, 'class', 'name', 81, 'cn', '陈述性物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (632, 'class', 'comment', 81, 'en', 'This class comprises immaterial items, including but not limited to stories, plots, procedural prescriptions, algorithms, laws of physics or images that are, or represent in some sense, sets of propositions about real or imaginary things and that are documented as single units or serve as topics of discourse.

This class also comprises items that are “about” something in the sense of a subject. In the wider sense, this class includes expressions of psychological value such as non-figural art and musical themes. However, conceptual items such as types and classes are not instances of E89 Propositional Object. This should not be confused with the definition of a type, which is indeed an instance of E89 Propositional Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (633, 'class', 'name', 82, 'de', 'Symbolisches Objekt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (634, 'class', 'name', 82, 'en', 'Symbolic Object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (635, 'class', 'name', 82, 'cn', '符号物件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (636, 'class', 'comment', 82, 'en', 'This class comprises identifiable symbols and any aggregation of symbols, such as characters, identifiers, traffic signs, emblems, texts, data sets, images, musical scores, multimedia objects, computer program code or mathematical formulae that have an objectively recognizable structure and that are documented as single units.
	It includes sets of signs of any nature, which may serve to designate something, or to communicate some propositional content.
	An instance of E90 Symbolic Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously. An instance of E90 Symbolic Object may or may not have a specific meaning, for example an arbitrary character string.
	In some cases, the content of an instance of E90 Symbolic Object may completely be represented by a serialized content model, such.. as the property P3 has note allows for describing this content model…P3.1 has type: E55 Type to specify the encoding..
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (637, 'class', 'name', 83, 'en', 'Primitive Value', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (639, 'class', 'comment', 83, 'en', 'This class comprises primitive values used as documentation elements, which are not further elaborated upon within the model. As such they are not considered as elements within our universe of discourse. No specific implementation recommendations are made. It is recommended that the primitive value system from the implementation platform be used to substitute for this class and its subclasses.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (640, 'class', 'name', 84, 'en', 'Number', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (641, 'class', 'name', 84, 'de', 'Zahl', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (642, 'class', 'comment', 84, 'en', 'This class comprises any encoding of computable (algebraic) values such as integers, real numbers, complex numbers, vectors, tensors etc., including intervals of these values to express limited precision. Numbers are fundamentally distinct from identifiers in continua, such as instances of E50 Date and E47 Spatial Coordinate, even though their encoding may be similar. Instances of E60 Number can be combined with each other in algebraic operations to yield other instances of E60 Number, e.g., 1+1=2. Identifiers in continua may be combined with numbers expressing distances to yield new identifiers, e.g., 1924-01-31 + 2 days = 1924-02-02. Cf. E54 Dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (643, 'class', 'name', 85, 'en', 'Time Primitive', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (644, 'class', 'name', 85, 'de', 'Zeitprimitiv', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (645, 'class', 'comment', 85, 'en', 'This class comprises instances of E59 Primitive Value for time that should be implemented with appropriate validation, precision and interval logic to express date ranges relevant to cultural documentation. E61 Time Primitive is not further elaborated upon within the model.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (646, 'class', 'name', 86, 'en', 'String', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (647, 'class', 'name', 86, 'de', 'Zeichenkette', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (648, 'class', 'comment', 86, 'en', 'This class comprises the instances of E59 Primitive Values used for documentation such as free text strings, bitmaps, vector graphics, etc. E62 String is not further elaborated upon within the model', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (649, 'property', 'name', 1, 'el', 'αναγνωρίζεται ως', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (650, 'property', 'name', 1, 'de', 'wird bezeichnet als', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (651, 'property', 'name', 1, 'en', 'is identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (652, 'property', 'name', 1, 'ru', 'идентифицируется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (653, 'property', 'name', 1, 'fr', 'est identifiée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (654, 'property', 'name', 1, 'pt', 'é identificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (655, 'property', 'name', 1, 'cn', '有识别称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (656, 'property', 'name_inverse', 1, 'de', 'bezeichnet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (657, 'property', 'name_inverse', 1, 'ru', 'идентифицирует', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (658, 'property', 'name_inverse', 1, 'fr', 'identifie', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (659, 'property', 'name_inverse', 1, 'el', 'είναι αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (660, 'property', 'name_inverse', 1, 'en', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (661, 'property', 'name_inverse', 1, 'pt', 'identifica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (662, 'property', 'name_inverse', 1, 'cn', '被用来识别', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (663, 'property', 'comment', 1, 'en', 'This property describes the naming or identification of any real world item by a name or any other identifier.
This property is intended for identifiers in general use, which form part of the world the model intends to describe, and not merely for internal database identifiers which are specific to a technical system, unless these latter also have a more general use outside the technical context. This property includes in particular identification by mathematical expressions such as coordinate systems used for the identification of instances of E53 Place. The property does not reveal anything about when, where and by whom this identifier was used. A more detailed representation can be made using the fully developed (i.e. indirect) path through E15 Identifier Assignment.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (664, 'property', 'name', 2, 'de', 'hat den Typus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (665, 'property', 'name', 2, 'en', 'has type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (666, 'property', 'name', 2, 'el', 'έχει τύπο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (667, 'property', 'name', 2, 'fr', 'est de type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (668, 'property', 'name', 2, 'ru', 'имеет тип', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (669, 'property', 'name', 2, 'pt', 'é do tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (670, 'property', 'name', 2, 'cn', '有类型', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (671, 'property', 'name_inverse', 2, 'ru', 'является типом для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (672, 'property', 'name_inverse', 2, 'fr', 'est le type de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (673, 'property', 'name_inverse', 2, 'el', 'είναι ο τύπος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (674, 'property', 'name_inverse', 2, 'de', 'ist Typus von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (675, 'property', 'name_inverse', 2, 'en', 'is type of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (676, 'property', 'name_inverse', 2, 'pt', 'é o tipo de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (677, 'property', 'name_inverse', 2, 'cn', '被用来分类', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (678, 'property', 'comment', 2, 'en', 'This property allows sub typing of CRM entities - a form of specialisation – through the use of a terminological hierarchy, or thesaurus.
The CRM is intended to focus on the high-level entities and relationships needed to describe data structures. Consequently, it does not specialise entities any further than is required for this immediate purpose. However, entities in the isA hierarchy of the CRM may by specialised into any number of sub entities, which can be defined in the E55 Type hierarchy. E51 Contact Point, for example, may be specialised into “e-mail address”, “telephone number”, “post office box”, “URL” etc. none of which figures explicitly in the CRM hierarchy. Sub typing obviously requires consistency between the meaning of the terms assigned and the more general intent of the CRM entity in question.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (679, 'property', 'name', 3, 'de', 'hat Anmerkung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (680, 'property', 'name', 3, 'ru', 'имеет примечание', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (681, 'property', 'name', 3, 'en', 'has note', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (682, 'property', 'name', 3, 'fr', 'a pour note', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (683, 'property', 'name', 3, 'el', 'έχει επεξήγηση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (684, 'property', 'name', 3, 'pt', 'tem nota', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (685, 'property', 'name', 3, 'cn', '有说明', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (686, 'property', 'comment', 3, 'en', 'This property is a container for all informal descriptions about an object that have not been expressed in terms of CRM constructs.
In particular it captures the characterisation of the item itself, its internal structures, appearance etc.
Like property P2 has type (is type of), this property is a consequence of the restricted focus of the CRM. The aim is not to capture, in a structured form, everything that can be said about an item; indeed, the CRM formalism is not regarded as sufficient to express everything that can be said. Good practice requires use of distinct note fields for different aspects of a characterisation. The P3.1 has type property of P3 has note allows differentiation of specific notes, e.g. “construction”, “decoration” etc.
An item may have many notes, but a note is attached to a specific item.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (687, 'property', 'name', 4, 'fr', 'a pour durée', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (691, 'property', 'name', 4, 'ru', 'имеет временной отрезок', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (692, 'property', 'name', 4, 'pt', 'tem período de tempo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (693, 'property', 'name', 4, 'cn', '发生时段是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (694, 'property', 'name_inverse', 4, 'en', 'is time-span of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (695, 'property', 'name_inverse', 4, 'el', 'είναι χρονικό διάστημα του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (696, 'property', 'name_inverse', 4, 'fr', 'est la durée de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (697, 'property', 'name_inverse', 4, 'ru', 'является временным отрезком для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (698, 'property', 'name_inverse', 4, 'de', 'ist Zeitspanne von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (699, 'property', 'name_inverse', 4, 'pt', 'é o período de tempo de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (700, 'property', 'name_inverse', 4, 'cn', '开始并完成了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (701, 'property', 'comment', 4, 'en', 'This property describes the temporal confinement of an instance of an E2 Temporal Entity.
The related E52 Time-Span is understood as the real Time-Span during which the phenomena were active, which make up the temporal entity instance. It does not convey any other meaning than a positioning on the “time-line” of chronology. The Time-Span in turn is approximated by a set of dates (E61 Time Primitive). A temporal entity can have in reality only one Time-Span, but there may exist alternative opinions about it, which we would express by assigning multiple Time-Spans. Related temporal entities may share a Time-Span. Time-Spans may have completely unknown dates but other descriptions by which we can infer knowledge.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (702, 'property', 'name', 5, 'en', 'consists of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (703, 'property', 'name', 5, 'fr', 'consiste en', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (704, 'property', 'name', 5, 'el', 'αποτελείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (705, 'property', 'name', 5, 'de', 'besteht aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (706, 'property', 'name', 5, 'ru', 'состоит из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (707, 'property', 'name', 5, 'pt', 'consiste de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (708, 'property', 'name', 5, 'cn', '包含', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (709, 'property', 'name_inverse', 5, 'de', 'bildet Teil von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (710, 'property', 'name_inverse', 5, 'fr', 'fait partie de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (711, 'property', 'name_inverse', 5, 'ru', 'формирует часть', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (712, 'property', 'name_inverse', 5, 'en', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (713, 'property', 'name_inverse', 5, 'el', 'αποτελεί μέρος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (714, 'property', 'name_inverse', 5, 'pt', 'faz parte de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (715, 'property', 'name_inverse', 5, 'cn', '组成了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (716, 'property', 'comment', 5, 'en', 'This property describes the decomposition of an E3 Condition State into discrete, subsidiary states.
It is assumed that the sub-states into which the condition state is analysed form a logical whole - although the entire story may not be completely known – and that the sub-states are in fact constitutive of the general condition state. For example, a general condition state of “in ruins” may be decomposed into the individual stages of decay', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (717, 'property', 'name', 6, 'fr', 'a eu lieu dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (718, 'property', 'name', 6, 'ru', 'совершался на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (719, 'property', 'name', 6, 'el', 'έλαβε χώρα σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (720, 'property', 'name', 6, 'de', 'fand statt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (721, 'property', 'name', 6, 'en', 'took place at', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (722, 'property', 'name', 6, 'pt', 'ocorreu em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (723, 'property', 'name', 6, 'cn', '发生地在', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (724, 'property', 'name_inverse', 6, 'fr', 'a été témoin de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (725, 'property', 'name_inverse', 6, 'en', 'witnessed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (726, 'property', 'name_inverse', 6, 'de', 'bezeugte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (727, 'property', 'name_inverse', 6, 'ru', 'был местом совершения', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (728, 'property', 'name_inverse', 6, 'el', 'υπήρξε τόπος του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (729, 'property', 'name_inverse', 6, 'pt', 'testemunhou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (730, 'property', 'name_inverse', 6, 'cn', '发生过', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (731, 'property', 'comment', 6, 'en', 'This property describes the spatial location of an instance of E4 Period.
The related E53 Place should be seen as an approximation of the geographical area within which the phenomena that characterise the period in question occurred. P7took place at (witnessed) does not convey any meaning other than spatial positioning (generally on the surface of the earth).  For example, the period “R?volution fran?aise” can be said to have taken place in “France”, the “Victorian” period, may be said to have taken place in “Britain” and its colonies, as well as other parts of Europe and north America.
A period can take place at multiple locations.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (732, 'property', 'name', 7, 'ru', 'имел место на или в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (733, 'property', 'name', 7, 'el', 'έλαβε χώρα σε ή εντός', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (734, 'property', 'name', 7, 'de', 'fand statt auf oder innerhalb von ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (735, 'property', 'name', 7, 'en', 'took place on or within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (736, 'property', 'name', 7, 'fr', 'a eu lieu sur ou dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (737, 'property', 'name', 7, 'pt', 'ocorreu em ou dentro', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (738, 'property', 'name', 7, 'cn', '发生所在物件是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (739, 'property', 'name_inverse', 7, 'ru', 'являлся местом для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (740, 'property', 'name_inverse', 7, 'de', 'bezeugte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (741, 'property', 'name_inverse', 7, 'en', 'witnessed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (742, 'property', 'name_inverse', 7, 'fr', 'a été témoin de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (743, 'property', 'name_inverse', 7, 'el', 'υπήρξε τόπος του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (744, 'property', 'name_inverse', 7, 'pt', 'testemunhou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (745, 'property', 'name_inverse', 7, 'cn', '发生过', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (746, 'property', 'comment', 7, 'en', 'This property describes the location of an instance of E4 Period with respect to an E18 Physical Thing.
P8 took place on or within (witnessed) is a short-cut of a path defining a E53 Place with respect to the geometry of an object. cf. E46 Section Definition.
This property is in effect a special case of P7 took place at. It describes a period that can be located with respect to the space defined by an E18 Physical Thing such as a ship or a building. The precise geographical location of the object during the period in question may be unknown or unimportant.
For example, the French and German armistice of 22 June 1940 was signed in the same railway carriage as the armistice of 11 November 1918.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (747, 'property', 'name', 8, 'el', 'αποτελείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (748, 'property', 'name', 8, 'en', 'consists of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (749, 'property', 'name', 8, 'de', 'setzt sich zusammen aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (750, 'property', 'name', 8, 'ru', 'состоит из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (751, 'property', 'name', 8, 'fr', 'consiste en', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (752, 'property', 'name', 8, 'pt', 'consiste de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (753, 'property', 'name', 8, 'cn', '包含子时期', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (754, 'property', 'name_inverse', 8, 'el', 'αποτελεί μέρος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (755, 'property', 'name_inverse', 8, 'ru', 'формирует часть', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (756, 'property', 'name_inverse', 8, 'de', 'bildet Teil von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (757, 'property', 'name_inverse', 8, 'fr', 'fait partie de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (758, 'property', 'name_inverse', 8, 'en', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (759, 'property', 'name_inverse', 8, 'pt', 'faz parte de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (760, 'property', 'name_inverse', 8, 'cn', '附属於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (761, 'property', 'comment', 8, 'en', 'This property describes the decomposition of an instance of E4 Period into discrete, subsidiary periods.
The sub-periods into which the period is decomposed form a logical whole - although the entire picture may not be completely known - and the sub-periods are constitutive of the general period.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (762, 'property', 'name', 9, 'ru', 'находится в пределах', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (763, 'property', 'name', 9, 'el', 'εμπίπτει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (764, 'property', 'name', 9, 'fr', 's’insère dans le cours de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (765, 'property', 'name', 9, 'en', 'falls within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (766, 'property', 'name', 9, 'de', 'fällt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (767, 'property', 'name', 9, 'pt', 'está contido em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (768, 'property', 'name', 9, 'cn', '发生时间涵盖於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (769, 'property', 'name_inverse', 9, 'el', 'περιλαμβάνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (770, 'property', 'name_inverse', 9, 'ru', 'содержит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (771, 'property', 'name_inverse', 9, 'en', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (772, 'property', 'name_inverse', 9, 'fr', 'contient', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (773, 'property', 'name_inverse', 9, 'de', 'enthält', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (774, 'property', 'name_inverse', 9, 'pt', 'contém', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (775, 'property', 'name_inverse', 9, 'cn', '时间上涵盖', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (776, 'property', 'comment', 9, 'en', 'This property describes an instance of E4 Period, which falls within the E53 Place and E52 Time-Span of another.
The difference with P9 consists of (forms part of) is subtle. Unlike P9 consists of (forms part of), P10 falls within (contains) does not imply any logical connection between the two periods and it may refer to a period of a completely different type.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (777, 'property', 'name', 10, 'fr', 'a eu pour participant', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (778, 'property', 'name', 10, 'ru', 'имел участника', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (779, 'property', 'name', 10, 'de', 'hatte Teilnehmer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (780, 'property', 'name', 10, 'en', 'had participant', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (781, 'property', 'name', 10, 'el', 'είχε συμμέτοχο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (782, 'property', 'name', 10, 'pt', 'tem participante', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (783, 'property', 'name', 10, 'cn', '有参与者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (784, 'property', 'name_inverse', 10, 'el', 'συμμετείχε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (785, 'property', 'name_inverse', 10, 'de', 'nahm Teil an', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (786, 'property', 'name_inverse', 10, 'ru', 'участвовал в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (787, 'property', 'name_inverse', 10, 'en', 'participated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (788, 'property', 'name_inverse', 10, 'fr', 'a participé à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (789, 'property', 'name_inverse', 10, 'pt', 'participa em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (790, 'property', 'name_inverse', 10, 'cn', '参与了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (791, 'property', 'comment', 10, 'en', 'This property describes the active or passive participation of instances of E39 Actors in an E5 Event.
It connects the life-line of the related E39 Actor with the E53 Place and E50 Date of the event. The property implies that the Actor was involved in the event but does not imply any causal relationship. The subject of a portrait can be said to have participated in the creation of the portrait.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (792, 'property', 'name', 11, 'en', 'occurred in the presence of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (793, 'property', 'name', 11, 'ru', 'появился в присутствии', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (794, 'property', 'name', 11, 'de', 'fand statt im Beisein von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (795, 'property', 'name', 11, 'el', 'συνέβη παρουσία του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (796, 'property', 'name', 11, 'fr', 'est arrivé en présence de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (797, 'property', 'name', 11, 'pt', 'ocorreu na presença de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (798, 'property', 'name', 11, 'cn', '发生现场存在', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (799, 'property', 'name_inverse', 11, 'en', 'was present at', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (800, 'property', 'name_inverse', 11, 'el', 'ήταν παρών/παρούσα/παρόν σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (801, 'property', 'name_inverse', 11, 'de', 'war anwesend bei', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (802, 'property', 'name_inverse', 11, 'fr', 'était présent à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (803, 'property', 'name_inverse', 11, 'ru', 'присутствовал при', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (804, 'property', 'name_inverse', 11, 'pt', 'estava presente no', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (805, 'property', 'name_inverse', 11, 'cn', '当时在场於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (806, 'property', 'comment', 11, 'en', 'This property describes the active or passive presence of an E77 Persistent Item in an E5 Event without implying any specific role.
It connects the history of a thing with the E53 Place and E50 Date of an event. For example, an object may be the desk, now in a museum on which a treaty was signed. The presence of an immaterial thing implies the presence of at least one of its carriers.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (807, 'property', 'name', 12, 'de', 'zerstörte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (808, 'property', 'name', 12, 'fr', 'a détruit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (809, 'property', 'name', 12, 'ru', 'уничтожил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (810, 'property', 'name', 12, 'el', 'κατέστρεψε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (811, 'property', 'name', 12, 'en', 'destroyed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (812, 'property', 'name', 12, 'pt', 'destruiu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (813, 'property', 'name', 12, 'cn', '毁灭了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (814, 'property', 'name_inverse', 12, 'de', 'wurde zerstört durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (815, 'property', 'name_inverse', 12, 'en', 'was destroyed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (816, 'property', 'name_inverse', 12, 'el', 'καταστράφηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (817, 'property', 'name_inverse', 12, 'fr', 'a été détruite par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (818, 'property', 'name_inverse', 12, 'ru', 'был уничтожен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (819, 'property', 'name_inverse', 12, 'pt', 'foi destruído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (820, 'property', 'name_inverse', 12, 'cn', '被毁灭於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (821, 'property', 'comment', 12, 'en', 'This property allows specific instances of E18 Physical Thing that have been destroyed to be related to a destruction event.
Destruction implies the end of an item’s life as a subject of cultural documentation – the physical matter of which the item was composed may in fact continue to exist. A destruction event may be contiguous with a Production that brings into existence a derived object composed partly of matter from the destroyed object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (822, 'property', 'name', 13, 'de', 'wurde ausgeführt von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (823, 'property', 'name', 13, 'fr', 'réalisée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (824, 'property', 'name', 13, 'en', 'carried out by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (825, 'property', 'name', 13, 'el', 'πραγματοποιήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (826, 'property', 'name', 13, 'ru', 'выполнялся', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (827, 'property', 'name', 13, 'pt', 'realizada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (828, 'property', 'name', 13, 'cn', '有执行者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (829, 'property', 'name_inverse', 13, 'ru', 'выполнял', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (830, 'property', 'name_inverse', 13, 'el', 'πραγματοποίησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (831, 'property', 'name_inverse', 13, 'de', 'führte aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (832, 'property', 'name_inverse', 13, 'en', 'performed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (833, 'property', 'name_inverse', 13, 'fr', 'a exécuté', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (834, 'property', 'name_inverse', 13, 'pt', 'executou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (835, 'property', 'name_inverse', 13, 'cn', '执行了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (836, 'property', 'comment', 13, 'en', 'This property describes the active participation of an E39 Actor in an E7 Activity.
It implies causal or legal responsibility. The P14.1 in the role of property of the property allows the nature of an Actor’s participation to be specified.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (837, 'property', 'name', 14, 'de', 'wurde beeinflußt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (838, 'property', 'name', 14, 'fr', 'a été influencée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (839, 'property', 'name', 14, 'el', 'επηρεάστηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (840, 'property', 'name', 14, 'ru', 'находился под влиянием', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (841, 'property', 'name', 14, 'en', 'was influenced by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (842, 'property', 'name', 14, 'pt', 'foi influenciado por ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (843, 'property', 'name', 14, 'cn', '有影响事物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (844, 'property', 'name_inverse', 14, 'ru', 'оказал влияние на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (845, 'property', 'name_inverse', 14, 'el', 'επηρέασε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (846, 'property', 'name_inverse', 14, 'fr', 'a influencé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (847, 'property', 'name_inverse', 14, 'de', 'beeinflußte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (848, 'property', 'name_inverse', 14, 'en', 'influenced', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (849, 'property', 'name_inverse', 14, 'pt', 'influenciou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (850, 'property', 'name_inverse', 14, 'cn', '影响了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (851, 'property', 'comment', 14, 'en', 'This is a high level property, which captures the relationship between an E7 Activity and anything that may have had some bearing upon it.
The property has more specific sub properties.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (852, 'property', 'name', 15, 'fr', 'a utilisé l''objet spécifique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (853, 'property', 'name', 15, 'el', 'χρησιμοποίησε αντικείμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (854, 'property', 'name', 15, 'en', 'used specific object', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (855, 'property', 'name', 15, 'de', 'benutzte das bestimmte Objekt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (856, 'property', 'name', 15, 'ru', 'использовал особый объект', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (857, 'property', 'name', 15, 'pt', 'usou objeto específico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (858, 'property', 'name', 15, 'cn', '使用特定物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (859, 'property', 'name_inverse', 15, 'fr', 'a été utilisé pour', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (860, 'property', 'name_inverse', 15, 'de', 'wurde benutzt für', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (861, 'property', 'name_inverse', 15, 'ru', 'был использован для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (862, 'property', 'name_inverse', 15, 'en', 'was used for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (863, 'property', 'name_inverse', 15, 'el', 'χρησιμοποιήθηκε για', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (864, 'property', 'name_inverse', 15, 'pt', 'foi usado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (865, 'property', 'name_inverse', 15, 'cn', '被用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (866, 'property', 'comment', 15, 'en', 'This property describes the use of material or immaterial things in a way essential to the performance or the outcome of an E7 Activity.
This property typically applies to tools, instruments, moulds, raw materials and items embedded in a product. It implies that the presence of the object in question was a necessary condition for the action. For example, the activity of writing this text required the use of a computer. An immaterial thing can be used if at least one of its carriers is present. For example, the software tools on a computer.
Another example is the use of a particular name by a particular group of people over some span to identify a thing, such as a settlement. In this case, the physical carriers of this name are at least the people understanding its use.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (867, 'property', 'name', 16, 'ru', 'был обусловлен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (868, 'property', 'name', 16, 'de', 'wurde angeregt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (869, 'property', 'name', 16, 'el', 'είχε ως αφορμή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (870, 'property', 'name', 16, 'en', 'was motivated by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (871, 'property', 'name', 16, 'fr', 'a été motivée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (872, 'property', 'name', 16, 'pt', 'foi motivado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (873, 'property', 'name', 16, 'cn', '有促动事物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (874, 'property', 'name_inverse', 16, 'el', 'ήταν αφορμή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (875, 'property', 'name_inverse', 16, 'en', 'motivated', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (876, 'property', 'name_inverse', 16, 'de', 'regte an', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (877, 'property', 'name_inverse', 16, 'ru', 'обусловил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (878, 'property', 'name_inverse', 16, 'fr', 'a motivé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (879, 'property', 'name_inverse', 16, 'pt', 'motivou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (880, 'property', 'name_inverse', 16, 'cn', '促动了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (881, 'property', 'comment', 16, 'en', 'This property describes an item or items that are regarded as a reason for carrying out the E7 Activity.
For example, the discovery of a large hoard of treasure may call for a celebration, an order from head quarters can start a military manoeuvre.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (882, 'property', 'name', 17, 'ru', 'был предполагаемым использованием для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (883, 'property', 'name', 17, 'fr', 'était l''utilisation prévue de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (884, 'property', 'name', 17, 'de', 'war beabsichtigteter Gebrauch von ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (885, 'property', 'name', 17, 'el', 'ήταν προορισμένη χρήση του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (886, 'property', 'name', 17, 'en', 'was intended use of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (887, 'property', 'name', 17, 'pt', 'era prevista a utilização de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (888, 'property', 'name', 17, 'cn', '特别使用了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (889, 'property', 'name_inverse', 17, 'fr', 'a été fabriquée pour', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (890, 'property', 'name_inverse', 17, 'el', 'έγινε για', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (891, 'property', 'name_inverse', 17, 'ru', 'был создан для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (892, 'property', 'name_inverse', 17, 'de', 'wurde hergestellt für', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (893, 'property', 'name_inverse', 17, 'en', 'was made for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (894, 'property', 'name_inverse', 17, 'pt', 'foi feito para', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (895, 'property', 'name_inverse', 17, 'cn', '被制造来用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (896, 'property', 'comment', 17, 'en', 'This property relates an E7 Activity with objects created specifically for use in the activity.
This is distinct from the intended use of an item in some general type of activity such as the book of common prayer which was intended for use in Church of England services (see P101 had as general use (was use of)).', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (897, 'property', 'name', 18, 'de', 'hatte den bestimmten Zweck', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (898, 'property', 'name', 18, 'fr', 'avait pour but spécifique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (899, 'property', 'name', 18, 'el', 'είχε συγκεκριμένο σκοπό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (900, 'property', 'name', 18, 'en', 'had specific purpose', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (901, 'property', 'name', 18, 'ru', 'имел конкретную цель', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (902, 'property', 'name', 18, 'pt', 'tinha propósito específico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (903, 'property', 'name', 18, 'cn', '有特定目地', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (904, 'property', 'name_inverse', 18, 'de', 'war Zweck von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (905, 'property', 'name_inverse', 18, 'ru', 'был целью для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (906, 'property', 'name_inverse', 18, 'el', 'ήταν σκοπός του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (907, 'property', 'name_inverse', 18, 'fr', 'était le but de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (908, 'property', 'name_inverse', 18, 'en', 'was purpose of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (909, 'property', 'name_inverse', 18, 'pt', 'era o propósito de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (910, 'property', 'name_inverse', 18, 'cn', '之準備活動是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (911, 'property', 'comment', 18, 'en', 'This property identifies the relationship between a preparatory activity and the event it is intended to be preparation for.
This includes activities, orders and other organisational actions, taken in preparation for other activities or events.
P20 had specific purpose (was purpose of) implies that an activity succeeded in achieving its aim. If it does not succeed, such as the setting of a trap that did not catch anything, one may document the unrealized intention using P21 had general purpose (was purpose of):E55 Type and/or  P33 used specific technique (was used by): E29 Design or Procedure.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (912, 'property', 'name', 19, 'el', 'είχε γενικό σκοπό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (913, 'property', 'name', 19, 'de', 'hatte den allgemeinen Zweck', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (914, 'property', 'name', 19, 'fr', 'avait pour but général', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (915, 'property', 'name', 19, 'ru', 'имел общую цель', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (916, 'property', 'name', 19, 'en', 'had general purpose', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (917, 'property', 'name', 19, 'pt', 'tinha propósito geral', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (918, 'property', 'name', 19, 'cn', '有通用目地', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (919, 'property', 'name_inverse', 19, 'ru', 'был целью для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (920, 'property', 'name_inverse', 19, 'fr', 'était le but de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (921, 'property', 'name_inverse', 19, 'el', 'ήταν σκοπός του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (922, 'property', 'name_inverse', 19, 'de', 'war Zweck von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (923, 'property', 'name_inverse', 19, 'en', 'was purpose of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (924, 'property', 'name_inverse', 19, 'pt', 'era o propósito de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (925, 'property', 'name_inverse', 19, 'cn', '可利用', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (926, 'property', 'comment', 19, 'en', 'This property describes an intentional relationship between an E7 Activity and some general goal or purpose.
This may involve activities intended as preparation for some type of activity or event. P21had general purpose (was purpose of) differs from P20 had specific purpose (was purpose of) in that no occurrence of an event is implied as the purpose.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (927, 'property', 'name', 20, 'el', 'μετεβίβασε τον τίτλο σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (928, 'property', 'name', 20, 'fr', 'a fait passer le droit de propriété à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (929, 'property', 'name', 20, 'de', 'übertrug Besitztitel auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (930, 'property', 'name', 20, 'en', 'transferred title to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (931, 'property', 'name', 20, 'ru', 'передал право собственности', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (932, 'property', 'name', 20, 'pt', 'transferiu os direitos de propriedade para', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (933, 'property', 'name', 20, 'cn', '转交所有权给', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (934, 'property', 'name_inverse', 20, 'el', 'απέκτησε τον τίτλο μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (935, 'property', 'name_inverse', 20, 'en', 'acquired title through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (936, 'property', 'name_inverse', 20, 'de', 'erwarb Besitztitel durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (937, 'property', 'name_inverse', 20, 'fr', 'a acquis le droit de propriété du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (938, 'property', 'name_inverse', 20, 'ru', 'получил право собственности через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (939, 'property', 'name_inverse', 20, 'pt', 'adquiriu os direitos de propriedade por meio da', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (940, 'property', 'name_inverse', 20, 'cn', '获取所有权於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (941, 'property', 'comment', 20, 'en', 'This property identifies the E39 Actor that acquires the legal ownership of an object as a result of an E8 Acquisition.
The property will typically describe an Actor purchasing or otherwise acquiring an object from another Actor. However, title may also be acquired, without any corresponding loss of title by another Actor, through legal fieldwork such as hunting, shooting or fishing.
In reality the title is either transferred to or from someone, or both.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (942, 'property', 'name', 21, 'el', 'μετεβίβασε τον τίτλο από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (943, 'property', 'name', 21, 'fr', 'a fait passer le droit de propriété de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (944, 'property', 'name', 21, 'ru', 'передал право собственности от', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (945, 'property', 'name', 21, 'de', 'übertrug Besitztitel von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (946, 'property', 'name', 21, 'en', 'transferred title from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (947, 'property', 'name', 21, 'pt', 'transferiu os direitos de propriedade de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (948, 'property', 'name', 21, 'cn', '原所有权者是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (949, 'property', 'name_inverse', 21, 'fr', 'a perdu le droit de propriété du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (950, 'property', 'name_inverse', 21, 'de', 'trat Besitztitel ab in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (951, 'property', 'name_inverse', 21, 'ru', 'право собственности отдано через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (952, 'property', 'name_inverse', 21, 'en', 'surrendered title through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (953, 'property', 'name_inverse', 21, 'el', 'παρέδωσε τον τίτλο μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (954, 'property', 'name_inverse', 21, 'pt', 'perdeu os direitos de propriedade por meio da', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (955, 'property', 'name_inverse', 21, 'cn', '交出所有权於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (956, 'property', 'comment', 21, 'en', 'This property identifies the E39 Actor or Actors who relinquish legal ownership as the result of an E8 Acquisition.
The property will typically be used to describe a person donating or selling an object to a museum. In reality title is either transferred to or from someone, or both.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (957, 'property', 'name', 22, 'de', 'übertrug Besitz über', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (958, 'property', 'name', 22, 'ru', 'передал право собственности на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (959, 'property', 'name', 22, 'el', 'μετεβίβασε τον τίτλο του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (960, 'property', 'name', 22, 'fr', 'a fait passer le droit de propriété sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (961, 'property', 'name', 22, 'en', 'transferred title of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (962, 'property', 'name', 22, 'pt', 'transferiu os direitos de propriedade sobre o', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (963, 'property', 'name', 22, 'cn', '转移所有权的标的物是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (964, 'property', 'name_inverse', 22, 'ru', 'сменил владельца через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (965, 'property', 'name_inverse', 22, 'en', 'changed ownership through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (966, 'property', 'name_inverse', 22, 'de', 'ging über in Besitz durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (967, 'property', 'name_inverse', 22, 'el', 'άλλαξε ιδιοκτησία μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (968, 'property', 'name_inverse', 22, 'fr', 'a changé de mains du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (969, 'property', 'name_inverse', 22, 'pt', 'mudou de proprietário por meio de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (970, 'property', 'name_inverse', 22, 'cn', '转移了所有权於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (971, 'property', 'comment', 22, 'en', 'This property identifies the E18 Physical Thing or things involved in an E8 Acquisition.
In reality, an acquisition must refer to at least one transferred item.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (972, 'property', 'name', 23, 'en', 'moved', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (973, 'property', 'name', 23, 'el', 'μετεκίνησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (974, 'property', 'name', 23, 'ru', 'переместил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (975, 'property', 'name', 23, 'fr', 'a déplacé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (976, 'property', 'name', 23, 'de', 'bewegte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (977, 'property', 'name', 23, 'pt', 'locomoveu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (978, 'property', 'name', 23, 'cn', '移动了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (979, 'property', 'name_inverse', 23, 'ru', 'перемещен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (980, 'property', 'name_inverse', 23, 'en', 'moved by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (981, 'property', 'name_inverse', 23, 'el', 'μετακινήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (982, 'property', 'name_inverse', 23, 'fr', 'a été déplacé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (983, 'property', 'name_inverse', 23, 'de', 'wurde bewegt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (984, 'property', 'name_inverse', 23, 'pt', 'foi locomovido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (985, 'property', 'name_inverse', 23, 'cn', '被移动於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (986, 'property', 'comment', 23, 'en', 'This property identifies the E19 Physical Object that is moved during a move event.
The property implies the object’s passive participation. For example, Monet’s painting “Impression sunrise” was moved for the first Impressionist exhibition in 1874.
In reality, a move must concern at least one object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (987, 'property', 'name', 24, 'el', 'μετακινήθηκε προς', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (988, 'property', 'name', 24, 'en', 'moved to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (989, 'property', 'name', 24, 'fr', 'a déplacé vers', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (990, 'property', 'name', 24, 'ru', 'перемещен в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (991, 'property', 'name', 24, 'de', 'bewegte bis zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (992, 'property', 'name', 24, 'pt', 'locomoveu para', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (993, 'property', 'name', 24, 'cn', '移入物件至', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (994, 'property', 'name_inverse', 24, 'en', 'was destination of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (995, 'property', 'name_inverse', 24, 'de', 'war Zielort von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (996, 'property', 'name_inverse', 24, 'el', 'ήταν προορισμός του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (997, 'property', 'name_inverse', 24, 'ru', 'был пунктом назначения для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (998, 'property', 'name_inverse', 24, 'fr', 'a été la destination de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (999, 'property', 'name_inverse', 24, 'pt', 'era destinação de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1000, 'property', 'name_inverse', 24, 'cn', '被作为移入地於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1001, 'property', 'comment', 24, 'en', 'This property identifies the destination of a E9 Move.
A move will be linked to a destination, such as the move of an artefact from storage to display. A move may be linked to many terminal instances of E53 Places. In this case the move describes a distribution of a set of objects. The area of the move includes the origin, route and destination.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1002, 'property', 'name', 25, 'el', 'μετακινήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1003, 'property', 'name', 25, 'en', 'moved from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1004, 'property', 'name', 25, 'fr', 'a retiré de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1005, 'property', 'name', 25, 'de', 'bewegte weg von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1006, 'property', 'name', 25, 'ru', 'перемещен из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1007, 'property', 'name', 25, 'pt', 'locomoveu de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1008, 'property', 'name', 25, 'cn', '有移出地', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1009, 'property', 'name_inverse', 25, 'en', 'was origin of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1010, 'property', 'name_inverse', 25, 'de', 'war Ausgangsort von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1011, 'property', 'name_inverse', 25, 'ru', 'был исходной точкой для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1012, 'property', 'name_inverse', 25, 'fr', 'a été l''origine de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1013, 'property', 'name_inverse', 25, 'el', 'ήταν αφετηρία του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1014, 'property', 'name_inverse', 25, 'pt', 'era origem de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1015, 'property', 'name_inverse', 25, 'cn', '被作为移出地於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1016, 'property', 'comment', 25, 'en', 'This property identifies the starting E53 Place of an E9 Move.
A move will be linked to an origin, such as the move of an artefact from storage to display. A move may be linked to many origins. In this case the move describes the picking up of a set of objects. The area of the move includes the origin, route and destination.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1017, 'property', 'name', 26, 'fr', 'changement de détenteur au détriment de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1018, 'property', 'name', 26, 'de', 'übergab Gewahrsam an', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1019, 'property', 'name', 26, 'en', 'custody surrendered by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1020, 'property', 'name', 26, 'el', 'μετεβίβασε κατοχή από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1021, 'property', 'name', 26, 'ru', 'опека отдана', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1022, 'property', 'name', 26, 'pt', 'custódia concedida por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1023, 'property', 'name', 26, 'cn', '有原保管人', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1024, 'property', 'name_inverse', 26, 'en', 'surrendered custody through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1025, 'property', 'name_inverse', 26, 'ru', 'опека отдана через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1026, 'property', 'name_inverse', 26, 'fr', 'a cessé d’être détenteur à cause de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1027, 'property', 'name_inverse', 26, 'el', 'παρέδωσε κατοχή μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1028, 'property', 'name_inverse', 26, 'de', 'wurde Gewahrsam übergeben durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1029, 'property', 'name_inverse', 26, 'pt', 'final da custódia por meio de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1030, 'property', 'name_inverse', 26, 'cn', '交出保管作业於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1031, 'property', 'comment', 26, 'en', 'This property identifies the E39 Actor or Actors who surrender custody of an instance of E18 Physical Thing in an E10 Transfer of Custody activity.
The property will typically describe an Actor surrendering custody of an object when it is handed over to someone else’s care. On occasion, physical custody may be surrendered involuntarily – through accident, loss or theft.
In reality, custody is either transferred to someone or from someone, or both.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1032, 'property', 'name', 27, 'el', 'μετεβίβασε κατοχή σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1033, 'property', 'name', 27, 'ru', 'опека получена', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1034, 'property', 'name', 27, 'en', 'custody received by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1035, 'property', 'name', 27, 'fr', 'changement de détenteur au profit de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1036, 'property', 'name', 27, 'de', 'übertrug Gewahrsam auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1037, 'property', 'name', 27, 'pt', 'custódia recebida por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1038, 'property', 'name', 27, 'cn', '移转保管作业给', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1039, 'property', 'name_inverse', 27, 'el', 'παρέλαβε κατοχή μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1040, 'property', 'name_inverse', 27, 'en', 'received custody through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1041, 'property', 'name_inverse', 27, 'ru', 'получил опеку через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1042, 'property', 'name_inverse', 27, 'fr', 'est devenu détenteur grâce à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1043, 'property', 'name_inverse', 27, 'de', 'erhielt Gewahrsam durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1044, 'property', 'name_inverse', 27, 'pt', 'início da custódia por meio de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1045, 'property', 'name_inverse', 27, 'cn', '取得保管作业於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1046, 'property', 'comment', 27, 'en', 'This property identifies the E39 Actor or Actors who receive custody of an instance of E18 Physical Thing in an E10 Transfer of Custody activity.
The property will typically describe Actors receiving custody of an object when it is handed over from another Actor’s care. On occasion, physical custody may be received involuntarily or illegally – through accident, unsolicited donation, or theft.
In reality, custody is either transferred to someone or from someone, or both.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1047, 'property', 'name', 28, 'ru', 'передало опеку на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1048, 'property', 'name', 28, 'en', 'transferred custody of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1049, 'property', 'name', 28, 'fr', 'changement de détenteur concernant', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1050, 'property', 'name', 28, 'de', 'übertrug Gewahrsam über', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1051, 'property', 'name', 28, 'el', 'μετεβίβασε κατοχή του/της/των', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1052, 'property', 'name', 28, 'pt', 'transferida custódia de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1053, 'property', 'name', 28, 'cn', '有保管标的物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1054, 'property', 'name_inverse', 28, 'en', 'custody transferred through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1055, 'property', 'name_inverse', 28, 'el', 'άλλαξε κατοχή μέσω', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1056, 'property', 'name_inverse', 28, 'fr', 'a changé de détenteur du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1057, 'property', 'name_inverse', 28, 'de', 'wechselte Gewahrsam durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1058, 'property', 'name_inverse', 28, 'ru', 'опека передана через', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1059, 'property', 'name_inverse', 28, 'pt', 'custódia transferida por meio de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1060, 'property', 'name_inverse', 28, 'cn', '被移转了保管作业於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1061, 'property', 'comment', 28, 'en', 'This property identifies an item or items of E18 Physical Thing concerned in an E10 Transfer of Custody activity.
The property will typically describe the object that is handed over by an E39 Actor to another Actor’s custody. On occasion, physical custody may be transferred involuntarily or illegally – through accident, unsolicited donation, or theft.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1062, 'property', 'name', 29, 'de', 'veränderte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1063, 'property', 'name', 29, 'fr', 'a modifié', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1064, 'property', 'name', 29, 'en', 'has modified', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1065, 'property', 'name', 29, 'ru', 'изменил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1066, 'property', 'name', 29, 'el', 'τροποποίησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1067, 'property', 'name', 29, 'pt', 'modificou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1068, 'property', 'name', 29, 'cn', '修改了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1069, 'property', 'name_inverse', 29, 'fr', 'a été modifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1070, 'property', 'name_inverse', 29, 'de', 'wurde verändert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1071, 'property', 'name_inverse', 29, 'el', 'τροποποιήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1072, 'property', 'name_inverse', 29, 'ru', 'был изменен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1073, 'property', 'name_inverse', 29, 'en', 'was modified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1074, 'property', 'name_inverse', 29, 'pt', 'foi modificada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1075, 'property', 'name_inverse', 29, 'cn', '被修改於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1076, 'property', 'comment', 29, 'en', 'This property identifies the E24 Physical Man-Made Thing modified in an E11 Modification.
If a modification is applied to a non-man-made object, it is regarded as an E22 Man-Made Object from that time onwards.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1077, 'property', 'name', 30, 'el', 'χρησιμοποίησε γενική τεχνική', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1078, 'property', 'name', 30, 'de', 'benutzte das allgemeine Verfahren', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1079, 'property', 'name', 30, 'fr', 'a employé comme technique générique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1080, 'property', 'name', 30, 'ru', 'использовал общую технику', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1081, 'property', 'name', 30, 'en', 'used general technique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1082, 'property', 'name', 30, 'pt', 'usou técnica geral', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1083, 'property', 'name', 30, 'cn', '使用通用技术', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1084, 'property', 'name_inverse', 30, 'ru', 'был техникой для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1085, 'property', 'name_inverse', 30, 'el', 'ήταν τεχνική του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1086, 'property', 'name_inverse', 30, 'de', 'war Verfahren von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1087, 'property', 'name_inverse', 30, 'en', 'was technique of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1088, 'property', 'name_inverse', 30, 'fr', 'a été la technique mise en œuvre dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1089, 'property', 'name_inverse', 30, 'pt', 'foi técnica da', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1090, 'property', 'name_inverse', 30, 'cn', '被使用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1091, 'property', 'comment', 30, 'en', 'This property identifies the technique that was employed in an act of modification.
These techniques should be drawn from an external E55 Type hierarchy of consistent terminology of general techniques such as embroidery, oil-painting, etc. Specific techniques may be further described as instances of E29 Design or Procedure.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1092, 'property', 'name', 31, 'el', 'χρησιμοποίησε συγκεκριμένη τεχνική', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1093, 'property', 'name', 31, 'en', 'used specific technique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1094, 'property', 'name', 31, 'fr', 'a employé comme technique spécifique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1095, 'property', 'name', 31, 'ru', 'использовал особую технику', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1096, 'property', 'name', 31, 'de', 'benutzte das bestimmte Verfahren', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1097, 'property', 'name', 31, 'pt', 'usou técnica específica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1098, 'property', 'name', 31, 'cn', '使用特定技术', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1099, 'property', 'name_inverse', 31, 'en', 'was used by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1100, 'property', 'name_inverse', 31, 'fr', 'a été employée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1101, 'property', 'name_inverse', 31, 'ru', 'был использован посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1102, 'property', 'name_inverse', 31, 'de', 'wurde benutzt von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1103, 'property', 'name_inverse', 31, 'el', 'χρησιμοποιήθηκε για', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1104, 'property', 'name_inverse', 31, 'pt', 'foi usada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1105, 'property', 'name_inverse', 31, 'cn', '被特别使用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1106, 'property', 'comment', 31, 'en', 'This property identifies a specific instance of E29 Design or Procedure in order to carry out an instance of E7 Activity or parts of it.
The property differs from P32 used general technique (was technique of) in that P33 refers to an instance of E29 Design or Procedure, which is a concrete information object in its own right rather than simply being a term or a method known by tradition.
Typical examples would include intervention plans for conservation or the construction plans of a building.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1107, 'property', 'name', 32, 'el', 'αφορούσε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1108, 'property', 'name', 32, 'ru', 'имел дело с', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1109, 'property', 'name', 32, 'de', 'betraf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1110, 'property', 'name', 32, 'en', 'concerned', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1111, 'property', 'name', 32, 'fr', 'a concerné', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1112, 'property', 'name', 32, 'pt', 'interessada', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1113, 'property', 'name', 32, 'cn', '评估了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1114, 'property', 'name_inverse', 32, 'de', 'wurde beurteilt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1115, 'property', 'name_inverse', 32, 'el', 'εκτιμήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1116, 'property', 'name_inverse', 32, 'fr', 'expertisé par le biais de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1117, 'property', 'name_inverse', 32, 'en', 'was assessed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1118, 'property', 'name_inverse', 32, 'ru', 'был оценен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1119, 'property', 'name_inverse', 32, 'pt', 'foi avaliada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1120, 'property', 'name_inverse', 32, 'cn', '被评估於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1121, 'property', 'comment', 32, 'en', 'This property identifies the E18 Physical Thing that was assessed during an E14 Condition Assessment activity.
Conditions may be assessed either by direct observation or using recorded evidence. In the latter case the E18 Physical Thing does not need to be present or extant.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1122, 'property', 'name', 33, 'ru', 'идентифицировал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1123, 'property', 'name', 33, 'de', 'hat identifiziert', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1124, 'property', 'name', 33, 'fr', 'a identifié', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1125, 'property', 'name', 33, 'el', 'έχει διαπιστώσει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1126, 'property', 'name', 33, 'en', 'has identified', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1127, 'property', 'name', 33, 'pt', 'identificou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1128, 'property', 'name', 33, 'cn', '评估认定了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1129, 'property', 'name_inverse', 33, 'ru', 'идентифицирован посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1130, 'property', 'name_inverse', 33, 'de', 'wurde identifiziert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1131, 'property', 'name_inverse', 33, 'fr', 'est identifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1132, 'property', 'name_inverse', 33, 'el', 'έχει διαπιστωθεί από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1133, 'property', 'name_inverse', 33, 'en', 'was identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1134, 'property', 'name_inverse', 33, 'pt', 'foi identificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1135, 'property', 'name_inverse', 33, 'cn', '被评估认定於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1136, 'property', 'comment', 33, 'en', 'This property identifies the E3 Condition State that was observed in an E14 Condition Assessment activity.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1137, 'property', 'name', 34, 'fr', 'a attribué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1138, 'property', 'name', 34, 'el', 'απέδωσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1139, 'property', 'name', 34, 'en', 'assigned', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1140, 'property', 'name', 34, 'de', 'wies zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1141, 'property', 'name', 34, 'ru', 'назначил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1142, 'property', 'name', 34, 'pt', 'atribuiu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1143, 'property', 'name', 34, 'cn', '指定标识符为', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1144, 'property', 'name_inverse', 34, 'de', 'wurde zugewiesen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1145, 'property', 'name_inverse', 34, 'el', 'αποδόθηκε ως ιδιότητα από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1146, 'property', 'name_inverse', 34, 'en', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1147, 'property', 'name_inverse', 34, 'ru', 'был присвоен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1148, 'property', 'name_inverse', 34, 'fr', 'a été attribuée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1149, 'property', 'name_inverse', 34, 'pt', 'foi atribuído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1150, 'property', 'name_inverse', 34, 'cn', '被指定为标识符於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1151, 'property', 'comment', 34, 'en', 'This property records the identifier that was assigned to an item in an Identifier Assignment activity.
The same identifier may be assigned on more than one occasion.
An Identifier might be created prior to an assignment.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1152, 'property', 'name', 35, 'el', 'ακύρωσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1153, 'property', 'name', 35, 'ru', 'отменил назначение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1154, 'property', 'name', 35, 'en', 'deassigned', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1155, 'property', 'name', 35, 'de', ' hob Zuweisung auf von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1156, 'property', 'name', 35, 'fr', 'a désattribué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1157, 'property', 'name', 35, 'pt', 'retirou a atribuição do', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1158, 'property', 'name', 35, 'cn', '取消标识符', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1159, 'property', 'name_inverse', 35, 'ru', 'был отменен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1160, 'property', 'name_inverse', 35, 'fr', 'a été désattribué par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1161, 'property', 'name_inverse', 35, 'de', 'wurde aufgehoben durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1162, 'property', 'name_inverse', 35, 'el', 'ακυρώθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1163, 'property', 'name_inverse', 35, 'en', 'was deassigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1164, 'property', 'name_inverse', 35, 'pt', 'foi retirada a atribuição por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1165, 'property', 'name_inverse', 35, 'cn', '被取消标识符於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1166, 'property', 'comment', 35, 'en', 'This property records the identifier that was deassigned from an instance of E1 CRM Entity.
Deassignment of an identifier may be necessary when an item is taken out of an inventory, a new numbering system is introduced or items are merged or split up.
The same identifier may be deassigned on more than one occasion.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1167, 'property', 'name', 36, 'fr', 'a mesuré', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1168, 'property', 'name', 36, 'de', 'vermaß', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1169, 'property', 'name', 36, 'el', 'μέτρησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1170, 'property', 'name', 36, 'en', 'measured', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1171, 'property', 'name', 36, 'ru', 'измерил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1172, 'property', 'name', 36, 'pt', 'mediu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1173, 'property', 'name', 36, 'cn', '测量了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1174, 'property', 'name_inverse', 36, 'de', 'wurde vermessen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1175, 'property', 'name_inverse', 36, 'ru', 'был измерен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1176, 'property', 'name_inverse', 36, 'en', 'was measured by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1177, 'property', 'name_inverse', 36, 'el', 'μετρήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1178, 'property', 'name_inverse', 36, 'fr', 'a été mesuré par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1179, 'property', 'name_inverse', 36, 'pt', 'foi medida por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1180, 'property', 'name_inverse', 36, 'cn', '被测量於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1181, 'property', 'comment', 36, 'en', 'This property associates an instance of E16 Measurement with the instance of E1 CRM Entity to which it applied. An instance of E1 CRM Entity may be measured more than once. Material and immaterial things and processes may be measured, e.g. the number of words in a text, or the duration of an event.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1182, 'property', 'name', 37, 'en', 'observed dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1183, 'property', 'name', 37, 'el', 'παρατήρησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1184, 'property', 'name', 37, 'ru', 'определил величину', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1185, 'property', 'name', 37, 'de', 'beobachtete Dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1186, 'property', 'name', 37, 'fr', 'a relevé comme dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1187, 'property', 'name', 37, 'pt', 'verificou a dimensão', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1188, 'property', 'name', 37, 'cn', '观察认定的规模是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1189, 'property', 'name_inverse', 37, 'ru', 'наблюдался в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1190, 'property', 'name_inverse', 37, 'el', 'παρατηρήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1191, 'property', 'name_inverse', 37, 'en', 'was observed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1192, 'property', 'name_inverse', 37, 'de', 'wurde beobachtet in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1193, 'property', 'name_inverse', 37, 'fr', 'a été relevée au cours de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1194, 'property', 'name_inverse', 37, 'pt', 'foi verificada durante', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1195, 'property', 'name_inverse', 37, 'cn', '被观察认定於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1196, 'property', 'comment', 37, 'en', 'This property records the dimension that was observed in an E16 Measurement Event.
E54 Dimension can be any quantifiable aspect of E70 Thing. Weight, image colour depth and monetary value are dimensions in this sense. One measurement activity may determine more than one dimension of one object.
Dimensions may be determined either by direct observation or using recorded evidence. In the latter case the measured Thing does not need to be present or extant.
Even though knowledge of the value of a dimension requires measurement, the dimension may be an object of discourse prior to, or even without, any measurement being made.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1197, 'property', 'name', 38, 'ru', 'классифицировал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1198, 'property', 'name', 38, 'en', 'classified', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1199, 'property', 'name', 38, 'fr', 'a classifié', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1200, 'property', 'name', 38, 'el', 'χαρακτήρισε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1201, 'property', 'name', 38, 'de', 'klassifizierte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1202, 'property', 'name', 38, 'pt', 'classificou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1203, 'property', 'name', 38, 'cn', '分类了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1204, 'property', 'name_inverse', 38, 'fr', 'a été classifiée par le biais de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1205, 'property', 'name_inverse', 38, 'en', 'was classified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1206, 'property', 'name_inverse', 38, 'ru', 'был классифицирован посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1207, 'property', 'name_inverse', 38, 'el', 'χαρακτηρίσθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1208, 'property', 'name_inverse', 38, 'de', 'wurde klassifiziert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1209, 'property', 'name_inverse', 38, 'pt', 'foi classificada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1210, 'property', 'name_inverse', 38, 'cn', '被分类於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1211, 'property', 'comment', 38, 'en', 'This property records the item to which a type was assigned in an E17 Type Assignment activity.
Any instance of a CRM entity may be assigned a type through type assignment. Type assignment events allow a more detailed path from E1 CRM Entity through P41 classified (was classified), E17 Type Assignment, P42 assigned (was assigned by) to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1212, 'property', 'name', 39, 'el', 'απέδωσε ως ιδιότητα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1213, 'property', 'name', 39, 'en', 'assigned', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1214, 'property', 'name', 39, 'fr', 'a attribué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1215, 'property', 'name', 39, 'ru', 'назначил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1216, 'property', 'name', 39, 'de', 'wies zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1217, 'property', 'name', 39, 'pt', 'atribuiu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1218, 'property', 'name', 39, 'cn', '指定类型为', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1219, 'property', 'name_inverse', 39, 'ru', 'был присвоен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1220, 'property', 'name_inverse', 39, 'el', 'αποδόθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1221, 'property', 'name_inverse', 39, 'en', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1222, 'property', 'name_inverse', 39, 'de', 'wurde zugewiesen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1223, 'property', 'name_inverse', 39, 'fr', 'a été attribué par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1224, 'property', 'name_inverse', 39, 'pt', 'foi atribuído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1225, 'property', 'name_inverse', 39, 'cn', '被指定类型於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1226, 'property', 'comment', 39, 'en', 'This property records the type that was assigned to an entity by an E17 Type Assignment activity.
Type assignment events allow a more detailed path from E1 CRM Entity through P41 classified (was classified by), E17 Type Assignment, P42 assigned (was assigned by) to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).
For example, a fragment of an antique vessel could be assigned the type “attic red figured belly handled amphora” by expert A. The same fragment could be assigned the type “shoulder handled amphora” by expert B.
A Type may be intellectually constructed independent from assigning an instance of it.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1227, 'property', 'name', 40, 'de', 'hat Dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1228, 'property', 'name', 40, 'fr', 'a pour dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1229, 'property', 'name', 40, 'ru', 'имеет величину', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1230, 'property', 'name', 40, 'en', 'has dimension', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1231, 'property', 'name', 40, 'el', 'έχει μέγεθος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1232, 'property', 'name', 40, 'pt', 'tem dimensão', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1233, 'property', 'name', 40, 'cn', '有规模数量', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1234, 'property', 'name_inverse', 40, 'de', 'ist Dimension von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1235, 'property', 'name_inverse', 40, 'en', 'is dimension of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1236, 'property', 'name_inverse', 40, 'ru', 'является величиной для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1237, 'property', 'name_inverse', 40, 'fr', 'est dimension de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1238, 'property', 'name_inverse', 40, 'el', 'είναι μέγεθος του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1239, 'property', 'name_inverse', 40, 'pt', 'é dimensão de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1240, 'property', 'name_inverse', 40, 'cn', '估量的标的物是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1241, 'property', 'comment', 40, 'en', 'This property records a E54 Dimension of some E70 Thing.
It is a shortcut of the more fully developed path from E70 Thing through P39 measured (was measured by), E16 Measurement P40 observed dimension (was observed in) to E54 Dimension. It offers no information about how and when an E54 Dimension was established, nor by whom.
An instance of E54 Dimension is specific to an instance of E70 Thing.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1242, 'property', 'name', 41, 'ru', 'имеет условие', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1243, 'property', 'name', 41, 'de', 'hat Zustand', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1244, 'property', 'name', 41, 'fr', 'a pour état matériel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1245, 'property', 'name', 41, 'en', 'has condition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1246, 'property', 'name', 41, 'el', 'έχει κατάσταση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1247, 'property', 'name', 41, 'pt', 'tem estado material ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1248, 'property', 'name', 41, 'cn', '有状态', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1249, 'property', 'name_inverse', 41, 'de', 'ist Zustand von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1250, 'property', 'name_inverse', 41, 'fr', 'état matériel de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1251, 'property', 'name_inverse', 41, 'el', 'είναι κατάσταση του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1252, 'property', 'name_inverse', 41, 'ru', 'является условием для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1253, 'property', 'name_inverse', 41, 'en', 'is condition of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1254, 'property', 'name_inverse', 41, 'pt', 'estado material de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1255, 'property', 'name_inverse', 41, 'cn', '描述的标的物是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1256, 'property', 'comment', 41, 'en', 'This property records an E3 Condition State for some E18 Physical Thing.
It is a shortcut of the more fully developed path from E18 Physical Thing through P34 concerned (was assessed by), E14 Condition Assessment P35 has identified (was identified by) to E3 Condition State. It offers no information about how and when the E3 Condition State was established, nor by whom.
An instance of Condition State is specific to an instance of Physical Thing.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1257, 'property', 'name', 42, 'fr', 'consiste en', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1258, 'property', 'name', 42, 'el', 'αποτελείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1259, 'property', 'name', 42, 'de', 'besteht aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1260, 'property', 'name', 42, 'en', 'consists of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1261, 'property', 'name', 42, 'ru', 'составлен из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1262, 'property', 'name', 42, 'pt', 'consiste de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1263, 'property', 'name', 42, 'cn', '有构成材料', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1264, 'property', 'name_inverse', 42, 'de', 'ist enthalten in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1265, 'property', 'name_inverse', 42, 'el', 'είναι ενσωματωμένος/η/ο σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1266, 'property', 'name_inverse', 42, 'en', 'is incorporated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1267, 'property', 'name_inverse', 42, 'ru', 'входит в состав', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1268, 'property', 'name_inverse', 42, 'fr', 'est présent dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1269, 'property', 'name_inverse', 42, 'pt', 'está presente em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1270, 'property', 'name_inverse', 42, 'cn', '被用来构成', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1271, 'property', 'comment', 42, 'en', 'This property identifies the instances of E57 Materials of which an instance of E18 Physical Thing is composed.
All physical things consist of physical materials. P45 consists of (is incorporated in) allows the different Materials to be recorded. P45 consists of (is incorporated in) refers here to observed Material as opposed to the consumed raw material.
A Material, such as a theoretical alloy, may not have any physical instances', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1272, 'property', 'name', 43, 'en', 'is composed of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1273, 'property', 'name', 43, 'fr', 'est composée de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1274, 'property', 'name', 43, 'el', 'αποτελείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1275, 'property', 'name', 43, 'de', 'ist zusammengesetzt aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1276, 'property', 'name', 43, 'ru', 'составлен из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1277, 'property', 'name', 43, 'pt', 'é composto de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1278, 'property', 'name', 43, 'cn', '有组件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1279, 'property', 'name_inverse', 43, 'ru', 'формирует часть', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1280, 'property', 'name_inverse', 43, 'fr', 'fait partie de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1281, 'property', 'name_inverse', 43, 'el', 'αποτελεί μέρος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1282, 'property', 'name_inverse', 43, 'de', 'bildet Teil von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1283, 'property', 'name_inverse', 43, 'en', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1284, 'property', 'name_inverse', 43, 'pt', 'faz parte de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1285, 'property', 'name_inverse', 43, 'cn', '被用来组成', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1286, 'property', 'comment', 43, 'en', 'This property allows instances of E18 Physical Thing to be analysed into component elements.
Component elements, since they are themselves instances of E18 Physical Thing, may be further analysed into sub-components, thereby creating a hierarchy of part decomposition. An instance of E18 Physical Thing may be shared between multiple wholes, for example two buildings may share a common wall.
This property is intended to describe specific components that are individually documented, rather than general aspects. Overall descriptions of the structure of an instance of E18 Physical Thing are captured by the P3 has note property.
The instances of E57 Materials of which an item of E18 Physical Thing is composed should be documented using P45 consists of (is incorporated in).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1287, 'property', 'name', 44, 'en', 'has preferred identifier', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1288, 'property', 'name', 44, 'fr', 'a pour identificateur retenu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1289, 'property', 'name', 44, 'de', 'hat bevorzugtes Kennzeichen', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1290, 'property', 'name', 44, 'ru', 'имеет предпочтительный идентификатор', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1291, 'property', 'name', 44, 'el', 'έχει προτιμώμενο αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1292, 'property', 'name', 44, 'pt', 'tem identificador preferido', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1293, 'property', 'name', 44, 'cn', '有首选标识符', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1294, 'property', 'name_inverse', 44, 'en', 'is preferred identifier of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1295, 'property', 'name_inverse', 44, 'ru', 'является предпочтительным идентификатором для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1296, 'property', 'name_inverse', 44, 'de', 'ist bevorzugtes Kennzeichen für', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1297, 'property', 'name_inverse', 44, 'el', 'είναι προτιμώμενο αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1298, 'property', 'name_inverse', 44, 'fr', 'est l’identificateur retenu de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1299, 'property', 'name_inverse', 44, 'pt', 'é o identificador preferido de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1300, 'property', 'name_inverse', 44, 'cn', '首选标识符的标的物是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1301, 'property', 'comment', 44, 'en', 'This property records the preferred E42 Identifier that was used to identify an instance of E1 CRM Entity at the time this property was recorded.
More than one preferred identifier may have been assigned to an item over time.
Use of this property requires an external mechanism for assigning temporal validity to the respective CRM instance.
P48 has preferred identifier (is preferred identifier of), is a shortcut for the path from E1 CRM Entity through P140 assigned attribute to (was attributed by), E15 Identifier Assignment, P37 assigned (was assigned by) to E42 Identifier. The fact that an identifier is a preferred one for an organisation can be better expressed in a context independent form by assigning a suitable E55 Type to the respective instance of E15 Identifier Assignment using the P2 has type property.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1302, 'property', 'name', 45, 'ru', 'имеет бывшего или текущего смотрителя', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1303, 'property', 'name', 45, 'el', 'είναι ή ήταν στην κατοχή του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1304, 'property', 'name', 45, 'fr', 'est ou a été détenu par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1305, 'property', 'name', 45, 'de', 'hat früheren oder derzeitigen Betreuer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1306, 'property', 'name', 45, 'en', 'has former or current keeper', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1307, 'property', 'name', 45, 'pt', 'é ou foi guardada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1308, 'property', 'name', 45, 'cn', '有前任或现任保管者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1309, 'property', 'name_inverse', 45, 'en', 'is former or current keeper of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1310, 'property', 'name_inverse', 45, 'el', 'κατέχει ή κατείχε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1311, 'property', 'name_inverse', 45, 'fr', 'est ou a été détenteur de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1312, 'property', 'name_inverse', 45, 'de', 'ist früherer oder derzeitiger Betreuer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1313, 'property', 'name_inverse', 45, 'ru', 'является бывшим или текущим смотрителем для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1314, 'property', 'name_inverse', 45, 'pt', 'é ou foi guardador de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1315, 'property', 'name_inverse', 45, 'cn', '目前或曾经保管', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1316, 'property', 'comment', 45, 'en', 'This property identifies the E39 Actor or Actors who have or have had custody of an instance of E18 Physical Thing at some time.
The distinction with P50 has current keeper (is current keeper of) is that P49 has former or current keeper (is former or current keeper of) leaves open the question as to whether the specified keepers are current.
P49 has former or current keeper (is former or current keeper of) is a shortcut for the more detailed path from E18 Physical Thing through P30 transferred custody of (custody transferred through), E10 Transfer of Custody, P28 custody surrendered by (surrendered custody through) or P29 custody received by (received custody through) to E39 Actor.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1317, 'property', 'name', 46, 'de', 'hat derzeitigen Betreuer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1318, 'property', 'name', 46, 'en', 'has current keeper', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1319, 'property', 'name', 46, 'el', 'είναι στην κατοχή του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1320, 'property', 'name', 46, 'fr', 'est actuellement détenu par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1321, 'property', 'name', 46, 'ru', 'имеет текущего смотрителя', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1322, 'property', 'name', 46, 'pt', 'é guardada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1323, 'property', 'name', 46, 'cn', '有现任保管者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1324, 'property', 'name_inverse', 46, 'ru', 'является текущим смотрителем для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1325, 'property', 'name_inverse', 46, 'en', 'is current keeper of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1326, 'property', 'name_inverse', 46, 'de', 'ist derzeitiger Betreuer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1327, 'property', 'name_inverse', 46, 'fr', 'est actuel détenteur de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1328, 'property', 'name_inverse', 46, 'el', 'κατέχει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1329, 'property', 'name_inverse', 46, 'pt', 'é guardador de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1330, 'property', 'name_inverse', 46, 'cn', '目前保管', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1331, 'property', 'comment', 46, 'en', 'This property identifies the E39 Actor or Actors who had custody of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
	P50 has current keeper (is current keeper of) is a shortcut for the more detailed path from E18 Physical Thing through P30 transferred custody of (custody transferred through), E10 Transfer of Custody, P29 custody received by (received custody through) to E39 Actor.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1332, 'property', 'name', 47, 'de', 'hat früheren oder derzeitigen Besitzer ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1333, 'property', 'name', 47, 'ru', 'имеет бывшего или текущего владельца', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1334, 'property', 'name', 47, 'el', 'έχει ή είχε ιδιοκτήτη', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1335, 'property', 'name', 47, 'fr', 'est ou a été possédée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1336, 'property', 'name', 47, 'en', 'has former or current owner', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1337, 'property', 'name', 47, 'pt', 'é ou foi propriedade de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1338, 'property', 'name', 47, 'cn', '有前任或现任物主', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1339, 'property', 'name_inverse', 47, 'ru', 'является бывшим или текущим владельцем для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1340, 'property', 'name_inverse', 47, 'el', 'είναι ή ήταν ιδιοκτήτης του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1341, 'property', 'name_inverse', 47, 'fr', 'est ou a été propriétaire de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1342, 'property', 'name_inverse', 47, 'en', 'is former or current owner of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1343, 'property', 'name_inverse', 47, 'de', 'ist früherer oder derzeitiger Besitzer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1344, 'property', 'name_inverse', 47, 'pt', 'é ou foi proprietário de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1345, 'property', 'name_inverse', 47, 'cn', '目前或曾经拥有', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1346, 'property', 'comment', 47, 'en', 'This property identifies the E39 Actor that is or has been the legal owner (i.e. title holder) of an instance of E18 Physical Thing at some time.
The distinction with P52 has current owner (is current owner of) is that P51 has former or current owner (is former or current owner of) does not indicate whether the specified owners are current. P51 has former or current owner (is former or current owner of) is a shortcut for the more detailed path from E18 Physical Thing through P24 transferred title of (changed ownership through), E8 Acquisition, P23 transferred title from (surrendered title through), or P22 transferred title to (acquired title through) to E39 Actor.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1347, 'property', 'name', 48, 'en', 'has current owner', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1348, 'property', 'name', 48, 'de', 'hat derzeitigen Besitzer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1349, 'property', 'name', 48, 'ru', 'имеет текущего владельца', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1350, 'property', 'name', 48, 'fr', 'est actuellement possédée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1351, 'property', 'name', 48, 'el', 'έχει ιδιοκτήτη', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1352, 'property', 'name', 48, 'pt', 'é propriedade de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1353, 'property', 'name', 48, 'cn', '有现任物主', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1354, 'property', 'name_inverse', 48, 'de', 'ist derzeitiger Besitzer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1355, 'property', 'name_inverse', 48, 'fr', 'est le propriétaire actuel de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1356, 'property', 'name_inverse', 48, 'en', 'is current owner of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1357, 'property', 'name_inverse', 48, 'ru', 'является текущим владельцем для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1358, 'property', 'name_inverse', 48, 'el', 'είναι ιδιοκτήτης του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1359, 'property', 'name_inverse', 48, 'pt', 'é proprietário de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1360, 'property', 'name_inverse', 48, 'cn', '目前拥有', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1361, 'property', 'comment', 48, 'en', 'This property identifies the E21 Person, E74 Group or E40 Legal Body that was the owner of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
P52 has current owner (is current owner of) is a shortcut for the more detailed path from E18 Physical Thing through P24 transferred title of (changed ownership through), E8 Acquisition, P22 transferred title to (acquired title through) to E39 Actor, if and only if this acquisition event is the most recent.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1362, 'property', 'name', 49, 'fr', 'a ou a eu pour localisation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1363, 'property', 'name', 49, 'el', 'βρίσκεται ή βρισκόταν σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1364, 'property', 'name', 49, 'ru', 'имеет текущее или бывшее местоположение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1365, 'property', 'name', 49, 'en', 'has former or current location', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1366, 'property', 'name', 49, 'de', 'hat früheren oder derzeitigen Standort', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1367, 'property', 'name', 49, 'pt', 'é ou foi localizada em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1368, 'property', 'name', 49, 'cn', '目前或曾经被置放於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1369, 'property', 'name_inverse', 49, 'ru', 'является текущим или бывшим местоположением для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1370, 'property', 'name_inverse', 49, 'en', 'is former or current location of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1371, 'property', 'name_inverse', 49, 'el', 'είναι ή ήταν θέση του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1372, 'property', 'name_inverse', 49, 'de', 'ist früherer oder derzeitiger Standort von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1373, 'property', 'name_inverse', 49, 'fr', 'est ou a été localisation de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1374, 'property', 'name_inverse', 49, 'pt', 'é ou foi localização de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1375, 'property', 'name_inverse', 49, 'cn', '目前或曾经被置放了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1376, 'property', 'comment', 49, 'en', 'This property allows an instance of E53 Place to be associated as the former or current location of an instance of E18 Physical Thing.
In the case of E19 Physical Objects, the property does not allow any indication of the Time-Span during which the Physical Object was located at this Place, nor if this is the current location.
In the case of immobile objects, the Place would normally correspond to the Place of creation.
P53 has former or current location (is former or current location of) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P25 moved (moved by), E9 Move, P26 moved to (was destination of) or P27 moved from (was origin of) to E53 Place.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1377, 'property', 'name', 50, 'fr', 'a actuellement pour localisation à demeure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1378, 'property', 'name', 50, 'de', 'hat derzeitigen permanenten Standort', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1379, 'property', 'name', 50, 'en', 'has current permanent location', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1380, 'property', 'name', 50, 'el', 'έχει μόνιμη θέση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1381, 'property', 'name', 50, 'ru', 'имеет текущее постоянное местоположение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1382, 'property', 'name', 50, 'pt', 'é localizado permanentemente em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1383, 'property', 'name', 50, 'cn', '目前的永久位置位於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1384, 'property', 'name_inverse', 50, 'el', 'είναι μόνιμη θέση του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1385, 'property', 'name_inverse', 50, 'de', 'ist derzeitiger permanenter Standort von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1386, 'property', 'name_inverse', 50, 'fr', 'est actuellement localisation à demeure de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1387, 'property', 'name_inverse', 50, 'en', 'is current permanent location of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1388, 'property', 'name_inverse', 50, 'ru', 'является текущим постоянным местоположением для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1389, 'property', 'name_inverse', 50, 'pt', 'é localização permanente de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1390, 'property', 'name_inverse', 50, 'cn', '目前被用来永久置放', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1391, 'property', 'comment', 50, 'en', 'This property records the foreseen permanent location of an instance of E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
P54 has current permanent location (is current permanent location of) is similar to P55 has current location (currently holds). However, it indicates the E53 Place currently reserved for an object, such as the permanent storage location or a permanent exhibit location. The object may be temporarily removed from the permanent location, for example when used in temporary exhibitions or loaned to another institution. The object may never actually be located at its permanent location.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1392, 'property', 'name', 51, 'el', 'βρίσκεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1393, 'property', 'name', 51, 'en', 'has current location', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1394, 'property', 'name', 51, 'fr', 'a pour localisation actuelle', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1395, 'property', 'name', 51, 'ru', 'в данный момент находится в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1396, 'property', 'name', 51, 'de', 'hat derzeitigen Standort', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1397, 'property', 'name', 51, 'pt', 'é localizado em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1398, 'property', 'name', 51, 'cn', '目前被置放於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1399, 'property', 'name_inverse', 51, 'de', 'hält derzeitig', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1400, 'property', 'name_inverse', 51, 'el', 'είναι θέση του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1401, 'property', 'name_inverse', 51, 'ru', 'в данный момент содержит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1402, 'property', 'name_inverse', 51, 'fr', 'est localisation actuelle de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1403, 'property', 'name_inverse', 51, 'en', 'currently holds', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1404, 'property', 'name_inverse', 51, 'pt', 'é localização atual de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1405, 'property', 'name_inverse', 51, 'cn', '目前置放了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1459, 'property', 'comment', 55, 'en', 'This property links an area to the instance of E18 Physical Thing upon which it is found.
It is typically used when a named E46 Section Definition is not appropriate.
E18 Physical Thing may be subdivided into arbitrary regions.
P59 has section (is located on or within) is a shortcut. If the E53 Place is identified by a Section Definition, a more detailed representation can make use of the fully developed (i.e. indirect) path from E18 Physical Thing through P58 has section definition (defines section), E46 Section Definition, P87 is identified by (identifies) to E53 Place. A Place can only be located on or within one Physical Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1406, 'property', 'comment', 51, 'en', 'This property records the location of an E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
	This property is a specialisation of P53 has former or current location (is former or current location of). It indicates that the E53 Place associated with the E19 Physical Object is the current location of the object. The property does not allow any indication of how long the Object has been at the current location.
P55 has current location (currently holds) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P25 moved (moved by), E9 Move P26 moved to (was destination of) to E53 Place if and only if this Move is the most recent.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1407, 'property', 'name', 52, 'ru', 'несет признак', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1408, 'property', 'name', 52, 'de', 'trägt Merkmal', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1409, 'property', 'name', 52, 'fr', 'présente pour caractéristique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1410, 'property', 'name', 52, 'el', 'φέρει μόρφωμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1411, 'property', 'name', 52, 'en', 'bears feature', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1412, 'property', 'name', 52, 'pt', 'possui característica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1413, 'property', 'name', 52, 'cn', '有外貌表征', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1414, 'property', 'name_inverse', 52, 'el', 'βρίσκεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1415, 'property', 'name_inverse', 52, 'fr', 'se trouve sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1416, 'property', 'name_inverse', 52, 'de', 'wird gefunden auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1417, 'property', 'name_inverse', 52, 'en', 'is found on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1418, 'property', 'name_inverse', 52, 'ru', 'найден на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1419, 'property', 'name_inverse', 52, 'pt', 'é encontrada em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1420, 'property', 'name_inverse', 52, 'cn', '被见於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1421, 'property', 'comment', 52, 'en', 'This property describes a E26 Physical Feature found on a E19 Physical Object It does not specify the location of the feature on the object.
P56 bears feature (is found on) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P59 has section (is located on or within), E53 Place, P53 has former or current location (is former or current location of) to E26 Physical Feature.
A Physical Feature can only exist on one object. One object may bear more than one Physical Feature. An E27 Site should be considered as an E26 Physical Feature on the surface of the Earth.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1422, 'property', 'name', 53, 'en', 'has number of parts', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1423, 'property', 'name', 53, 'ru', 'имеет число частей', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1424, 'property', 'name', 53, 'el', 'έχει αριθμό μερών', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1425, 'property', 'name', 53, 'fr', 'a pour nombre de parties', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1426, 'property', 'name', 53, 'de', 'hat Anzahl Teile', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1427, 'property', 'name', 53, 'pt', 'tem número de partes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1428, 'property', 'name', 53, 'cn', '有组件数目', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1429, 'property', 'comment', 53, 'en', 'This property documents the E60 Number of parts of which an instance of E19 Physical Object is composed.
This may be used as a method of checking inventory counts with regard to aggregate or collective objects. What constitutes a part or component depends on the context and requirements of the documentation. Normally, the parts documented in this way would not be considered as worthy of individual attention.
For a more complete description, objects may be decomposed into their components and constituents using P46 is composed of (forms parts of) and P45 consists of (is incorporated in). This allows each element to be described individually.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1430, 'property', 'name', 54, 'en', 'has section definition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1431, 'property', 'name', 54, 'de', 'hat Abschittsdefinition', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1432, 'property', 'name', 54, 'ru', 'имеет определение района', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1433, 'property', 'name', 54, 'el', 'έχει ορισμό τμήματος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1434, 'property', 'name', 54, 'fr', 'a pour désignation de section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1435, 'property', 'name', 54, 'pt', 'tem designação de seção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1436, 'property', 'name', 54, 'cn', '有区域定义', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1437, 'property', 'name_inverse', 54, 'ru', 'определяет район', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1438, 'property', 'name_inverse', 54, 'en', 'defines section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1439, 'property', 'name_inverse', 54, 'de', 'definiert Abschitt auf oder von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1440, 'property', 'name_inverse', 54, 'fr', 'définit une section de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1441, 'property', 'name_inverse', 54, 'el', 'ορίζει τμήμα σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1442, 'property', 'name_inverse', 54, 'pt', 'define uma seção de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1443, 'property', 'name_inverse', 54, 'cn', '界定了区域於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1444, 'property', 'comment', 54, 'en', 'This property links an area (section) named by a E46 Section Definition to the instance of E18 Physical Thing upon which it is found.
The CRM handles sections as locations (instances of E53 Place) within or on E18 Physical Thing that are identified by E46 Section Definitions. Sections need not be discrete and separable components or parts of an object.
This is part of a more developed path from E18 Physical Thing through P58, E46 Section Definition, P87 is identified by (identifies) that allows a more precise definition of a location found on an object than the shortcut P59 has section (is located on or within).
A particular instance of a Section Definition only applies to one instance of Physical Thing.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1445, 'property', 'name', 55, 'en', 'has section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1446, 'property', 'name', 55, 'el', 'έχει τομέα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1447, 'property', 'name', 55, 'de', 'hat Bereich', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1448, 'property', 'name', 55, 'ru', 'имеет район', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1449, 'property', 'name', 55, 'fr', 'a pour section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1450, 'property', 'name', 55, 'pt', 'tem seção', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1451, 'property', 'name', 55, 'cn', '有区域', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1452, 'property', 'name_inverse', 55, 'ru', 'находится на или внутри', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1453, 'property', 'name_inverse', 55, 'de', 'befindet sich auf oder in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1454, 'property', 'name_inverse', 55, 'el', 'βρίσκεται σε ή εντός', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1455, 'property', 'name_inverse', 55, 'fr', 'se situe sur ou dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1456, 'property', 'name_inverse', 55, 'en', 'is located on or within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1457, 'property', 'name_inverse', 55, 'pt', 'está localizada sobre ou dentro de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1458, 'property', 'name_inverse', 55, 'cn', '位於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1460, 'property', 'name', 56, 'de', 'bildet ab', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1461, 'property', 'name', 56, 'ru', 'описывает', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1462, 'property', 'name', 56, 'en', 'depicts', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1463, 'property', 'name', 56, 'el', 'απεικονίζει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1464, 'property', 'name', 56, 'fr', 'figure', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1465, 'property', 'name', 56, 'pt', 'retrata', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1466, 'property', 'name', 56, 'cn', '描绘', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1467, 'property', 'name_inverse', 56, 'el', 'απεικονίζεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1468, 'property', 'name_inverse', 56, 'de', 'wird abgebildet durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1469, 'property', 'name_inverse', 56, 'en', 'is depicted by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1470, 'property', 'name_inverse', 56, 'ru', 'описан посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1471, 'property', 'name_inverse', 56, 'fr', 'est figurée sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1472, 'property', 'name_inverse', 56, 'pt', 'é retratada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1473, 'property', 'name_inverse', 56, 'cn', '被描绘於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1474, 'property', 'comment', 56, 'en', 'This property identifies something that is depicted by an instance of E24 Physical Man-Made Thing.
This property is a shortcut of the more fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1CRM Entity. P62.1 mode of depiction allows the nature of the depiction to be refined.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1475, 'property', 'name', 57, 'fr', 'présente l''item visuel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1476, 'property', 'name', 57, 'en', 'shows visual item', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1477, 'property', 'name', 57, 'de', 'zeigt Bildliches', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1478, 'property', 'name', 57, 'ru', 'показывает визуальный предмет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1479, 'property', 'name', 57, 'el', 'εμφανίζει οπτικό στοιχείο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1480, 'property', 'name', 57, 'pt', 'apresenta item visual', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1481, 'property', 'name', 57, 'cn', '显示视觉项目', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1482, 'property', 'name_inverse', 57, 'de', 'wird gezeigt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1483, 'property', 'name_inverse', 57, 'fr', 'est présenté par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1484, 'property', 'name_inverse', 57, 'en', 'is shown by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1485, 'property', 'name_inverse', 57, 'el', 'εμφανίζεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1486, 'property', 'name_inverse', 57, 'ru', 'показан посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1487, 'property', 'name_inverse', 57, 'pt', 'é apresentado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1488, 'property', 'name_inverse', 57, 'cn', '被显示於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1489, 'property', 'comment', 57, 'en', 'This property documents an E36 Visual Item shown by an instance of E24 Physical Man-Made Thing.
This property is similar to P62 depicts (is depicted by) in that it associates an item of E24 Physical Man-Made Thing with a visual representation. However, P65 shows visual item (is shown by) differs from the P62 depicts (is depicted by) property in that it makes no claims about what the E36 Visual Item is deemed to represent. E36 Visual Item identifies a recognisable image or visual symbol, regardless of what this image may or may not represent.
For example, all recent British coins bear a portrait of Queen Elizabeth II, a fact that is correctly documented using P62 depicts (is depicted by). Different portraits have been used at different periods, however. P65 shows visual item (is shown by) can be used to refer to a particular portrait.
P65 shows visual item (is shown by) may also be used for Visual Items such as signs, marks and symbols, for example the ''Maltese Cross'' or the ''copyright symbol’ that have no particular representational content.
This property is part of the fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1 CRM Entity which is shortcut by, P62 depicts (is depicted by).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1490, 'property', 'name', 58, 'el', 'αναφέρεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1491, 'property', 'name', 58, 'en', 'refers to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1492, 'property', 'name', 58, 'ru', 'ссылается на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1493, 'property', 'name', 58, 'fr', 'fait référence à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1494, 'property', 'name', 58, 'de', 'verweist auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1495, 'property', 'name', 58, 'pt', 'referencia', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1496, 'property', 'name', 58, 'cn', '论及', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1497, 'property', 'name_inverse', 58, 'fr', 'est référencé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1498, 'property', 'name_inverse', 58, 'el', 'αναφέρεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1499, 'property', 'name_inverse', 58, 'de', 'wird angeführt von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1500, 'property', 'name_inverse', 58, 'en', 'is referred to by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1501, 'property', 'name_inverse', 58, 'ru', 'имеет ссылку на себя от', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1502, 'property', 'name_inverse', 58, 'pt', 'é referenciado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1503, 'property', 'name_inverse', 58, 'cn', '被论及於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1504, 'property', 'comment', 58, 'en', 'This property documents that an E89 Propositional Object makes a statement about an instance of E1 CRM Entity. P67 refers to (is referred to by) has the P67.1 has type link to an instance of E55 Type. This is intended to allow a more detailed description of the type of reference. This differs from P129 is about (is subject of), which describes the primary subject or subjects of the E89 Propositional Object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1505, 'property', 'name', 59, 'en', 'foresees use of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1506, 'property', 'name', 59, 'de', ' sieht den Gebrauch vor von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1507, 'property', 'name', 59, 'ru', 'обычно применяет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1508, 'property', 'name', 59, 'fr', 'utilise habituellement', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1509, 'property', 'name', 59, 'el', 'συνήθως χρησιμοποιεί', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1510, 'property', 'name', 59, 'pt', 'normalmente emprega', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1511, 'property', 'name', 59, 'cn', '指定使用材料', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1512, 'property', 'name_inverse', 59, 'el', 'συνήθως χρησιμοποιείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1513, 'property', 'name_inverse', 59, 'de', 'vorgesehen für Gebrauch durch defined', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1514, 'property', 'name_inverse', 59, 'fr', 'est habituellement utilisé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1515, 'property', 'name_inverse', 59, 'ru', 'обычно используется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1516, 'property', 'name_inverse', 59, 'en', 'use foreseen by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1517, 'property', 'name_inverse', 59, 'pt', 'é empregado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1518, 'property', 'name_inverse', 59, 'cn', '被指定使用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1519, 'property', 'comment', 59, 'en', 'This property identifies an E57 Material foreseeen to be used by an E29 Design or Procedure.
E29 Designs and procedures commonly foresee the use of particular E57 Materials. The fabrication of adobe bricks, for example, requires straw, clay and water. This property enables this to be documented.
This property is not intended for the documentation of E57 Materials that were used on a particular occasion when an instance of E29 Design or Procedure was executed.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1520, 'property', 'name', 60, 'fr', 'est associée à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1521, 'property', 'name', 60, 'el', 'σχετίζεται με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1522, 'property', 'name', 60, 'ru', 'ассоциирован с', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1523, 'property', 'name', 60, 'de', 'ist verbunden mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1524, 'property', 'name', 60, 'en', 'is associated with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1525, 'property', 'name', 60, 'pt', 'é associado com', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1526, 'property', 'name', 60, 'cn', '相关於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1527, 'property', 'comment', 60, 'en', 'This symmetric property describes the association of an E29 Design or Procedure with other Designs or Procedures.
Any instance of E29 Design or Procedure may be associated with other designs or procedures. The P69.1 has type property of P69 is associated with allows the nature of the association to be specified; examples of types of association between instances of E29 Design or Procedure include: whole-part, sequence, prerequisite, etc.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1528, 'property', 'name', 61, 'fr', 'mentionne', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1529, 'property', 'name', 61, 'ru', 'документирует', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1530, 'property', 'name', 61, 'el', 'τεκμηριώνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1531, 'property', 'name', 61, 'en', 'documents', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1532, 'property', 'name', 61, 'de', 'belegt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1533, 'property', 'name', 61, 'pt', 'documenta', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1534, 'property', 'name', 61, 'cn', '记录了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1535, 'property', 'name_inverse', 61, 'en', 'is documented in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1536, 'property', 'name_inverse', 61, 'el', 'τεκμηριώνεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1537, 'property', 'name_inverse', 61, 'de', 'wird belegt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1538, 'property', 'name_inverse', 61, 'fr', 'est mentionnée dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1539, 'property', 'name_inverse', 61, 'ru', 'документирован в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1540, 'property', 'name_inverse', 61, 'pt', 'é documentado em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1541, 'property', 'name_inverse', 61, 'cn', '被记录於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1542, 'property', 'comment', 61, 'en', 'This property describes the CRM Entities documented by instances of E31 Document.
Documents may describe any conceivable entity, hence the link to the highest-level entity in the CRM hierarchy. This property is intended for cases where a reference is regarded as being of a documentary character, in the scholarly or scientific sense.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1543, 'property', 'name', 62, 'de', 'listet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1544, 'property', 'name', 62, 'ru', 'перечисляет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1545, 'property', 'name', 62, 'en', 'lists', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1546, 'property', 'name', 62, 'el', 'περιλαμβάνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1547, 'property', 'name', 62, 'fr', 'définit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1548, 'property', 'name', 62, 'pt', 'define', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1549, 'property', 'name', 62, 'cn', '条列出', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1550, 'property', 'name_inverse', 62, 'el', 'περιλαμβάνεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1551, 'property', 'name_inverse', 62, 'de', 'wird aufgelistet in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1552, 'property', 'name_inverse', 62, 'en', 'is listed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1553, 'property', 'name_inverse', 62, 'ru', 'перечислен в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1554, 'property', 'name_inverse', 62, 'fr', 'est défini par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1555, 'property', 'name_inverse', 62, 'pt', 'é definido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1556, 'property', 'name_inverse', 62, 'cn', '被条列於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1557, 'property', 'comment', 62, 'en', 'This property documents a source E32 Authority Document for an instance of an E1 CRM Entity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1558, 'property', 'name', 63, 'fr', 'est en langue', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1559, 'property', 'name', 63, 'ru', 'имеет язык', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1560, 'property', 'name', 63, 'en', 'has language', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1561, 'property', 'name', 63, 'de', 'hat Sprache', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1562, 'property', 'name', 63, 'el', 'έχει γλώσσα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1563, 'property', 'name', 63, 'pt', 'é da língua ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1564, 'property', 'name', 63, 'cn', '使用语言', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1565, 'property', 'name_inverse', 63, 'de', 'ist Sprache von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1566, 'property', 'name_inverse', 63, 'el', 'είναι γλώσσα του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1567, 'property', 'name_inverse', 63, 'fr', 'est la langue de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1568, 'property', 'name_inverse', 63, 'ru', 'является языком для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1569, 'property', 'name_inverse', 63, 'en', 'is language of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1570, 'property', 'name_inverse', 63, 'pt', 'é a língua de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1571, 'property', 'name_inverse', 63, 'cn', '被用来撰写', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1572, 'property', 'comment', 63, 'en', 'This property describes the E56 Language of an E33 Linguistic Object.
Linguistic Objects are composed in one or more human Languages. This property allows these languages to be documented.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1573, 'property', 'name', 64, 'el', 'έχει μετάφραση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1574, 'property', 'name', 64, 'de', 'hat Übersetzung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1575, 'property', 'name', 64, 'ru', 'имеет перевод', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1576, 'property', 'name', 64, 'en', 'has translation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1577, 'property', 'name', 64, 'fr', 'a pour traduction', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1578, 'property', 'name', 64, 'pt', 'tem tradução', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1579, 'property', 'name', 64, 'cn', '有译文', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1580, 'property', 'name_inverse', 64, 'fr', 'est la traduction de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1581, 'property', 'name_inverse', 64, 'ru', 'является переводом', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1582, 'property', 'name_inverse', 64, 'el', 'είναι μετάφραση του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1583, 'property', 'name_inverse', 64, 'de', 'ist Übersetzung von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1584, 'property', 'name_inverse', 64, 'en', 'is translation of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1585, 'property', 'name_inverse', 64, 'pt', 'é tradução de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1586, 'property', 'name_inverse', 64, 'cn', '翻译自', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1587, 'property', 'comment', 64, 'en', 'This property describes the source and target of instances of E33Linguistic Object involved in a translation.
When a Linguistic Object is translated into a new language it becomes a new Linguistic Object, despite being conceptually similar to the source object.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1588, 'property', 'name', 65, 'ru', 'имеет текущее или бывшее местожительства', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1589, 'property', 'name', 65, 'en', 'has current or former residence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1590, 'property', 'name', 65, 'de', 'hat derzeitigen oder früheren Sitz', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1591, 'property', 'name', 65, 'el', 'έχει ή είχε κατοικία', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1592, 'property', 'name', 65, 'fr', 'réside ou a résidé à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1593, 'property', 'name', 65, 'pt', 'reside ou residiu em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1594, 'property', 'name', 65, 'cn', '目前或曾经居住於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1595, 'property', 'name_inverse', 65, 'el', 'είναι ή ήταν κατοικία του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1596, 'property', 'name_inverse', 65, 'de', 'ist derzeitiger oder früherer Sitz von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1597, 'property', 'name_inverse', 65, 'fr', 'est ou a été la résidence de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1598, 'property', 'name_inverse', 65, 'ru', 'является текущим или бывшим местом жительства для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1599, 'property', 'name_inverse', 65, 'en', 'is current or former residence of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1600, 'property', 'name_inverse', 65, 'pt', 'é ou foi residência de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1601, 'property', 'name_inverse', 65, 'cn', '历年来的居住者包括', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1602, 'property', 'comment', 65, 'en', 'This property describes the current or former E53 Place of residence of an E39 Actor.
The residence may be either the Place where the Actor resides, or a legally registered address of any kind.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1603, 'property', 'name', 66, 'ru', 'владеет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1604, 'property', 'name', 66, 'el', 'κατέχει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1605, 'property', 'name', 66, 'de', 'besitzt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1606, 'property', 'name', 66, 'fr', 'est détenteur de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1607, 'property', 'name', 66, 'en', 'possesses', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1608, 'property', 'name', 66, 'pt', 'é detentor de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1609, 'property', 'name', 66, 'cn', '拥有', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1610, 'property', 'name_inverse', 66, 'el', 'κατέχεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1611, 'property', 'name_inverse', 66, 'ru', 'принадлежит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1612, 'property', 'name_inverse', 66, 'de', 'sind im Besitz von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1613, 'property', 'name_inverse', 66, 'fr', 'est détenu par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1614, 'property', 'name_inverse', 66, 'en', 'is possessed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1615, 'property', 'name_inverse', 66, 'pt', 'são detidos por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1616, 'property', 'name_inverse', 66, 'cn', '有拥有者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1617, 'property', 'comment', 66, 'en', 'This property identifies former or current instances of E30 Rights held by an E39 Actor.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1618, 'property', 'name', 67, 'en', 'has contact point', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1619, 'property', 'name', 67, 'ru', 'имеет контакт', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1620, 'property', 'name', 67, 'fr', 'a pour coordonnées individuelles', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1621, 'property', 'name', 67, 'el', 'έχει σημείο επικοινωνίας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1622, 'property', 'name', 67, 'de', 'hat Kontaktpunkt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1623, 'property', 'name', 67, 'pt', 'possui ponto de contato', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1624, 'property', 'name', 67, 'cn', '有联系方式', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1625, 'property', 'name_inverse', 67, 'fr', 'permettent de contacter', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1626, 'property', 'name_inverse', 67, 'de', 'bietet Zugang zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1627, 'property', 'name_inverse', 67, 'en', 'provides access to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1628, 'property', 'name_inverse', 67, 'el', 'παρέχει πρόσβαση σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1629, 'property', 'name_inverse', 67, 'ru', 'предоставляет доступ к', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1630, 'property', 'name_inverse', 67, 'pt', 'é ponto de contado de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1631, 'property', 'name_inverse', 67, 'cn', '被用来联系', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1632, 'property', 'comment', 67, 'en', 'This property identifies an E51 Contact Point of any type that provides access to an E39 Actor by any communication method, such as e-mail or fax.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1633, 'property', 'name', 68, 'el', 'αναγνωρίζεται ως', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1634, 'property', 'name', 68, 'fr', 'est identifiée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1635, 'property', 'name', 68, 'en', 'is identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1636, 'property', 'name', 68, 'ru', 'идентифицируется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1637, 'property', 'name', 68, 'de', 'wird bezeichnet als', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1638, 'property', 'name', 68, 'pt', 'é identificado por ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1639, 'property', 'name', 68, 'cn', '有识别称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1640, 'property', 'name_inverse', 68, 'en', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1641, 'property', 'name_inverse', 68, 'de', 'bezeichnet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1642, 'property', 'name_inverse', 68, 'fr', 'identifie', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1643, 'property', 'name_inverse', 68, 'el', 'είναι αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1644, 'property', 'name_inverse', 68, 'ru', 'идентифицирует', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1645, 'property', 'name_inverse', 68, 'pt', 'identifica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1646, 'property', 'name_inverse', 68, 'cn', '被用来识别', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1647, 'property', 'comment', 68, 'en', 'This property identifies an E52 Time-Span using an E49Time Appellation.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1648, 'property', 'name', 69, 'el', 'αρχή προσδιορίζεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1649, 'property', 'name', 69, 'ru', 'начало ограничено', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1650, 'property', 'name', 69, 'de', 'hat Anfangsbegründung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1651, 'property', 'name', 69, 'en', 'beginning is qualified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1652, 'property', 'name', 69, 'fr', 'début est qualifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1653, 'property', 'name', 69, 'pt', 'início é qualificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1654, 'property', 'name', 69, 'cn', '起点认定的性质是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1655, 'property', 'comment', 69, 'en', 'This property qualifies the beginning of an E52 Time-Span in some way.
The nature of the qualification may be certainty, precision, source etc.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1656, 'property', 'name', 70, 'el', 'τέλος προσδιορίζεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1657, 'property', 'name', 70, 'fr', 'fin est qualifiée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1658, 'property', 'name', 70, 'de', 'hat Begründung des Endes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1659, 'property', 'name', 70, 'ru', 'конец ограничен', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1660, 'property', 'name', 70, 'en', 'end is qualified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1661, 'property', 'name', 70, 'pt', 'final é qualificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1662, 'property', 'name', 70, 'cn', '终点认定的性质是', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1663, 'property', 'comment', 70, 'en', 'This property qualifies the end of an E52 Time-Span in some way.
The nature of the qualification may be certainty, precision, source etc.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1664, 'property', 'name', 71, 'en', 'ongoing throughout', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1665, 'property', 'name', 71, 'el', 'καθόλη τη διάρκεια του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1666, 'property', 'name', 71, 'de', 'andauernd während', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1667, 'property', 'name', 71, 'fr', 'couvre au moins', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1668, 'property', 'name', 71, 'ru', 'длится в течение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1669, 'property', 'name', 71, 'pt', 'abrange no mínimo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1670, 'property', 'name', 71, 'cn', '时段的数值至少涵盖', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1671, 'property', 'comment', 71, 'en', 'This property describes the minimum period of time covered by an E52 Time-Span.
Since Time-Spans may not have precisely known temporal extents, the CRM supports statements about the minimum and maximum temporal extents of Time-Spans. This property allows a Time-Span’s minimum temporal extent (i.e. its inner boundary) to be assigned an E61 Time Primitive value. Time Primitives are treated by the CRM as application or system specific date intervals, and are not further analysed.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1672, 'property', 'name', 72, 'el', 'κάποτε εντός', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1673, 'property', 'name', 72, 'ru', 'некоторое время в течение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1674, 'property', 'name', 72, 'de', 'irgendwann innerhalb von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1675, 'property', 'name', 72, 'fr', 'couvre au plus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1676, 'property', 'name', 72, 'en', 'at some time within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1677, 'property', 'name', 72, 'pt', 'abrange no máximo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1678, 'property', 'name', 72, 'cn', '时段的数值不会超越', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1679, 'property', 'comment', 72, 'en', 'This property describes the maximum period of time within which an E52 Time-Span falls.
Since Time-Spans may not have precisely known temporal extents, the CRM supports statements about the minimum and maximum temporal extents of Time-Spans. This property allows a Time-Span’s maximum temporal extent (i.e. its outer boundary) to be assigned an E61 Time Primitive value. Time Primitives are treated by the CRM as application or system specific date intervals, and are not further analysed.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1680, 'property', 'name', 73, 'fr', 'a duré au moins', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1681, 'property', 'name', 73, 'el', 'είχε ελάχιστη διάρκεια', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1682, 'property', 'name', 73, 'de', 'hatte Mindestdauer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1683, 'property', 'name', 73, 'en', 'had at least duration', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1684, 'property', 'name', 73, 'ru', 'имеет длительность по крайней мере больше чем', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1685, 'property', 'name', 73, 'pt', 'durou no mínimo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1686, 'property', 'name', 73, 'cn', '时间最少持续了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1687, 'property', 'name_inverse', 73, 'el', 'είναι ελάχιστη διάρκεια του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1688, 'property', 'name_inverse', 73, 'fr', 'a été la durée minimum de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1689, 'property', 'name_inverse', 73, 'ru', 'был минимальной длительностью для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1690, 'property', 'name_inverse', 73, 'en', 'was minimum duration of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1691, 'property', 'name_inverse', 73, 'de', 'war Mindestdauer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1692, 'property', 'name_inverse', 73, 'pt', 'foi a duração mínima de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1693, 'property', 'comment', 73, 'en', 'This property describes the minimum length of time covered by an E52 Time-Span.
It allows an E52 Time-Span to be associated with an E54 Dimension representing it’s minimum duration (i.e. it’s inner boundary) independent from the actual beginning and end.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1694, 'property', 'name', 74, 'el', 'είχε μέγιστη διάρκεια', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1695, 'property', 'name', 74, 'en', 'had at most duration', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1696, 'property', 'name', 74, 'de', 'hatte Höchstdauer', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1697, 'property', 'name', 74, 'ru', 'имеет длительность меньше чем', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1698, 'property', 'name', 74, 'fr', 'a duré au plus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1699, 'property', 'name', 74, 'pt', 'durou no máximo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1700, 'property', 'name', 74, 'cn', '时间最多持续了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1701, 'property', 'name_inverse', 74, 'ru', 'был максимальной длительностью для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1702, 'property', 'name_inverse', 74, 'de', 'war längste Dauer von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1703, 'property', 'name_inverse', 74, 'en', 'was maximum duration of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1704, 'property', 'name_inverse', 74, 'el', 'είναι μέγιστη διάρκεια του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1705, 'property', 'name_inverse', 74, 'fr', 'a été la durée maximum de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1706, 'property', 'name_inverse', 74, 'pt', 'foi a duração máxima de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1707, 'property', 'name_inverse', 74, 'cn', '', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1708, 'property', 'comment', 74, 'en', 'This property describes the maximum length of time covered by an E52 Time-Span.
It allows an E52 Time-Span to be associated with an E54 Dimension representing it’s maximum duration (i.e. it’s outer boundary) independent from the actual beginning and end.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1709, 'property', 'name', 75, 'en', 'falls within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1710, 'property', 'name', 75, 'ru', 'содержится в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1711, 'property', 'name', 75, 'el', 'περιέχεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1712, 'property', 'name', 75, 'fr', 's’insère dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1713, 'property', 'name', 75, 'de', 'fällt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1714, 'property', 'name', 75, 'pt', 'está contido em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1715, 'property', 'name', 75, 'cn', '时间上被涵盖於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1716, 'property', 'name_inverse', 75, 'fr', 'inclut', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1717, 'property', 'name_inverse', 75, 'de', 'enthält', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1718, 'property', 'name_inverse', 75, 'en', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1719, 'property', 'name_inverse', 75, 'el', 'περιέχει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1720, 'property', 'name_inverse', 75, 'ru', 'содержит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1721, 'property', 'name_inverse', 75, 'pt', 'contém', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1722, 'property', 'name_inverse', 75, 'cn', '时间上涵盖了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1723, 'property', 'comment', 75, 'en', 'This property describes the inclusion relationship between two instances of E52 Time-Span.
This property supports the notion that a Time-Span’s temporal extent falls within the temporal extent of another Time-Span. It addresses temporal containment only, and no contextual link between the two instances of Time-Span is implied.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1724, 'property', 'name', 76, 'el', 'αναγνωρίζεται ως', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1725, 'property', 'name', 76, 'en', 'is identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1726, 'property', 'name', 76, 'ru', 'идентифицируется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1727, 'property', 'name', 76, 'fr', 'est identifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1728, 'property', 'name', 76, 'de', 'wird bezeichnet als', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1729, 'property', 'name', 76, 'pt', 'é identificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1730, 'property', 'name', 76, 'cn', '有辨认码', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1731, 'property', 'name_inverse', 76, 'de', 'bezeichnet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1732, 'property', 'name_inverse', 76, 'el', 'είναι αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1733, 'property', 'name_inverse', 76, 'ru', 'идентифицирует', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1734, 'property', 'name_inverse', 76, 'fr', 'identifie', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1735, 'property', 'name_inverse', 76, 'en', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1736, 'property', 'name_inverse', 76, 'pt', 'identifica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1737, 'property', 'name_inverse', 76, 'cn', '被用来辨认', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1738, 'property', 'comment', 76, 'en', 'This property identifies an E53 Place using an E44 Place Appellation.
Examples of Place Appellations used to identify Places include instances of E48 Place Name, addresses, E47 Spatial Coordinates etc.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1739, 'property', 'name', 77, 'fr', 's’insère dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1740, 'property', 'name', 77, 'en', 'falls within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1741, 'property', 'name', 77, 'ru', 'содержится в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1742, 'property', 'name', 77, 'de', 'fällt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1743, 'property', 'name', 77, 'el', 'περιέχεται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1744, 'property', 'name', 77, 'pt', 'está contido em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1745, 'property', 'name', 77, 'cn', '空间上被包围於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1746, 'property', 'name_inverse', 77, 'fr', 'inclut', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1747, 'property', 'name_inverse', 77, 'ru', 'содержит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1748, 'property', 'name_inverse', 77, 'el', 'περιέχει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1749, 'property', 'name_inverse', 77, 'de', 'enthält', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1750, 'property', 'name_inverse', 77, 'en', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1751, 'property', 'name_inverse', 77, 'pt', 'contém', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1752, 'property', 'name_inverse', 77, 'cn', '空间上包含了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1753, 'property', 'comment', 77, 'en', 'This property identifies the instances of E53 Places that fall within the area covered by another Place.
It addresses spatial containment only, and no ‘whole-part’ relationship between the two places is implied.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1754, 'property', 'name', 78, 'de', 'hat Wert', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1755, 'property', 'name', 78, 'el', 'έχει τιμή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1756, 'property', 'name', 78, 'fr', 'a la valeur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1757, 'property', 'name', 78, 'ru', 'имеет значение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1758, 'property', 'name', 78, 'en', 'has value', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1759, 'property', 'name', 78, 'pt', 'tem valor', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1760, 'property', 'name', 78, 'cn', '有数值', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1761, 'property', 'comment', 78, 'en', 'This property allows an E54 Dimension to be approximated by an E60 Number primitive.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1762, 'property', 'name', 79, 'ru', 'имеет единицу', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1763, 'property', 'name', 79, 'el', 'έχει μονάδα μέτρησης', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1764, 'property', 'name', 79, 'fr', 'a pour unité', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1765, 'property', 'name', 79, 'de', 'hat Einheit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1766, 'property', 'name', 79, 'en', 'has unit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1767, 'property', 'name', 79, 'pt', 'tem unidade', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1768, 'property', 'name', 79, 'cn', '有单位', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1769, 'property', 'name_inverse', 79, 'ru', 'является единицей для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1770, 'property', 'name_inverse', 79, 'fr', 'est l''unité de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1771, 'property', 'name_inverse', 79, 'de', 'ist Einheit von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1772, 'property', 'name_inverse', 79, 'el', 'αποτελεί μονάδα μέτρησης του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1773, 'property', 'name_inverse', 79, 'en', 'is unit of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1774, 'property', 'name_inverse', 79, 'pt', 'é unidade de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1775, 'property', 'name_inverse', 79, 'cn', '被当做单位来表示', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1776, 'property', 'comment', 79, 'en', 'This property shows the type of unit an E54 Dimension was expressed in.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1777, 'property', 'name', 80, 'fr', 'a fait exister', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1778, 'property', 'name', 80, 'en', 'brought into existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1779, 'property', 'name', 80, 'ru', 'создал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1780, 'property', 'name', 80, 'de', 'brachte in Existenz', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1781, 'property', 'name', 80, 'el', 'γέννησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1782, 'property', 'name', 80, 'pt', 'trouxe à existência', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1783, 'property', 'name', 80, 'cn', '开始了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1784, 'property', 'name_inverse', 80, 'en', 'was brought into existence by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1785, 'property', 'name_inverse', 80, 'el', 'γεννήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1786, 'property', 'name_inverse', 80, 'de', 'wurde in Existenz gebracht durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1787, 'property', 'name_inverse', 80, 'fr', 'a commencé à exister du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1788, 'property', 'name_inverse', 80, 'ru', 'был создан посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1789, 'property', 'name_inverse', 80, 'pt', 'passou a existir por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1790, 'property', 'name_inverse', 80, 'cn', '被开始於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1791, 'property', 'comment', 80, 'en', 'This property allows an E63 Beginning of Existence event to be linked to the E77 Persistent Item brought into existence by it.
It allows a “start” to be attached to any Persistent Item being documented i.e. E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation, E51 Contact Point and E55 Type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1792, 'property', 'name', 81, 'fr', 'a fait cesser d’exister', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1793, 'property', 'name', 81, 'ru', 'положил конец существованию', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1794, 'property', 'name', 81, 'de', 'beendete die Existenz von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1795, 'property', 'name', 81, 'en', 'took out of existence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1796, 'property', 'name', 81, 'el', 'αναίρεσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1797, 'property', 'name', 81, 'pt', 'cessou a existência de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1798, 'property', 'name', 81, 'cn', '结束了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1799, 'property', 'name_inverse', 81, 'ru', 'прекратил существование посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1800, 'property', 'name_inverse', 81, 'fr', 'a cessé d’exister du fait de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1801, 'property', 'name_inverse', 81, 'en', 'was taken out of existence by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1802, 'property', 'name_inverse', 81, 'el', 'αναιρέθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1803, 'property', 'name_inverse', 81, 'de', 'wurde seiner Existenz beraubt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1804, 'property', 'name_inverse', 81, 'pt', 'deixou de existir', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1805, 'property', 'name_inverse', 81, 'cn', '被结束於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1806, 'property', 'comment', 81, 'en', 'This property allows an E64 End of Existence event to be linked to the E77 Persistent Item taken out of existence by it.
In the case of immaterial things, the E64 End of Existence is considered to take place with the destruction of the last physical carrier.
This allows an “end” to be attached to any Persistent Item being documented i.e. E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation, E51 Contact Point and E55 Type. For many Persistent Items we know the maximum life-span and can infer, that they must have ended to exist. We assume in that case an End of Existence, which may be as unnoticeable as forgetting the secret knowledge by the last representative of some indigenous nation.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1807, 'property', 'name', 82, 'el', 'δημιούργησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1808, 'property', 'name', 82, 'ru', 'создал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1809, 'property', 'name', 82, 'en', 'has created', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1810, 'property', 'name', 82, 'de', 'hat erschaffen', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1811, 'property', 'name', 82, 'fr', 'a créé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1812, 'property', 'name', 82, 'pt', 'criou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1813, 'property', 'name', 82, 'cn', '创造了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1814, 'property', 'name_inverse', 82, 'el', 'δημιουργήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1815, 'property', 'name_inverse', 82, 'fr', 'a été créé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1816, 'property', 'name_inverse', 82, 'ru', 'был создан посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1817, 'property', 'name_inverse', 82, 'en', 'was created by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1818, 'property', 'name_inverse', 82, 'de', 'wurde erschaffen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1819, 'property', 'name_inverse', 82, 'pt', 'foi criado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1820, 'property', 'name_inverse', 82, 'cn', '被创造於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1821, 'property', 'comment', 82, 'en', 'This property allows a conceptual E65 Creation to be linked to the E28 Conceptual Object created by it.
It represents the act of conceiving the intellectual content of the E28 Conceptual Object. It does not represent the act of creating the first physical carrier of the E28 Conceptual Object. As an example, this is the composition of a poem, not its commitment to paper.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1822, 'property', 'name', 83, 'fr', 'a fondé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1823, 'property', 'name', 83, 'ru', 'сформировал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1824, 'property', 'name', 83, 'de', 'hat gebildet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1825, 'property', 'name', 83, 'en', 'has formed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1826, 'property', 'name', 83, 'el', 'σχημάτισε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1827, 'property', 'name', 83, 'pt', 'formou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1828, 'property', 'name', 83, 'cn', '组成了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1829, 'property', 'name_inverse', 83, 'fr', 'a été fondé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1830, 'property', 'name_inverse', 83, 'de', 'wurde gebildet von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1831, 'property', 'name_inverse', 83, 'el', 'σχηματίστηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1832, 'property', 'name_inverse', 83, 'en', 'was formed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1833, 'property', 'name_inverse', 83, 'ru', 'была сформирована посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1834, 'property', 'name_inverse', 83, 'pt', 'foi formado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1835, 'property', 'name_inverse', 83, 'cn', '被组成於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1836, 'property', 'comment', 83, 'en', 'This property links the founding or E66 Formation for an E74 Group with the Group itself.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1837, 'property', 'name', 84, 'ru', 'посредством матери', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1838, 'property', 'name', 84, 'de', 'durch Mutter', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1839, 'property', 'name', 84, 'fr', 'de mère', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1840, 'property', 'name', 84, 'en', 'by mother', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1841, 'property', 'name', 84, 'el', 'είχε μητέρα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1842, 'property', 'name', 84, 'pt', 'pela mãe', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1843, 'property', 'name', 84, 'cn', '来自生母', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1844, 'property', 'name_inverse', 84, 'el', 'ήταν μητέρα του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1845, 'property', 'name_inverse', 84, 'fr', 'a donné naissance à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1846, 'property', 'name_inverse', 84, 'en', 'gave birth', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1847, 'property', 'name_inverse', 84, 'ru', 'дал рождение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1848, 'property', 'name_inverse', 84, 'de', 'gebar', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1849, 'property', 'name_inverse', 84, 'pt', 'deu nascimento', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1850, 'property', 'name_inverse', 84, 'cn', '成为生母於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1851, 'property', 'comment', 84, 'en', 'This property links an E67 Birth event to an E21 Person as a participant in the role of birth-giving mother.

Note that biological fathers are not necessarily participants in the Birth (see P97 from father (was father for)). The Person being born is linked to the Birth with the property P98 brought into life (was born). This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions. This is a sub-property of P11 had participant (participated in).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1852, 'property', 'name', 85, 'de', 'gab Vaterschaft', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1853, 'property', 'name', 85, 'ru', 'от отца', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1854, 'property', 'name', 85, 'en', 'from father', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1855, 'property', 'name', 85, 'el', 'είχε πατέρα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1856, 'property', 'name', 85, 'fr', 'de père', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1857, 'property', 'name', 85, 'pt', 'pelo pai', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1858, 'property', 'name', 85, 'cn', '来自父亲', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1859, 'property', 'name_inverse', 85, 'en', 'was father for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1860, 'property', 'name_inverse', 85, 'el', 'ήταν πατέρας του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1861, 'property', 'name_inverse', 85, 'fr', 'a été père dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1862, 'property', 'name_inverse', 85, 'de', 'war Vater für', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1863, 'property', 'name_inverse', 85, 'ru', 'был отцом для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1864, 'property', 'name_inverse', 85, 'pt', 'foi pai para', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1865, 'property', 'name_inverse', 85, 'cn', '成为生父於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1866, 'property', 'comment', 85, 'en', 'This property links an E67 Birth event to an E21 Person in the role of biological father.
Note that biological fathers are not seen as necessary participants in the Birth, whereas birth-giving mothers are (see P96 by mother (gave birth)). The Person being born is linked to the Birth with the property P98 brought into life (was born).
This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions.
A Birth event is normally (but not always) associated with one biological father.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1867, 'property', 'name', 86, 'fr', 'a donné vie à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1868, 'property', 'name', 86, 'de', 'brachte zur Welt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1869, 'property', 'name', 86, 'en', 'brought into life', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1870, 'property', 'name', 86, 'ru', 'породил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1871, 'property', 'name', 86, 'el', 'έφερε στη ζωή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1872, 'property', 'name', 86, 'pt', 'trouxe à vida', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1873, 'property', 'name', 86, 'cn', '诞生了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1874, 'property', 'name_inverse', 86, 'fr', 'est né', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1875, 'property', 'name_inverse', 86, 'el', 'γεννήθηκε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1876, 'property', 'name_inverse', 86, 'de', 'wurde geboren durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1877, 'property', 'name_inverse', 86, 'en', 'was born', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1878, 'property', 'name_inverse', 86, 'ru', 'был рожден', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1879, 'property', 'name_inverse', 86, 'pt', 'veio à vida pelo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1880, 'property', 'name_inverse', 86, 'cn', '诞生於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1881, 'property', 'comment', 86, 'en', 'This property links an E67Birth event to an E21 Person in the role of offspring.
Twins, triplets etc. are brought into life by the same Birth event. This is not intended for use with general Natural History material, only people. There is no explicit method for modelling conception and gestation except by using extensions.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1882, 'property', 'name', 87, 'el', 'διέλυσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1883, 'property', 'name', 87, 'ru', 'распустил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1884, 'property', 'name', 87, 'fr', 'a dissous', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1885, 'property', 'name', 87, 'en', 'dissolved', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1886, 'property', 'name', 87, 'de', 'löste auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1887, 'property', 'name', 87, 'pt', 'dissolveu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1888, 'property', 'name', 87, 'cn', '解散了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1889, 'property', 'name_inverse', 87, 'de', 'wurde aufgelöst durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1890, 'property', 'name_inverse', 87, 'ru', 'был распущен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1891, 'property', 'name_inverse', 87, 'fr', 'a été dissous par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1892, 'property', 'name_inverse', 87, 'el', 'διαλύθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1893, 'property', 'name_inverse', 87, 'en', 'was dissolved by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1894, 'property', 'name_inverse', 87, 'pt', 'foi dissolvido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1895, 'property', 'name_inverse', 87, 'cn', '被解散於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1896, 'property', 'comment', 87, 'en', 'This property links the disbanding or E68 Dissolution of an E74 Group to the Group itself.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1897, 'property', 'name', 88, 'en', 'was death of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1898, 'property', 'name', 88, 'fr', 'a été la mort de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1899, 'property', 'name', 88, 'el', 'ήταν θάνατος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1900, 'property', 'name', 88, 'de', 'Tod von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1901, 'property', 'name', 88, 'ru', 'был смертью для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1902, 'property', 'name', 88, 'pt', 'foi a morte para ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1903, 'property', 'name', 88, 'cn', '灭亡了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1904, 'property', 'name_inverse', 88, 'de', 'starb in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1905, 'property', 'name_inverse', 88, 'fr', 'est mort par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1906, 'property', 'name_inverse', 88, 'en', 'died in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1907, 'property', 'name_inverse', 88, 'el', 'πέθανε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1908, 'property', 'name_inverse', 88, 'ru', 'умер в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1909, 'property', 'name_inverse', 88, 'pt', 'morreu em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1910, 'property', 'name_inverse', 88, 'cn', '死亡於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1911, 'property', 'comment', 88, 'en', 'This property property links an E69 Death event to the E21 Person that died.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1912, 'property', 'name', 89, 'en', 'had as general use', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1913, 'property', 'name', 89, 'fr', 'avait comme utilisation générale', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1914, 'property', 'name', 89, 'el', 'είχε ως γενική χρήση', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1915, 'property', 'name', 89, 'de', 'hatte die allgemeine Verwendung', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1916, 'property', 'name', 89, 'ru', 'имел основное применение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1917, 'property', 'name', 89, 'pt', 'tem como uso geral', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1918, 'property', 'name', 89, 'cn', '被惯用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1919, 'property', 'name_inverse', 89, 'de', 'war die Verwendung von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1920, 'property', 'name_inverse', 89, 'en', 'was use of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1921, 'property', 'name_inverse', 89, 'fr', 'était l’utilisation de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1922, 'property', 'name_inverse', 89, 'ru', 'был применением для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1923, 'property', 'name_inverse', 89, 'el', 'ήταν χρήση του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1924, 'property', 'name_inverse', 89, 'pt', 'foi uso de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1925, 'property', 'name_inverse', 89, 'cn', '可使用', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1926, 'property', 'comment', 89, 'en', 'This property links an instance of E70 Thing to an E55 Type of usage.
It allows the relationship between particular things, both physical and immaterial, and general methods and techniques of use to be documented. Thus it can be asserted that a baseball bat had a general use for sport and a specific use for threatening people during the Great Train Robbery.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1927, 'property', 'name', 90, 'en', 'has title', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1928, 'property', 'name', 90, 'ru', 'имеет заголовок', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1929, 'property', 'name', 90, 'de', 'trägt den Titel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1930, 'property', 'name', 90, 'fr', 'a pour titre', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1931, 'property', 'name', 90, 'el', 'έχει τίτλο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1932, 'property', 'name', 90, 'pt', 'tem título', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1933, 'property', 'name', 90, 'cn', '有标题', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1934, 'property', 'name_inverse', 90, 'en', 'is title of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1935, 'property', 'name_inverse', 90, 'de', 'ist der Titel von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1936, 'property', 'name_inverse', 90, 'el', 'είναι τίτλος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1937, 'property', 'name_inverse', 90, 'fr', 'est le titre de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1938, 'property', 'name_inverse', 90, 'ru', 'является заголовком для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1939, 'property', 'name_inverse', 90, 'pt', 'é título de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1940, 'property', 'name_inverse', 90, 'cn', '被用为标题来称呼', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1941, 'property', 'comment', 90, 'en', 'This property describes the E35 Title applied to an instance of E71 Man-Made Thing. The E55 Type of Title is assigned in a sub property.
The P102.1 has type property of the P102 has title (is title of) property enables the relationship between the Title and the thing to be further clarified, for example, if the Title was a given Title, a supplied Title etc.
It allows any man-made material or immaterial thing to be given a Title. It is possible to imagine a Title being created without a specific object in mind.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1942, 'property', 'name', 91, 'fr', 'était destiné à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1943, 'property', 'name', 91, 'en', 'was intended for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1944, 'property', 'name', 91, 'de', 'bestimmt für', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1945, 'property', 'name', 91, 'ru', 'был задуман для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1946, 'property', 'name', 91, 'el', 'προοριζόταν για', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1947, 'property', 'name', 91, 'pt', 'era destinado à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1948, 'property', 'name', 91, 'cn', '被制作来用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1949, 'property', 'name_inverse', 91, 'de', 'war Bestimmung von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1950, 'property', 'name_inverse', 91, 'en', 'was intention of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1951, 'property', 'name_inverse', 91, 'ru', 'был интенцией для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1952, 'property', 'name_inverse', 91, 'el', 'ήταν προορισμός του', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1953, 'property', 'name_inverse', 91, 'fr', 'était la raison d''être de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1954, 'property', 'name_inverse', 91, 'pt', 'era a destinação de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1955, 'property', 'comment', 91, 'en', 'This property links an instance of E71 Man-Made Thing to an E55 Type of usage.
It creates a property between specific man-made things, both physical and immaterial, to Types of intended methods and techniques of use. Note: A link between specific man-made things and a specific use activity should be expressed using P19 was intended use of (was made for).', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1956, 'property', 'name', 92, 'fr', 'est sujet à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1957, 'property', 'name', 92, 'en', 'is subject to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1958, 'property', 'name', 92, 'ru', 'является объектом для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1959, 'property', 'name', 92, 'el', 'υπόκειται σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1960, 'property', 'name', 92, 'de', 'Gegenstand von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1961, 'property', 'name', 92, 'pt', 'está sujeito à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1962, 'property', 'name', 92, 'cn', '受制於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1963, 'property', 'name_inverse', 92, 'el', 'ισχύει για', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1964, 'property', 'name_inverse', 92, 'fr', 's’applique à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1965, 'property', 'name_inverse', 92, 'de', 'findet Anwendung auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1966, 'property', 'name_inverse', 92, 'ru', 'применяется к', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1967, 'property', 'name_inverse', 92, 'en', 'applies to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1968, 'property', 'name_inverse', 92, 'pt', 'se aplicam à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1969, 'property', 'name_inverse', 92, 'cn', '被应用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1970, 'property', 'comment', 92, 'en', 'This property links a particular E72 Legal Object to the instances of E30 Right to which it is subject.
The Right is held by an E39 Actor as described by P75 possesses (is possessed by).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1971, 'property', 'name', 93, 'ru', 'право принадлежит', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1972, 'property', 'name', 93, 'fr', 'droit détenu par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1973, 'property', 'name', 93, 'de', 'Rechte stehen zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1974, 'property', 'name', 93, 'el', 'δικαίωμα κατέχεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1975, 'property', 'name', 93, 'en', 'right held by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1976, 'property', 'name', 93, 'pt', 'são direitos de ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1977, 'property', 'name', 93, 'cn', '有权限持有者', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1978, 'property', 'name_inverse', 93, 'de', 'hat Rechte an', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1979, 'property', 'name_inverse', 93, 'ru', 'владеет правом на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1980, 'property', 'name_inverse', 93, 'en', 'has right on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1981, 'property', 'name_inverse', 93, 'fr', 'détient un droit sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1982, 'property', 'name_inverse', 93, 'el', 'έχει δικαίωμα σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1983, 'property', 'name_inverse', 93, 'pt', 'possui direitos sobre', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1984, 'property', 'name_inverse', 93, 'cn', '持有权限来管制', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1985, 'property', 'comment', 93, 'en', 'This property identifies the E39 Actor who holds the instances of E30 Right to an E72 Legal Object.
	It is a superproperty of P52 has current owner (is current owner of) because ownership is a right that is held on the owned object.
P105 right held by (has right on) is a shortcut of the fully developed path from E72 Legal Object through P104 is subject to (applies to), E30 Right, P75 possesses (is possessed by) to E39 Actor.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1986, 'property', 'name', 94, 'de', ' ist zusammengesetzt aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1987, 'property', 'name', 94, 'ru', 'составлен из', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1988, 'property', 'name', 94, 'en', 'is composed of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1989, 'property', 'name', 94, 'fr', 'est composé de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1990, 'property', 'name', 94, 'el', 'αποτελείται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1991, 'property', 'name', 94, 'pt', 'é composto de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1992, 'property', 'name', 94, 'cn', '有组成元素', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1993, 'property', 'name_inverse', 94, 'ru', 'формирует часть', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1994, 'property', 'name_inverse', 94, 'el', 'αποτελεί μέρος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1995, 'property', 'name_inverse', 94, 'de', 'bildet Teil von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1996, 'property', 'name_inverse', 94, 'fr', 'fait partie de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1997, 'property', 'name_inverse', 94, 'en', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1998, 'property', 'name_inverse', 94, 'pt', 'faz parte de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (1999, 'property', 'name_inverse', 94, 'cn', '组成了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2000, 'property', 'comment', 94, 'en', 'This property associates an instance of E90 Symbolic Object with a part of it that is by itself an instance of E90 Symbolic Object, such as fragments of texts or clippings from an image.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2001, 'property', 'name', 95, 'fr', 'a pour membre actuel ou ancien', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2002, 'property', 'name', 95, 'en', 'has current or former member', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2003, 'property', 'name', 95, 'el', 'έχει ή είχε μέλος', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2004, 'property', 'name', 95, 'ru', 'имеет действующего или бывшего члена', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2005, 'property', 'name', 95, 'de', 'hat derzeitiges oder früheres Mitglied', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2006, 'property', 'name', 95, 'pt', 'tem ou teve membro', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2007, 'property', 'name', 95, 'cn', '有现任或前任成员', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2008, 'property', 'name_inverse', 95, 'el', 'είναι ή ήταν μέλος του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2009, 'property', 'name_inverse', 95, 'en', 'is current or former member of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2010, 'property', 'name_inverse', 95, 'de', 'ist derzeitiges oder früheres Mitglied von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2011, 'property', 'name_inverse', 95, 'ru', 'является действующим или бывшим членом', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2012, 'property', 'name_inverse', 95, 'fr', 'est actuel ou ancien membre de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2013, 'property', 'name_inverse', 95, 'pt', 'é ou foi membro de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2014, 'property', 'name_inverse', 95, 'cn', '目前或曾经加入群组', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2015, 'property', 'comment', 95, 'en', 'This property relates an E39 Actor to the E74 Group of which that E39 Actor is a member.
Groups, Legal Bodies and Persons, may all be members of Groups. A Group necessarily consists of more than one member.
This property is a shortcut of the more fully developed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor
The property P107.1 kind of member can be used to specify the type of membership or the role the member has in the group.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2016, 'property', 'name', 96, 'el', 'παρήγαγε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2017, 'property', 'name', 96, 'fr', 'a produit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2018, 'property', 'name', 96, 'ru', 'произвел', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2019, 'property', 'name', 96, 'de', 'hat hergestellt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2020, 'property', 'name', 96, 'en', 'has produced', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2021, 'property', 'name', 96, 'pt', 'produziu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2022, 'property', 'name', 96, 'cn', '有产出物', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2023, 'property', 'name_inverse', 96, 'el', 'παρήχθη από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2024, 'property', 'name_inverse', 96, 'fr', 'a été produit par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2025, 'property', 'name_inverse', 96, 'de', 'wurde hergestellt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2026, 'property', 'name_inverse', 96, 'ru', 'был произведен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2027, 'property', 'name_inverse', 96, 'en', 'was produced by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2028, 'property', 'name_inverse', 96, 'pt', 'foi produzido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2029, 'property', 'name_inverse', 96, 'cn', '被制作於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2030, 'property', 'comment', 96, 'en', 'This property identifies the E24 Physical Man-Made Thing that came into existence as a result of an E12 Production.
The identity of an instance of E24 Physical Man-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Man-Made Thing.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2031, 'property', 'name', 97, 'fr', 'a pour conservateur actuel ou ancien', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2032, 'property', 'name', 97, 'de', 'hat derzeitigen oder früheren Kurator', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2033, 'property', 'name', 97, 'en', 'has current or former curator', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2034, 'property', 'name', 97, 'el', 'έχει ή είχε επιμελητή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2111, 'property', 'name', 102, 'pt', 'é temporalmente igual a', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2035, 'property', 'name', 97, 'ru', 'имеет действующего или бывшего хранителя', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2036, 'property', 'name', 97, 'pt', 'tem ou teve curador', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2037, 'property', 'name', 97, 'cn', '有现任或前任典藏管理员', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2038, 'property', 'name_inverse', 97, 'ru', 'является действующим или бывшим хранителем', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2039, 'property', 'name_inverse', 97, 'el', 'είναι ή ήταν επιμελητής του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2040, 'property', 'name_inverse', 97, 'fr', 'est ou a été le conservateur de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2041, 'property', 'name_inverse', 97, 'de', 'ist derzeitiger oder früherer Kurator von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2042, 'property', 'name_inverse', 97, 'en', 'is current or former curator of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2043, 'property', 'name_inverse', 97, 'pt', 'é ou foi curador de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2044, 'property', 'name_inverse', 97, 'cn', '目前或曾经典藏管理', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2045, 'property', 'comment', 97, 'en', 'This property identifies the E39 Actor or Actors who assume or have assumed overall curatorial responsibility for an E78 Collection.
This property is effectively a short-cut. It does not allow a history of curation to be recorded. This would require use of an Event assigning responsibility for a Collection to a curator.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2046, 'property', 'name', 98, 'ru', 'увеличил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2047, 'property', 'name', 98, 'fr', 'a augmenté', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2048, 'property', 'name', 98, 'de', 'erweiterte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2049, 'property', 'name', 98, 'el', 'επαύξησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2050, 'property', 'name', 98, 'en', 'augmented', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2051, 'property', 'name', 98, 'pt', 'aumentou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2052, 'property', 'name', 98, 'cn', '扩增了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2053, 'property', 'name_inverse', 98, 'fr', 'a été augmenté par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2054, 'property', 'name_inverse', 98, 'en', 'was augmented by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2055, 'property', 'name_inverse', 98, 'ru', 'был увеличен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2056, 'property', 'name_inverse', 98, 'el', 'επαυξήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2057, 'property', 'name_inverse', 98, 'de', 'wurde erweitert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2058, 'property', 'name_inverse', 98, 'pt', 'foi aumentada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2059, 'property', 'name_inverse', 98, 'cn', '被扩增於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2060, 'property', 'comment', 98, 'en', 'This property identifies the E24 Physical Man-Made Thing that is added to (augmented) in an E79 Part Addition.
Although a Part Addition event normally concerns only one item of Physical Man-Made Thing, it is possible to imagine circumstances under which more than one item might be added to (augmented). For example, the artist Jackson Pollock trailing paint onto multiple canvasses.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2061, 'property', 'name', 99, 'de', 'fügte hinzu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2062, 'property', 'name', 99, 'el', 'προσέθεσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2063, 'property', 'name', 99, 'fr', 'a ajouté', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2064, 'property', 'name', 99, 'en', 'added', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2065, 'property', 'name', 99, 'ru', 'добавил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2066, 'property', 'name', 99, 'pt', 'adicionou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2067, 'property', 'name', 99, 'cn', '附加上部件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2068, 'property', 'name_inverse', 99, 'fr', 'a été ajouté par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2069, 'property', 'name_inverse', 99, 'de', 'wurde hinzugefügt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2070, 'property', 'name_inverse', 99, 'en', 'was added by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2071, 'property', 'name_inverse', 99, 'el', 'προστέθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2072, 'property', 'name_inverse', 99, 'ru', 'был добавлен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2073, 'property', 'name_inverse', 99, 'pt', 'foi adicionado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2074, 'property', 'name_inverse', 99, 'cn', '被附加於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2075, 'property', 'comment', 99, 'en', 'This property identifies the E18 Physical Thing that is added during an E79 Part Addition activity
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2076, 'property', 'name', 100, 'ru', 'уменьшил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2077, 'property', 'name', 100, 'en', 'diminished', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2078, 'property', 'name', 100, 'de', 'verminderte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2079, 'property', 'name', 100, 'fr', 'a diminué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2080, 'property', 'name', 100, 'el', 'εξάλειψε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2081, 'property', 'name', 100, 'pt', 'diminuiu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2082, 'property', 'name', 100, 'cn', '缩减了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2083, 'property', 'name_inverse', 100, 'en', 'was diminished by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2084, 'property', 'name_inverse', 100, 'el', 'εξαλείφθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2085, 'property', 'name_inverse', 100, 'fr', 'a été diminué par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2086, 'property', 'name_inverse', 100, 'ru', 'был уменьшен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2087, 'property', 'name_inverse', 100, 'de', 'wurde vermindert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2088, 'property', 'name_inverse', 100, 'pt', 'foi diminuído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2089, 'property', 'name_inverse', 100, 'cn', '被缩减於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2090, 'property', 'comment', 100, 'en', 'This property identifies the E24 Physical Man-Made Thing that was diminished by E80 Part Removal.
Although a Part removal activity normally concerns only one item of Physical Man-Made Thing, it is possible to imagine circumstances under which more than one item might be diminished by a single Part Removal activity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2091, 'property', 'name', 101, 'ru', 'удален', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2092, 'property', 'name', 101, 'de', 'entfernte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2093, 'property', 'name', 101, 'en', 'removed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2094, 'property', 'name', 101, 'el', 'αφαίρεσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2095, 'property', 'name', 101, 'fr', 'a enlevé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2096, 'property', 'name', 101, 'pt', 'removeu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2097, 'property', 'name', 101, 'cn', '移除了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2098, 'property', 'name_inverse', 101, 'el', 'αφαιρέθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2099, 'property', 'name_inverse', 101, 'de', 'wurde entfernt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2100, 'property', 'name_inverse', 101, 'en', 'was removed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2101, 'property', 'name_inverse', 101, 'fr', 'a été enlevée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2102, 'property', 'name_inverse', 101, 'ru', 'был удален посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2103, 'property', 'name_inverse', 101, 'pt', 'foi removido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2104, 'property', 'name_inverse', 101, 'cn', '被移除於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2105, 'property', 'comment', 101, 'en', 'This property identifies the E18 Physical Thing that is removed during an E80 Part Removal activity.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2106, 'property', 'name', 102, 'fr', 'est temporellement égale à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2107, 'property', 'name', 102, 'de', 'zeitgleich zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2108, 'property', 'name', 102, 'el', 'συμπίπτει χρονικά με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2109, 'property', 'name', 102, 'ru', 'равен по времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2110, 'property', 'name', 102, 'en', 'is equal in time to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2112, 'property', 'name', 102, 'cn', '时段相同於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2113, 'property', 'comment', 102, 'en', 'This symmetric property allows the instances of E2 Temporal Entity with the same E52 Time-Span to be equated.
This property is only necessary if the time span is unknown (otherwise the equivalence can be calculated).
This property is the same as the "equal" relationship of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2114, 'property', 'name', 103, 'en', 'finishes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2115, 'property', 'name', 103, 'ru', 'заканчивает', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2116, 'property', 'name', 103, 'de', 'beendet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2117, 'property', 'name', 103, 'fr', 'termine', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2118, 'property', 'name', 103, 'el', 'περατώνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2119, 'property', 'name', 103, 'pt', 'finaliza', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2120, 'property', 'name', 103, 'cn', '结束了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2121, 'property', 'name_inverse', 103, 'fr', 'est terminée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2122, 'property', 'name_inverse', 103, 'ru', 'заканчивается', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2123, 'property', 'name_inverse', 103, 'el', 'περατώνεται με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2124, 'property', 'name_inverse', 103, 'de', 'wurde beendet mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2125, 'property', 'name_inverse', 103, 'en', 'is finished by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2126, 'property', 'name_inverse', 103, 'pt', 'é finalizada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2127, 'property', 'name_inverse', 103, 'cn', '被结束于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2128, 'property', 'comment', 103, 'en', 'This property allows the ending point for a E2 Temporal Entity to be situated by reference to the ending point of another temporal entity of longer duration.
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "finishes / finished-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2129, 'property', 'name', 104, 'fr', 'commence', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2130, 'property', 'name', 104, 'en', 'starts', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2131, 'property', 'name', 104, 'ru', 'начинает', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2132, 'property', 'name', 104, 'de', 'beginnt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2133, 'property', 'name', 104, 'el', 'αρχίζει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2134, 'property', 'name', 104, 'pt', 'inicia', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2135, 'property', 'name', 104, 'cn', '开始了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2136, 'property', 'name_inverse', 104, 'fr', 'est commencée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2137, 'property', 'name_inverse', 104, 'de', 'wurde begonnen mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2138, 'property', 'name_inverse', 104, 'el', 'αρχίζει με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2139, 'property', 'name_inverse', 104, 'ru', 'начинается', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2140, 'property', 'name_inverse', 104, 'en', 'is started by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2141, 'property', 'name_inverse', 104, 'pt', 'é iniciada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2142, 'property', 'name_inverse', 104, 'cn', '被开始于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2143, 'property', 'comment', 104, 'en', 'This property allows the starting point for a E2 Temporal Entity to be situated by reference to the starting point of another temporal entity of longer duration.
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "starts / started-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2144, 'property', 'name', 105, 'de', 'fällt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2145, 'property', 'name', 105, 'el', 'εμφανίζεται κατά τη διάρκεια', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2146, 'property', 'name', 105, 'ru', 'появляется во течение', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2147, 'property', 'name', 105, 'en', 'occurs during', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2148, 'property', 'name', 105, 'fr', 'a lieu pendant', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2149, 'property', 'name', 105, 'pt', 'ocorre durante', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2150, 'property', 'name', 105, 'cn', '时段被涵盖於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2151, 'property', 'name_inverse', 105, 'el', 'περιλαμβάνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2152, 'property', 'name_inverse', 105, 'ru', 'включает', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2153, 'property', 'name_inverse', 105, 'fr', 'comporte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2154, 'property', 'name_inverse', 105, 'en', 'includes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2155, 'property', 'name_inverse', 105, 'de', 'beinhaltet', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2156, 'property', 'name_inverse', 105, 'pt', 'inclui', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2157, 'property', 'name_inverse', 105, 'cn', '时段涵盖了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2158, 'property', 'comment', 105, 'en', 'This property allows the entire E52 Time-Span of an E2 Temporal Entity to be situated within the Time-Span of another temporal entity that starts before and ends after the included temporal entity.
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "during / includes" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2159, 'property', 'name', 106, 'en', 'overlaps in time with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2160, 'property', 'name', 106, 'ru', 'перекрывает во времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2161, 'property', 'name', 106, 'el', 'προηγείται μερικώς επικαλύπτοντας', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2162, 'property', 'name', 106, 'de', 'überlappt zeitlich mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2163, 'property', 'name', 106, 'fr', 'est partiellement recouverte dans le temps par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2164, 'property', 'name', 106, 'pt', 'sobrepõe temporalmente', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2165, 'property', 'name', 106, 'cn', '时段重叠了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2166, 'property', 'name_inverse', 106, 'de', 'wird zeitlich überlappt von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2167, 'property', 'name_inverse', 106, 'ru', 'перекрывается во времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2168, 'property', 'name_inverse', 106, 'fr', 'recouvre partiellement dans le temps', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2169, 'property', 'name_inverse', 106, 'en', 'is overlapped in time by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2170, 'property', 'name_inverse', 106, 'el', 'έπεται μερικώς επικαλυπτόμενο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2171, 'property', 'name_inverse', 106, 'pt', 'é sobreposto temporalmente por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2172, 'property', 'name_inverse', 106, 'cn', '时段被重叠于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2173, 'property', 'comment', 106, 'en', 'This property identifies an overlap between the instances of E52 Time-Span of two instances of E2 Temporal Entity.
It implies a temporal order between the two entities: if A overlaps in time B, then A must start before B, and B must end after A. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated).
This property is the same as the "overlaps / overlapped-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2174, 'property', 'name', 107, 'en', 'meets in time with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2175, 'property', 'name', 107, 'el', 'προηγείται', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2176, 'property', 'name', 107, 'de', 'trifft zeitlich auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2177, 'property', 'name', 107, 'ru', 'следует во времени за', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2178, 'property', 'name', 107, 'fr', 'est temporellement contiguë avec', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2179, 'property', 'name', 107, 'pt', 'é temporalmente contíguo com', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2180, 'property', 'name', 107, 'cn', '紧接续了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2181, 'property', 'name_inverse', 107, 'fr', 'est immédiatement précédé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2182, 'property', 'name_inverse', 107, 'el', 'έπεται', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2183, 'property', 'name_inverse', 107, 'en', 'is met in time by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2184, 'property', 'name_inverse', 107, 'de', 'wird zeitlich getroffen von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2185, 'property', 'name_inverse', 107, 'ru', 'предшествует во времени', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2186, 'property', 'name_inverse', 107, 'pt', 'é imediatamente precedido por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2187, 'property', 'name_inverse', 107, 'cn', '紧接续於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2188, 'property', 'comment', 107, 'en', 'This property indicates that one E2 Temporal Entity immediately follows another.
It implies a particular order between the two entities: if A meets in time with B, then A must precede B. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated).
This property is the same as the "meets / met-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2189, 'property', 'name', 108, 'ru', 'появляется до', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2190, 'property', 'name', 108, 'fr', 'a lieu avant', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2191, 'property', 'name', 108, 'el', 'εμφανίζεται πριν', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2192, 'property', 'name', 108, 'en', 'occurs before', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2193, 'property', 'name', 108, 'de', 'kommt vor', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2194, 'property', 'name', 108, 'pt', 'ocorre antes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2195, 'property', 'name', 108, 'cn', '发生时段先於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2196, 'property', 'name_inverse', 108, 'fr', 'a lieu après', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2197, 'property', 'name_inverse', 108, 'el', 'εμφανίζεται μετά', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2198, 'property', 'name_inverse', 108, 'ru', 'появляется после', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2199, 'property', 'name_inverse', 108, 'de', 'kommt nach', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2200, 'property', 'name_inverse', 108, 'en', 'occurs after', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2201, 'property', 'name_inverse', 108, 'pt', 'ocorre depois', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2202, 'property', 'name_inverse', 108, 'cn', '发生时段后於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2203, 'property', 'comment', 108, 'en', 'This property identifies the relative chronological sequence of two temporal entities.
It implies that a temporal gap exists between the end of A and the start of B. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated).
This property is the same as the "before / after" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2204, 'property', 'name', 109, 'el', 'επικαλύπτεται με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2205, 'property', 'name', 109, 'de', 'überlappt mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2206, 'property', 'name', 109, 'fr', 'chevauche', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2207, 'property', 'name', 109, 'ru', 'пересекается с', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2208, 'property', 'name', 109, 'en', 'overlaps with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2209, 'property', 'name', 109, 'pt', 'sobrepõe com', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2210, 'property', 'name', 109, 'cn', '空间重叠于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2211, 'property', 'comment', 109, 'en', 'This symmetric property allows the instances of E53 Place with overlapping geometric extents to be associated with each other.
It does not specify anything about the shared area. This property is purely spatial, in contrast to Allen operators, which are purely temporal.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2212, 'property', 'name', 110, 'ru', 'граничит с', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2213, 'property', 'name', 110, 'en', 'borders with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2214, 'property', 'name', 110, 'fr', 'jouxte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2215, 'property', 'name', 110, 'de', 'grenzt an', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2216, 'property', 'name', 110, 'el', 'συνορεύει με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2217, 'property', 'name', 110, 'pt', 'fronteira com', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2218, 'property', 'name', 110, 'cn', '接壤于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2219, 'property', 'comment', 110, 'en', 'This symmetric property allows the instances of E53 Place which share common borders to be related as such.
This property is purely spatial, in contrast to Allen operators, which are purely temporal.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2220, 'property', 'name', 111, 'fr', 'a eu pour résultat', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2221, 'property', 'name', 111, 'de', 'ergab', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2222, 'property', 'name', 111, 'el', 'είχε ως αποτέλεσμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2223, 'property', 'name', 111, 'ru', 'повлек появление', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2224, 'property', 'name', 111, 'en', 'resulted in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2225, 'property', 'name', 111, 'pt', 'resultou em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2226, 'property', 'name', 111, 'cn', '转变出', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2227, 'property', 'name_inverse', 111, 'fr', 'est le résultat de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2228, 'property', 'name_inverse', 111, 'el', 'προέκυψε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2229, 'property', 'name_inverse', 111, 'ru', 'был результатом', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2230, 'property', 'name_inverse', 111, 'de', 'ergab sich aus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2231, 'property', 'name_inverse', 111, 'en', 'resulted from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2232, 'property', 'name_inverse', 111, 'pt', 'resultado de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2233, 'property', 'name_inverse', 111, 'cn', '肇因於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2234, 'property', 'comment', 111, 'en', 'This property identifies the E77 Persistent Item or items that are the result of an E81 Transformation.
New items replace the transformed item or items, which cease to exist as units of documentation. The physical continuity between the old and the new is expressed by the link to the common Transformation.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2235, 'property', 'name', 112, 'en', 'transformed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2236, 'property', 'name', 112, 'de', 'wandelte um', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2237, 'property', 'name', 112, 'el', 'μετέτρεψε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2238, 'property', 'name', 112, 'ru', 'трансформировал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2239, 'property', 'name', 112, 'fr', 'a transformé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2240, 'property', 'name', 112, 'pt', 'transformou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2241, 'property', 'name', 112, 'cn', '转变了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2242, 'property', 'name_inverse', 112, 'fr', 'a été transformé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2243, 'property', 'name_inverse', 112, 'ru', 'был трансформирован посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2244, 'property', 'name_inverse', 112, 'el', 'μετατράπηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2245, 'property', 'name_inverse', 112, 'en', 'was transformed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2246, 'property', 'name_inverse', 112, 'de', 'wurde umgewandelt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2247, 'property', 'name_inverse', 112, 'pt', 'foi transformado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2248, 'property', 'name_inverse', 112, 'cn', '被转变於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2323, 'property', 'comment', 117, 'en', 'This property documents that an E89 Propositional Object has as subject an instance of E1 CRM Entity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2324, 'property', 'name', 118, 'el', 'παρουσιάζει χαρακτηριστικά του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2249, 'property', 'comment', 112, 'en', 'This property identifies the E77 Persistent Item or items that cease to exist due to a E81 Transformation.
It is replaced by the result of the Transformation, which becomes a new unit of documentation. The continuity between both items, the new and the old, is expressed by the link to the common Transformation.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2250, 'property', 'name', 113, 'en', 'used object of type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2251, 'property', 'name', 113, 'fr', 'a employé un objet du type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2252, 'property', 'name', 113, 'ru', 'использовал объект типа', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2253, 'property', 'name', 113, 'de', 'benutzte Objekt des Typus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2254, 'property', 'name', 113, 'el', 'χρησιμοποίησε αντικείμενο τύπου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2255, 'property', 'name', 113, 'pt', 'usou objeto do tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2256, 'property', 'name', 113, 'cn', '有使用物件类型', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2257, 'property', 'name_inverse', 113, 'ru', 'был типом объекта использованного в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2258, 'property', 'name_inverse', 113, 'en', 'was type of object used in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2259, 'property', 'name_inverse', 113, 'de', 'Objekt des Typus ... wurde benutzt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2260, 'property', 'name_inverse', 113, 'fr', 'était le type d’objet employé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2261, 'property', 'name_inverse', 113, 'el', 'ήταν o τύπος αντικείμενου που χρησιμοποιήθηκε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2262, 'property', 'name_inverse', 113, 'pt', 'foi tipo do objeto usado em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2263, 'property', 'name_inverse', 113, 'cn', '被使用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2264, 'property', 'comment', 113, 'en', 'This property defines the kind of objects used in an E7 Activity, when the specific instance is either unknown or not of interest, such as use of "a hammer".
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2265, 'property', 'name', 114, 'fr', 'a employé', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2266, 'property', 'name', 114, 'de', 'verwendete', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2267, 'property', 'name', 114, 'en', 'employed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2268, 'property', 'name', 114, 'ru', 'использовал', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2269, 'property', 'name', 114, 'el', 'χρησιμοποίησε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2270, 'property', 'name', 114, 'pt', 'empregou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2271, 'property', 'name', 114, 'cn', '采用了材料', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2272, 'property', 'name_inverse', 114, 'en', 'was employed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2273, 'property', 'name_inverse', 114, 'de', 'wurde verwendet bei', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2274, 'property', 'name_inverse', 114, 'ru', 'использовался в', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2275, 'property', 'name_inverse', 114, 'el', 'χρησιμοποιήθηκε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2276, 'property', 'name_inverse', 114, 'fr', 'a été employé dans', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2277, 'property', 'name_inverse', 114, 'pt', 'foi empregado em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2278, 'property', 'name_inverse', 114, 'cn', '被使用於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2279, 'property', 'comment', 114, 'en', 'This property identifies E57 Material employed in an E11 Modification.
The E57 Material used during the E11 Modification does not necessarily become incorporated into the E24 Physical Man-Made Thing that forms the subject of the E11 Modification.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2280, 'property', 'name', 115, 'el', 'έχει ευρύτερο όρο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2281, 'property', 'name', 115, 'fr', 'a pour terme générique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2282, 'property', 'name', 115, 'de', 'hat den Oberbegriff', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2283, 'property', 'name', 115, 'en', 'has broader term', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2284, 'property', 'name', 115, 'ru', 'имеет вышестоящий термин', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2285, 'property', 'name', 115, 'pt', 'tem termo genérico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2286, 'property', 'name', 115, 'cn', '有广义术语', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2287, 'property', 'name_inverse', 115, 'fr', 'a pour terme spécifique', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2288, 'property', 'name_inverse', 115, 'de', 'hat den Unterbegriff', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2289, 'property', 'name_inverse', 115, 'en', 'has narrower term', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2290, 'property', 'name_inverse', 115, 'el', 'έχει στενότερο όρο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2291, 'property', 'name_inverse', 115, 'pt', 'tem termo específico', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2292, 'property', 'name_inverse', 115, 'cn', '有狭义术语', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2293, 'property', 'comment', 115, 'en', 'This property identifies a super-Type to which an E55 Type is related.
		It allows Types to be organised into hierarchies. This is the sense of "broader term generic  		(BTG)" as defined in ISO 2788
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2294, 'property', 'name', 116, 'en', 'carries', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2295, 'property', 'name', 116, 'fr', 'est le support de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2296, 'property', 'name', 116, 'ru', 'несет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2297, 'property', 'name', 116, 'el', 'φέρει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2298, 'property', 'name', 116, 'de', 'trägt', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2299, 'property', 'name', 116, 'pt', 'é o suporte de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2300, 'property', 'name', 116, 'cn', '承载信息', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2301, 'property', 'name_inverse', 116, 'el', 'φέρεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2302, 'property', 'name_inverse', 116, 'en', 'is carried by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2303, 'property', 'name_inverse', 116, 'ru', 'переносится посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2304, 'property', 'name_inverse', 116, 'fr', 'a pour support', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2305, 'property', 'name_inverse', 116, 'de', 'wird getragen von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2306, 'property', 'name_inverse', 116, 'pt', 'é suportado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2307, 'property', 'name_inverse', 116, 'cn', '被承载于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2308, 'property', 'comment', 116, 'en', 'This property identifies an E90 Symbolic Object carried by an instance of E24 Physical Man-Made Thing.
In general this would be an E84 Information Carrier P65 shows visual item (is shown by) is a specialisation of P128 carries (is carried by) which should be used for carrying visual items.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2309, 'property', 'name', 117, 'fr', 'est au sujet de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2310, 'property', 'name', 117, 'en', 'is about', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2311, 'property', 'name', 117, 'ru', 'касается', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2312, 'property', 'name', 117, 'el', 'έχει ως θέμα', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2313, 'property', 'name', 117, 'de', 'handelt über', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2314, 'property', 'name', 117, 'pt', 'é sobre', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2315, 'property', 'name', 117, 'cn', '陈述关於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2316, 'property', 'name_inverse', 117, 'fr', 'est le sujet de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2317, 'property', 'name_inverse', 117, 'de', 'wird behandelt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2318, 'property', 'name_inverse', 117, 'ru', 'является предметом для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2319, 'property', 'name_inverse', 117, 'el', 'είναι θέμα  του/της', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2320, 'property', 'name_inverse', 117, 'en', 'is subject of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2321, 'property', 'name_inverse', 117, 'pt', 'é assunto de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2322, 'property', 'name_inverse', 117, 'cn', '被陈述於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2325, 'property', 'name', 118, 'en', 'shows features of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2326, 'property', 'name', 118, 'ru', 'демонстрирует признаки', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2327, 'property', 'name', 118, 'fr', 'présente des caractéristiques de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2328, 'property', 'name', 118, 'de', 'zeigt Merkmale von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2329, 'property', 'name', 118, 'pt', 'apresenta características de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2330, 'property', 'name', 118, 'cn', '外观特征原出现於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2331, 'property', 'name_inverse', 118, 'el', 'χαρακτηριστικά του βρίσκονται επίσης σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2332, 'property', 'name_inverse', 118, 'fr', 'a des caractéristiques se trouvant aussi sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2333, 'property', 'name_inverse', 118, 'de', 'Merkmale auch auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2334, 'property', 'name_inverse', 118, 'ru', 'признаки также найдены на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2335, 'property', 'name_inverse', 118, 'en', 'features are also found on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2336, 'property', 'name_inverse', 118, 'pt', 'características são também encontradas em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2337, 'property', 'name_inverse', 118, 'cn', '外观特征被复制於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2338, 'property', 'comment', 118, 'en', 'This property generalises the notions of  "copy of" and "similar to" into a dynamic, asymmetric relationship, where the domain expresses the derivative, if such a direction can be established.
Otherwise, the relationship is symmetric. It is a short-cut of P15 was influenced by (influenced) in a creation or production, if such a reason for the similarity can be verified. Moreover it expresses similarity in cases that can be stated between two objects only, without historical knowledge about its reasons.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2339, 'property', 'name', 119, 'el', 'αναγνωρίζεται ως', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2340, 'property', 'name', 119, 'de', 'wird identifziert durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2341, 'property', 'name', 119, 'en', 'is identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2342, 'property', 'name', 119, 'fr', 'est identifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2343, 'property', 'name', 119, 'ru', 'идентифицируется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2344, 'property', 'name', 119, 'pt', 'é identificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2345, 'property', 'name', 119, 'cn', '有称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2346, 'property', 'name_inverse', 119, 'fr', 'identifie', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2347, 'property', 'name_inverse', 119, 'en', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2348, 'property', 'name_inverse', 119, 'el', 'είναι αναγνωριστικό', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2349, 'property', 'name_inverse', 119, 'ru', 'идентифицирует', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2350, 'property', 'name_inverse', 119, 'de', 'identifiziert', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2351, 'property', 'name_inverse', 119, 'pt', 'identifica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2352, 'property', 'name_inverse', 119, 'cn', '被用来识别', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2353, 'property', 'comment', 119, 'en', 'This property identifies a name used specifically to identify an E39 Actor.
This property is a specialisation of P1 is identified by (identifies) is identified by.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2354, 'property', 'name', 120, 'el', 'επικαλύπτεται με', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2355, 'property', 'name', 120, 'de', 'überlappt mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2356, 'property', 'name', 120, 'fr', 'chevauche', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2357, 'property', 'name', 120, 'ru', 'пересекается с', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2358, 'property', 'name', 120, 'en', 'overlaps with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2359, 'property', 'name', 120, 'pt', 'sobrepõe', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2360, 'property', 'name', 120, 'cn', '时空重叠于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2361, 'property', 'comment', 120, 'en', 'This symmetric property allows instances of E4 Period that overlap both temporally and spatially to be related, i,e. they share some spatio-temporal extent.
This property does not imply any ordering or sequence between the two periods, either spatial or temporal.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2362, 'property', 'name', 121, 'de', 'getrennt von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2363, 'property', 'name', 121, 'en', 'is separated from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2364, 'property', 'name', 121, 'el', 'διαχωρίζεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2365, 'property', 'name', 121, 'fr', 'est séparée de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2366, 'property', 'name', 121, 'ru', 'отделен от', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2367, 'property', 'name', 121, 'pt', 'é separado de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2368, 'property', 'name', 121, 'cn', '时空不重叠于', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2369, 'property', 'comment', 121, 'en', 'This symmetric property allows instances of E4 Period that do not overlap both temporally and spatially, to be related i,e. they do not share any spatio-temporal extent.
This property does not imply any ordering or sequence between the two periods either spatial or temporal.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2370, 'property', 'name', 122, 'de', 'setzte sich fort in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2371, 'property', 'name', 122, 'el', 'συνέχισε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2372, 'property', 'name', 122, 'ru', 'продолжил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2373, 'property', 'name', 122, 'fr', 'est la suite de', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2374, 'property', 'name', 122, 'en', 'continued', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2375, 'property', 'name', 122, 'pt', 'continuou', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2376, 'property', 'name', 122, 'cn', '延续了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2377, 'property', 'name_inverse', 122, 'de', 'wurde fortgesetzt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2378, 'property', 'name_inverse', 122, 'ru', 'был продолжен', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2379, 'property', 'name_inverse', 122, 'fr', 'a été continuée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2380, 'property', 'name_inverse', 122, 'en', 'was continued by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2381, 'property', 'name_inverse', 122, 'el', 'συνεχίστηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2382, 'property', 'name_inverse', 122, 'pt', 'foi continuada por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2383, 'property', 'name_inverse', 122, 'cn', '有延续活动', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2384, 'property', 'comment', 122, 'en', 'This property allows two activities to be related where the domain is considered as an intentional continuation of the range.
Used multiple times, this allows a chain of related activities to be created which follow each other in sequence.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2385, 'property', 'name', 123, 'en', 'created type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2386, 'property', 'name', 123, 'de', 'erschuf Typus', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2387, 'property', 'name', 123, 'el', 'δημιούργησε τύπο', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2388, 'property', 'name', 123, 'fr', 'a créé le type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2389, 'property', 'name', 123, 'ru', 'создал тип', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2390, 'property', 'name', 123, 'pt', 'criou tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2391, 'property', 'name', 123, 'cn', '创造了类型', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2392, 'property', 'name_inverse', 123, 'en', 'was created by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2393, 'property', 'name_inverse', 123, 'de', 'wurde geschaffen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2394, 'property', 'name_inverse', 123, 'fr', 'a été créé par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2395, 'property', 'name_inverse', 123, 'el', 'δημιουργήθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2396, 'property', 'name_inverse', 123, 'ru', 'был создан посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2397, 'property', 'name_inverse', 123, 'pt', 'foi criado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2398, 'property', 'name_inverse', 123, 'cn', '被创造於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2399, 'property', 'comment', 123, 'en', 'This property identifies the E55 Type, which is created in an E83Type Creation activity.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2400, 'property', 'name', 124, 'fr', 's’est fondée sur', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2401, 'property', 'name', 124, 'ru', 'был основан на', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2402, 'property', 'name', 124, 'de', 'stützte sich auf', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2403, 'property', 'name', 124, 'el', 'βασίστηκε σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2404, 'property', 'name', 124, 'en', 'was based on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2405, 'property', 'name', 124, 'pt', 'foi baseado em', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2406, 'property', 'name', 124, 'cn', '根据了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2407, 'property', 'name_inverse', 124, 'en', 'supported type creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2408, 'property', 'name_inverse', 124, 'el', 'υποστήριξε τη δημιουργία τύπου', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2409, 'property', 'name_inverse', 124, 'fr', 'a justifié la création de type', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2410, 'property', 'name_inverse', 124, 'de', 'belegte', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2411, 'property', 'name_inverse', 124, 'ru', 'поддержал создание типа', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2412, 'property', 'name_inverse', 124, 'pt', 'suportou a criação de tipo', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2413, 'property', 'name_inverse', 124, 'cn', '提供證據给类型创造', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2414, 'property', 'comment', 124, 'en', 'This property identifies one or more items that were used as evidence to declare a new E55 Type.
The examination of these items is often the only objective way to understand the precise characteristics of a new Type. Such items should be deposited in a museum or similar institution for that reason. The taxonomic role renders the specific relationship of each item to the Type, such as "holotype" or "original element".
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2415, 'property', 'name', 125, 'en', 'exemplifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2416, 'property', 'name', 125, 'fr', 'exemplifie', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2417, 'property', 'name', 125, 'el', 'δειγματίζει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2418, 'property', 'name', 125, 'ru', 'поясняет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2419, 'property', 'name', 125, 'de', 'erläutert', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2420, 'property', 'name', 125, 'pt', 'é exemplificado por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2421, 'property', 'name', 125, 'cn', '例示了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2422, 'property', 'name_inverse', 125, 'ru', 'поясняется посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2423, 'property', 'name_inverse', 125, 'de', 'erläutert durch Beispiel', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2424, 'property', 'name_inverse', 125, 'en', 'is exemplified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2425, 'property', 'name_inverse', 125, 'el', 'δειγματίζεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2426, 'property', 'name_inverse', 125, 'fr', 'est exemplifié par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2427, 'property', 'name_inverse', 125, 'pt', 'exemplifica', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2428, 'property', 'name_inverse', 125, 'cn', '有例示', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2429, 'property', 'comment', 125, 'en', 'This property allows an item to be declared as a particular example of an E55 Type or taxon
	The P137.1 in the taxonomic role property of P137 exemplifies (is exemplified by) allows differentiation of taxonomic roles. The taxonomic role renders the specific relationship of this example to the Type, such as "prototypical", "archetypical", "lectotype", etc. The taxonomic role "lectotype" is not associated with the Type Creation (E83) itself, but selected in a later phase.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2430, 'property', 'name', 126, 'el', 'παριστάνει', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2431, 'property', 'name', 126, 'en', 'represents', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2432, 'property', 'name', 126, 'ru', 'представляет', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2433, 'property', 'name', 126, 'de', 'stellt dar', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2434, 'property', 'name', 126, 'fr', 'représente', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2435, 'property', 'name', 126, 'pt', 'representa', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2436, 'property', 'name', 126, 'cn', '描绘了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2437, 'property', 'name_inverse', 126, 'en', 'has representation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2438, 'property', 'name_inverse', 126, 'ru', 'имеет представление', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2439, 'property', 'name_inverse', 126, 'fr', 'est représentée par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2440, 'property', 'name_inverse', 126, 'el', 'παριστάνεται από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2441, 'property', 'name_inverse', 126, 'de', 'wird dargestellt durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2442, 'property', 'name_inverse', 126, 'pt', 'tem representação', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2443, 'property', 'name_inverse', 126, 'cn', '有图像描绘', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2444, 'property', 'comment', 126, 'en', 'This property establishes the relationship between an E36 Visual Item and the entity that it visually represents.
Any entity may be represented visually. This property is part of the fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1 CRM Entity, which is shortcut by P62depicts (is depicted by). P138.1 mode of representation allows the nature of the representation to be refined.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2445, 'property', 'name', 127, 'fr', 'a pour autre forme', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2446, 'property', 'name', 127, 'ru', 'имеет альтернативную форму', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2447, 'property', 'name', 127, 'en', 'has alternative form', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2448, 'property', 'name', 127, 'de', 'hat alternative Form', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2449, 'property', 'name', 127, 'el', 'έχει εναλλακτική μορφή', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2450, 'property', 'name', 127, 'pt', 'tem forma alternativa', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2451, 'property', 'name', 127, 'cn', '有替代称号', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2452, 'property', 'comment', 127, 'en', 'This property establishes a relationship of equivalence between two instances of E41 Appellation independent from any item identified by them. It is a dynamic asymmetric relationship, where the range expresses the derivative, if such a direction can be established. Otherwise, the relationship is symmetric. The relationship is not transitive.
The equivalence applies to all cases of use of an instance of E41 Appellation. Multiple names assigned to an object, which are not equivalent for all things identified with a specific instance of E41 Appellation, should be modelled as repeated values of P1 is identified by (identifies).
P139.1 has type allows the type of derivation, such as “transliteration from Latin 1 to ASCII” be refined..
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2453, 'property', 'name', 128, 'de', 'wies Merkmal zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2454, 'property', 'name', 128, 'el', 'απέδωσε ιδιότητα σε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2455, 'property', 'name', 128, 'en', 'assigned attribute to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2456, 'property', 'name', 128, 'fr', 'a affecté un attribut à', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2457, 'property', 'name', 128, 'ru', 'присвоил атрибут для', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2458, 'property', 'name', 128, 'pt', 'atribuiu atributo para', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2459, 'property', 'name', 128, 'cn', '指定属性给', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2460, 'property', 'name_inverse', 128, 'en', 'was attributed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2461, 'property', 'name_inverse', 128, 'fr', 'a reçu un attribut par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2462, 'property', 'name_inverse', 128, 'ru', 'получил атрибут посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2463, 'property', 'name_inverse', 128, 'de', 'bekam Merkmal zugewiesen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2464, 'property', 'name_inverse', 128, 'el', 'χαρακτηρίστηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2465, 'property', 'name_inverse', 128, 'pt', 'foi atribuído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2466, 'property', 'name_inverse', 128, 'cn', '被指定属性於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2467, 'property', 'comment', 128, 'en', 'This property indicates the item to which an attribute or relation is assigned. ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2468, 'property', 'name', 129, 'en', 'assigned', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2469, 'property', 'name', 129, 'ru', 'присвоил', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2470, 'property', 'name', 129, 'de', 'wies zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2471, 'property', 'name', 129, 'el', 'απέδωσε', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2472, 'property', 'name', 129, 'fr', 'a attribué', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2473, 'property', 'name', 129, 'pt', 'atribuiu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2474, 'property', 'name', 129, 'cn', '指定了属性值', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2475, 'property', 'name_inverse', 129, 'ru', 'был присвоен посредством', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2476, 'property', 'name_inverse', 129, 'de', 'wurde zugewiesen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2477, 'property', 'name_inverse', 129, 'fr', 'a été attribué par', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2478, 'property', 'name_inverse', 129, 'en', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2479, 'property', 'name_inverse', 129, 'el', 'αποδόθηκε από', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2480, 'property', 'name_inverse', 129, 'pt', 'foi atribuído por', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2481, 'property', 'name_inverse', 129, 'cn', '被指定了属性值於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2482, 'property', 'comment', 129, 'en', 'This property indicates the attribute that was assigned or the item that was related to the item denoted by a property P140 assigned attribute to in an Attribute assignment action.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2483, 'property', 'name', 130, 'en', 'used constituent', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2484, 'property', 'name', 130, 'de', 'benutzte Bestandteil', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2485, 'property', 'name', 130, 'cn', '使用称号构成部分', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2486, 'property', 'name_inverse', 130, 'de', 'wurde benutzt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2487, 'property', 'name_inverse', 130, 'en', 'was used in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2488, 'property', 'name_inverse', 130, 'cn', '被用来构成称号於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2489, 'property', 'comment', 130, 'en', 'This property associates the event of assigning an instance of E42 Identifier to an entity, with  the instances of E41 Appellation that were used as elements of the identifier.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2490, 'property', 'name', 131, 'en', 'joined', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2491, 'property', 'name', 131, 'de', 'verband', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2492, 'property', 'name', 131, 'cn', '加入了成员', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2493, 'property', 'name_inverse', 131, 'en', 'was joined by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2494, 'property', 'name_inverse', 131, 'de', 'wurde verbunden durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2495, 'property', 'name_inverse', 131, 'cn', '被加入为成员於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2496, 'property', 'comment', 131, 'en', 'This property identifies the instance of E39 Actor that becomes member of a E74 Group in an E85 Joining.
 	Joining events allow for describing people becoming members of a group with a more detailed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2497, 'property', 'name', 132, 'en', 'joined with', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2498, 'property', 'name', 132, 'de', 'verband mit', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2499, 'property', 'name', 132, 'cn', '加入成员到', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2500, 'property', 'name_inverse', 132, 'en', 'gained member by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2501, 'property', 'name_inverse', 132, 'de', 'erwarb Mitglied durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2502, 'property', 'name_inverse', 132, 'cn', '获得成员於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2503, 'property', 'comment', 132, 'en', 'This property identifies the instance of E74 Group of which an instance of E39 Actor becomes a member through an instance of E85 Joining.
Although a Joining activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which becoming member of one Group implies becoming member of another Group as well.
Joining events allow for describing people becoming members of a group with a more detailed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).
The property P144.1 kind of member can be used to specify the type of membership or the role the member has in the group.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2504, 'property', 'name', 133, 'en', 'separated', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2505, 'property', 'name', 133, 'de', 'entließ', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2506, 'property', 'name', 133, 'cn', '分离了成员', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2507, 'property', 'name_inverse', 133, 'en', 'left by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2508, 'property', 'name_inverse', 133, 'de', 'wurde entlassen durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2509, 'property', 'name_inverse', 133, 'cn', '脱离群组於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2510, 'property', 'comment', 133, 'en', 'This property identifies the instance of E39 Actor that leaves an instance of E74 Group through an instance of E86 Leaving.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2511, 'property', 'name', 134, 'en', 'separated from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2512, 'property', 'name', 134, 'de', 'entließ von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2513, 'property', 'name', 134, 'cn', '脱离了群组', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2514, 'property', 'name_inverse', 134, 'en', 'lost member by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2515, 'property', 'name_inverse', 134, 'de', 'verlor Mitglied durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2516, 'property', 'name_inverse', 134, 'cn', '失去成员於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2517, 'property', 'comment', 134, 'en', 'This property identifies the instance of E74 Group an instance of E39 Actor leaves through an instance of E86 Leaving.
Although a Leaving activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which leaving one E74 Group implies leaving another E74 Group as well.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2518, 'property', 'name', 135, 'en', 'curated', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2519, 'property', 'name', 135, 'de', 'betreute kuratorisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2520, 'property', 'name', 135, 'cn', '典藏管理了', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2521, 'property', 'name_inverse', 135, 'en', 'was curated by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2522, 'property', 'name_inverse', 135, 'de', 'wurde kuratorisch betreut durch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2523, 'property', 'name_inverse', 135, 'cn', '被典藏管理於', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2524, 'property', 'comment', 135, 'en', 'This property associates an instance of E87 Curation Activity with the instance of E78 Collection that is subject of that  curation activity.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2525, 'property', 'name', 136, 'en', 'has component', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2526, 'property', 'name', 136, 'de', 'hat Bestandteil', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2527, 'property', 'name', 136, 'cn', '有组件', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2528, 'property', 'name_inverse', 136, 'en', 'is component of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2529, 'property', 'name_inverse', 136, 'de', 'ist Bestandteil von', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2530, 'property', 'name_inverse', 136, 'cn', '被用来组成', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2569, 'property', 'name', 149, '0', 'erscheint zuletzt in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2531, 'property', 'comment', 136, 'en', 'This property associates an instance of E89 Propositional Object with a structural part of it that is by itself an instance of E89 Propositional Object.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2532, 'property', 'name', 137, 'en', 'is identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2533, 'property', 'name_inverse', 137, 'en', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2534, 'property', 'comment', 137, 'en', 'This property identifies an instance of E28 Conceptual Object using an instance of E75 Conceptual Object Appellation.', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2535, 'property', 'name', 138, 'en', 'defines typical parts of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2536, 'property', 'name_inverse', 138, 'en', 'defines typical wholes for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2537, 'property', 'comment', 138, 'en', 'The property "broaderPartitive" associates an instance of E55 Type “A” with an instance of E55 Type “B”, when items of type “A” typically form part of items of type “B”, such as “car motors” and “cars”.
It allows Types to be organised into hierarchies. This is the sense of "broader term partitive (BTP)" as defined in ISO 2788 and “broaderPartitive” in SKOS.
', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2538, 'property', 'name', 139, 'en', 'was formed from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2539, 'property', 'name_inverse', 139, 'en', 'participated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2540, 'property', 'comment', 139, 'en', 'This property associates an instance of E66 Formation with an instance of E74 Group from which the new group was formed preserving a sense of continuity such as in mission, membership or tradition.
	', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2541, 'property', 'name', 140, 'en', 'has parent', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2542, 'property', 'name_inverse', 140, 'en', 'is parent of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2543, 'property', 'comment', 140, 'en', 'It appears that there is a notion of events justifying parenthood relationships in a biological or legal sense. There is a notion of legal parenthood being equal to or equivalent to biological parenthood. The fact that the legal system may not acknowledge biological parenthood is not a contradiction to a more general concept comprising both biological and legal sense. In particular, such a notion should imply as default children being heirs, if the society supports such concept. Superproperty of paths for was born – gave birth, was born, by father
	', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2544, 'property', 'name', 141, 'en', 'begins chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2545, 'property', 'name', 141, 'de', 'beginnt chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2546, 'property', 'comment', 141, 'en', 'OA1 is used to link the beginning of a persistent item''s (E77) life span (or time of usage)
    with a certain date in time. E77 (Persistent Item) - P92i (was brought into existence by) - E63 (Beginning of Existence)
    - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [Holy Lance (E22)] was brought into existence by [forging of Holy Lance (E12)] has time span
    [Moment/Duration of Forging of Holy Lance (E52)] ongoing througout [0770-12-24 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2547, 'property', 'name', 142, 'en', 'ends chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2548, 'property', 'name', 142, 'de', 'endet chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2549, 'property', 'comment', 142, 'en', 'OA2 is used to link the end of a persistent item''s (E77) life span (or time of usage) with
    a certain date in time.
    E77 (Persistent Item) - P93i (was taken out of existence by) - E64 (End of Existence) - P4 (has time span) -
    E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [The one ring (E22)] was destroyed by [Destruction of the one ring (E12)] has time span
    [Moment of throwing it down the lava (E52)] ongoing througout [3019-03-25 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2550, 'property', 'name', 143, 'en', 'born chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2551, 'property', 'name', 143, 'de', 'geboren chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2552, 'property', 'comment', 143, 'en', 'OA3 is used to link the birth of a person with a certain date in time.
    21 (Person) - P98i (was born) by - E67 (Birth) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) -
    E61 (Time Primitive)
    Example: [Stefan (E21)] was born by [birth of Stefan (E12)] has time span
    [Moment/Duration of Stefan''s birth (E52)] ongoing througout [1981-11-23 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2553, 'property', 'name', 144, 'en', 'died chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2554, 'property', 'name', 144, 'de', 'gestorben chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2555, 'property', 'comment', 144, 'en', 'OA4 is used to link the death of a person with a certain date in time.
    E21 (Person) - P100i (died in) - E69 (Death) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) -
    E61 (Time Primitive)
    Example: [Lady Diana (E21)] died in [death of Diana (E69)] has time span [Moment/Duration of Diana''s death (E52)]
    ongoing througout [1997-08-31 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2556, 'property', 'name', 145, 'en', 'begins chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2557, 'property', 'name', 145, 'de', 'beginnt chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2558, 'property', 'comment', 145, 'en', 'OA5 is used to link the beginning of a temporal entity (E2) with a certain date in time.
    It can also be used to determine the beginning of a property''s duration.
    E2 (Temporal Entity) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [ Thirty Years'' War (E7)] has time span [Moment/Duration of Beginning of Thirty Years'' War (E52)] ongoing
    througout [1618-05-23 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2559, 'property', 'name', 146, 'en', 'ends chronologically', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2560, 'property', 'name', 146, 'de', 'endet chronologisch', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2561, 'property', 'comment', 146, 'en', 'OA6 is used to link the end of a temporal entity''s (E2) with a certain date in time.
    It can also be used to determine the end of a property''s duration.
    E2 (temporal entity) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [ Thirty Years'' War (E7)] has time span [Moment/Duration of End of Thirty Years'' War (E52)] ongoing
    througout [1648-10-24 (E61)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2562, 'property', 'name', 147, 'en', 'has relationship to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2563, 'property', 'name', 147, 'de', 'hat Beziehung zu', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2564, 'property', 'comment', 147, 'en', 'OA7 is used to link two Actors (E39) via a certain relationship E39 Actor linked with
    E39 Actor: E39 (Actor) - P11i (participated in) - E5 (Event) - P11 (had participant) - E39 (Actor) Example:
    [ Stefan (E21)] participated in [ Relationship from Stefan to Joachim (E5)] had participant [Joachim (E21)] The
    connecting event is defined by an entity of class E55 (Type): [Relationship from Stefan to Joachim (E5)] has type
    [Son to Father (E55)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2565, 'property', 'name', 148, 'en', 'appears for the first time in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2566, 'property', 'name', 148, 'de', 'erscheint erstes mal in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2567, 'property', 'comment', 148, 'en', 'OA9 is used to link the beginning of a persistent item''s (E77) life span (or time of
    usage) with a certain place. E.g to document the birthplace of a person. E77 Persistent Item linked with a E53
    Place: E77 (Persistent Item) - P92i (was brought into existence by) - E63 (Beginning of Existence) - P7 (took
    place at) - E53 (Place) Example: [Albert Einstein (E21)] was brought into existence by [Birth of Albert Einstein
    (E12)] took place at [Ulm (E53)]', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2568, 'property', 'name', 149, 'en', 'appears for the last time in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO i18n VALUES (2570, 'property', 'comment', 149, 'en', 'OA10 is used to link the end of a persistent item''s (E77) life span (or time of usage)
    with a certain place. E.g to document a person''s place of death. E77 Persistent Item linked with a E53 Place:
    E77 (Persistent Item) - P93i (was taken out of existence by) - E64 (End of Existence) - P7 (took place at) - E53
    (Place) Example: [Albert Einstein (E21)] was taken out of by [Death of Albert Einstein (E12)] took place at
    [Princeton (E53)]', '2015-06-11 19:26:28.25822', NULL);


--
-- Name: i18n_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('i18n_id_seq', 2570, true);


--
-- Data for Name: property; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO property VALUES (1, 'P1', 40, 1, 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (2, 'P2', 53, 1, 'has type', 'is type of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (3, 'P3', 57, 1, 'has note', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (4, 'P4', 50, 2, 'has time-span', 'is time-span of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (5, 'P5', 3, 3, 'consists of', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (6, 'P7', 51, 4, 'took place at', 'witnessed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (7, 'P8', 18, 4, 'took place on or within', 'witnessed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (8, 'P9', 4, 4, 'consists of', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (9, 'P10', 4, 4, 'falls within', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (10, 'P11', 38, 5, 'had participant', 'participated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (11, 'P12', 70, 5, 'occurred in the presence of', 'was present at', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (12, 'P13', 18, 6, 'destroyed', 'was destroyed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (13, 'P14', 38, 7, 'carried out by', 'performed', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (14, 'P15', 1, 7, 'was influenced by', 'influenced', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (15, 'P16', 64, 7, 'used specific object', 'was used for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (16, 'P17', 1, 7, 'was motivated by', 'motivated', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (17, 'P19', 65, 7, 'was intended use of', 'was made for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (18, 'P20', 5, 7, 'had specific purpose', 'was purpose of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (19, 'P21', 53, 7, 'had general purpose', 'was purpose of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (20, 'P22', 38, 8, 'transferred title to', 'acquired title through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (21, 'P23', 38, 8, 'transferred title from', 'surrendered title through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (22, 'P24', 18, 8, 'transferred title of', 'changed ownership through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (23, 'P25', 19, 9, 'moved', 'moved by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (24, 'P26', 51, 9, 'moved to', 'was destination of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (25, 'P27', 51, 9, 'moved from', 'was origin of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (26, 'P28', 38, 10, 'custody surrendered by', 'surrendered custody through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (27, 'P29', 38, 10, 'custody received by', 'received custody through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (28, 'P30', 18, 10, 'transferred custody of', 'custody transferred through', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (29, 'P31', 23, 11, 'has modified', 'was modified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (30, 'P32', 53, 7, 'used general technique', 'was technique of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (31, 'P33', 28, 7, 'used specific technique', 'was used by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (32, 'P34', 18, 14, 'concerned', 'was assessed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (33, 'P35', 3, 14, 'has identified', 'was identified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (34, 'P37', 41, 15, 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (35, 'P38', 41, 15, 'deassigned', 'was deassigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (36, 'P39', 1, 16, 'measured', 'was measured by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (37, 'P40', 52, 16, 'observed dimension', 'was observed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (38, 'P41', 1, 17, 'classified', 'was classified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (39, 'P42', 53, 17, 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (40, 'P43', 52, 64, 'has dimension', 'is dimension of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (41, 'P44', 3, 18, 'has condition', 'is condition of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (42, 'P45', 55, 18, 'consists of', 'is incorporated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (43, 'P46', 18, 18, 'is composed of', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (44, 'P48', 41, 1, 'has preferred identifier', 'is preferred identifier of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (45, 'P49', 38, 18, 'has former or current keeper', 'is former or current keeper of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (46, 'P50', 38, 18, 'has current keeper', 'is current keeper of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (47, 'P51', 38, 18, 'has former or current owner', 'is former or current owner of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (48, 'P52', 38, 18, 'has current owner', 'is current owner of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (49, 'P53', 51, 18, 'has former or current location', 'is former or current location of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (50, 'P54', 51, 19, 'has current permanent location', 'is current permanent location of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (51, 'P55', 51, 19, 'has current location', 'currently holds', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (52, 'P56', 25, 19, 'bears feature', 'is found on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (53, 'P57', 25, 19, 'has number of parts', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (54, 'P58', 44, 18, 'has section definition', 'defines section', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (55, 'P59', 51, 18, 'has section', 'is located on or within', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (56, 'P62', 1, 23, 'depicts', 'is depicted by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (57, 'P65', 35, 23, 'shows visual item', 'is shown by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (58, 'P67', 1, 81, 'refers to', 'is referred to by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (59, 'P68', 55, 28, 'foresees use of', 'use foreseen by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (60, 'P69', 28, 28, 'is associated with', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (61, 'P70', 1, 30, 'documents', 'is documented in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (62, 'P71', 1, 31, 'lists', 'is listed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (63, 'P72', 54, 32, 'has language', 'is language of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (64, 'P73', 32, 32, 'has translation', 'is translation of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (65, 'P74', 51, 38, 'has current or former residence', 'is current or former residence of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (66, 'P75', 29, 38, 'possesses', 'is possessed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (67, 'P76', 49, 38, 'has contact point', 'provides access to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (68, 'P78', 47, 50, 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (69, 'P79', 86, 50, 'beginning is qualified by', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (70, 'P80', 86, 50, 'end is qualified by', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (71, 'P81', 85, 50, 'ongoing throughout', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (72, 'P82', 85, 50, 'at some time within', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (73, 'P83', 52, 50, 'had at least duration', 'was minimum duration of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (74, 'P84', 52, 50, 'had at most duration', 'was maximum duration of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (75, 'P86', 50, 50, 'falls within', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (76, 'P87', 42, 51, 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (77, 'P89', 51, 51, 'falls within', 'contains', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (78, 'P90', 84, 52, 'has value', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (79, 'P91', 56, 52, 'has unit', 'is unit of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (80, 'P92', 70, 57, 'brought into existence', 'was brought into existence by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (81, 'P93', 70, 58, 'took out of existence', 'was taken out of existence by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (82, 'P94', 27, 59, 'has created', 'was created by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (83, 'P95', 68, 60, 'has formed', 'was formed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (84, 'P96', 21, 61, 'by mother', 'gave birth', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (85, 'P97', 21, 61, 'from father', 'was father for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (86, 'P98', 21, 61, 'brought into life', 'was born', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (87, 'P99', 68, 62, 'dissolved', 'was dissolved by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (88, 'P100', 21, 63, 'was death of', 'died in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (89, 'P101', 53, 64, 'had as general use', 'was use of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (90, 'P102', 34, 65, 'has title', 'is title of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (91, 'P103', 53, 65, 'was intended for', 'was intention of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (92, 'P104', 29, 66, 'is subject to', 'applies to', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (93, 'P105', 38, 66, 'right held by', 'has right on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (94, 'P106', 82, 82, 'is composed of', 'forms part of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (95, 'P107', 38, 68, 'has current or former member', 'is current or former member of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (96, 'P108', 23, 12, 'has produced', 'was produced by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (97, 'P109', 38, 71, 'has current or former curator', 'is current or former curator of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (98, 'P110', 23, 72, 'augmented', 'was augmented by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (99, 'P111', 18, 72, 'added', 'was added by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (100, 'P112', 23, 73, 'diminished', 'was diminished by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (101, 'P113', 18, 73, 'removed', 'was removed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (102, 'P114', 2, 2, 'is equal in time to', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (103, 'P115', 2, 2, 'finishes', 'is finished by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (104, 'P116', 2, 2, 'starts', 'is started by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (105, 'P117', 2, 2, 'occurs during', 'includes', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (106, 'P118', 2, 2, 'overlaps in time with', 'is overlapped in time by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (107, 'P119', 2, 2, 'meets in time with', 'is met in time by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (108, 'P120', 2, 2, 'occurs before', 'occurs after', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (109, 'P121', 51, 51, 'overlaps with', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (110, 'P122', 51, 51, 'borders with', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (111, 'P123', 70, 74, 'resulted in', 'resulted from', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (112, 'P124', 70, 74, 'transformed', 'was transformed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (113, 'P125', 53, 7, 'used object of type', 'was type of object used in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (114, 'P126', 55, 11, 'employed', 'was employed in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (115, 'P127', 53, 53, 'has broader term', 'has narrower term', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (116, 'P128', 82, 23, 'carries', 'is carried by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (117, 'P129', 1, 81, 'is about', 'is subject of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (118, 'P130', 64, 64, 'shows features of', 'features are also found on', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (119, 'P131', 75, 38, 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (120, 'P132', 4, 4, 'overlaps with', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (121, 'P133', 4, 4, 'is separated from', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (122, 'P134', 7, 7, 'continued', 'was continued by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (123, 'P135', 53, 76, 'created type', 'was created by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (124, 'P136', 1, 76, 'was based on', 'supported type creation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (125, 'P137', 53, 1, 'exemplifies', 'is exemplified by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (126, 'P138', 1, 35, 'represents', 'has representation', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (127, 'P139', 40, 40, 'has alternative form', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (128, 'P140', 1, 13, 'assigned attribute to', 'was attributed by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (129, 'P141', 1, 13, 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (130, 'P142', 82, 15, 'used constituent', 'was used in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (131, 'P143', 38, 78, 'joined', 'was joined by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (132, 'P144', 68, 78, 'joined with', 'gained member by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (133, 'P145', 38, 79, 'separated', 'left by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (134, 'P146', 68, 79, 'separated from', 'lost member by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (135, 'P147', 71, 80, 'curated', 'was curated by', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (136, 'P148', 81, 81, 'has component', 'is component of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (137, 'P149', 69, 27, 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (138, 'P150', 53, 53, 'defines typical parts of', 'defines typical wholes for', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (139, 'P151', 68, 60, 'was formed from', 'participated in', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (140, 'P152', 21, 21, 'has parent', 'is parent of', '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (141, 'OA1', 85, 70, 'begins chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (142, 'OA2', 85, 70, 'ends chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (143, 'OA3', 85, 21, 'born chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (144, 'OA4', 85, 21, 'died chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (145, 'OA5', 85, 2, 'begins chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (146, 'OA6', 85, 2, 'ends chronologically', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (147, 'OA7', 38, 38, 'has relationship to', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (148, 'OA8', 51, 70, 'appears for the first time in', NULL, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property VALUES (149, 'OA9', 51, 70, 'appears for the last time in', NULL, '2015-06-11 19:26:28.25822', NULL);


--
-- Data for Name: link; Type: TABLE DATA; Schema: model; Owner: openatlas
--



--
-- Name: link_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('link_id_seq', 1, false);


--
-- Data for Name: link_property; Type: TABLE DATA; Schema: model; Owner: openatlas
--



--
-- Name: link_property_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('link_property_id_seq', 1, false);


--
-- Name: property_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('property_id_seq', 149, true);


--
-- Data for Name: property_inheritance; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO property_inheritance VALUES (1, 11, 10, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (2, 81, 12, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (3, 10, 13, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (4, 11, 15, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (5, 14, 15, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (6, 14, 16, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (7, 13, 20, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (8, 13, 21, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (9, 11, 23, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (10, 6, 24, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (11, 6, 25, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (12, 13, 26, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (13, 13, 27, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (14, 11, 29, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (15, 113, 30, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (16, 15, 31, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (17, 128, 32, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (18, 129, 33, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (19, 129, 34, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (20, 129, 35, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (21, 128, 36, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (22, 129, 37, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (23, 128, 38, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (24, 129, 39, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (25, 1, 44, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (26, 45, 46, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (27, 47, 48, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (28, 93, 48, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (29, 49, 51, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (30, 43, 52, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (31, 116, 57, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (32, 58, 59, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (33, 58, 61, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (34, 58, 62, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (35, 118, 64, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (36, 1, 68, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (37, 3, 69, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (38, 3, 70, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (39, 1, 76, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (40, 11, 80, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (41, 11, 81, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (42, 80, 82, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (43, 80, 83, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (44, 10, 84, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (45, 80, 86, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (46, 10, 87, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (47, 81, 87, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (48, 81, 88, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (49, 1, 90, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (50, 29, 96, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (51, 80, 96, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (52, 45, 97, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (53, 29, 98, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (54, 15, 99, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (55, 11, 99, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (56, 29, 100, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (57, 11, 101, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (58, 80, 111, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (59, 81, 112, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (60, 118, 116, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (61, 58, 117, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (62, 1, 119, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (63, 14, 122, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (64, 82, 123, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (65, 14, 124, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (66, 2, 125, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (67, 58, 126, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (68, 15, 130, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (69, 10, 131, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (70, 10, 132, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (71, 10, 133, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (72, 10, 134, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (73, 1, 137, '2015-06-11 19:26:28.25822', NULL);
INSERT INTO property_inheritance VALUES (74, 10, 139, '2015-06-11 19:26:28.25822', NULL);


--
-- Name: property_inheritance_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('property_inheritance_id_seq', 74, true);


--
-- PostgreSQL database dump complete
--

