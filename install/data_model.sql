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
-- Data for Name: class_i18n; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO class_i18n VALUES (1, 'E1', 'el', 'name', 'Οντότητα CIDOC CRM', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (2, 'E1', 'en', 'name', 'CRM Entity', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (3, 'E1', 'de', 'name', 'CRM Entität', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (4, 'E1', 'ru', 'name', 'CRM Сущность', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (5, 'E1', 'fr', 'name', 'Entité CRM', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (6, 'E1', 'pt', 'name', 'Entidade CRM', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (7, 'E1', 'cn', 'name', 'CRM实体', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (8, 'E1', 'en', 'comment', 'This class comprises all things in the universe of discourse of the CIDOC Conceptual Reference Model. 
It is an abstract concept providing for three general properties:
1.	Identification by name or appellation, and in particular by a preferred identifier
2.	Classification by type, allowing further refinement of the specific subclass an instance belongs to 
3.	Attachment of free text for the expression of anything not captured by formal properties
With the exception of E59 Primitive Value, all other classes within the CRM are directly or indirectly specialisations of E1 CRM Entity. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (9, 'E2', 'fr', 'name', 'Entité temporelle', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (10, 'E2', 'en', 'name', 'Temporal Entity', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (11, 'E2', 'ru', 'name', 'Временная Сущность', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (12, 'E2', 'el', 'name', 'Έγχρονη  Οντότητα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (13, 'E2', 'de', 'name', 'Geschehendes', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (14, 'E2', 'pt', 'name', 'Entidade Temporal', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (15, 'E2', 'cn', 'name', '时间实体', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (16, 'E2', 'en', 'comment', 'This class comprises all phenomena, such as the instances of E4 Periods, E5 Events and states, which happen over a limited extent in time. 
	In some contexts, these are also called perdurants. This class is disjoint from E77 Persistent Item. This is an abstract class and has no direct instances. E2 Temporal Entity is specialized into E4 Period, which applies to a particular geographic area (defined with a greater or lesser degree of precision), and E3 Condition State, which applies to instances of E18 Physical Thing.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (17, 'E3', 'ru', 'name', 'Состояние', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (18, 'E3', 'en', 'name', 'Condition State', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (19, 'E3', 'de', 'name', 'Zustandsphase', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (20, 'E3', 'fr', 'name', 'État matériel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (21, 'E3', 'el', 'name', 'Κατάσταση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (22, 'E3', 'pt', 'name', 'Estado Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (23, 'E3', 'cn', 'name', '状态', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (24, 'E3', 'en', 'comment', 'This class comprises the states of objects characterised by a certain condition over a time-span. 
An instance of this class describes the prevailing physical condition of any material object or feature during a specific E52 Time Span. In general, the time-span for which a certain condition can be asserted may be shorter than the real time-span, for which this condition held.
 The nature of that condition can be described using P2 has type. For example, the E3 Condition State “condition of the SS Great Britain between 22 September 1846 and 27 August 1847” can be characterized as E55 Type “wrecked”. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (25, 'E4', 'de', 'name', 'Phase', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (26, 'E4', 'en', 'name', 'Period', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (27, 'E4', 'fr', 'name', 'Période', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (28, 'E4', 'ru', 'name', 'Период', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (29, 'E4', 'el', 'name', 'Περίοδος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (30, 'E4', 'pt', 'name', 'Período', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (31, 'E4', 'cn', 'name', '期间', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (32, 'E4', 'en', 'comment', '	This class comprises sets of coherent phenomena or cultural manifestations bounded in time and space. 
It is the social or physical coherence of these phenomena that identify an E4 Period and not the associated spatio-temporal bounds. These bounds are a mere approximation of the actual process of growth, spread and retreat. Consequently, different periods can overlap and coexist in time and space, such as when a nomadic culture exists in the same area as a sedentary culture. 
Typically this class is used to describe prehistoric or historic periods such as the “Neolithic Period”, the “Ming Dynasty” or the “McCarthy Era”. There are however no assumptions about the scale of the associated phenomena. In particular all events are seen as synthetic processes consisting of coherent phenomena. Therefore E4 Period is a superclass of E5 Event. For example, a modern clinical E67 Birth can be seen as both an atomic E5 Event and as an E4 Period that consists of multiple activities performed by multiple instances of E39 Actor. 
There are two different conceptualisations of ‘artistic style’, defined either by physical features or by historical context. For example, “Impressionism” can be viewed as a period lasting from approximately 1870 to 1905 during which paintings with particular characteristics were produced by a group of artists that included (among others) Monet, Renoir, Pissarro, Sisley and Degas. Alternatively, it can be regarded as a style applicable to all paintings sharing the characteristics of the works produced by the Impressionist painters, regardless of historical context. The first interpretation is an E4 Period, and the second defines morphological object types that fall under E55 Type.
Another specific case of an E4 Period is the set of activities and phenomena associated with a settlement, such as the populated period of Nineveh.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (33, 'E5', 'el', 'name', 'Συμβάν', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (34, 'E5', 'fr', 'name', 'Événement', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (35, 'E5', 'ru', 'name', 'Событие', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (36, 'E5', 'en', 'name', 'Event', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (37, 'E5', 'de', 'name', 'Ereignis', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (38, 'E5', 'pt', 'name', 'Evento', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (39, 'E5', 'cn', 'name', '事件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (40, 'E5', 'en', 'comment', 'This class comprises changes of states in cultural, social or physical systems, regardless of scale, brought about by a series or group of coherent physical, cultural, technological or legal phenomena. Such changes of state will affect instances of E77 Persistent Item or its subclasses.
The distinction between an E5 Event and an E4 Period is partly a question of the scale of observation. Viewed at a coarse level of detail, an E5 Event is an ‘instantaneous’ change of state. At a fine level, the E5 Event can be analysed into its component phenomena within a space and time frame, and as such can be seen as an E4 Period. The reverse is not necessarily the case: not all instances of E4 Period give rise to a noteworthy change of state.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (41, 'E6', 'ru', 'name', 'Разрушение', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (42, 'E6', 'en', 'name', 'Destruction', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (43, 'E6', 'fr', 'name', 'Destruction', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (44, 'E6', 'de', 'name', 'Zerstörung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (45, 'E6', 'el', 'name', 'Καταστροφή', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (46, 'E6', 'pt', 'name', 'Destruição', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (47, 'E6', 'cn', 'name', '摧毁', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (48, 'E16', 'de', 'name', 'Messung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (49, 'E16', 'fr', 'name', 'Mesurage', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (50, 'E16', 'en', 'name', 'Measurement', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (190, 'E25', 'pt', 'name', 'Característica Fabricada', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (191, 'E25', 'cn', 'name', '人造外貌表征', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (248, 'E32', 'en', 'comment', 'This class comprises encyclopaedia, thesauri, authority lists and other documents that define terminology or conceptual systems for consistent use.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (51, 'E6', 'en', 'comment', 'This class comprises events that destroy one or more instances of E18 Physical Thing such that they lose their identity as the subjects of documentation.  
Some destruction events are intentional, while others are independent of human activity. Intentional destruction may be documented by classifying the event as both an E6 Destruction and E7 Activity. 
The decision to document an object as destroyed, transformed or modified is context sensitive: 
1.  If the matter remaining from the destruction is not documented, the event is modelled solely as E6 Destruction. 
2. An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the original. In this case, the new items have separate identities. Matter is preserved, but identity is not.
3. When the initial identity of the changed instance of E18 Physical Thing is preserved, the event should be documented as E11 Modification. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (52, 'E7', 'en', 'name', 'Activity', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (53, 'E7', 'fr', 'name', 'Activité', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (54, 'E7', 'de', 'name', 'Handlung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (55, 'E7', 'ru', 'name', 'Деятельность', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (56, 'E7', 'el', 'name', 'Δράση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (57, 'E7', 'pt', 'name', 'Atividade', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (58, 'E7', 'cn', 'name', '活动', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (59, 'E7', 'en', 'comment', 'This class comprises actions intentionally carried out by instances of E39 Actor that result in changes of state in the cultural, social, or physical systems documented. 
This notion includes complex, composite and long-lasting actions such as the building of a settlement or a war, as well as simple, short-lived actions such as the opening of a door.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (60, 'E8', 'fr', 'name', 'Acquisition', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (61, 'E8', 'el', 'name', 'Απόκτηση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (62, 'E8', 'ru', 'name', 'Событие Приобретения', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (63, 'E8', 'en', 'name', 'Acquisition', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (64, 'E8', 'de', 'name', 'Erwerb', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (65, 'E8', 'pt', 'name', 'Aquisição', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (66, 'E8', 'cn', 'name', '征集取得', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (67, 'E8', 'en', 'comment', 'This class comprises transfers of legal ownership from one or more instances of E39 Actor to one or more other instances of E39 Actor. 
The class also applies to the establishment or loss of ownership of instances of E18 Physical Thing. It does not, however, imply changes of any other kinds of right. The recording of the donor and/or recipient is optional. It is possible that in an instance of E8 Acquisition there is either no donor or no recipient. Depending on the circumstances, it may describe:
1.	the beginning of ownership
2.	the end of ownership
3.	the transfer of ownership
4.	the acquisition from an unknown source 
5.	the loss of title due to destruction of the item
It may also describe events where a collector appropriates legal title, for example by annexation or field collection. The interpretation of the museum notion of "accession" differs between institutions. The CRM therefore models legal ownership (E8 Acquisition) and physical custody (E10 Transfer of Custody) separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (68, 'E9', 'en', 'name', 'Move', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (69, 'E9', 'el', 'name', 'Μετακίνηση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (70, 'E9', 'de', 'name', 'Objektbewegung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (71, 'E9', 'ru', 'name', 'Перемещение', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (72, 'E9', 'fr', 'name', 'Déplacement', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (73, 'E9', 'pt', 'name', 'Locomoção', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (74, 'E9', 'cn', 'name', '移动', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (75, 'E9', 'en', 'comment', 'This class comprises changes of the physical location of the instances of E19 Physical Object. 
Note, that the class E9 Move inherits the property P7 took place at (witnessed): E53 Place. This property should be used to describe the trajectory or a larger area within which a move takes place, whereas the properties P26 moved to (was destination of), P27 moved from (was origin of) describe the start and end points only. Moves may also be documented to consist of other moves (via P9 consists of (forms part of)), in order to describe intermediate stages on a trajectory. In that case, start and end points of the partial moves should match appropriately between each other and with the overall event.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (76, 'E10', 'fr', 'name', 'Changement de détenteur', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (77, 'E10', 'en', 'name', 'Transfer of Custody', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (78, 'E10', 'de', 'name', 'Übertragung des Gewahrsams', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (79, 'E10', 'el', 'name', 'Μεταβίβαση  Κατοχής', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (80, 'E10', 'ru', 'name', 'Передача Опеки', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (81, 'E10', 'pt', 'name', 'Transferência de Custódia', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (82, 'E10', 'cn', 'name', '保管作业转移', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (83, 'E10', 'en', 'comment', 'This class comprises transfers of physical custody of objects between instances of E39 Actor. 
The recording of the donor and/or recipient is optional. It is possible that in an instance of E10 Transfer of Custody there is either no donor or no recipient. Depending on the circumstances it may describe:
1.	the beginning of custody 
2.	the end of custody 
3.	the transfer of custody 
4.	the receipt of custody from an unknown source
5.	the declared loss of an object
The distinction between the legal responsibility for custody and the actual physical possession of the object should be expressed using the property P2 has type (is type of). A specific case of transfer of custody is theft.
The interpretation of the museum notion of "accession" differs between institutions. The CRM therefore models legal ownership and physical custody separately. Institutions will then model their specific notions of accession and deaccession as combinations of these.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (84, 'E11', 'ru', 'name', 'Событие Изменения', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (85, 'E11', 'en', 'name', 'Modification', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (86, 'E11', 'el', 'name', 'Τροποποίηση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (87, 'E11', 'fr', 'name', 'Modification', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (88, 'E11', 'de', 'name', 'Bearbeitung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (89, 'E11', 'pt', 'name', 'Modificação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (90, 'E11', 'cn', 'name', '修改', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (91, 'E16', 'pt', 'name', 'Medição', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (92, 'E16', 'cn', 'name', '测量', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (93, 'E24', 'pt', 'name', 'Coisa Material Fabricada', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (94, 'E24', 'cn', 'name', '人造实体物', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (95, 'E24', 'en', 'comment', 'This class comprises all persistent physical items that are purposely created by human activity.
This class comprises man-made objects, such as a swords, and man-made features, such as rock art. No assumptions are made as to the extent of modification required to justify regarding an object as man-made. For example, a “cup and ring” carving on bedrock is regarded as instance of E24 Physical Man-Made Thing. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (96, 'E25', 'fr', 'name', 'Caractéristique fabriquée', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (242, 'E32', 'ru', 'name', 'Официальный Документ', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (243, 'E32', 'fr', 'name', 'Document de référence', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (244, 'E32', 'el', 'name', 'Πηγή Καθιερωμένων Όρων', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (245, 'E32', 'en', 'name', 'Authority Document', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (97, 'E11', 'en', 'comment', 'This class comprises all instances of E7 Activity that create, alter or change E24 Physical Man-Made Thing. 
This class includes the production of an item from raw materials, and other so far undocumented objects, and the preventive treatment or restoration of an object for conservation. 
Since the distinction between modification and production is not always clear, modification is regarded as the more generally applicable concept. This implies that some items may be consumed or destroyed in a Modification, and that others may be produced as a result of it. An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities. 
If the instance of the E29 Design or Procedure utilized for the modification prescribes the use of specific materials, they should be documented using property P68 foresees use of (use foreseen by): E57 Material of E29 Design or Procedure, rather than via P126 employed (was employed in): E57 Material.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (98, 'E12', 'fr', 'name', 'Production', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (99, 'E12', 'el', 'name', 'Παραγωγή', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (100, 'E12', 'de', 'name', 'Herstellung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (101, 'E12', 'ru', 'name', 'Событие Производства', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (102, 'E12', 'en', 'name', 'Production', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (103, 'E12', 'pt', 'name', 'Produção', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (104, 'E12', 'cn', 'name', '生产', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (105, 'E12', 'en', 'comment', 'This class comprises activities that are designed to, and succeed in, creating one or more new items. 
It specializes the notion of modification into production. The decision as to whether or not an object is regarded as new is context sensitive. Normally, items are considered “new” if there is no obvious overall similarity between them and the consumed items and material used in their production. In other cases, an item is considered “new” because it becomes relevant to documentation by a modification. For example, the scribbling of a name on a potsherd may make it a voting token. The original potsherd may not be worth documenting, in contrast to the inscribed one. 
This entity can be collective: the printing of a thousand books, for example, would normally be considered a single event. 
An event should also be documented using E81 Transformation if it results in the destruction of one or more objects and the simultaneous production of others using parts or material from the originals. In this case, the new items have separate identities and matter is preserved, but identity is not.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (106, 'E13', 'ru', 'name', 'Присвоение Атрибута', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (107, 'E13', 'fr', 'name', 'Affectation d''attribut', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (108, 'E13', 'de', 'name', 'Merkmalszuweisung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (109, 'E13', 'en', 'name', 'Attribute Assignment', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (110, 'E13', 'el', 'name', 'Απόδοση Ιδιοτήτων', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (111, 'E13', 'pt', 'name', 'Atribuição de Característica', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (112, 'E13', 'cn', 'name', '屬性指定', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (113, 'E13', 'en', 'comment', 'This class comprises the actions of making assertions about properties of an object or any relation between two items or concepts. 
This class allows the documentation of how the respective assignment came about, and whose opinion it was. All the attributes or properties assigned in such an action can also be seen as directly attached to the respective item or concept, possibly as a collection of contradictory values. All cases of properties in this model that are also described indirectly through an action are characterised as "short cuts" of this action. This redundant modelling of two alternative views is preferred because many implementations may have good reasons to model either the action or the short cut, and the relation between both alternatives can be captured by simple rules. 
In particular, the class describes the actions of people making propositions and statements during certain museum procedures, e.g. the person and date when a condition statement was made, an identifier was assigned, the museum object was measured, etc. Which kinds of such assignments and statements need to be documented explicitly in structures of a schema rather than free text, depends on if this information should be accessible by structured queries. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (114, 'E14', 'el', 'name', 'Εκτίμηση Κατάστασης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (115, 'E14', 'ru', 'name', 'Оценка Состояния', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (116, 'E14', 'fr', 'name', 'Expertise de l''état matériel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (117, 'E14', 'de', 'name', 'Zustandsfeststellung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (118, 'E14', 'en', 'name', 'Condition Assessment', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (119, 'E14', 'pt', 'name', 'Avaliação do Estado Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (120, 'E14', 'cn', 'name', '状态评估', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (121, 'E14', 'en', 'comment', 'This class describes the act of assessing the state of preservation of an object during a particular period. 
The condition assessment may be carried out by inspection, measurement or through historical research. This class is used to document circumstances of the respective assessment that may be relevant to interpret its quality at a later stage, or to continue research on related documents. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (122, 'E15', 'el', 'name', 'Απόδοση Αναγνωριστικού', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (123, 'E15', 'ru', 'name', 'Назначение Идентификатора', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (124, 'E15', 'en', 'name', 'Identifier Assignment', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (125, 'E15', 'de', 'name', 'Kennzeichenzuweisung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (126, 'E15', 'fr', 'name', 'Attribution d’identificateur', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (127, 'E15', 'pt', 'name', 'Atribuição de Identificador', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (128, 'E15', 'cn', 'name', '标识符指定', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (129, 'E15', 'en', 'comment', 'This class comprises activities that result in the allocation of an identifier to an instance of E1 CRM Entity. An E15 Identifier Assignment may include the creation of the identifier from multiple constituents, which themselves may be instances of E41 Appellation. The syntax and kinds of constituents to be used may be declared in a rule constituting an instance of E29 Design or Procedure.
Examples of such identifiers include Find Numbers, Inventory Numbers, uniform titles in the sense of librarianship and Digital Object Identifiers (DOI). Documenting the act of identifier assignment and deassignment is especially useful when objects change custody or the identification system of an organization is changed. In order to keep track of the identity of things in such cases, it is important to document by whom, when and for what purpose an identifier is assigned to an item.
The fact that an identifier is a preferred one for an organisation can be expressed by using the property E1 CRM Entity. P48 has preferred identifier (is preferred identifier of): E42 Identifier. It can better be expressed in a context independent form by assigning a suitable E55 Type, such as “preferred identifier assignment”, to the respective instance of E15 Identifier Assignment via the P2 has type property.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (130, 'E16', 'ru', 'name', 'Событие Измерения', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (131, 'E16', 'el', 'name', 'Μέτρηση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (246, 'E32', 'pt', 'name', 'Documento de Referência', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (247, 'E32', 'cn', 'name', '权威文献', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (249, 'E33', 'ru', 'name', 'Линвистический Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (132, 'E16', 'en', 'comment', 'This class comprises actions measuring physical properties and other values that can be determined by a systematic procedure. 
Examples include measuring the monetary value of a collection of coins or the running time of a specific video cassette. 
The E16 Measurement may use simple counting or tools, such as yardsticks or radiation detection devices. The interest is in the method and care applied, so that the reliability of the result may be judged at a later stage, or research continued on the associated documents. The date of the event is important for dimensions, which may change value over time, such as the length of an object subject to shrinkage. Details of methods and devices are best handled as free text, whereas basic techniques such as "carbon 14 dating" should be encoded using P2 has type (is type of:) E55 Type.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (133, 'E17', 'de', 'name', 'Typuszuweisung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (134, 'E17', 'ru', 'name', 'Присвоение Типа', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (135, 'E17', 'fr', 'name', 'Attribution de type', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (136, 'E17', 'en', 'name', 'Type Assignment', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (137, 'E17', 'el', 'name', 'Απόδοση Τύπου', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (138, 'E17', 'pt', 'name', 'Atribuição de Tipo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (139, 'E17', 'cn', 'name', '类型指定', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (140, 'E17', 'en', 'comment', 'This class comprises the actions of classifying items of whatever kind. Such items include objects, specimens, people, actions and concepts. 
This class allows for the documentation of the context of classification acts in cases where the value of the classification depends on the personal opinion of the classifier, and the date that the classification was made. This class also encompasses the notion of "determination," i.e. the systematic and molecular identification of a specimen in biology. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (141, 'E18', 'de', 'name', 'Materielles', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (142, 'E18', 'el', 'name', 'Υλικό Πράγμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (143, 'E18', 'en', 'name', 'Physical Thing', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (144, 'E18', 'fr', 'name', 'Chose matérielle', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (145, 'E18', 'ru', 'name', 'Физическая Вещь', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (146, 'E18', 'pt', 'name', 'Coisa Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (147, 'E18', 'cn', 'name', '实体物', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (148, 'E18', 'en', 'comment', 'This class comprises all persistent physical items with a relatively stable form, man-made or natural. 
Depending on the existence of natural boundaries of such things, the CRM distinguishes the instances of E19 Physical Object from instances of E26 Physical Feature, such as holes, rivers, pieces of land etc. Most instances of E19 Physical Object can be moved (if not too heavy), whereas features are integral to the surrounding matter. 
The CRM is generally not concerned with amounts of matter in fluid or gaseous states. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (149, 'E19', 'ru', 'name', 'Физический Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (150, 'E19', 'fr', 'name', 'Objet matériel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (151, 'E19', 'en', 'name', 'Physical Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (152, 'E19', 'el', 'name', 'Υλικό Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (153, 'E19', 'de', 'name', 'Materieller Gegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (154, 'E19', 'pt', 'name', 'Objeto Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (155, 'E19', 'cn', 'name', '实体物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (156, 'E19', 'en', 'comment', 'This class comprises items of a material nature that are units for documentation and have physical boundaries that separate them completely in an objective way from other objects. 
The class also includes all aggregates of objects made for functional purposes of whatever kind, independent of physical coherence, such as a set of chessmen. Typically, instances of E19 Physical Object can be moved (if not too heavy).
In some contexts, such objects, except for aggregates, are also called “bona fide objects” (Smith & Varzi, 2000, pp.401-420), i.e. naturally defined objects. 
The decision as to what is documented as a complete item, rather than by its parts or components, may be a purely administrative decision or may be a result of the order in which the item was acquired.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (157, 'E20', 'ru', 'name', 'Биологический Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (158, 'E20', 'en', 'name', 'Biological Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (159, 'E20', 'el', 'name', 'Βιολογικό Ακτικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (160, 'E20', 'fr', 'name', 'Objet biologique', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (161, 'E20', 'de', 'name', 'Biologischer Gegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (162, 'E20', 'pt', 'name', 'Objeto Biológico', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (163, 'E20', 'cn', 'name', '生物体', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (164, 'E20', 'en', 'comment', 'This class comprises individual items of a material nature, which live, have lived or are natural products of or from living organisms. 
Artificial objects that incorporate biological elements, such as Victorian butterfly frames, can be documented as both instances of E20 Biological Object and E22 Man-Made Object. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (165, 'E21', 'de', 'name', 'Person', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (166, 'E21', 'fr', 'name', 'Personne', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (167, 'E21', 'en', 'name', 'Person', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (168, 'E21', 'ru', 'name', 'Личность', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (169, 'E21', 'el', 'name', 'Πρόσωπο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (170, 'E21', 'pt', 'name', 'Pessoa', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (171, 'E21', 'cn', 'name', '人物', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (172, 'E21', 'en', 'comment', 'This class comprises real persons who live or are assumed to have lived. 
Legendary figures that may have existed, such as Ulysses and King Arthur, fall into this class if the documentation refers to them as historical figures. In cases where doubt exists as to whether several persons are in fact identical, multiple instances can be created and linked to indicate their relationship. The CRM does not propose a specific form to support reasoning about possible identity.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (173, 'E22', 'fr', 'name', 'Objet fabriqué', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (174, 'E22', 'el', 'name', 'Ανθρωπογενές Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (175, 'E22', 'de', 'name', 'Künstlicher Gegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (176, 'E22', 'ru', 'name', 'Рукотворный Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (177, 'E22', 'en', 'name', 'Man-Made Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (178, 'E22', 'pt', 'name', 'Objeto Fabricado', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (179, 'E22', 'cn', 'name', '人造物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (180, 'E22', 'en', 'comment', 'This class comprises physical objects purposely created by human activity.
No assumptions are made as to the extent of modification required to justify regarding an object as man-made. For example, an inscribed piece of rock or a preserved butterfly are both regarded as instances of E22 Man-Made Object.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (181, 'E24', 'ru', 'name', 'Физическая Рукотворная Вещь', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (182, 'E24', 'en', 'name', 'Physical Man-Made Thing', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (183, 'E24', 'el', 'name', 'Ανθρωπογενές Υλικό Πράγμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (184, 'E24', 'de', 'name', 'Hergestelltes', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (185, 'E24', 'fr', 'name', 'Chose matérielle fabriquée', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (186, 'E25', 'en', 'name', 'Man-Made Feature', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (187, 'E25', 'ru', 'name', 'Искусственный Признак', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (188, 'E25', 'el', 'name', 'Ανθρωπογενές Μόρφωμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (189, 'E25', 'de', 'name', 'Hergestelltes Merkmal', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (192, 'E25', 'en', 'comment', 'This class comprises physical features that are purposely created by human activity, such as scratches, artificial caves, artificial water channels, etc. 
No assumptions are made as to the extent of modification required to justify regarding a feature as man-made. For example, rock art or even “cup and ring” carvings on bedrock a regarded as types of E25 Man-Made Feature.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (193, 'E26', 'el', 'name', 'Υλικό Μόρφωμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (194, 'E26', 'en', 'name', 'Physical Feature', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (195, 'E26', 'ru', 'name', 'Физический Признак', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (196, 'E26', 'de', 'name', 'Materielles Merkmal', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (197, 'E26', 'fr', 'name', 'Caractéristique matérielle', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (198, 'E26', 'pt', 'name', 'Característica Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (199, 'E26', 'cn', 'name', '实体外貌表征', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (200, 'E26', 'en', 'comment', 'This class comprises identifiable features that are physically attached in an integral way to particular physical objects. 
Instances of E26 Physical Feature share many of the attributes of instances of E19 Physical Object. They may have a one-, two- or three-dimensional geometric extent, but there are no natural borders that separate them completely in an objective way from the carrier objects. For example, a doorway is a feature but the door itself, being attached by hinges, is not. 
Instances of E26 Physical Feature can be features in a narrower sense, such as scratches, holes, reliefs, surface colours, reflection zones in an opal crystal or a density change in a piece of wood. In the wider sense, they are portions of particular objects with partially imaginary borders, such as the core of the Earth, an area of property on the surface of the Earth, a landscape or the head of a contiguous marble statue. They can be measured and dated, and it is sometimes possible to state who or what is or was responsible for them. They cannot be separated from the carrier object, but a segment of the carrier object may be identified (or sometimes removed) carrying the complete feature. 
This definition coincides with the definition of "fiat objects" (Smith & Varzi, 2000, pp.401-420), with the exception of aggregates of “bona fide objects”. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (201, 'E27', 'el', 'name', 'Φυσικός Χώρος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (202, 'E27', 'en', 'name', 'Site', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (203, 'E27', 'fr', 'name', 'Site', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (204, 'E27', 'ru', 'name', 'Участок', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (205, 'E27', 'de', 'name', 'Gelände', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (206, 'E27', 'pt', 'name', 'Lugar', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (207, 'E27', 'cn', 'name', '场地', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (208, 'E27', 'en', 'comment', 'This class comprises pieces of land or sea floor. 
In contrast to the purely geometric notion of E53 Place, this class describes constellations of matter on the surface of the Earth or other celestial body, which can be represented by photographs, paintings and maps.
 Instances of E27 Site are composed of relatively immobile material items and features in a particular configuration at a particular location', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (209, 'E28', 'fr', 'name', 'Objet conceptuel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (210, 'E28', 'de', 'name', 'Begrifflicher Gegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (211, 'E28', 'ru', 'name', 'Концептуальный Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (212, 'E28', 'en', 'name', 'Conceptual Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (213, 'E28', 'el', 'name', 'Νοητικό Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (214, 'E28', 'pt', 'name', 'Objeto Conceitual', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (215, 'E28', 'cn', 'name', '概念物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (216, 'E28', 'en', 'comment', 'This class comprises non-material products of our minds and other human produced data that 		have become objects of a discourse about their identity, circumstances of creation or historical 		implication. The production of such information may have been supported by the use of    		technical devices such as cameras or computers.
Characteristically, instances of this class are created, invented or thought by someone, and then may be documented or communicated between persons. Instances of E28 Conceptual Object have the ability to exist on more than one particular carrier at the same time, such as paper, electronic signals, marks, audio media, paintings, photos, human memories, etc.
They cannot be destroyed. They exist as long as they can be found on at least one carrier or in at least one human memory. Their existence ends when the last carrier and the last memory are lost. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (217, 'E29', 'el', 'name', 'Σχέδιο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (218, 'E29', 'de', 'name', 'Entwurf oder Verfahren', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (219, 'E29', 'fr', 'name', 'Conception ou procédure', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (220, 'E29', 'ru', 'name', 'Проект или Процедура', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (221, 'E29', 'en', 'name', 'Design or Procedure', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (222, 'E29', 'pt', 'name', 'Projeto ou Procedimento', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (223, 'E29', 'cn', 'name', '设计或程序', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (224, 'E29', 'en', 'comment', 'This class comprises documented plans for the execution of actions in order to achieve a result of a specific quality, form or contents. In particular it comprises plans for deliberate human activities that may result in the modification or production of instances of E24 Physical Thing. 
Instances of E29 Design or Procedure can be structured in parts and sequences or depend on others. This is modelled using P69 has association with (is associated with). 
Designs or procedures can be seen as one of the following:
1.	A schema for the activities it describes
2.	A schema of the products that result from their application. 
3.	An independent intellectual product that may have never been applied, such as Leonardo da Vinci’s famous plans for flying machines.
Because designs or procedures may never be applied or only partially executed, the CRM models a loose relationship between the plan and the respective product.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (225, 'E30', 'ru', 'name', 'Право', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (226, 'E30', 'el', 'name', 'Δικαίωμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (227, 'E30', 'fr', 'name', 'Droit', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (228, 'E30', 'en', 'name', 'Right', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (229, 'E30', 'de', 'name', 'Recht', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (230, 'E30', 'pt', 'name', 'Direitos', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (231, 'E30', 'cn', 'name', '权限', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (232, 'E30', 'en', 'comment', 'This class comprises legal privileges concerning material and immaterial things or their derivatives. 
These include reproduction and property rights', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (233, 'E31', 'fr', 'name', 'Document', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (234, 'E31', 'en', 'name', 'Document', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (235, 'E31', 'de', 'name', 'Dokument', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (236, 'E31', 'ru', 'name', 'Документ', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (237, 'E31', 'el', 'name', 'Τεκμήριο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (238, 'E31', 'pt', 'name', 'Documento', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (239, 'E31', 'cn', 'name', '文献', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (240, 'E31', 'en', 'comment', 'This class comprises identifiable immaterial items that make propositions about reality.
These propositions may be expressed in text, graphics, images, audiograms, videograms or by other similar means. Documentation databases are regarded as a special case of E31 Document. This class should not be confused with the term “document” in Information Technology, which is compatible with E73 Information Object.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (241, 'E32', 'de', 'name', 'Referenzdokument', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (250, 'E33', 'en', 'name', 'Linguistic Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (251, 'E33', 'el', 'name', 'Γλωσσικό Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (252, 'E33', 'fr', 'name', 'Objet linguistique', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (253, 'E33', 'de', 'name', 'Sprachlicher Gegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (254, 'E33', 'pt', 'name', 'Objeto Lingüístico', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (255, 'E33', 'cn', 'name', '语言物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (256, 'E33', 'en', 'comment', 'This class comprises identifiable expressions in natural language or languages. 
Instances of E33 Linguistic Object can be expressed in many ways: e.g. as written texts, recorded speech or sign language. However, the CRM treats instances of E33 Linguistic Object independently from the medium or method by which they are expressed. Expressions in formal languages, such as computer code or mathematical formulae, are not treated as instances of E33 Linguistic Object by the CRM. These should be modelled as instances of E73 Information Object.
The text of an instance of E33 Linguistic Object can be documented in a note by P3 has note: E62 String
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (257, 'E34', 'el', 'name', 'Επιγραφή', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (258, 'E34', 'en', 'name', 'Inscription', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (259, 'E34', 'fr', 'name', 'Inscription', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (260, 'E34', 'ru', 'name', 'Надпись', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (261, 'E34', 'de', 'name', 'Inschrift', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (262, 'E34', 'pt', 'name', 'Inscrição', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (263, 'E34', 'cn', 'name', '题字', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (264, 'E34', 'en', 'comment', 'This class comprises recognisable, short texts attached to instances of E24 Physical Man-Made Thing. 
The transcription of the text can be documented in a note by P3 has note: E62 String. The alphabet used can be documented by P2 has type: E55 Type. This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of an inscription, but the underlying prototype. The physical embodiment is modelled in the CRM as E24 Physical Man-Made Thing.
The relationship of a physical copy of a book to the text it contains is modelled using E84 Information Carrier. P128 carries (is carried by): E33 Linguistic Object. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (265, 'E35', 'ru', 'name', 'Заголовок', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (266, 'E35', 'fr', 'name', 'Titre', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (267, 'E35', 'de', 'name', 'Titel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (268, 'E35', 'en', 'name', 'Title', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (269, 'E35', 'el', 'name', ' Τίτλος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (270, 'E35', 'pt', 'name', 'Título', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (271, 'E35', 'cn', 'name', '题目', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (272, 'E35', 'en', 'comment', 'This class comprises the names assigned to works, such as texts, artworks or pieces of music. 
Titles are proper noun phrases or verbal phrases, and should not be confused with generic object names such as “chair”, “painting” or “book” (the latter are common nouns that stand for instances of E55 Type). Titles may be assigned by the creator of the work itself, or by a social group. 
This class also comprises the translations of titles that are used as surrogates for the original titles in different social contexts.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (273, 'E36', 'ru', 'name', 'Визуальный Предмет', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (274, 'E36', 'fr', 'name', 'Item visuel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (275, 'E36', 'el', 'name', 'Οπτικό Στοιχείο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (276, 'E36', 'en', 'name', 'Visual Item', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (277, 'E36', 'de', 'name', 'Bildliches', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (278, 'E36', 'pt', 'name', 'Item Visual', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (279, 'E36', 'cn', 'name', '视觉项目', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (280, 'E36', 'en', 'comment', 'This class comprises the intellectual or conceptual aspects of recognisable marks and images.
This class does not intend to describe the idiosyncratic characteristics of an individual physical embodiment of a visual item, but the underlying prototype. For example, a mark such as the ICOM logo is generally considered to be the same logo when used on any number of publications. The size, orientation and colour may change, but the logo remains uniquely identifiable. The same is true of images that are reproduced many times. This means that visual items are independent of their physical support. 
The class E36 Visual Item provides a means of identifying and linking together instances of E24 Physical Man-Made Thing that carry the same visual symbols, marks or images etc. The property P62 depicts (is depicted by) between E24 Physical Man-Made Thing and depicted subjects (E1 CRM Entity) can be regarded as a short-cut of the more fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1CRM Entity, which in addition captures the optical features of the depiction.  
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (281, 'E37', 'ru', 'name', 'Пометка', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (282, 'E37', 'fr', 'name', 'Marque', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (283, 'E37', 'el', 'name', 'Σήμανση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (284, 'E37', 'en', 'name', 'Mark', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (285, 'E37', 'de', 'name', 'Marke', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (286, 'E37', 'pt', 'name', 'Marca', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (287, 'E37', 'cn', 'name', '标志', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (288, 'E37', 'en', 'comment', 'This class comprises symbols, signs, signatures or short texts applied to instances of E24 Physical Man-Made Thing by arbitrary techniques in order to indicate the creator, owner, dedications, purpose, etc. 
This class specifically excludes features that have no semantic significance, such as scratches or tool marks. These should be documented as instances of E25 Man-Made Feature. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (289, 'E38', 'ru', 'name', 'Изображение', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (290, 'E38', 'el', 'name', 'Εικόνα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (291, 'E38', 'de', 'name', 'Bild', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (292, 'E38', 'fr', 'name', 'Image', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (293, 'E38', 'en', 'name', 'Image', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (294, 'E38', 'pt', 'name', 'Imagem', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (295, 'E38', 'cn', 'name', '图像', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (296, 'E38', 'en', 'comment', 'This class comprises distributions of form, tone and colour that may be found on surfaces such as photos, paintings, prints and sculptures or directly on electronic media. 
The degree to which variations in the distribution of form and colour affect the identity of an instance of E38 Image depends on a given purpose. The original painting of the Mona Lisa in the Louvre may be said to bear the same instance of E38 Image as reproductions in the form of transparencies, postcards, posters or T-shirts, even though they may differ in size and carrier and may vary in tone and colour. The images in a “spot the difference” competition are not the same with respect to their context, however similar they may at first appear.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (297, 'E39', 'de', 'name', 'Akteur', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (298, 'E39', 'ru', 'name', 'Агент', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (299, 'E39', 'fr', 'name', 'Agent', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (300, 'E39', 'el', 'name', 'Δράστης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (301, 'E39', 'en', 'name', 'Actor', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (302, 'E39', 'pt', 'name', 'Agente', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (303, 'E39', 'cn', 'name', '角色', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (355, 'E47', 'fr', 'name', 'Coordonnées spatiales', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (356, 'E47', 'ru', 'name', 'Пространственные Координаты', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (357, 'E47', 'el', 'name', 'Χωρικές Συντεταγμένες', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (358, 'E47', 'de', 'name', 'Raumkoordinaten', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (359, 'E47', 'en', 'name', 'Spatial Coordinates', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (304, 'E39', 'en', 'comment', 'This class comprises people, either individually or in groups, who have the potential to perform intentional actions for which they can be held responsible. 
The CRM does not attempt to model the inadvertent actions of such actors. Individual people should be documented as instances of E21 Person, whereas groups should be documented as instances of either E74 Group or its subclass E40 Legal Body.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (305, 'E40', 'fr', 'name', 'Collectivité', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (306, 'E40', 'de', 'name', 'Juristische Person', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (307, 'E40', 'el', 'name', 'Νομικό Πρόσωπο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (308, 'E40', 'ru', 'name', 'Юридическое Лицо', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (309, 'E40', 'en', 'name', 'Legal Body', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (310, 'E40', 'pt', 'name', 'Pessoa Jurídica', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (311, 'E40', 'cn', 'name', '法律组织', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (312, 'E40', 'en', 'comment', 'This class comprises institutions or groups of people that have obtained a legal recognition as a group and can act collectively as agents.  
This means that they can perform actions, own property, create or destroy things and can be held collectively responsible for their actions like individual people. The term ''personne morale'' is often used for this in French. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (313, 'E41', 'de', 'name', 'Benennung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (314, 'E41', 'ru', 'name', 'Обозначение', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (315, 'E41', 'en', 'name', 'Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (316, 'E41', 'fr', 'name', 'Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (317, 'E41', 'el', 'name', 'Ονομασία', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (318, 'E41', 'pt', 'name', 'Designação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (319, 'E41', 'cn', 'name', '称号', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (320, 'E41', 'en', 'comment', 'This class comprises signs, either meaningful or not, or arrangements of signs following a specific syntax, that are used or can be used to refer to and identify a specific instance of some class or category within a certain context.
Instances of E41 Appellation do not identify things by their meaning, even if they happen to have one, but instead by convention, tradition, or agreement. Instances of E41 Appellation are cultural constructs; as such, they have a context, a history, and a use in time and space by some group of users. A given instance of E41 Appellation can have alternative forms, i.e., other instances of E41 Appellation that are always regarded as equivalent independent from the thing it denotes. 
Specific subclasses of E41 Appellation should be used when instances of E41 Appellation of a characteristic form are used for particular objects. Instances of E49 Time Appellation, for example, which take the form of instances of E50 Date, can be easily recognised.
E41 Appellation should not be confused with the act of naming something. Cf. E15 Identifier Assignment
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (321, 'E42', 'fr', 'name', 'Identificateur d''objet', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (322, 'E42', 'el', 'name', 'Κωδικός Αναγνώρισης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (323, 'E42', 'ru', 'name', 'Идентификатор Объекта', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (324, 'E42', 'de', 'name', 'Kennung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (325, 'E42', 'en', 'name', 'Identifier', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (326, 'E42', 'pt', 'name', 'Identificador de Objeto', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (327, 'E42', 'cn', 'name', '标识符', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (328, 'E42', 'en', 'comment', 'This class comprises strings or codes assigned to instances of E1 CRM Entity in order to identify them uniquely and permanently within the context of one or more organisations. Such codes are often known as inventory numbers, registration codes, etc. and are typically composed of alphanumeric sequences. The class E42 Identifier is not normally used for machine-generated identifiers used for automated processing unless these are also used by human agents.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (329, 'E44', 'ru', 'name', 'Обозначение Места', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (330, 'E44', 'en', 'name', 'Place Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (331, 'E44', 'fr', 'name', 'Appellation de lieu', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (332, 'E44', 'de', 'name', 'Ortsbenennung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (333, 'E44', 'el', 'name', 'Ονομασία Τόπου', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (334, 'E44', 'pt', 'name', 'Designação de Local', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (335, 'E44', 'cn', 'name', '地点称号', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (336, 'E44', 'en', 'comment', 'This class comprises any sort of identifier characteristically used to refer to an E53 Place. 
Instances of E44 Place Appellation may vary in their degree of precision and their meaning may vary over time - the same instance of E44 Place Appellation may be used to refer to several places, either because of cultural shifts, or because objects used as reference points have moved around. Instances of E44 Place Appellation can be extremely varied in form: postal addresses, instances of E47 Spatial Coordinate, and parts of buildings can all be considered as instances of E44 Place Appellation.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (337, 'E45', 'fr', 'name', 'Adresse', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (338, 'E45', 'de', 'name', 'Adresse', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (339, 'E45', 'el', 'name', 'Διεύθυνση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (340, 'E45', 'ru', 'name', 'Адрес', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (341, 'E45', 'en', 'name', 'Address', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (342, 'E45', 'pt', 'name', 'Endereço', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (343, 'E45', 'cn', 'name', '地址', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (344, 'E68', 'en', 'comment', 'This class comprises the events that result in the formal or informal termination of an E74 Group of people. 
If the dissolution was deliberate, the Dissolution event should also be instantiated as an E7 Activity.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (345, 'E69', 'ru', 'name', 'Смерть', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (346, 'E45', 'en', 'comment', 'This class comprises identifiers expressed in coding systems for places, such as postal addresses used for mailing.
An E45 Address can be considered both as the name of an E53 Place and as an E51 Contact Point for an E39 Actor. This dual aspect is reflected in the multiple inheritance. However, some forms of mailing addresses, such as a postal box, are only instances of E51 Contact Point, since they do not identify any particular Place. These should not be documented as instances of E45 Address.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (347, 'E46', 'fr', 'name', 'Désignation de section', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (348, 'E46', 'ru', 'name', 'Определение Района', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (349, 'E46', 'en', 'name', 'Section Definition', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (350, 'E46', 'de', 'name', 'Abschnittsdefinition', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (351, 'E46', 'el', 'name', 'Ονομασία Τμήματος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (352, 'E46', 'pt', 'name', 'Designação de Seção', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (353, 'E46', 'cn', 'name', '区域定义', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (354, 'E46', 'en', 'comment', 'This class comprises areas of objects referred to in terms specific to the general geometry or structure of its kind. 
The ''prow'' of the boat, the ''frame'' of the picture, the ''front'' of the building are all instances of E46 Section Definition. The class highlights the fact that parts of objects can be treated as locations. This holds in particular for features without natural boundaries, such as the “head” of a marble statue made out of one block (cf. E53 Place). In answer to the question ''where is the signature?'' one might reply ''on the lower left corner''. (Section Definition is closely related to the term “segment” in Gerstl, P.& Pribbenow, S, 1996 “ A conceptual theory of part – whole relations and its applications”, Data & Knowledge 	Engineering 20 305-322, North Holland- Elsevier ).
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (360, 'E47', 'pt', 'name', 'Coordenadas Espaciais', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (361, 'E47', 'cn', 'name', '空间坐标', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (362, 'E47', 'en', 'comment', 'This class comprises the textual or numeric information required to locate specific instances of E53 Place within schemes of spatial identification. 

Coordinates are a specific form of E44 Place Appellation, that is, a means of referring to a particular E53 Place. Coordinates are not restricted to longitude, latitude and altitude. Any regular system of reference that maps onto an E19 Physical Object can be used to generate coordinates.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (363, 'E48', 'ru', 'name', 'Название Места', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (364, 'E48', 'fr', 'name', 'Toponyme', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (365, 'E48', 'el', 'name', 'Τοπωνύμιο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (366, 'E48', 'en', 'name', 'Place Name', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (367, 'E48', 'de', 'name', 'Orts- oder Flurname', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (368, 'E48', 'pt', 'name', 'Nome de Local', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (369, 'E48', 'cn', 'name', '地名', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (370, 'E48', 'en', 'comment', 'This class comprises particular and common forms of E44 Place Appellation. 
Place Names may change their application over time: the name of an E53 Place may change, and a name may be reused for a different E53 Place. Instances of E48 Place Name are typically subject to place name gazetteers.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (371, 'E49', 'ru', 'name', 'Обозначение Времени', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (372, 'E49', 'el', 'name', 'Ονομασία Χρόνου', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (373, 'E49', 'de', 'name', 'Zeitbenennung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (374, 'E49', 'en', 'name', 'Time Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (375, 'E49', 'fr', 'name', 'Appellation temporelle', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (376, 'E49', 'pt', 'name', 'Designação de Tempo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (377, 'E49', 'cn', 'name', '时间称号', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (378, 'E49', 'en', 'comment', 'This class comprises all forms of names or codes, such as historical periods, and dates, which are characteristically used to refer to a specific E52 Time-Span. 
The instances of E49 Time Appellation may vary in their degree of precision, and they may be relative to other time frames, “Before Christ” for example. Instances of E52 Time-Span are often defined by reference to a cultural period or an event e.g. ‘the duration of the Ming Dynasty’.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (379, 'E50', 'de', 'name', 'Datum', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (380, 'E50', 'el', 'name', 'Ημερομηνία', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (381, 'E50', 'ru', 'name', 'Дата', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (382, 'E50', 'fr', 'name', 'Date', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (383, 'E50', 'en', 'name', 'Date', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (384, 'E50', 'pt', 'name', 'Data', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (385, 'E50', 'cn', 'name', '日期', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (386, 'E50', 'en', 'comment', 'This class comprises specific forms of E49 Time Appellation.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (387, 'E51', 'de', 'name', 'Kontaktpunkt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (388, 'E51', 'el', 'name', 'Στοιχείο Επικοινωνίας', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (389, 'E51', 'fr', 'name', 'Coordonnées individuelles', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (390, 'E51', 'en', 'name', 'Contact Point', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (391, 'E51', 'ru', 'name', 'Контакт', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (392, 'E51', 'pt', 'name', 'Ponto de Contato', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (393, 'E51', 'cn', 'name', '联系方式', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (394, 'E51', 'en', 'comment', 'This class comprises identifiers employed, or understood, by communication services to direct communications to an instance of E39 Actor. These include E-mail addresses, telephone numbers, post office boxes, Fax numbers, URLs etc. Most postal addresses can be considered both as instances of E44 Place Appellation and E51 Contact Point. In such cases the subclass E45 Address should be used. 
URLs are addresses used by machines to access another machine through an http request. Since the accessed machine acts on behalf of the E39 Actor providing the machine, URLs are considered as instances of E51 Contact Point to that E39 Actor.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (395, 'E52', 'fr', 'name', 'Durée', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (396, 'E52', 'de', 'name', 'Zeitspanne', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (397, 'E52', 'ru', 'name', 'Интервал Времени', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (398, 'E52', 'el', 'name', 'Χρονικό Διάστημα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (399, 'E52', 'en', 'name', 'Time-Span', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (400, 'E52', 'pt', 'name', 'Período de Tempo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (401, 'E52', 'cn', 'name', '时段', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (402, 'E69', 'en', 'name', 'Death', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (403, 'E69', 'de', 'name', 'Tod', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (404, 'E69', 'fr', 'name', 'Mort', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (405, 'E69', 'el', 'name', 'Θάνατος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (406, 'E69', 'pt', 'name', 'Morte', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (407, 'E69', 'cn', 'name', '死亡', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (408, 'E52', 'en', 'comment', 'This class comprises abstract temporal extents, in the sense of Galilean physics, having a beginning, an end and a duration. 
Time Span has no other semantic connotations. Time-Spans are used to define the temporal extent of instances of E4 Period, E5 Event and any other phenomena valid for a certain time. An E52 Time-Span may be identified by one or more instances of E49 Time Appellation. 
Since our knowledge of history is imperfect, instances of E52 Time-Span can best be considered as approximations of the actual Time-Spans of temporal entities. The properties of E52 Time-Span are intended to allow these approximations to be expressed precisely.  An extreme case of approximation, might, for example, define an E52 Time-Span having unknown beginning, end and duration. Used as a common E52 Time-Span for two events, it would nevertheless define them as being simultaneous, even if nothing else was known. 
	Automatic processing and querying of instances of E52 Time-Span is facilitated if data can be parsed into an E61 Time Primitive.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (409, 'E53', 'fr', 'name', 'Lieu', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (410, 'E53', 'en', 'name', 'Place', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (411, 'E53', 'el', 'name', 'Τόπος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (412, 'E53', 'ru', 'name', 'Место', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (413, 'E53', 'de', 'name', 'Ort', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (414, 'E53', 'pt', 'name', 'Local', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (415, 'E53', 'cn', 'name', '地点', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (461, 'E58', 'en', 'comment', 'This class is a specialization of E55 Type and comprises the types of measurement units: feet, inches, centimetres, litres, lumens, etc. 
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E58 Measurement Unit, e.g.: “instances of cm”.
Syst?me International (SI) units or internationally recognized non-SI terms should be used whenever possible. (ISO 1000:1992). Archaic Measurement Units used in historical records should be preserved.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (462, 'E63', 'fr', 'name', 'Début d''existence', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (463, 'E63', 'en', 'name', 'Beginning of Existence', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (464, 'E63', 'de', 'name', 'Daseinsbeginn', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (465, 'E63', 'el', 'name', 'Αρχή Ύπαρξης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (466, 'E63', 'ru', 'name', 'Начало Существования', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (467, 'E63', 'pt', 'name', 'Início da Existência', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (468, 'E63', 'cn', 'name', '存在开始', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (470, 'E64', 'de', 'name', 'Daseinsende', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (471, 'E64', 'ru', 'name', 'Конец Существования', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (472, 'E64', 'el', 'name', 'Τέλος Ύπαρξης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (416, 'E53', 'en', 'comment', 'This class comprises extents in space, in particular on the surface of the earth, in the pure sense of physics: independent from temporal phenomena and matter. 
The instances of E53 Place are usually determined by reference to the position of “immobile” objects such as buildings, cities, mountains, rivers, or dedicated geodetic marks. A Place can be determined by combining a frame of reference and a location with respect to this frame. It may be identified by one or more instances of E44 Place Appellation.
 It is sometimes argued that instances of E53 Place are best identified by global coordinates or absolute reference systems. However, relative references are often more relevant in the context of cultural documentation and tend to be more precise. In particular, we are often interested in position in relation to large, mobile objects, such as ships. For example, the Place at which Nelson died is known with reference to a large mobile object – H.M.S Victory. A resolution of this Place in terms of absolute coordinates would require knowledge of the movements of the vessel and the precise time of death, either of which may be revised, and the result would lack historical and cultural relevance.
Any object can serve as a frame of reference for E53 Place determination. The model foresees the notion of a "section" of an E19 Physical Object as a valid E53 Place determination.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (417, 'E54', 'en', 'name', 'Dimension', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (418, 'E54', 'fr', 'name', 'Dimensions', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (419, 'E54', 'el', 'name', 'Μέγεθος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (420, 'E54', 'ru', 'name', 'Величина', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (421, 'E54', 'de', 'name', 'Maß', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (422, 'E54', 'pt', 'name', 'Dimensão', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (423, 'E54', 'cn', 'name', '规模数量', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (424, 'E54', 'en', 'comment', 'This class comprises quantifiable properties that can be measured by some calibrated means and can be approximated by values, i.e. points or regions in a mathematical or conceptual space, such as natural or real numbers, RGB values etc.
An instance of E54 Dimension represents the true quantity, independent from its numerical approximation, e.g. in inches or in cm. The properties of the class E54 Dimension allow for expressing the numerical approximation of the values of an instance of E54 Dimension. If the true values belong to a non-discrete space, such as spatial distances, it is recommended to record them as approximations by intervals or regions of indeterminacy enclosing the assumed true values. For instance, a length of 5 cm may be recorded as 4.5-5.5 cm, according to the precision of the respective observation. Note, that interoperability of values described in different units depends critically on the representation as value regions.
Numerical approximations in archaic instances of E58 Measurement Unit used in historical records should be preserved. Equivalents corresponding to current knowledge should be recorded as additional instances of E54 Dimension as appropriate.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (425, 'E55', 'el', 'name', 'Τύπος', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (426, 'E55', 'en', 'name', 'Type', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (427, 'E55', 'fr', 'name', 'Type', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (428, 'E55', 'ru', 'name', 'Тип', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (429, 'E55', 'de', 'name', 'Typus', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (430, 'E55', 'pt', 'name', 'Tipo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (431, 'E55', 'cn', 'name', '类型', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (432, 'E55', 'en', 'comment', 'This class comprises concepts denoted by terms from thesauri and controlled vocabularies used to characterize and classify instances of CRM classes. Instances of E55 Type represent concepts  in contrast to instances of E41 Appellation which are used to name instances of CRM classes. 
E55 Type is the CRM’s interface to domain specific ontologies and thesauri. These can be represented in the CRM as subclasses of E55 Type, forming hierarchies of terms, i.e. instances of E55 Type linked via P127 has broader  term (has narrower term). Such hierarchies may be extended with additional properties. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (433, 'E56', 'fr', 'name', 'Langue', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (434, 'E56', 'ru', 'name', 'Язык', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (435, 'E56', 'en', 'name', 'Language', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (436, 'E56', 'el', 'name', 'Γλώσσα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (437, 'E56', 'de', 'name', 'Sprache', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (438, 'E56', 'pt', 'name', 'Língua', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (439, 'E56', 'cn', 'name', '语言', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (440, 'E56', 'en', 'comment', 'This class is a specialization of E55 Type and comprises the natural languages in the sense of concepts. 
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E56 Language, e.g.: “instances of  Mandarin Chinese”.
It is recommended that internationally or nationally agreed codes and terminology are used to denote instances of E56 Language, such as those defined in ISO 639:1988. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (441, 'E57', 'fr', 'name', 'Matériau', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (442, 'E57', 'el', 'name', 'Υλικό', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (443, 'E57', 'ru', 'name', 'Материал', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (444, 'E57', 'en', 'name', 'Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (445, 'E57', 'de', 'name', 'Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (446, 'E57', 'pt', 'name', 'Material', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (447, 'E57', 'cn', 'name', '材料', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (448, 'E69', 'en', 'comment', 'This class comprises the deaths of human beings. 
If a person is killed, their death should be instantiated as E69 Death and as E7 Activity. The death or perishing of other living beings should be documented using E64 End of Existence.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (449, 'E70', 'ru', 'name', '', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (450, 'E70', 'fr', 'name', 'Chose', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (451, 'E70', 'en', 'name', 'Thing', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (452, 'E70', 'el', 'name', 'Πράγμα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (453, 'E57', 'en', 'comment', 'This class is a specialization of E55 Type and comprises the concepts of materials. 
Instances of E57 Material may denote properties of matter before its use, during its use, and as incorporated in an object, such as ultramarine powder, tempera paste, reinforced concrete. Discrete pieces of raw-materials kept in museums, such as bricks, sheets of fabric, pieces of metal, should be modelled individually in the same way as other objects. Discrete used or processed pieces, such as the stones from Nefer Titi''s temple, should be modelled as parts (cf. P46 is composed of).
This type is used categorically in the model without reference to instances of it, i.e. the Model does not foresee the description of instances of instances of E57 Material, e.g.: “instances of  gold”.
It is recommended that internationally or nationally agreed codes and terminology are used.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (454, 'E58', 'fr', 'name', 'Unité de mesure', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (455, 'E58', 'en', 'name', 'Measurement Unit', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (456, 'E58', 'el', 'name', 'Μονάδα Μέτρησης', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (457, 'E58', 'de', 'name', 'Maßeinheit', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (458, 'E58', 'ru', 'name', 'Единица Измерения', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (459, 'E58', 'pt', 'name', 'Unidade de Medida', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (460, 'E58', 'cn', 'name', '测量单位', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (469, 'E63', 'en', 'comment', 'This class comprises events that bring into existence any E77 Persistent Item. 
It may be used for temporal reasoning about things (intellectual products, physical items, groups of people, living beings) beginning to exist; it serves as a hook for determination of a terminus post quem and ante quem. ', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (473, 'E64', 'fr', 'name', 'Fin d''existence', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (474, 'E64', 'en', 'name', 'End of Existence', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (475, 'E64', 'pt', 'name', 'Fim da Existência', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (476, 'E64', 'cn', 'name', '存在结束', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (477, 'E64', 'en', 'comment', 'This class comprises events that end the existence of any E77 Persistent Item. 
It may be used for temporal reasoning about things (physical items, groups of people, living beings) ceasing to exist; it serves as a hook for determination of a terminus postquem and antequem. In cases where substance from a Persistent Item continues to exist in a new form, the process would be documented by E81 Transformation.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (478, 'E65', 'el', 'name', 'Δημιουργία', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (479, 'E65', 'ru', 'name', 'Событие Творения', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (480, 'E65', 'fr', 'name', 'Création', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (481, 'E65', 'de', 'name', 'Begriffliche Schöpfung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (482, 'E65', 'en', 'name', 'Creation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (483, 'E65', 'pt', 'name', 'Criação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (484, 'E65', 'cn', 'name', '创造', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (485, 'E65', 'en', 'comment', 'This class comprises events that result in the creation of conceptual items or immaterial products, such as legends, poems, texts, music, images, movies, laws, types etc.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (486, 'E66', 'en', 'name', 'Formation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (487, 'E66', 'ru', 'name', 'Событие Формирования', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (488, 'E66', 'fr', 'name', 'Formation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (489, 'E66', 'de', 'name', 'Gruppenbildung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (490, 'E66', 'el', 'name', 'Συγκρότηση Ομάδας', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (491, 'E66', 'pt', 'name', 'Formação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (492, 'E66', 'cn', 'name', '组成', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (493, 'E66', 'en', 'comment', 'This class comprises events that result in the formation of a formal or informal E74 Group of people, such as a club, society, association, corporation or nation. 
E66 Formation does not include the arbitrary aggregation of people who do not act as a collective.
The formation of an instance of E74 Group does not mean that the group is populated with members at the time of formation. In order to express the joining of members at the time of formation, the respective activity should be simultaneously an instance of both E66 Formation and E85 Joining. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (494, 'E67', 'en', 'name', 'Birth', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (495, 'E67', 'ru', 'name', 'Рождение', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (496, 'E67', 'fr', 'name', 'Naissance', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (497, 'E67', 'de', 'name', 'Geburt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (498, 'E67', 'el', 'name', 'Γέννηση', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (499, 'E67', 'pt', 'name', 'Nascimento', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (500, 'E67', 'cn', 'name', '诞生', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (501, 'E67', 'en', 'comment', 'This class comprises the births of human beings. E67 Birth is a biological event focussing on the context of people coming into life. (E63 Beginning of Existence comprises the coming into life of any living beings). 
Twins, triplets etc. are brought into life by the same E67 Birth event. The introduction of the E67 Birth event as a documentation element allows the description of a range of family relationships in a simple model. Suitable extensions may describe more details and the complexity of motherhood with the intervention of modern medicine. In this model, the biological father is not seen as a necessary participant in the E67 Birth event.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (502, 'E68', 'ru', 'name', 'Роспуск', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (503, 'E68', 'de', 'name', 'Gruppenauflösung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (504, 'E68', 'el', 'name', 'Διάλυση Ομάδας', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (505, 'E68', 'en', 'name', 'Dissolution', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (506, 'E68', 'fr', 'name', 'Dissolution', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (507, 'E68', 'pt', 'name', 'Dissolução', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (508, 'E68', 'cn', 'name', '解散', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (509, 'E70', 'de', 'name', 'Sache', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (510, 'E70', 'pt', 'name', 'Coisa', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (511, 'E70', 'cn', 'name', '万物', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (512, 'E70', 'en', 'comment', 'This general class comprises usable discrete, identifiable, instances of E77 Persistent Item that are documented as single units. 

They can be either intellectual products or physical things, and are characterized by relative stability. They may for instance either have a solid physical form, an electronic encoding, or they may be logical concept or structure. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (513, 'E71', 'de', 'name', 'Künstliches', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (514, 'E71', 'fr', 'name', 'Chose fabriquée', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (515, 'E71', 'ru', 'name', 'Рукотворная Вещь', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (516, 'E71', 'en', 'name', 'Man-Made Thing', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (517, 'E71', 'el', 'name', 'Ανθρώπινο Δημιούργημα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (518, 'E71', 'pt', 'name', 'Coisa Fabricada', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (519, 'E71', 'cn', 'name', '人造物', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (520, 'E71', 'en', 'comment', 'This class comprises discrete, identifiable man-made items that are documented as single units. 
These items are either intellectual products or man-made physical things, and are characterized by relative stability. They may for instance have a solid physical form, an electronic encoding, or they may be logical concepts or structures.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (521, 'E72', 'fr', 'name', 'Objet juridique', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (522, 'E72', 'ru', 'name', 'Объект Права', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (523, 'E72', 'el', 'name', 'Νομικό Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (524, 'E72', 'en', 'name', 'Legal Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (525, 'E72', 'de', 'name', 'Rechtsobjekt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (526, 'E72', 'pt', 'name', 'Objeto Jurídico', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (527, 'E72', 'cn', 'name', '法律物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (528, 'E72', 'en', 'comment', 'This class comprises those material or immaterial items to which instances of E30 Right, such as the right of ownership or use, can be applied. 
This is true for all E18 Physical Thing. In the case of instances of E28 Conceptual Object, however, the identity of the E28 Conceptual Object or the method of its use may be too ambiguous to reliably establish instances of E30 Right, as in the case of taxa and inspirations. Ownership of corporations is currently regarded as out of scope of the CRM. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (529, 'E73', 'de', 'name', 'Informationsgegenstand', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (530, 'E73', 'en', 'name', 'Information Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (531, 'E73', 'el', 'name', 'Πληροφοριακό Αντικείμενο', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (532, 'E73', 'fr', 'name', 'Objet d''information', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (533, 'E73', 'ru', 'name', 'Информационный Объект', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (534, 'E73', 'pt', 'name', 'Objeto de Informação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (535, 'E73', 'cn', 'name', '信息物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (575, 'E79', 'pt', 'name', 'Adição de Parte', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (576, 'E79', 'cn', 'name', '部件增加', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (625, 'E86', 'en', 'comment', 'This class comprises the activities that result in an instance of E39 Actor to be disassociated from an instance of E74 Group. This class does not imply initiative by either party. 
Typical scenarios include the termination of membership in a social organisation, ending the employment at a company, divorce, and the end of tenure of somebody in an official position.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (626, 'E87', 'de', 'name', 'Kuratorische Tätigkeit', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (536, 'E73', 'en', 'comment', 'This class comprises identifiable immaterial items, such as a poems, jokes, data sets, images, texts, multimedia objects, procedural prescriptions, computer program code, algorithm or mathematical formulae, that have an objectively recognizable structure and are documented as single units. 
An E73 Information Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously.
Instances of E73 Information Object of a linguistic nature should be declared as instances of the E33 Linguistic Object subclass. Instances of E73 Information Object of a documentary nature should be declared as instances of the E31 Document subclass. Conceptual items such as types and classes are not instances of E73 Information Object, nor are ideas without a reproducible expression. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (537, 'E74', 'ru', 'name', 'Группа', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (538, 'E74', 'en', 'name', 'Group', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (539, 'E74', 'el', 'name', 'Ομάδα', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (540, 'E74', 'de', 'name', 'Menschliche Gruppe', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (541, 'E74', 'fr', 'name', 'Groupe', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (542, 'E74', 'pt', 'name', 'Grupo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (543, 'E74', 'cn', 'name', '群组', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (544, 'E74', 'en', 'comment', 'This class comprises any gatherings or organizations of two or more people that act collectively or in a similar way due to any form of unifying relationship. In the wider sense this class also comprises official positions which used to be regarded in certain contexts as one actor, independent of the current holder of the office, such as the president of a country. 
A gathering of people becomes an E74 Group when it exhibits organizational characteristics usually typified by a set of ideas or beliefs held in common, or actions performed together. These might be communication, creating some common artifact, a common purpose such as study, worship, business, sports, etc. Nationality can be modeled as membership in an E74 Group (cf. HumanML markup). Married couples and other concepts of family are regarded as particular examples of E74 Group.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (545, 'E75', 'fr', 'name', 'Appellation d''objet conceptuel', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (546, 'E75', 'ru', 'name', 'Обозначение Концептуального Объекта', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (547, 'E75', 'de', 'name', 'Begriff- oder Konzeptbenennung ', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (548, 'E75', 'en', 'name', 'Conceptual Object Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (549, 'E75', 'el', 'name', 'Ονομασία Νοητικού Αντικειμένου', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (550, 'E75', 'pt', 'name', 'Designação de Objeto Conceitual', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (551, 'E75', 'cn', 'name', '概念物件称号', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (552, 'E75', 'en', 'comment', 'This class comprises all appellations specific to intellectual products or standardized patterns.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (553, 'E77', 'en', 'name', 'Persistent Item', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (554, 'E77', 'ru', 'name', 'Постоянная Сущность', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (555, 'E77', 'de', 'name', 'Seiendes', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (556, 'E77', 'el', 'name', 'Ον', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (557, 'E77', 'fr', 'name', 'Entité persistante', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (558, 'E77', 'pt', 'name', 'Entidade Persistente', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (559, 'E77', 'cn', 'name', '持续性项目', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (560, 'E81', 'en', 'comment', 'This class comprises the events that result in the simultaneous destruction of one or more than one E77 Persistent Item and the creation of one or more than one E77 Persistent Item that preserves recognizable substance from the first one(s) but has fundamentally different nature and identity. 
Although the old and the new instances of E77 Persistent Item are treated as discrete entities having separate, unique identities, they are causally connected through the E81 Transformation; the destruction of the old E77 Persistent Item(s) directly causes the creation of the new one(s) using or preserving some relevant substance. Instances of E81 Transformation are therefore distinct from re-classifications (documented using E17 Type Assignment) or modifications (documented using E11 Modification) of objects that do not fundamentally change their nature or identity. Characteristic cases are reconstructions and repurposing of historical buildings or ruins, fires leaving buildings in ruins, taxidermy of specimen in natural history and the reorganization of a corporate body into a new one.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (561, 'E77', 'en', 'comment', 'This class comprises items that have a persistent identity, sometimes known as “endurants” in philosophy. 
They can be repeatedly recognized within the duration of their existence by identity criteria rather than by continuity or observation. Persistent Items can be either physical entities, such as people, animals or things, or conceptual entities such as ideas, concepts, products of the imagination or common names.
The criteria that determine the identity of an item are often difficult to establish -; the decision depends largely on the judgement of the observer. For example, a building is regarded as no longer existing if it is dismantled and the materials reused in a different configuration. On the other hand, human beings go through radical and profound changes during their life-span, affecting both material composition and form, yet preserve their identity by other criteria. Similarly, inanimate objects may be subject to exchange of parts and matter. The class E77 Persistent Item does not take any position about the nature of the applicable identity criteria and if actual knowledge about identity of an instance of this class exists. There may be cases, where the identity of an E77 Persistent Item is not decidable by a certain state of knowledge.
The main classes of objects that fall outside the scope the E77 Persistent Item class are temporal objects such as periods, events and acts, and descriptive properties. ', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (562, 'E78', 'ru', 'name', 'Коллекция', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (563, 'E78', 'el', 'name', 'Συλλογή', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (564, 'E78', 'fr', 'name', 'Collection', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (565, 'E78', 'en', 'name', 'Collection', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (566, 'E78', 'de', 'name', 'Sammlung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (567, 'E78', 'pt', 'name', 'Coleção', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (568, 'E78', 'cn', 'name', '收藏', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (569, 'E78', 'en', 'comment', 'This class comprises aggregations of instances of E18 Physical Thing that are assembled and maintained (“curated” and “preserved,” in museological terminology) by one or more instances of E39 Actor over time for a specific purpose and audience, and according to a particular collection development plan.  
Items may be added or removed from an E78 Collection in pursuit of this plan. This class should not be confused with the E39 Actor maintaining the E78 Collection often referred to with the name of the E78 Collection (e.g. “The Wallace Collection decided…”).
Collective objects in the general sense, like a tomb full of gifts, a folder with stamps or a set of chessmen, should be documented as instances of E19 Physical Object, and not as instances of E78 Collection. This is because they form wholes either because they are physically bound together or because they are kept together for their functionality.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (570, 'E79', 'fr', 'name', 'Addition d''élément', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (571, 'E79', 'en', 'name', 'Part Addition', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (572, 'E79', 'de', 'name', 'Teilhinzufügung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (573, 'E79', 'ru', 'name', 'Добавление Части', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (574, 'E79', 'el', 'name', 'Προσθήκη Μερών', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (577, 'E79', 'en', 'comment', 'This class comprises activities that result in an instance of E24 Physical Man-Made Thing being increased, enlarged or augmented by the addition of a part. 
Typical scenarios include the attachment of an accessory, the integration of a component, the addition of an element to an aggregate object, or the accessioning of an object into a curated E78 Collection. Objects to which parts are added are, by definition, man-made, since the addition of a part implies a human activity. Following the addition of parts, the resulting man-made assemblages are treated objectively as single identifiable wholes, made up of constituent or component parts bound together either physically (for example the engine becoming a part of the car), or by sharing a common purpose (such as the 32 chess pieces that make up a chess set). This class of activities forms a basis for reasoning about the history and continuity of identity of objects that are integrated into other objects over time, such as precious gemstones being repeatedly incorporated into different items of jewellery, or cultural artifacts being added to different museum instances of E78 Collection over their lifespan.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (578, 'E80', 'de', 'name', 'Teilentfernung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (579, 'E80', 'fr', 'name', 'Soustraction d''élément', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (580, 'E80', 'en', 'name', 'Part Removal', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (581, 'E80', 'ru', 'name', 'Удаление Части', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (582, 'E80', 'el', 'name', 'Αφαίρεση Μερών', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (583, 'E80', 'pt', 'name', 'Remoção de Parte', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (584, 'E80', 'cn', 'name', '部件删除', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (585, 'E80', 'en', 'comment', 'This class comprises the activities that result in an instance of E18 Physical Thing being decreased by the removal of a part.
Typical scenarios include the detachment of an accessory, the removal of a component or part of a composite object, or the deaccessioning of an object from a curated E78 Collection. If the E80 Part Removal results in the total decomposition of the original object into pieces, such that the whole ceases to exist, the activity should instead be modelled as an E81 Transformation, i.e. a simultaneous destruction and production. In cases where the part removed has no discernible identity prior to its removal but does have an identity subsequent to its removal, the activity should be regarded as both E80 Part Removal and E12 Production. This class of activities forms a basis for reasoning about the history, and continuity of identity over time, of objects that are removed from other objects, such as precious gemstones being extracted from different items of jewelry, or cultural artifacts being deaccessioned from different museum collections over their lifespan.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (586, 'E81', 'ru', 'name', 'Трансформация', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (587, 'E81', 'en', 'name', 'Transformation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (588, 'E81', 'fr', 'name', 'Transformation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (589, 'E81', 'de', 'name', 'Umwandlung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (590, 'E81', 'el', 'name', 'Μετατροπή', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (591, 'E81', 'pt', 'name', 'Transformação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (592, 'E81', 'cn', 'name', '转变', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (593, 'E82', 'en', 'name', 'Actor Appellation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (594, 'E82', 'ru', 'name', 'Обозначение Агента', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (595, 'E82', 'el', 'name', 'Ονομασία Δράστη', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (596, 'E82', 'fr', 'name', 'Appellation d''agent', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (597, 'E82', 'de', 'name', 'Akteurbenennung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (598, 'E82', 'pt', 'name', 'Designação de Agente', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (599, 'E82', 'cn', 'name', '角色称号', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (600, 'E59', 'de', 'name', 'Primitiver Wert', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (601, 'E82', 'en', 'comment', 'This class comprises any sort of name, number, code or symbol characteristically used to identify an E39 Actor. 
An E39 Actor will typically have more than one E82 Actor Appellation, and instances of E82 Actor Appellation in turn may have alternative representations. The distinction between corporate and personal names, which is particularly important in library applications, should be made by explicitly linking the E82 Actor Appellation to an instance of either E21 Person or E74 Group/E40 Legal Body. If this is not possible, the distinction can be made through the use of the P2 has type mechanism. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (602, 'E83', 'de', 'name', 'Typuserfindung', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (603, 'E83', 'ru', 'name', 'Создание Типа', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (604, 'E83', 'en', 'name', 'Type Creation', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (605, 'E83', 'fr', 'name', 'Création de type', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (606, 'E83', 'el', 'name', 'Δημιουργία Τύπου', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (607, 'E83', 'pt', 'name', 'Criação de Tipo', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (608, 'E83', 'cn', 'name', '类型创造', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (609, 'E83', 'en', 'comment', 'This class comprises activities formally defining new types of items. 
It is typically a rigorous scholarly or scientific process that ensures a type is exhaustively described and appropriately named. In some cases, particularly in archaeology and the life sciences, E83 Type Creation requires the identification of an exemplary specimen and the publication of the type definition in an appropriate scholarly forum. The activity of E83 Type Creation is central to research in the life sciences, where a type would be referred to as a “taxon,” the type description as a “protologue,” and the exemplary specimens as “orgininal element” or “holotype”.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (610, 'E84', 'el', 'name', 'Φορέας Πληροφορίας', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (611, 'E84', 'en', 'name', 'Information Carrier', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (612, 'E84', 'ru', 'name', 'Носитель Информации', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (613, 'E84', 'fr', 'name', 'Support d''information', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (614, 'E84', 'de', 'name', 'Informationsträger', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (615, 'E84', 'pt', 'name', 'Suporte de Informação', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (616, 'E84', 'cn', 'name', '信息载体', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (617, 'E84', 'en', 'comment', 'This class comprises all instances of E22 Man-Made Object that are explicitly designed to act as persistent physical carriers for instances of E73 Information Object. 
This allows a relationship to be asserted between an E19 Physical Object and its immaterial information contents. An E84 Information Carrier may or may not contain information, e.g., a diskette. Note that any E18 Physical Thing may carry information, such as an E34 Inscription. However, unless it was specifically designed for this purpose, it is not an Information Carrier. Therefore the property P128 carries (is carried by) applies to E18 Physical Thing in general.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (618, 'E85', 'de', 'name', 'Beitritt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (619, 'E85', 'en', 'name', 'Joining', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (620, 'E85', 'cn', 'name', '加入', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (621, 'E85', 'en', 'comment', 'This class comprises the activities that result in an instance of E39 Actor becoming a member of an instance of E74 Group. This class does not imply initiative by either party.
Typical scenarios include becoming a member of a social organisation, becoming employee of a company, marriage, the adoption of a child by a family and the inauguration of somebody into an official position. 
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (622, 'E86', 'de', 'name', 'Austritt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (623, 'E86', 'en', 'name', 'Leaving', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (624, 'E86', 'cn', 'name', '脱离', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (627, 'E87', 'en', 'name', 'Curation Activity', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (628, 'E87', 'cn', 'name', '典藏管理', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (629, 'E87', 'en', 'comment', 'This class comprises the activities that result in the continuity of management and the preservation and evolution of instances of E78 Collection, following an implicit or explicit curation plan. 
It specializes the notion of activity into the curation of a collection and allows the history of curation to be recorded.
Items are accumulated and organized following criteria like subject, chronological period, material type, style of art etc. and can be added or removed from an E78 Collection for a specific purpose and/or audience. The initial aggregation of items of a collection is regarded as an instance of E12 Production Event while the activity of evolving, preserving and promoting a collection is regarded as an instance of E87 Curation Activity.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (630, 'E89', 'de', 'name', 'Aussagenobjekt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (631, 'E89', 'en', 'name', 'Propositional Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (632, 'E89', 'cn', 'name', '陈述性物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (633, 'E89', 'en', 'comment', 'This class comprises immaterial items, including but not limited to stories, plots, procedural prescriptions, algorithms, laws of physics or images that are, or represent in some sense, sets of propositions about real or imaginary things and that are documented as single units or serve as topics of discourse. 
	
This class also comprises items that are “about” something in the sense of a subject. In the wider sense, this class includes expressions of psychological value such as non-figural art and musical themes. However, conceptual items such as types and classes are not instances of E89 Propositional Object. This should not be confused with the definition of a type, which is indeed an instance of E89 Propositional Object.
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (634, 'E90', 'de', 'name', 'Symbolisches Objekt', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (635, 'E90', 'en', 'name', 'Symbolic Object', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (636, 'E90', 'cn', 'name', '符号物件', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (637, 'E90', 'en', 'comment', 'This class comprises identifiable symbols and any aggregation of symbols, such as characters, identifiers, traffic signs, emblems, texts, data sets, images, musical scores, multimedia objects, computer program code or mathematical formulae that have an objectively recognizable structure and that are documented as single units.
	It includes sets of signs of any nature, which may serve to designate something, or to communicate some propositional content.
	An instance of E90 Symbolic Object does not depend on a specific physical carrier, which can include human memory, and it can exist on one or more carriers simultaneously. An instance of E90 Symbolic Object may or may not have a specific meaning, for example an arbitrary character string.
	In some cases, the content of an instance of E90 Symbolic Object may completely be represented by a serialized content model, such.. as the property P3 has note allows for describing this content model…P3.1 has type: E55 Type to specify the encoding..
', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (638, 'E59', 'en', 'name', 'Primitive Value', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (639, 'E59', 'en', 'comment', 'This class comprises primitive values used as documentation elements, which are not further elaborated upon within the model. As such they are not considered as elements within our universe of discourse. No specific implementation recommendations are made. It is recommended that the primitive value system from the implementation platform be used to substitute for this class and its subclasses.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (640, 'E60', 'en', 'name', 'Number', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (641, 'E60', 'de', 'name', 'Zahl', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (642, 'E60', 'en', 'comment', 'This class comprises any encoding of computable (algebraic) values such as integers, real numbers, complex numbers, vectors, tensors etc., including intervals of these values to express limited precision. Numbers are fundamentally distinct from identifiers in continua, such as instances of E50 Date and E47 Spatial Coordinate, even though their encoding may be similar. Instances of E60 Number can be combined with each other in algebraic operations to yield other instances of E60 Number, e.g., 1+1=2. Identifiers in continua may be combined with numbers expressing distances to yield new identifiers, e.g., 1924-01-31 + 2 days = 1924-02-02. Cf. E54 Dimension', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (643, 'E61', 'en', 'name', 'Time Primitive', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (644, 'E61', 'de', 'name', 'Zeitprimitiv', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (645, 'E61', 'en', 'comment', 'This class comprises instances of E59 Primitive Value for time that should be implemented with appropriate validation, precision and interval logic to express date ranges relevant to cultural documentation. E61 Time Primitive is not further elaborated upon within the model.', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (646, 'E62', 'en', 'name', 'String', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (647, 'E62', 'de', 'name', 'Zeichenkette', '2017-11-28 16:35:09.762308', NULL);
INSERT INTO class_i18n VALUES (648, 'E62', 'en', 'comment', 'This class comprises the instances of E59 Primitive Values used for documentation such as free text strings, bitmaps, vector graphics, etc. E62 String is not further elaborated upon within the model', '2017-11-28 16:35:09.762308', NULL);


--
-- Name: class_i18n_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('class_i18n_id_seq', 648, true);


--
-- Name: class_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('class_id_seq', 86, true);


--
-- Data for Name: class_inheritance; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO class_inheritance VALUES (1, 'E1', 'E2', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (2, 'E2', 'E3', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (3, 'E2', 'E4', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (4, 'E4', 'E5', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (5, 'E64', 'E6', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (6, 'E5', 'E7', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (7, 'E7', 'E8', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (8, 'E7', 'E9', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (9, 'E7', 'E10', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (10, 'E7', 'E11', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (11, 'E11', 'E12', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (12, 'E63', 'E12', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (13, 'E7', 'E13', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (14, 'E13', 'E14', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (15, 'E13', 'E15', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (16, 'E13', 'E16', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (17, 'E13', 'E17', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (18, 'E72', 'E18', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (19, 'E18', 'E19', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (20, 'E19', 'E20', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (21, 'E20', 'E21', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (22, 'E39', 'E21', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (23, 'E19', 'E22', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (24, 'E24', 'E22', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (25, 'E18', 'E24', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (26, 'E71', 'E24', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (27, 'E24', 'E25', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (28, 'E26', 'E25', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (29, 'E18', 'E26', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (30, 'E26', 'E27', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (31, 'E71', 'E28', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (32, 'E73', 'E29', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (33, 'E89', 'E30', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (34, 'E73', 'E31', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (35, 'E31', 'E32', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (36, 'E73', 'E33', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (37, 'E33', 'E34', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (38, 'E37', 'E34', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (39, 'E33', 'E35', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (40, 'E41', 'E35', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (41, 'E73', 'E36', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (42, 'E36', 'E37', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (43, 'E36', 'E38', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (44, 'E77', 'E39', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (45, 'E74', 'E40', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (46, 'E90', 'E41', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (47, 'E41', 'E42', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (48, 'E41', 'E44', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (49, 'E44', 'E45', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (50, 'E51', 'E45', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (51, 'E44', 'E46', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (52, 'E44', 'E47', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (53, 'E44', 'E48', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (54, 'E41', 'E49', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (55, 'E49', 'E50', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (56, 'E41', 'E51', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (57, 'E1', 'E52', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (58, 'E1', 'E53', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (59, 'E1', 'E54', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (60, 'E28', 'E55', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (61, 'E55', 'E56', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (62, 'E55', 'E57', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (63, 'E55', 'E58', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (64, 'E5', 'E63', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (65, 'E5', 'E64', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (66, 'E7', 'E65', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (67, 'E63', 'E65', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (68, 'E7', 'E66', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (69, 'E63', 'E66', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (70, 'E63', 'E67', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (71, 'E64', 'E68', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (72, 'E64', 'E69', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (73, 'E77', 'E70', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (74, 'E70', 'E71', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (75, 'E70', 'E72', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (76, 'E89', 'E73', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (77, 'E90', 'E73', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (78, 'E39', 'E74', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (79, 'E41', 'E75', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (80, 'E1', 'E77', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (81, 'E24', 'E78', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (82, 'E11', 'E79', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (83, 'E11', 'E80', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (84, 'E63', 'E81', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (85, 'E64', 'E81', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (86, 'E41', 'E82', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (87, 'E65', 'E83', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (88, 'E22', 'E84', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (89, 'E7', 'E85', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (90, 'E7', 'E86', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (91, 'E7', 'E87', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (92, 'E28', 'E89', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (93, 'E28', 'E90', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (94, 'E72', 'E90', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (95, 'E59', 'E60', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (96, 'E59', 'E61', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO class_inheritance VALUES (97, 'E59', 'E62', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');


--
-- Name: class_inheritance_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('class_inheritance_id_seq', 97, true);


--
-- Data for Name: property; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO property VALUES (1, 'P1', 'E41', 'E1', 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (2, 'P2', 'E55', 'E1', 'has type', 'is type of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (3, 'P3', 'E63', 'E1', 'has note', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (4, 'P4', 'E52', 'E2', 'has time-span', 'is time-span of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (5, 'P5', 'E3', 'E3', 'consists of', 'forms part of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (6, 'P7', 'E53', 'E4', 'took place at', 'witnessed', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (7, 'P8', 'E18', 'E4', 'took place on or within', 'witnessed', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (8, 'P9', 'E4', 'E4', 'consists of', 'forms part of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (9, 'P10', 'E4', 'E4', 'falls within', 'contains', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (10, 'P11', 'E39', 'E5', 'had participant', 'participated in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (11, 'P12', 'E77', 'E5', 'occurred in the presence of', 'was present at', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (12, 'P13', 'E18', 'E6', 'destroyed', 'was destroyed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (13, 'P14', 'E39', 'E7', 'carried out by', 'performed', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (14, 'P15', 'E1', 'E7', 'was influenced by', 'influenced', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (15, 'P16', 'E70', 'E7', 'used specific object', 'was used for', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (16, 'P17', 'E1', 'E7', 'was motivated by', 'motivated', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (17, 'P19', 'E71', 'E7', 'was intended use of', 'was made for', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (18, 'P20', 'E5', 'E7', 'had specific purpose', 'was purpose of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (19, 'P21', 'E55', 'E7', 'had general purpose', 'was purpose of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (20, 'P22', 'E39', 'E8', 'transferred title to', 'acquired title through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (21, 'P23', 'E39', 'E8', 'transferred title from', 'surrendered title through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (22, 'P24', 'E18', 'E8', 'transferred title of', 'changed ownership through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (23, 'P25', 'E19', 'E9', 'moved', 'moved by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (24, 'P26', 'E53', 'E9', 'moved to', 'was destination of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (25, 'P27', 'E53', 'E9', 'moved from', 'was origin of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (26, 'P28', 'E39', 'E10', 'custody surrendered by', 'surrendered custody through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (27, 'P29', 'E39', 'E10', 'custody received by', 'received custody through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (28, 'P30', 'E18', 'E10', 'transferred custody of', 'custody transferred through', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (29, 'P31', 'E24', 'E11', 'has modified', 'was modified by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (30, 'P32', 'E55', 'E7', 'used general technique', 'was technique of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (31, 'P33', 'E29', 'E7', 'used specific technique', 'was used by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (32, 'P34', 'E18', 'E14', 'concerned', 'was assessed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (33, 'P35', 'E3', 'E14', 'has identified', 'was identified by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (34, 'P37', 'E42', 'E15', 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (35, 'P38', 'E42', 'E15', 'deassigned', 'was deassigned by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (36, 'P39', 'E1', 'E16', 'measured', 'was measured by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (37, 'P40', 'E54', 'E16', 'observed dimension', 'was observed in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (38, 'P41', 'E1', 'E17', 'classified', 'was classified by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (39, 'P42', 'E55', 'E17', 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (40, 'P43', 'E54', 'E70', 'has dimension', 'is dimension of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (41, 'P44', 'E3', 'E18', 'has condition', 'is condition of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (42, 'P45', 'E57', 'E18', 'consists of', 'is incorporated in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (43, 'P46', 'E18', 'E18', 'is composed of', 'forms part of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (44, 'P48', 'E42', 'E1', 'has preferred identifier', 'is preferred identifier of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (45, 'P49', 'E39', 'E18', 'has former or current keeper', 'is former or current keeper of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (46, 'P50', 'E39', 'E18', 'has current keeper', 'is current keeper of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (47, 'P51', 'E39', 'E18', 'has former or current owner', 'is former or current owner of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (48, 'P52', 'E39', 'E18', 'has current owner', 'is current owner of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (49, 'P53', 'E53', 'E18', 'has former or current location', 'is former or current location of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (50, 'P54', 'E53', 'E19', 'has current permanent location', 'is current permanent location of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (51, 'P55', 'E53', 'E19', 'has current location', 'currently holds', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (52, 'P56', 'E26', 'E19', 'bears feature', 'is found on', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (53, 'P57', 'E26', 'E19', 'has number of parts', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (54, 'P58', 'E46', 'E18', 'has section definition', 'defines section', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (55, 'P59', 'E53', 'E18', 'has section', 'is located on or within', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (56, 'P62', 'E1', 'E24', 'depicts', 'is depicted by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (57, 'P65', 'E36', 'E24', 'shows visual item', 'is shown by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (58, 'P67', 'E1', 'E89', 'refers to', 'is referred to by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (59, 'P68', 'E57', 'E29', 'foresees use of', 'use foreseen by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (60, 'P69', 'E29', 'E29', 'is associated with', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (61, 'P70', 'E1', 'E31', 'documents', 'is documented in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (62, 'P71', 'E1', 'E32', 'lists', 'is listed in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (63, 'P72', 'E56', 'E33', 'has language', 'is language of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (64, 'P73', 'E33', 'E33', 'has translation', 'is translation of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (65, 'P74', 'E53', 'E39', 'has current or former residence', 'is current or former residence of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (66, 'P75', 'E30', 'E39', 'possesses', 'is possessed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (67, 'P76', 'E51', 'E39', 'has contact point', 'provides access to', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (68, 'P78', 'E49', 'E52', 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (69, 'P79', 'E62', 'E52', 'beginning is qualified by', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (70, 'P80', 'E62', 'E52', 'end is qualified by', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (71, 'P81', 'E61', 'E52', 'ongoing throughout', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (72, 'P82', 'E61', 'E52', 'at some time within', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (73, 'P83', 'E54', 'E52', 'had at least duration', 'was minimum duration of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (74, 'P84', 'E54', 'E52', 'had at most duration', 'was maximum duration of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (75, 'P86', 'E52', 'E52', 'falls within', 'contains', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (76, 'P87', 'E44', 'E53', 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (77, 'P89', 'E53', 'E53', 'falls within', 'contains', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (78, 'P90', 'E60', 'E54', 'has value', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (79, 'P91', 'E58', 'E54', 'has unit', 'is unit of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (80, 'P92', 'E77', 'E63', 'brought into existence', 'was brought into existence by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (81, 'P93', 'E77', 'E64', 'took out of existence', 'was taken out of existence by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (82, 'P94', 'E28', 'E65', 'has created', 'was created by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (83, 'P95', 'E74', 'E66', 'has formed', 'was formed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (84, 'P96', 'E21', 'E67', 'by mother', 'gave birth', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (85, 'P97', 'E21', 'E67', 'from father', 'was father for', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (86, 'P98', 'E21', 'E67', 'brought into life', 'was born', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (87, 'P99', 'E74', 'E68', 'dissolved', 'was dissolved by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (88, 'P100', 'E21', 'E69', 'was death of', 'died in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (89, 'P101', 'E55', 'E70', 'had as general use', 'was use of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (90, 'P102', 'E35', 'E71', 'has title', 'is title of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (91, 'P103', 'E55', 'E71', 'was intended for', 'was intention of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (92, 'P104', 'E30', 'E72', 'is subject to', 'applies to', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (93, 'P105', 'E39', 'E72', 'right held by', 'has right on', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (94, 'P106', 'E90', 'E90', 'is composed of', 'forms part of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (95, 'P107', 'E39', 'E74', 'has current or former member', 'is current or former member of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (96, 'P108', 'E24', 'E12', 'has produced', 'was produced by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (97, 'P109', 'E39', 'E78', 'has current or former curator', 'is current or former curator of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (98, 'P110', 'E24', 'E79', 'augmented', 'was augmented by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (99, 'P111', 'E18', 'E79', 'added', 'was added by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (100, 'P112', 'E24', 'E80', 'diminished', 'was diminished by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (101, 'P113', 'E18', 'E80', 'removed', 'was removed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (102, 'P114', 'E2', 'E2', 'is equal in time to', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (103, 'P115', 'E2', 'E2', 'finishes', 'is finished by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (104, 'P116', 'E2', 'E2', 'starts', 'is started by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (105, 'P117', 'E2', 'E2', 'occurs during', 'includes', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (106, 'P118', 'E2', 'E2', 'overlaps in time with', 'is overlapped in time by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (107, 'P119', 'E2', 'E2', 'meets in time with', 'is met in time by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (108, 'P120', 'E2', 'E2', 'occurs before', 'occurs after', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (109, 'P121', 'E53', 'E53', 'overlaps with', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (110, 'P122', 'E53', 'E53', 'borders with', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (111, 'P123', 'E77', 'E81', 'resulted in', 'resulted from', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (112, 'P124', 'E77', 'E81', 'transformed', 'was transformed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (113, 'P125', 'E55', 'E7', 'used object of type', 'was type of object used in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (114, 'P126', 'E57', 'E11', 'employed', 'was employed in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (115, 'P127', 'E55', 'E55', 'has broader term', 'has narrower term', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (116, 'P128', 'E90', 'E24', 'carries', 'is carried by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (117, 'P129', 'E1', 'E89', 'is about', 'is subject of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (118, 'P130', 'E70', 'E70', 'shows features of', 'features are also found on', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (119, 'P131', 'E82', 'E39', 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (120, 'P132', 'E4', 'E4', 'overlaps with', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (121, 'P133', 'E4', 'E4', 'is separated from', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (122, 'P134', 'E7', 'E7', 'continued', 'was continued by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (123, 'P135', 'E55', 'E83', 'created type', 'was created by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (124, 'P136', 'E1', 'E83', 'was based on', 'supported type creation', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (125, 'P137', 'E55', 'E1', 'exemplifies', 'is exemplified by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (126, 'P138', 'E1', 'E36', 'represents', 'has representation', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (127, 'P139', 'E41', 'E41', 'has alternative form', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (128, 'P140', 'E1', 'E13', 'assigned attribute to', 'was attributed by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (129, 'P141', 'E1', 'E13', 'assigned', 'was assigned by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (130, 'P142', 'E90', 'E15', 'used constituent', 'was used in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (131, 'P143', 'E39', 'E85', 'joined', 'was joined by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (132, 'P144', 'E74', 'E85', 'joined with', 'gained member by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (133, 'P145', 'E39', 'E86', 'separated', 'left by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (134, 'P146', 'E74', 'E86', 'separated from', 'lost member by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (135, 'P147', 'E78', 'E87', 'curated', 'was curated by', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (136, 'P148', 'E89', 'E89', 'has component', 'is component of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (137, 'P149', 'E75', 'E28', 'is identified by', 'identifies', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (138, 'P150', 'E55', 'E55', 'defines typical parts of', 'defines typical wholes for', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (139, 'P151', 'E74', 'E66', 'was formed from', 'participated in', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (140, 'P152', 'E21', 'E21', 'has parent', 'is parent of', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (141, 'OA1', 'E61', 'E77', 'begins chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (142, 'OA2', 'E61', 'E77', 'ends chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (143, 'OA3', 'E61', 'E21', 'born chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (144, 'OA4', 'E61', 'E21', 'died chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (145, 'OA5', 'E61', 'E2', 'begins chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (146, 'OA6', 'E61', 'E2', 'ends chronologically', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (147, 'OA7', 'E39', 'E39', 'has relationship to', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (148, 'OA8', 'E53', 'E77', 'appears for the first time in', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property VALUES (149, 'OA9', 'E53', 'E77', 'appears for the last time in', NULL, '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');


--
-- Data for Name: property_i18n; Type: TABLE DATA; Schema: model; Owner: blade
--

INSERT INTO property_i18n VALUES (1234, 'P4', 'en', 'name', 'has time-span', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1235, 'P4', 'de', 'name', 'hat Zeitspanne', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1236, 'P4', 'el', 'name', 'βρισκόταν σε εξέλιξη', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1237, 'P1', 'el', 'name', 'αναγνωρίζεται ως', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1238, 'P1', 'de', 'name', 'wird bezeichnet als', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1239, 'P1', 'en', 'name', 'is identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1240, 'P1', 'ru', 'name', 'идентифицируется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1241, 'P1', 'fr', 'name', 'est identifiée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1242, 'P1', 'pt', 'name', 'é identificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1243, 'P1', 'cn', 'name', '有识别称号', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1244, 'P1', 'de', 'name_inverse', 'bezeichnet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1245, 'P1', 'ru', 'name_inverse', 'идентифицирует', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1246, 'P1', 'fr', 'name_inverse', 'identifie', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1247, 'P1', 'el', 'name_inverse', 'είναι αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1248, 'P1', 'en', 'name_inverse', 'identifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1249, 'P1', 'pt', 'name_inverse', 'identifica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1250, 'P1', 'cn', 'name_inverse', '被用来识别', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1251, 'P1', 'en', 'comment', 'This property describes the naming or identification of any real world item by a name or any other identifier. 
This property is intended for identifiers in general use, which form part of the world the model intends to describe, and not merely for internal database identifiers which are specific to a technical system, unless these latter also have a more general use outside the technical context. This property includes in particular identification by mathematical expressions such as coordinate systems used for the identification of instances of E53 Place. The property does not reveal anything about when, where and by whom this identifier was used. A more detailed representation can be made using the fully developed (i.e. indirect) path through E15 Identifier Assignment.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1252, 'P2', 'de', 'name', 'hat den Typus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1253, 'P2', 'en', 'name', 'has type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1254, 'P2', 'el', 'name', 'έχει τύπο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1255, 'P2', 'fr', 'name', 'est de type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1256, 'P2', 'ru', 'name', 'имеет тип', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1257, 'P2', 'pt', 'name', 'é do tipo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1258, 'P2', 'cn', 'name', '有类型', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1259, 'P2', 'ru', 'name_inverse', 'является типом для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1260, 'P2', 'fr', 'name_inverse', 'est le type de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1261, 'P2', 'el', 'name_inverse', 'είναι ο τύπος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1262, 'P2', 'de', 'name_inverse', 'ist Typus von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1263, 'P2', 'en', 'name_inverse', 'is type of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1264, 'P2', 'pt', 'name_inverse', 'é o tipo de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1265, 'P2', 'cn', 'name_inverse', '被用来分类', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1266, 'P2', 'en', 'comment', 'This property allows sub typing of CRM entities - a form of specialisation – through the use of a terminological hierarchy, or thesaurus. 
The CRM is intended to focus on the high-level entities and relationships needed to describe data structures. Consequently, it does not specialise entities any further than is required for this immediate purpose. However, entities in the isA hierarchy of the CRM may by specialised into any number of sub entities, which can be defined in the E55 Type hierarchy. E51 Contact Point, for example, may be specialised into “e-mail address”, “telephone number”, “post office box”, “URL” etc. none of which figures explicitly in the CRM hierarchy. Sub typing obviously requires consistency between the meaning of the terms assigned and the more general intent of the CRM entity in question.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1267, 'P3', 'de', 'name', 'hat Anmerkung', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1268, 'P3', 'ru', 'name', 'имеет примечание', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1269, 'P3', 'en', 'name', 'has note', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1270, 'P3', 'fr', 'name', 'a pour note', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1271, 'P3', 'el', 'name', 'έχει επεξήγηση', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1272, 'P3', 'pt', 'name', 'tem nota', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1273, 'P3', 'cn', 'name', '有说明', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1274, 'P3', 'en', 'comment', 'This property is a container for all informal descriptions about an object that have not been expressed in terms of CRM constructs. 
In particular it captures the characterisation of the item itself, its internal structures, appearance etc.
Like property P2 has type (is type of), this property is a consequence of the restricted focus of the CRM. The aim is not to capture, in a structured form, everything that can be said about an item; indeed, the CRM formalism is not regarded as sufficient to express everything that can be said. Good practice requires use of distinct note fields for different aspects of a characterisation. The P3.1 has type property of P3 has note allows differentiation of specific notes, e.g. “construction”, “decoration” etc. 
An item may have many notes, but a note is attached to a specific item.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1275, 'P4', 'fr', 'name', 'a pour durée', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1276, 'P4', 'ru', 'name', 'имеет временной отрезок', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1277, 'P4', 'pt', 'name', 'tem período de tempo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1278, 'P4', 'cn', 'name', '发生时段是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1279, 'P4', 'en', 'name_inverse', 'is time-span of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1280, 'P4', 'el', 'name_inverse', 'είναι χρονικό διάστημα του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1281, 'P4', 'fr', 'name_inverse', 'est la durée de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1282, 'P4', 'ru', 'name_inverse', 'является временным отрезком для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1283, 'P4', 'de', 'name_inverse', 'ist Zeitspanne von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1284, 'P4', 'pt', 'name_inverse', 'é o período de tempo de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1285, 'P4', 'cn', 'name_inverse', '开始并完成了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1286, 'P4', 'en', 'comment', 'This property describes the temporal confinement of an instance of an E2 Temporal Entity.
The related E52 Time-Span is understood as the real Time-Span during which the phenomena were active, which make up the temporal entity instance. It does not convey any other meaning than a positioning on the “time-line” of chronology. The Time-Span in turn is approximated by a set of dates (E61 Time Primitive). A temporal entity can have in reality only one Time-Span, but there may exist alternative opinions about it, which we would express by assigning multiple Time-Spans. Related temporal entities may share a Time-Span. Time-Spans may have completely unknown dates but other descriptions by which we can infer knowledge.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1287, 'P5', 'en', 'name', 'consists of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1288, 'P5', 'fr', 'name', 'consiste en', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1289, 'P5', 'el', 'name', 'αποτελείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1290, 'P5', 'de', 'name', 'besteht aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1291, 'P5', 'ru', 'name', 'состоит из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1292, 'P5', 'pt', 'name', 'consiste de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1293, 'P5', 'cn', 'name', '包含', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1294, 'P5', 'de', 'name_inverse', 'bildet Teil von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1295, 'P5', 'fr', 'name_inverse', 'fait partie de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1296, 'P5', 'ru', 'name_inverse', 'формирует часть', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1297, 'P5', 'en', 'name_inverse', 'forms part of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1298, 'P5', 'el', 'name_inverse', 'αποτελεί μέρος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1299, 'P5', 'pt', 'name_inverse', 'faz parte de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1300, 'P5', 'cn', 'name_inverse', '组成了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1301, 'P5', 'en', 'comment', 'This property describes the decomposition of an E3 Condition State into discrete, subsidiary states. 
It is assumed that the sub-states into which the condition state is analysed form a logical whole - although the entire story may not be completely known – and that the sub-states are in fact constitutive of the general condition state. For example, a general condition state of “in ruins” may be decomposed into the individual stages of decay', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1302, 'P7', 'fr', 'name', 'a eu lieu dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1303, 'P7', 'ru', 'name', 'совершался на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1304, 'P7', 'el', 'name', 'έλαβε χώρα σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1305, 'P7', 'de', 'name', 'fand statt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1306, 'P7', 'en', 'name', 'took place at', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1307, 'P7', 'pt', 'name', 'ocorreu em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1308, 'P7', 'cn', 'name', '发生地在', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1309, 'P7', 'fr', 'name_inverse', 'a été témoin de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1310, 'P7', 'en', 'name_inverse', 'witnessed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1311, 'P7', 'de', 'name_inverse', 'bezeugte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1312, 'P7', 'ru', 'name_inverse', 'был местом совершения', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1313, 'P7', 'el', 'name_inverse', 'υπήρξε τόπος του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1314, 'P7', 'pt', 'name_inverse', 'testemunhou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1315, 'P7', 'cn', 'name_inverse', '发生过', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1316, 'P7', 'en', 'comment', 'This property describes the spatial location of an instance of E4 Period. 
The related E53 Place should be seen as an approximation of the geographical area within which the phenomena that characterise the period in question occurred. P7took place at (witnessed) does not convey any meaning other than spatial positioning (generally on the surface of the earth).  For example, the period “R?volution fran?aise” can be said to have taken place in “France”, the “Victorian” period, may be said to have taken place in “Britain” and its colonies, as well as other parts of Europe and north America.
A period can take place at multiple locations.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1317, 'P8', 'ru', 'name', 'имел место на или в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1318, 'P8', 'el', 'name', 'έλαβε χώρα σε ή εντός', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1319, 'P8', 'de', 'name', 'fand statt auf oder innerhalb von ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1320, 'P8', 'en', 'name', 'took place on or within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1321, 'P8', 'fr', 'name', 'a eu lieu sur ou dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1322, 'P8', 'pt', 'name', 'ocorreu em ou dentro', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1323, 'P8', 'cn', 'name', '发生所在物件是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1324, 'P8', 'ru', 'name_inverse', 'являлся местом для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1325, 'P8', 'de', 'name_inverse', 'bezeugte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1326, 'P8', 'en', 'name_inverse', 'witnessed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1327, 'P8', 'fr', 'name_inverse', 'a été témoin de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1328, 'P8', 'el', 'name_inverse', 'υπήρξε τόπος του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1329, 'P8', 'pt', 'name_inverse', 'testemunhou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1330, 'P8', 'cn', 'name_inverse', '发生过', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1331, 'P8', 'en', 'comment', 'This property describes the location of an instance of E4 Period with respect to an E18 Physical Thing.
P8 took place on or within (witnessed) is a short-cut of a path defining a E53 Place with respect to the geometry of an object. cf. E46 Section Definition.
This property is in effect a special case of P7 took place at. It describes a period that can be located with respect to the space defined by an E18 Physical Thing such as a ship or a building. The precise geographical location of the object during the period in question may be unknown or unimportant. 
For example, the French and German armistice of 22 June 1940 was signed in the same railway carriage as the armistice of 11 November 1918.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1332, 'P9', 'el', 'name', 'αποτελείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1333, 'P9', 'en', 'name', 'consists of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1334, 'P9', 'de', 'name', 'setzt sich zusammen aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1335, 'P9', 'ru', 'name', 'состоит из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1336, 'P9', 'fr', 'name', 'consiste en', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1337, 'P9', 'pt', 'name', 'consiste de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1338, 'P9', 'cn', 'name', '包含子时期', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1339, 'P9', 'el', 'name_inverse', 'αποτελεί μέρος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1340, 'P9', 'ru', 'name_inverse', 'формирует часть', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1341, 'P9', 'de', 'name_inverse', 'bildet Teil von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1342, 'P9', 'fr', 'name_inverse', 'fait partie de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1343, 'P9', 'en', 'name_inverse', 'forms part of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1344, 'P9', 'pt', 'name_inverse', 'faz parte de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1345, 'P9', 'cn', 'name_inverse', '附属於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1346, 'P9', 'en', 'comment', 'This property describes the decomposition of an instance of E4 Period into discrete, subsidiary periods.
The sub-periods into which the period is decomposed form a logical whole - although the entire picture may not be completely known - and the sub-periods are constitutive of the general period.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1347, 'P10', 'ru', 'name', 'находится в пределах', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1348, 'P10', 'el', 'name', 'εμπίπτει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1349, 'P10', 'fr', 'name', 's’insère dans le cours de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1350, 'P10', 'en', 'name', 'falls within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1351, 'P10', 'de', 'name', 'fällt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1352, 'P10', 'pt', 'name', 'está contido em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1353, 'P10', 'cn', 'name', '发生时间涵盖於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1354, 'P10', 'el', 'name_inverse', 'περιλαμβάνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1355, 'P10', 'ru', 'name_inverse', 'содержит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1356, 'P10', 'en', 'name_inverse', 'contains', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1357, 'P10', 'fr', 'name_inverse', 'contient', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1358, 'P10', 'de', 'name_inverse', 'enthält', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1359, 'P10', 'pt', 'name_inverse', 'contém', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1360, 'P10', 'cn', 'name_inverse', '时间上涵盖', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1361, 'P10', 'en', 'comment', 'This property describes an instance of E4 Period, which falls within the E53 Place and E52 Time-Span of another. 
The difference with P9 consists of (forms part of) is subtle. Unlike P9 consists of (forms part of), P10 falls within (contains) does not imply any logical connection between the two periods and it may refer to a period of a completely different type.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1362, 'P11', 'fr', 'name', 'a eu pour participant', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1363, 'P11', 'ru', 'name', 'имел участника', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1364, 'P11', 'de', 'name', 'hatte Teilnehmer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1365, 'P11', 'en', 'name', 'had participant', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1366, 'P11', 'el', 'name', 'είχε συμμέτοχο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1367, 'P11', 'pt', 'name', 'tem participante', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1368, 'P11', 'cn', 'name', '有参与者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1369, 'P11', 'el', 'name_inverse', 'συμμετείχε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1370, 'P11', 'de', 'name_inverse', 'nahm Teil an', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1371, 'P11', 'ru', 'name_inverse', 'участвовал в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1372, 'P11', 'en', 'name_inverse', 'participated in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1373, 'P11', 'fr', 'name_inverse', 'a participé à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1374, 'P11', 'pt', 'name_inverse', 'participa em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1375, 'P11', 'cn', 'name_inverse', '参与了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1376, 'P11', 'en', 'comment', 'This property describes the active or passive participation of instances of E39 Actors in an E5 Event. 
It connects the life-line of the related E39 Actor with the E53 Place and E50 Date of the event. The property implies that the Actor was involved in the event but does not imply any causal relationship. The subject of a portrait can be said to have participated in the creation of the portrait.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1377, 'P12', 'en', 'name', 'occurred in the presence of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1378, 'P12', 'ru', 'name', 'появился в присутствии', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1379, 'P12', 'de', 'name', 'fand statt im Beisein von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1380, 'P12', 'el', 'name', 'συνέβη παρουσία του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1381, 'P12', 'fr', 'name', 'est arrivé en présence de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1382, 'P12', 'pt', 'name', 'ocorreu na presença de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1383, 'P12', 'cn', 'name', '发生现场存在', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1384, 'P12', 'en', 'name_inverse', 'was present at', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1385, 'P12', 'el', 'name_inverse', 'ήταν παρών/παρούσα/παρόν σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1386, 'P12', 'de', 'name_inverse', 'war anwesend bei', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1387, 'P12', 'fr', 'name_inverse', 'était présent à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1388, 'P12', 'ru', 'name_inverse', 'присутствовал при', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1389, 'P12', 'pt', 'name_inverse', 'estava presente no', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1390, 'P12', 'cn', 'name_inverse', '当时在场於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1391, 'P12', 'en', 'comment', 'This property describes the active or passive presence of an E77 Persistent Item in an E5 Event without implying any specific role. 
It connects the history of a thing with the E53 Place and E50 Date of an event. For example, an object may be the desk, now in a museum on which a treaty was signed. The presence of an immaterial thing implies the presence of at least one of its carriers.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1392, 'P13', 'de', 'name', 'zerstörte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1393, 'P13', 'fr', 'name', 'a détruit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1394, 'P13', 'ru', 'name', 'уничтожил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1395, 'P13', 'el', 'name', 'κατέστρεψε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1396, 'P13', 'en', 'name', 'destroyed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1397, 'P13', 'pt', 'name', 'destruiu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1398, 'P13', 'cn', 'name', '毁灭了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1399, 'P13', 'de', 'name_inverse', 'wurde zerstört durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1400, 'P13', 'en', 'name_inverse', 'was destroyed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1401, 'P13', 'el', 'name_inverse', 'καταστράφηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1402, 'P13', 'fr', 'name_inverse', 'a été détruite par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1403, 'P13', 'ru', 'name_inverse', 'был уничтожен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1404, 'P13', 'pt', 'name_inverse', 'foi destruído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1405, 'P13', 'cn', 'name_inverse', '被毁灭於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1406, 'P13', 'en', 'comment', 'This property allows specific instances of E18 Physical Thing that have been destroyed to be related to a destruction event. 
Destruction implies the end of an item’s life as a subject of cultural documentation – the physical matter of which the item was composed may in fact continue to exist. A destruction event may be contiguous with a Production that brings into existence a derived object composed partly of matter from the destroyed object.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1407, 'P14', 'de', 'name', 'wurde ausgeführt von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1408, 'P14', 'fr', 'name', 'réalisée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1409, 'P14', 'en', 'name', 'carried out by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1410, 'P14', 'el', 'name', 'πραγματοποιήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1411, 'P14', 'ru', 'name', 'выполнялся', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1412, 'P14', 'pt', 'name', 'realizada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1413, 'P14', 'cn', 'name', '有执行者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1414, 'P14', 'ru', 'name_inverse', 'выполнял', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1415, 'P14', 'el', 'name_inverse', 'πραγματοποίησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1416, 'P14', 'de', 'name_inverse', 'führte aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1417, 'P14', 'en', 'name_inverse', 'performed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1418, 'P14', 'fr', 'name_inverse', 'a exécuté', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1419, 'P14', 'pt', 'name_inverse', 'executou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1420, 'P14', 'cn', 'name_inverse', '执行了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1421, 'P14', 'en', 'comment', 'This property describes the active participation of an E39 Actor in an E7 Activity. 
It implies causal or legal responsibility. The P14.1 in the role of property of the property allows the nature of an Actor’s participation to be specified.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1422, 'P15', 'de', 'name', 'wurde beeinflußt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1423, 'P15', 'fr', 'name', 'a été influencée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1424, 'P15', 'el', 'name', 'επηρεάστηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1425, 'P15', 'ru', 'name', 'находился под влиянием', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1426, 'P15', 'en', 'name', 'was influenced by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1427, 'P15', 'pt', 'name', 'foi influenciado por ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1428, 'P15', 'cn', 'name', '有影响事物', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1429, 'P15', 'ru', 'name_inverse', 'оказал влияние на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1430, 'P15', 'el', 'name_inverse', 'επηρέασε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1431, 'P15', 'fr', 'name_inverse', 'a influencé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1432, 'P15', 'de', 'name_inverse', 'beeinflußte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1433, 'P15', 'en', 'name_inverse', 'influenced', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1434, 'P15', 'pt', 'name_inverse', 'influenciou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1435, 'P15', 'cn', 'name_inverse', '影响了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1436, 'P15', 'en', 'comment', 'This is a high level property, which captures the relationship between an E7 Activity and anything that may have had some bearing upon it.
The property has more specific sub properties.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1437, 'P16', 'fr', 'name', 'a utilisé l''objet spécifique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1438, 'P16', 'el', 'name', 'χρησιμοποίησε αντικείμενο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1439, 'P16', 'en', 'name', 'used specific object', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1440, 'P16', 'de', 'name', 'benutzte das bestimmte Objekt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1441, 'P16', 'ru', 'name', 'использовал особый объект', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1442, 'P16', 'pt', 'name', 'usou objeto específico', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1443, 'P16', 'cn', 'name', '使用特定物', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1444, 'P16', 'fr', 'name_inverse', 'a été utilisé pour', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1445, 'P16', 'de', 'name_inverse', 'wurde benutzt für', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1446, 'P16', 'ru', 'name_inverse', 'был использован для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1447, 'P16', 'en', 'name_inverse', 'was used for', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1448, 'P16', 'el', 'name_inverse', 'χρησιμοποιήθηκε για', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1449, 'P16', 'pt', 'name_inverse', 'foi usado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1450, 'P16', 'cn', 'name_inverse', '被用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1451, 'P16', 'en', 'comment', 'This property describes the use of material or immaterial things in a way essential to the performance or the outcome of an E7 Activity. 
This property typically applies to tools, instruments, moulds, raw materials and items embedded in a product. It implies that the presence of the object in question was a necessary condition for the action. For example, the activity of writing this text required the use of a computer. An immaterial thing can be used if at least one of its carriers is present. For example, the software tools on a computer.
Another example is the use of a particular name by a particular group of people over some span to identify a thing, such as a settlement. In this case, the physical carriers of this name are at least the people understanding its use.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1452, 'P17', 'ru', 'name', 'был обусловлен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1453, 'P17', 'de', 'name', 'wurde angeregt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1454, 'P17', 'el', 'name', 'είχε ως αφορμή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1455, 'P17', 'en', 'name', 'was motivated by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1456, 'P17', 'fr', 'name', 'a été motivée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1457, 'P17', 'pt', 'name', 'foi motivado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1458, 'P17', 'cn', 'name', '有促动事物', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1459, 'P17', 'el', 'name_inverse', 'ήταν αφορμή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1460, 'P17', 'en', 'name_inverse', 'motivated', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1461, 'P17', 'de', 'name_inverse', 'regte an', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1462, 'P17', 'ru', 'name_inverse', 'обусловил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1463, 'P17', 'fr', 'name_inverse', 'a motivé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1464, 'P17', 'pt', 'name_inverse', 'motivou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1465, 'P17', 'cn', 'name_inverse', '促动了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1466, 'P17', 'en', 'comment', 'This property describes an item or items that are regarded as a reason for carrying out the E7 Activity. 
For example, the discovery of a large hoard of treasure may call for a celebration, an order from head quarters can start a military manoeuvre. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1467, 'P19', 'ru', 'name', 'был предполагаемым использованием для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1468, 'P19', 'fr', 'name', 'était l''utilisation prévue de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1469, 'P19', 'de', 'name', 'war beabsichtigteter Gebrauch von ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1470, 'P19', 'el', 'name', 'ήταν προορισμένη χρήση του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1471, 'P19', 'en', 'name', 'was intended use of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1472, 'P19', 'pt', 'name', 'era prevista a utilização de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1473, 'P19', 'cn', 'name', '特别使用了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1474, 'P19', 'fr', 'name_inverse', 'a été fabriquée pour', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1475, 'P19', 'el', 'name_inverse', 'έγινε για', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1476, 'P19', 'ru', 'name_inverse', 'был создан для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1477, 'P19', 'de', 'name_inverse', 'wurde hergestellt für', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1478, 'P19', 'en', 'name_inverse', 'was made for', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1479, 'P19', 'pt', 'name_inverse', 'foi feito para', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1480, 'P19', 'cn', 'name_inverse', '被制造来用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1481, 'P19', 'en', 'comment', 'This property relates an E7 Activity with objects created specifically for use in the activity. 
This is distinct from the intended use of an item in some general type of activity such as the book of common prayer which was intended for use in Church of England services (see P101 had as general use (was use of)).', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1482, 'P20', 'de', 'name', 'hatte den bestimmten Zweck', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1483, 'P20', 'fr', 'name', 'avait pour but spécifique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1484, 'P20', 'el', 'name', 'είχε συγκεκριμένο σκοπό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1485, 'P20', 'en', 'name', 'had specific purpose', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1486, 'P20', 'ru', 'name', 'имел конкретную цель', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1487, 'P20', 'pt', 'name', 'tinha propósito específico', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1488, 'P20', 'cn', 'name', '有特定目地', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1489, 'P20', 'de', 'name_inverse', 'war Zweck von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1490, 'P20', 'ru', 'name_inverse', 'был целью для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1491, 'P20', 'el', 'name_inverse', 'ήταν σκοπός του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1492, 'P20', 'fr', 'name_inverse', 'était le but de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1493, 'P20', 'en', 'name_inverse', 'was purpose of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1494, 'P20', 'pt', 'name_inverse', 'era o propósito de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1495, 'P20', 'cn', 'name_inverse', '之準備活動是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1496, 'P20', 'en', 'comment', 'This property identifies the relationship between a preparatory activity and the event it is intended to be preparation for.
This includes activities, orders and other organisational actions, taken in preparation for other activities or events. 
P20 had specific purpose (was purpose of) implies that an activity succeeded in achieving its aim. If it does not succeed, such as the setting of a trap that did not catch anything, one may document the unrealized intention using P21 had general purpose (was purpose of):E55 Type and/or  P33 used specific technique (was used by): E29 Design or Procedure.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1497, 'P21', 'el', 'name', 'είχε γενικό σκοπό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1498, 'P21', 'de', 'name', 'hatte den allgemeinen Zweck', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1499, 'P21', 'fr', 'name', 'avait pour but général', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1500, 'P21', 'ru', 'name', 'имел общую цель', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1501, 'P21', 'en', 'name', 'had general purpose', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1502, 'P21', 'pt', 'name', 'tinha propósito geral', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1503, 'P21', 'cn', 'name', '有通用目地', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1504, 'P21', 'ru', 'name_inverse', 'был целью для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1505, 'P21', 'fr', 'name_inverse', 'était le but de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1506, 'P21', 'el', 'name_inverse', 'ήταν σκοπός του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1507, 'P21', 'de', 'name_inverse', 'war Zweck von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1508, 'P21', 'en', 'name_inverse', 'was purpose of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1509, 'P21', 'pt', 'name_inverse', 'era o propósito de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1510, 'P21', 'cn', 'name_inverse', '可利用', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1511, 'P21', 'en', 'comment', 'This property describes an intentional relationship between an E7 Activity and some general goal or purpose. 
This may involve activities intended as preparation for some type of activity or event. P21had general purpose (was purpose of) differs from P20 had specific purpose (was purpose of) in that no occurrence of an event is implied as the purpose. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1512, 'P22', 'el', 'name', 'μετεβίβασε τον τίτλο σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1513, 'P22', 'fr', 'name', 'a fait passer le droit de propriété à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1514, 'P22', 'de', 'name', 'übertrug Besitztitel auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1515, 'P22', 'en', 'name', 'transferred title to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1516, 'P22', 'ru', 'name', 'передал право собственности', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1517, 'P22', 'pt', 'name', 'transferiu os direitos de propriedade para', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1518, 'P22', 'cn', 'name', '转交所有权给', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1519, 'P22', 'el', 'name_inverse', 'απέκτησε τον τίτλο μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1520, 'P22', 'en', 'name_inverse', 'acquired title through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1521, 'P22', 'de', 'name_inverse', 'erwarb Besitztitel durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1522, 'P22', 'fr', 'name_inverse', 'a acquis le droit de propriété du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1523, 'P22', 'ru', 'name_inverse', 'получил право собственности через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1524, 'P22', 'pt', 'name_inverse', 'adquiriu os direitos de propriedade por meio da', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1525, 'P22', 'cn', 'name_inverse', '获取所有权於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1526, 'P22', 'en', 'comment', 'This property identifies the E39 Actor that acquires the legal ownership of an object as a result of an E8 Acquisition. 
The property will typically describe an Actor purchasing or otherwise acquiring an object from another Actor. However, title may also be acquired, without any corresponding loss of title by another Actor, through legal fieldwork such as hunting, shooting or fishing.
In reality the title is either transferred to or from someone, or both.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1527, 'P23', 'el', 'name', 'μετεβίβασε τον τίτλο από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1528, 'P23', 'fr', 'name', 'a fait passer le droit de propriété de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1529, 'P23', 'ru', 'name', 'передал право собственности от', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1530, 'P23', 'de', 'name', 'übertrug Besitztitel von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1531, 'P23', 'en', 'name', 'transferred title from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1532, 'P23', 'pt', 'name', 'transferiu os direitos de propriedade de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1533, 'P23', 'cn', 'name', '原所有权者是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1534, 'P23', 'fr', 'name_inverse', 'a perdu le droit de propriété du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1535, 'P23', 'de', 'name_inverse', 'trat Besitztitel ab in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1536, 'P23', 'ru', 'name_inverse', 'право собственности отдано через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1537, 'P23', 'en', 'name_inverse', 'surrendered title through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1538, 'P23', 'el', 'name_inverse', 'παρέδωσε τον τίτλο μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1539, 'P23', 'pt', 'name_inverse', 'perdeu os direitos de propriedade por meio da', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1540, 'P23', 'cn', 'name_inverse', '交出所有权於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1541, 'P23', 'en', 'comment', 'This property identifies the E39 Actor or Actors who relinquish legal ownership as the result of an E8 Acquisition.
The property will typically be used to describe a person donating or selling an object to a museum. In reality title is either transferred to or from someone, or both.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1542, 'P24', 'de', 'name', 'übertrug Besitz über', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1543, 'P24', 'ru', 'name', 'передал право собственности на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1544, 'P24', 'el', 'name', 'μετεβίβασε τον τίτλο του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1545, 'P24', 'fr', 'name', 'a fait passer le droit de propriété sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1546, 'P24', 'en', 'name', 'transferred title of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1547, 'P24', 'pt', 'name', 'transferiu os direitos de propriedade sobre o', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1548, 'P24', 'cn', 'name', '转移所有权的标的物是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1549, 'P24', 'ru', 'name_inverse', 'сменил владельца через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1550, 'P24', 'en', 'name_inverse', 'changed ownership through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1551, 'P24', 'de', 'name_inverse', 'ging über in Besitz durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1552, 'P24', 'el', 'name_inverse', 'άλλαξε ιδιοκτησία μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1553, 'P24', 'fr', 'name_inverse', 'a changé de mains du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1554, 'P24', 'pt', 'name_inverse', 'mudou de proprietário por meio de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1555, 'P24', 'cn', 'name_inverse', '转移了所有权於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1556, 'P24', 'en', 'comment', 'This property identifies the E18 Physical Thing or things involved in an E8 Acquisition. 
In reality, an acquisition must refer to at least one transferred item.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1557, 'P25', 'en', 'name', 'moved', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1558, 'P25', 'el', 'name', 'μετεκίνησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1559, 'P25', 'ru', 'name', 'переместил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1560, 'P25', 'fr', 'name', 'a déplacé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1561, 'P25', 'de', 'name', 'bewegte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1562, 'P25', 'pt', 'name', 'locomoveu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1563, 'P25', 'cn', 'name', '移动了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1564, 'P25', 'ru', 'name_inverse', 'перемещен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1565, 'P25', 'en', 'name_inverse', 'moved by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1566, 'P25', 'el', 'name_inverse', 'μετακινήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1567, 'P25', 'fr', 'name_inverse', 'a été déplacé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1568, 'P25', 'de', 'name_inverse', 'wurde bewegt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1569, 'P25', 'pt', 'name_inverse', 'foi locomovido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1570, 'P25', 'cn', 'name_inverse', '被移动於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1571, 'P25', 'en', 'comment', 'This property identifies the E19 Physical Object that is moved during a move event. 
The property implies the object’s passive participation. For example, Monet’s painting “Impression sunrise” was moved for the first Impressionist exhibition in 1874. 
In reality, a move must concern at least one object.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1572, 'P26', 'el', 'name', 'μετακινήθηκε προς', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1573, 'P26', 'en', 'name', 'moved to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1574, 'P26', 'fr', 'name', 'a déplacé vers', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1575, 'P26', 'ru', 'name', 'перемещен в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1576, 'P26', 'de', 'name', 'bewegte bis zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1577, 'P26', 'pt', 'name', 'locomoveu para', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1578, 'P26', 'cn', 'name', '移入物件至', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1579, 'P26', 'en', 'name_inverse', 'was destination of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1580, 'P26', 'de', 'name_inverse', 'war Zielort von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1581, 'P26', 'el', 'name_inverse', 'ήταν προορισμός του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1582, 'P26', 'ru', 'name_inverse', 'был пунктом назначения для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1583, 'P26', 'fr', 'name_inverse', 'a été la destination de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1584, 'P26', 'pt', 'name_inverse', 'era destinação de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1585, 'P26', 'cn', 'name_inverse', '被作为移入地於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1586, 'P26', 'en', 'comment', 'This property identifies the destination of a E9 Move. 
A move will be linked to a destination, such as the move of an artefact from storage to display. A move may be linked to many terminal instances of E53 Places. In this case the move describes a distribution of a set of objects. The area of the move includes the origin, route and destination.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1587, 'P27', 'el', 'name', 'μετακινήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1588, 'P27', 'en', 'name', 'moved from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1589, 'P27', 'fr', 'name', 'a retiré de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1590, 'P27', 'de', 'name', 'bewegte weg von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1591, 'P27', 'ru', 'name', 'перемещен из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1592, 'P27', 'pt', 'name', 'locomoveu de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1593, 'P27', 'cn', 'name', '有移出地', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1594, 'P27', 'en', 'name_inverse', 'was origin of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1595, 'P27', 'de', 'name_inverse', 'war Ausgangsort von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1596, 'P27', 'ru', 'name_inverse', 'был исходной точкой для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1597, 'P27', 'fr', 'name_inverse', 'a été l''origine de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1598, 'P27', 'el', 'name_inverse', 'ήταν αφετηρία του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1599, 'P27', 'pt', 'name_inverse', 'era origem de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1600, 'P27', 'cn', 'name_inverse', '被作为移出地於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1601, 'P27', 'en', 'comment', 'This property identifies the starting E53 Place of an E9 Move.
A move will be linked to an origin, such as the move of an artefact from storage to display. A move may be linked to many origins. In this case the move describes the picking up of a set of objects. The area of the move includes the origin, route and destination.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1602, 'P28', 'fr', 'name', 'changement de détenteur au détriment de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1603, 'P28', 'de', 'name', 'übergab Gewahrsam an', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1604, 'P28', 'en', 'name', 'custody surrendered by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1605, 'P28', 'el', 'name', 'μετεβίβασε κατοχή από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1606, 'P28', 'ru', 'name', 'опека отдана', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1607, 'P28', 'pt', 'name', 'custódia concedida por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1608, 'P28', 'cn', 'name', '有原保管人', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1609, 'P28', 'en', 'name_inverse', 'surrendered custody through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1610, 'P28', 'ru', 'name_inverse', 'опека отдана через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1611, 'P28', 'fr', 'name_inverse', 'a cessé d’être détenteur à cause de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1612, 'P28', 'el', 'name_inverse', 'παρέδωσε κατοχή μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1613, 'P28', 'de', 'name_inverse', 'wurde Gewahrsam übergeben durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1614, 'P28', 'pt', 'name_inverse', 'final da custódia por meio de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1615, 'P28', 'cn', 'name_inverse', '交出保管作业於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1616, 'P28', 'en', 'comment', 'This property identifies the E39 Actor or Actors who surrender custody of an instance of E18 Physical Thing in an E10 Transfer of Custody activity. 
The property will typically describe an Actor surrendering custody of an object when it is handed over to someone else’s care. On occasion, physical custody may be surrendered involuntarily – through accident, loss or theft.
In reality, custody is either transferred to someone or from someone, or both.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1617, 'P29', 'el', 'name', 'μετεβίβασε κατοχή σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1618, 'P29', 'ru', 'name', 'опека получена', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1619, 'P29', 'en', 'name', 'custody received by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1620, 'P29', 'fr', 'name', 'changement de détenteur au profit de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1621, 'P29', 'de', 'name', 'übertrug Gewahrsam auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1622, 'P29', 'pt', 'name', 'custódia recebida por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1623, 'P29', 'cn', 'name', '移转保管作业给', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1624, 'P29', 'el', 'name_inverse', 'παρέλαβε κατοχή μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1625, 'P29', 'en', 'name_inverse', 'received custody through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1626, 'P29', 'ru', 'name_inverse', 'получил опеку через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1627, 'P29', 'fr', 'name_inverse', 'est devenu détenteur grâce à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1628, 'P29', 'de', 'name_inverse', 'erhielt Gewahrsam durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1629, 'P29', 'pt', 'name_inverse', 'início da custódia por meio de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1630, 'P29', 'cn', 'name_inverse', '取得保管作业於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1631, 'P29', 'en', 'comment', 'This property identifies the E39 Actor or Actors who receive custody of an instance of E18 Physical Thing in an E10 Transfer of Custody activity. 
The property will typically describe Actors receiving custody of an object when it is handed over from another Actor’s care. On occasion, physical custody may be received involuntarily or illegally – through accident, unsolicited donation, or theft.
In reality, custody is either transferred to someone or from someone, or both.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1632, 'P30', 'ru', 'name', 'передало опеку на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1633, 'P30', 'en', 'name', 'transferred custody of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1634, 'P30', 'fr', 'name', 'changement de détenteur concernant', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1635, 'P30', 'de', 'name', 'übertrug Gewahrsam über', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1636, 'P30', 'el', 'name', 'μετεβίβασε κατοχή του/της/των', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1637, 'P30', 'pt', 'name', 'transferida custódia de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1638, 'P30', 'cn', 'name', '有保管标的物', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1639, 'P30', 'en', 'name_inverse', 'custody transferred through', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1640, 'P30', 'el', 'name_inverse', 'άλλαξε κατοχή μέσω', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1641, 'P30', 'fr', 'name_inverse', 'a changé de détenteur du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1642, 'P30', 'de', 'name_inverse', 'wechselte Gewahrsam durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1643, 'P30', 'ru', 'name_inverse', 'опека передана через', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1644, 'P30', 'pt', 'name_inverse', 'custódia transferida por meio de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1645, 'P30', 'cn', 'name_inverse', '被移转了保管作业於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1646, 'P30', 'en', 'comment', 'This property identifies an item or items of E18 Physical Thing concerned in an E10 Transfer of Custody activity. 
The property will typically describe the object that is handed over by an E39 Actor to another Actor’s custody. On occasion, physical custody may be transferred involuntarily or illegally – through accident, unsolicited donation, or theft.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1647, 'P31', 'de', 'name', 'veränderte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1648, 'P31', 'fr', 'name', 'a modifié', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1649, 'P31', 'en', 'name', 'has modified', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1650, 'P31', 'ru', 'name', 'изменил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1651, 'P31', 'el', 'name', 'τροποποίησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1652, 'P31', 'pt', 'name', 'modificou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1653, 'P31', 'cn', 'name', '修改了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1654, 'P31', 'fr', 'name_inverse', 'a été modifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1655, 'P31', 'de', 'name_inverse', 'wurde verändert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1656, 'P31', 'el', 'name_inverse', 'τροποποιήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1657, 'P31', 'ru', 'name_inverse', 'был изменен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1658, 'P31', 'en', 'name_inverse', 'was modified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1659, 'P31', 'pt', 'name_inverse', 'foi modificada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1660, 'P31', 'cn', 'name_inverse', '被修改於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1661, 'P31', 'en', 'comment', 'This property identifies the E24 Physical Man-Made Thing modified in an E11 Modification.
If a modification is applied to a non-man-made object, it is regarded as an E22 Man-Made Object from that time onwards. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1662, 'P32', 'el', 'name', 'χρησιμοποίησε γενική τεχνική', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1663, 'P32', 'de', 'name', 'benutzte das allgemeine Verfahren', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1664, 'P32', 'fr', 'name', 'a employé comme technique générique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1665, 'P32', 'ru', 'name', 'использовал общую технику', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1666, 'P32', 'en', 'name', 'used general technique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1667, 'P32', 'pt', 'name', 'usou técnica geral', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1668, 'P32', 'cn', 'name', '使用通用技术', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1669, 'P32', 'ru', 'name_inverse', 'был техникой для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1670, 'P32', 'el', 'name_inverse', 'ήταν τεχνική του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1671, 'P32', 'de', 'name_inverse', 'war Verfahren von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1672, 'P32', 'en', 'name_inverse', 'was technique of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1673, 'P32', 'fr', 'name_inverse', 'a été la technique mise en œuvre dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1674, 'P32', 'pt', 'name_inverse', 'foi técnica da', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1675, 'P32', 'cn', 'name_inverse', '被使用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1676, 'P32', 'en', 'comment', 'This property identifies the technique that was employed in an act of modification. 
These techniques should be drawn from an external E55 Type hierarchy of consistent terminology of general techniques such as embroidery, oil-painting, etc. Specific techniques may be further described as instances of E29 Design or Procedure.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1677, 'P33', 'el', 'name', 'χρησιμοποίησε συγκεκριμένη τεχνική', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1678, 'P33', 'en', 'name', 'used specific technique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1679, 'P33', 'fr', 'name', 'a employé comme technique spécifique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1680, 'P33', 'ru', 'name', 'использовал особую технику', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1681, 'P33', 'de', 'name', 'benutzte das bestimmte Verfahren', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1682, 'P33', 'pt', 'name', 'usou técnica específica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1683, 'P33', 'cn', 'name', '使用特定技术', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1684, 'P33', 'en', 'name_inverse', 'was used by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1685, 'P33', 'fr', 'name_inverse', 'a été employée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1686, 'P33', 'ru', 'name_inverse', 'был использован посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1687, 'P33', 'de', 'name_inverse', 'wurde benutzt von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1688, 'P33', 'el', 'name_inverse', 'χρησιμοποιήθηκε για', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1689, 'P33', 'pt', 'name_inverse', 'foi usada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1690, 'P33', 'cn', 'name_inverse', '被特别使用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1691, 'P33', 'en', 'comment', 'This property identifies a specific instance of E29 Design or Procedure in order to carry out an instance of E7 Activity or parts of it. 
The property differs from P32 used general technique (was technique of) in that P33 refers to an instance of E29 Design or Procedure, which is a concrete information object in its own right rather than simply being a term or a method known by tradition. 
Typical examples would include intervention plans for conservation or the construction plans of a building.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1692, 'P34', 'el', 'name', 'αφορούσε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1693, 'P34', 'ru', 'name', 'имел дело с', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1694, 'P34', 'de', 'name', 'betraf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1695, 'P34', 'en', 'name', 'concerned', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1696, 'P34', 'fr', 'name', 'a concerné', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1697, 'P34', 'pt', 'name', 'interessada', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1698, 'P34', 'cn', 'name', '评估了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1699, 'P34', 'de', 'name_inverse', 'wurde beurteilt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1700, 'P34', 'el', 'name_inverse', 'εκτιμήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1701, 'P34', 'fr', 'name_inverse', 'expertisé par le biais de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1702, 'P34', 'en', 'name_inverse', 'was assessed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1703, 'P34', 'ru', 'name_inverse', 'был оценен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1704, 'P34', 'pt', 'name_inverse', 'foi avaliada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1705, 'P34', 'cn', 'name_inverse', '被评估於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1706, 'P34', 'en', 'comment', 'This property identifies the E18 Physical Thing that was assessed during an E14 Condition Assessment activity. 
Conditions may be assessed either by direct observation or using recorded evidence. In the latter case the E18 Physical Thing does not need to be present or extant.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1707, 'P35', 'ru', 'name', 'идентифицировал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1708, 'P35', 'de', 'name', 'hat identifiziert', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1709, 'P35', 'fr', 'name', 'a identifié', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1710, 'P35', 'el', 'name', 'έχει διαπιστώσει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1711, 'P35', 'en', 'name', 'has identified', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1712, 'P35', 'pt', 'name', 'identificou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1713, 'P35', 'cn', 'name', '评估认定了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1714, 'P35', 'ru', 'name_inverse', 'идентифицирован посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1715, 'P35', 'de', 'name_inverse', 'wurde identifiziert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1716, 'P35', 'fr', 'name_inverse', 'est identifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1717, 'P35', 'el', 'name_inverse', 'έχει διαπιστωθεί από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1718, 'P35', 'en', 'name_inverse', 'was identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1719, 'P35', 'pt', 'name_inverse', 'foi identificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1720, 'P35', 'cn', 'name_inverse', '被评估认定於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1721, 'P35', 'en', 'comment', 'This property identifies the E3 Condition State that was observed in an E14 Condition Assessment activity.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1722, 'P37', 'fr', 'name', 'a attribué', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1723, 'P37', 'el', 'name', 'απέδωσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1724, 'P37', 'en', 'name', 'assigned', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1725, 'P37', 'de', 'name', 'wies zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1726, 'P37', 'ru', 'name', 'назначил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1727, 'P37', 'pt', 'name', 'atribuiu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1728, 'P37', 'cn', 'name', '指定标识符为', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1729, 'P37', 'de', 'name_inverse', 'wurde zugewiesen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1730, 'P37', 'el', 'name_inverse', 'αποδόθηκε ως ιδιότητα από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1731, 'P37', 'en', 'name_inverse', 'was assigned by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1732, 'P37', 'ru', 'name_inverse', 'был присвоен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1733, 'P37', 'fr', 'name_inverse', 'a été attribuée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1734, 'P37', 'pt', 'name_inverse', 'foi atribuído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1735, 'P37', 'cn', 'name_inverse', '被指定为标识符於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1736, 'P37', 'en', 'comment', 'This property records the identifier that was assigned to an item in an Identifier Assignment activity.
The same identifier may be assigned on more than one occasion.
An Identifier might be created prior to an assignment.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1737, 'P38', 'el', 'name', 'ακύρωσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1738, 'P38', 'ru', 'name', 'отменил назначение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1739, 'P38', 'en', 'name', 'deassigned', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1740, 'P38', 'de', 'name', ' hob Zuweisung auf von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1741, 'P38', 'fr', 'name', 'a désattribué', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1742, 'P38', 'pt', 'name', 'retirou a atribuição do', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1743, 'P38', 'cn', 'name', '取消标识符', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1744, 'P38', 'ru', 'name_inverse', 'был отменен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1745, 'P38', 'fr', 'name_inverse', 'a été désattribué par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1746, 'P38', 'de', 'name_inverse', 'wurde aufgehoben durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1747, 'P38', 'el', 'name_inverse', 'ακυρώθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1748, 'P38', 'en', 'name_inverse', 'was deassigned by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1749, 'P38', 'pt', 'name_inverse', 'foi retirada a atribuição por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1750, 'P38', 'cn', 'name_inverse', '被取消标识符於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1824, 'P43', 'pt', 'name_inverse', 'é dimensão de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1825, 'P43', 'cn', 'name_inverse', '估量的标的物是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1751, 'P38', 'en', 'comment', 'This property records the identifier that was deassigned from an instance of E1 CRM Entity.
Deassignment of an identifier may be necessary when an item is taken out of an inventory, a new numbering system is introduced or items are merged or split up. 
The same identifier may be deassigned on more than one occasion.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1752, 'P39', 'fr', 'name', 'a mesuré', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1753, 'P39', 'de', 'name', 'vermaß', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1754, 'P39', 'el', 'name', 'μέτρησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1755, 'P39', 'en', 'name', 'measured', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1756, 'P39', 'ru', 'name', 'измерил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1757, 'P39', 'pt', 'name', 'mediu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1758, 'P39', 'cn', 'name', '测量了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1759, 'P39', 'de', 'name_inverse', 'wurde vermessen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1760, 'P39', 'ru', 'name_inverse', 'был измерен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1761, 'P39', 'en', 'name_inverse', 'was measured by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1762, 'P39', 'el', 'name_inverse', 'μετρήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1763, 'P39', 'fr', 'name_inverse', 'a été mesuré par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1764, 'P39', 'pt', 'name_inverse', 'foi medida por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1765, 'P39', 'cn', 'name_inverse', '被测量於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1766, 'P39', 'en', 'comment', 'This property associates an instance of E16 Measurement with the instance of E1 CRM Entity to which it applied. An instance of E1 CRM Entity may be measured more than once. Material and immaterial things and processes may be measured, e.g. the number of words in a text, or the duration of an event.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1767, 'P40', 'en', 'name', 'observed dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1768, 'P40', 'el', 'name', 'παρατήρησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1769, 'P40', 'ru', 'name', 'определил величину', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1770, 'P40', 'de', 'name', 'beobachtete Dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1771, 'P40', 'fr', 'name', 'a relevé comme dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1772, 'P40', 'pt', 'name', 'verificou a dimensão', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1773, 'P40', 'cn', 'name', '观察认定的规模是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1774, 'P40', 'ru', 'name_inverse', 'наблюдался в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1775, 'P40', 'el', 'name_inverse', 'παρατηρήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1776, 'P40', 'en', 'name_inverse', 'was observed in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1777, 'P40', 'de', 'name_inverse', 'wurde beobachtet in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1778, 'P40', 'fr', 'name_inverse', 'a été relevée au cours de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1779, 'P40', 'pt', 'name_inverse', 'foi verificada durante', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1780, 'P40', 'cn', 'name_inverse', '被观察认定於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1781, 'P40', 'en', 'comment', 'This property records the dimension that was observed in an E16 Measurement Event.
E54 Dimension can be any quantifiable aspect of E70 Thing. Weight, image colour depth and monetary value are dimensions in this sense. One measurement activity may determine more than one dimension of one object.
Dimensions may be determined either by direct observation or using recorded evidence. In the latter case the measured Thing does not need to be present or extant.
Even though knowledge of the value of a dimension requires measurement, the dimension may be an object of discourse prior to, or even without, any measurement being made.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1782, 'P41', 'ru', 'name', 'классифицировал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1783, 'P41', 'en', 'name', 'classified', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1784, 'P41', 'fr', 'name', 'a classifié', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1785, 'P41', 'el', 'name', 'χαρακτήρισε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1786, 'P41', 'de', 'name', 'klassifizierte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1787, 'P41', 'pt', 'name', 'classificou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1788, 'P41', 'cn', 'name', '分类了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1789, 'P41', 'fr', 'name_inverse', 'a été classifiée par le biais de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1790, 'P41', 'en', 'name_inverse', 'was classified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1791, 'P41', 'ru', 'name_inverse', 'был классифицирован посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1792, 'P41', 'el', 'name_inverse', 'χαρακτηρίσθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1793, 'P41', 'de', 'name_inverse', 'wurde klassifiziert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1794, 'P41', 'pt', 'name_inverse', 'foi classificada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1795, 'P41', 'cn', 'name_inverse', '被分类於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1796, 'P41', 'en', 'comment', 'This property records the item to which a type was assigned in an E17 Type Assignment activity.
Any instance of a CRM entity may be assigned a type through type assignment. Type assignment events allow a more detailed path from E1 CRM Entity through P41 classified (was classified), E17 Type Assignment, P42 assigned (was assigned by) to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1797, 'P42', 'el', 'name', 'απέδωσε ως ιδιότητα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1798, 'P42', 'en', 'name', 'assigned', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1799, 'P42', 'fr', 'name', 'a attribué', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1800, 'P42', 'ru', 'name', 'назначил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1801, 'P42', 'de', 'name', 'wies zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1802, 'P42', 'pt', 'name', 'atribuiu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1803, 'P42', 'cn', 'name', '指定类型为', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1804, 'P42', 'ru', 'name_inverse', 'был присвоен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1805, 'P42', 'el', 'name_inverse', 'αποδόθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1806, 'P42', 'en', 'name_inverse', 'was assigned by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1807, 'P42', 'de', 'name_inverse', 'wurde zugewiesen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1808, 'P42', 'fr', 'name_inverse', 'a été attribué par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1809, 'P42', 'pt', 'name_inverse', 'foi atribuído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1810, 'P42', 'cn', 'name_inverse', '被指定类型於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1811, 'P42', 'en', 'comment', 'This property records the type that was assigned to an entity by an E17 Type Assignment activity. 
Type assignment events allow a more detailed path from E1 CRM Entity through P41 classified (was classified by), E17 Type Assignment, P42 assigned (was assigned by) to E55 Type for assigning types to objects compared to the shortcut offered by P2 has type (is type of).
For example, a fragment of an antique vessel could be assigned the type “attic red figured belly handled amphora” by expert A. The same fragment could be assigned the type “shoulder handled amphora” by expert B.
A Type may be intellectually constructed independent from assigning an instance of it.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1812, 'P43', 'de', 'name', 'hat Dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1813, 'P43', 'fr', 'name', 'a pour dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1814, 'P43', 'ru', 'name', 'имеет величину', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1815, 'P43', 'en', 'name', 'has dimension', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1816, 'P43', 'el', 'name', 'έχει μέγεθος', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1817, 'P43', 'pt', 'name', 'tem dimensão', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1818, 'P43', 'cn', 'name', '有规模数量', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1819, 'P43', 'de', 'name_inverse', 'ist Dimension von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1820, 'P43', 'en', 'name_inverse', 'is dimension of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1821, 'P43', 'ru', 'name_inverse', 'является величиной для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1822, 'P43', 'fr', 'name_inverse', 'est dimension de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1823, 'P43', 'el', 'name_inverse', 'είναι μέγεθος του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1826, 'P43', 'en', 'comment', 'This property records a E54 Dimension of some E70 Thing.
It is a shortcut of the more fully developed path from E70 Thing through P39 measured (was measured by), E16 Measurement P40 observed dimension (was observed in) to E54 Dimension. It offers no information about how and when an E54 Dimension was established, nor by whom.
An instance of E54 Dimension is specific to an instance of E70 Thing.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1827, 'P44', 'ru', 'name', 'имеет условие', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1828, 'P44', 'de', 'name', 'hat Zustand', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1829, 'P44', 'fr', 'name', 'a pour état matériel', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1830, 'P44', 'en', 'name', 'has condition', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1831, 'P44', 'el', 'name', 'έχει κατάσταση', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1832, 'P44', 'pt', 'name', 'tem estado material ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1833, 'P44', 'cn', 'name', '有状态', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1834, 'P44', 'de', 'name_inverse', 'ist Zustand von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1835, 'P44', 'fr', 'name_inverse', 'état matériel de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1836, 'P44', 'el', 'name_inverse', 'είναι κατάσταση του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1837, 'P44', 'ru', 'name_inverse', 'является условием для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1838, 'P44', 'en', 'name_inverse', 'is condition of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1839, 'P44', 'pt', 'name_inverse', 'estado material de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1840, 'P44', 'cn', 'name_inverse', '描述的标的物是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1841, 'P44', 'en', 'comment', 'This property records an E3 Condition State for some E18 Physical Thing.
It is a shortcut of the more fully developed path from E18 Physical Thing through P34 concerned (was assessed by), E14 Condition Assessment P35 has identified (was identified by) to E3 Condition State. It offers no information about how and when the E3 Condition State was established, nor by whom. 
An instance of Condition State is specific to an instance of Physical Thing.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1842, 'P45', 'fr', 'name', 'consiste en', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1843, 'P45', 'el', 'name', 'αποτελείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1844, 'P45', 'de', 'name', 'besteht aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1845, 'P45', 'en', 'name', 'consists of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1846, 'P45', 'ru', 'name', 'составлен из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1847, 'P45', 'pt', 'name', 'consiste de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1848, 'P45', 'cn', 'name', '有构成材料', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1849, 'P45', 'de', 'name_inverse', 'ist enthalten in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1850, 'P45', 'el', 'name_inverse', 'είναι ενσωματωμένος/η/ο σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1851, 'P45', 'en', 'name_inverse', 'is incorporated in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1852, 'P45', 'ru', 'name_inverse', 'входит в состав', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1853, 'P45', 'fr', 'name_inverse', 'est présent dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1854, 'P45', 'pt', 'name_inverse', 'está presente em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1855, 'P45', 'cn', 'name_inverse', '被用来构成', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1856, 'P45', 'en', 'comment', 'This property identifies the instances of E57 Materials of which an instance of E18 Physical Thing is composed.
All physical things consist of physical materials. P45 consists of (is incorporated in) allows the different Materials to be recorded. P45 consists of (is incorporated in) refers here to observed Material as opposed to the consumed raw material.
A Material, such as a theoretical alloy, may not have any physical instances', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1857, 'P46', 'en', 'name', 'is composed of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1858, 'P46', 'fr', 'name', 'est composée de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1859, 'P46', 'el', 'name', 'αποτελείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1860, 'P46', 'de', 'name', 'ist zusammengesetzt aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1861, 'P46', 'ru', 'name', 'составлен из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1862, 'P46', 'pt', 'name', 'é composto de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1863, 'P46', 'cn', 'name', '有组件', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1864, 'P46', 'ru', 'name_inverse', 'формирует часть', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1865, 'P46', 'fr', 'name_inverse', 'fait partie de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1866, 'P46', 'el', 'name_inverse', 'αποτελεί μέρος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1867, 'P46', 'de', 'name_inverse', 'bildet Teil von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1868, 'P46', 'en', 'name_inverse', 'forms part of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1869, 'P46', 'pt', 'name_inverse', 'faz parte de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1870, 'P46', 'cn', 'name_inverse', '被用来组成', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1871, 'P46', 'en', 'comment', 'This property allows instances of E18 Physical Thing to be analysed into component elements.
Component elements, since they are themselves instances of E18 Physical Thing, may be further analysed into sub-components, thereby creating a hierarchy of part decomposition. An instance of E18 Physical Thing may be shared between multiple wholes, for example two buildings may share a common wall.
This property is intended to describe specific components that are individually documented, rather than general aspects. Overall descriptions of the structure of an instance of E18 Physical Thing are captured by the P3 has note property.
The instances of E57 Materials of which an item of E18 Physical Thing is composed should be documented using P45 consists of (is incorporated in).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1872, 'P48', 'en', 'name', 'has preferred identifier', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1873, 'P48', 'fr', 'name', 'a pour identificateur retenu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1874, 'P48', 'de', 'name', 'hat bevorzugtes Kennzeichen', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1875, 'P48', 'ru', 'name', 'имеет предпочтительный идентификатор', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1876, 'P48', 'el', 'name', 'έχει προτιμώμενο αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1877, 'P48', 'pt', 'name', 'tem identificador preferido', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1878, 'P48', 'cn', 'name', '有首选标识符', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1879, 'P48', 'en', 'name_inverse', 'is preferred identifier of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1880, 'P48', 'ru', 'name_inverse', 'является предпочтительным идентификатором для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1881, 'P48', 'de', 'name_inverse', 'ist bevorzugtes Kennzeichen für', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1882, 'P48', 'el', 'name_inverse', 'είναι προτιμώμενο αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1883, 'P48', 'fr', 'name_inverse', 'est l’identificateur retenu de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1884, 'P48', 'pt', 'name_inverse', 'é o identificador preferido de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1885, 'P48', 'cn', 'name_inverse', '首选标识符的标的物是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1886, 'P48', 'en', 'comment', 'This property records the preferred E42 Identifier that was used to identify an instance of E1 CRM Entity at the time this property was recorded.
More than one preferred identifier may have been assigned to an item over time.
Use of this property requires an external mechanism for assigning temporal validity to the respective CRM instance.
P48 has preferred identifier (is preferred identifier of), is a shortcut for the path from E1 CRM Entity through P140 assigned attribute to (was attributed by), E15 Identifier Assignment, P37 assigned (was assigned by) to E42 Identifier. The fact that an identifier is a preferred one for an organisation can be better expressed in a context independent form by assigning a suitable E55 Type to the respective instance of E15 Identifier Assignment using the P2 has type property.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1887, 'P49', 'ru', 'name', 'имеет бывшего или текущего смотрителя', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3096, 'P146', 'en', 'name', 'separated from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1888, 'P49', 'el', 'name', 'είναι ή ήταν στην κατοχή του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1889, 'P49', 'fr', 'name', 'est ou a été détenu par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1890, 'P49', 'de', 'name', 'hat früheren oder derzeitigen Betreuer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1891, 'P49', 'en', 'name', 'has former or current keeper', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1892, 'P49', 'pt', 'name', 'é ou foi guardada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1893, 'P49', 'cn', 'name', '有前任或现任保管者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1894, 'P49', 'en', 'name_inverse', 'is former or current keeper of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1895, 'P49', 'el', 'name_inverse', 'κατέχει ή κατείχε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1896, 'P49', 'fr', 'name_inverse', 'est ou a été détenteur de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1897, 'P49', 'de', 'name_inverse', 'ist früherer oder derzeitiger Betreuer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1898, 'P49', 'ru', 'name_inverse', 'является бывшим или текущим смотрителем для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1899, 'P49', 'pt', 'name_inverse', 'é ou foi guardador de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1900, 'P49', 'cn', 'name_inverse', '目前或曾经保管', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1901, 'P49', 'en', 'comment', 'This property identifies the E39 Actor or Actors who have or have had custody of an instance of E18 Physical Thing at some time. 
The distinction with P50 has current keeper (is current keeper of) is that P49 has former or current keeper (is former or current keeper of) leaves open the question as to whether the specified keepers are current. 
P49 has former or current keeper (is former or current keeper of) is a shortcut for the more detailed path from E18 Physical Thing through P30 transferred custody of (custody transferred through), E10 Transfer of Custody, P28 custody surrendered by (surrendered custody through) or P29 custody received by (received custody through) to E39 Actor.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1902, 'P50', 'de', 'name', 'hat derzeitigen Betreuer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1903, 'P50', 'en', 'name', 'has current keeper', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1904, 'P50', 'el', 'name', 'είναι στην κατοχή του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1905, 'P50', 'fr', 'name', 'est actuellement détenu par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1906, 'P50', 'ru', 'name', 'имеет текущего смотрителя', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1907, 'P50', 'pt', 'name', 'é guardada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1908, 'P50', 'cn', 'name', '有现任保管者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1909, 'P50', 'ru', 'name_inverse', 'является текущим смотрителем для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1910, 'P50', 'en', 'name_inverse', 'is current keeper of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1911, 'P50', 'de', 'name_inverse', 'ist derzeitiger Betreuer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1912, 'P50', 'fr', 'name_inverse', 'est actuel détenteur de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1913, 'P50', 'el', 'name_inverse', 'κατέχει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1914, 'P50', 'pt', 'name_inverse', 'é guardador de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1915, 'P50', 'cn', 'name_inverse', '目前保管', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1916, 'P50', 'en', 'comment', 'This property identifies the E39 Actor or Actors who had custody of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
	P50 has current keeper (is current keeper of) is a shortcut for the more detailed path from E18 Physical Thing through P30 transferred custody of (custody transferred through), E10 Transfer of Custody, P29 custody received by (received custody through) to E39 Actor.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1917, 'P51', 'de', 'name', 'hat früheren oder derzeitigen Besitzer ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1918, 'P51', 'ru', 'name', 'имеет бывшего или текущего владельца', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1919, 'P51', 'el', 'name', 'έχει ή είχε ιδιοκτήτη', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1920, 'P51', 'fr', 'name', 'est ou a été possédée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1921, 'P51', 'en', 'name', 'has former or current owner', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1922, 'P51', 'pt', 'name', 'é ou foi propriedade de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1923, 'P51', 'cn', 'name', '有前任或现任物主', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1924, 'P51', 'ru', 'name_inverse', 'является бывшим или текущим владельцем для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1925, 'P51', 'el', 'name_inverse', 'είναι ή ήταν ιδιοκτήτης του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1926, 'P51', 'fr', 'name_inverse', 'est ou a été propriétaire de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1927, 'P51', 'en', 'name_inverse', 'is former or current owner of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1928, 'P51', 'de', 'name_inverse', 'ist früherer oder derzeitiger Besitzer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1929, 'P51', 'pt', 'name_inverse', 'é ou foi proprietário de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1930, 'P51', 'cn', 'name_inverse', '目前或曾经拥有', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1931, 'P51', 'en', 'comment', 'This property identifies the E39 Actor that is or has been the legal owner (i.e. title holder) of an instance of E18 Physical Thing at some time.
The distinction with P52 has current owner (is current owner of) is that P51 has former or current owner (is former or current owner of) does not indicate whether the specified owners are current. P51 has former or current owner (is former or current owner of) is a shortcut for the more detailed path from E18 Physical Thing through P24 transferred title of (changed ownership through), E8 Acquisition, P23 transferred title from (surrendered title through), or P22 transferred title to (acquired title through) to E39 Actor.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1932, 'P52', 'en', 'name', 'has current owner', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1933, 'P52', 'de', 'name', 'hat derzeitigen Besitzer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1934, 'P52', 'ru', 'name', 'имеет текущего владельца', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1935, 'P52', 'fr', 'name', 'est actuellement possédée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1936, 'P52', 'el', 'name', 'έχει ιδιοκτήτη', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1937, 'P52', 'pt', 'name', 'é propriedade de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1938, 'P52', 'cn', 'name', '有现任物主', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1939, 'P52', 'de', 'name_inverse', 'ist derzeitiger Besitzer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1940, 'P52', 'fr', 'name_inverse', 'est le propriétaire actuel de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1941, 'P52', 'en', 'name_inverse', 'is current owner of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1942, 'P52', 'ru', 'name_inverse', 'является текущим владельцем для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1943, 'P52', 'el', 'name_inverse', 'είναι ιδιοκτήτης του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1944, 'P52', 'pt', 'name_inverse', 'é proprietário de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1945, 'P52', 'cn', 'name_inverse', '目前拥有', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1946, 'P52', 'en', 'comment', 'This property identifies the E21 Person, E74 Group or E40 Legal Body that was the owner of an instance of E18 Physical Thing at the time of validity of the record or database containing the statement that uses this property.
P52 has current owner (is current owner of) is a shortcut for the more detailed path from E18 Physical Thing through P24 transferred title of (changed ownership through), E8 Acquisition, P22 transferred title to (acquired title through) to E39 Actor, if and only if this acquisition event is the most recent.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1947, 'P53', 'fr', 'name', 'a ou a eu pour localisation', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1948, 'P53', 'el', 'name', 'βρίσκεται ή βρισκόταν σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1949, 'P53', 'ru', 'name', 'имеет текущее или бывшее местоположение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1950, 'P53', 'en', 'name', 'has former or current location', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1951, 'P53', 'de', 'name', 'hat früheren oder derzeitigen Standort', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1952, 'P53', 'pt', 'name', 'é ou foi localizada em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1953, 'P53', 'cn', 'name', '目前或曾经被置放於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1954, 'P53', 'ru', 'name_inverse', 'является текущим или бывшим местоположением для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1955, 'P53', 'en', 'name_inverse', 'is former or current location of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1956, 'P53', 'el', 'name_inverse', 'είναι ή ήταν θέση του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1957, 'P53', 'de', 'name_inverse', 'ist früherer oder derzeitiger Standort von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1958, 'P53', 'fr', 'name_inverse', 'est ou a été localisation de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1959, 'P53', 'pt', 'name_inverse', 'é ou foi localização de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1960, 'P53', 'cn', 'name_inverse', '目前或曾经被置放了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1961, 'P53', 'en', 'comment', 'This property allows an instance of E53 Place to be associated as the former or current location of an instance of E18 Physical Thing.
In the case of E19 Physical Objects, the property does not allow any indication of the Time-Span during which the Physical Object was located at this Place, nor if this is the current location.
In the case of immobile objects, the Place would normally correspond to the Place of creation.
P53 has former or current location (is former or current location of) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P25 moved (moved by), E9 Move, P26 moved to (was destination of) or P27 moved from (was origin of) to E53 Place.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1962, 'P54', 'fr', 'name', 'a actuellement pour localisation à demeure', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1963, 'P54', 'de', 'name', 'hat derzeitigen permanenten Standort', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1964, 'P54', 'en', 'name', 'has current permanent location', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1965, 'P54', 'el', 'name', 'έχει μόνιμη θέση', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1966, 'P54', 'ru', 'name', 'имеет текущее постоянное местоположение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1967, 'P54', 'pt', 'name', 'é localizado permanentemente em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1968, 'P54', 'cn', 'name', '目前的永久位置位於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1969, 'P54', 'el', 'name_inverse', 'είναι μόνιμη θέση του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1970, 'P54', 'de', 'name_inverse', 'ist derzeitiger permanenter Standort von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1971, 'P54', 'fr', 'name_inverse', 'est actuellement localisation à demeure de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1972, 'P54', 'en', 'name_inverse', 'is current permanent location of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1973, 'P54', 'ru', 'name_inverse', 'является текущим постоянным местоположением для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1974, 'P54', 'pt', 'name_inverse', 'é localização permanente de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1975, 'P54', 'cn', 'name_inverse', '目前被用来永久置放', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1976, 'P54', 'en', 'comment', 'This property records the foreseen permanent location of an instance of E19 Physical Object at the time of validity of the record or database containing the statement that uses this property.
P54 has current permanent location (is current permanent location of) is similar to P55 has current location (currently holds). However, it indicates the E53 Place currently reserved for an object, such as the permanent storage location or a permanent exhibit location. The object may be temporarily removed from the permanent location, for example when used in temporary exhibitions or loaned to another institution. The object may never actually be located at its permanent location.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1977, 'P55', 'el', 'name', 'βρίσκεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1978, 'P55', 'en', 'name', 'has current location', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1979, 'P55', 'fr', 'name', 'a pour localisation actuelle', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1980, 'P55', 'ru', 'name', 'в данный момент находится в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1981, 'P55', 'de', 'name', 'hat derzeitigen Standort', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1982, 'P55', 'pt', 'name', 'é localizado em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1983, 'P55', 'cn', 'name', '目前被置放於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1984, 'P55', 'de', 'name_inverse', 'hält derzeitig', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1985, 'P55', 'el', 'name_inverse', 'είναι θέση του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1986, 'P55', 'ru', 'name_inverse', 'в данный момент содержит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1987, 'P55', 'fr', 'name_inverse', 'est localisation actuelle de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1988, 'P55', 'en', 'name_inverse', 'currently holds', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1989, 'P55', 'pt', 'name_inverse', 'é localização atual de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1990, 'P55', 'cn', 'name_inverse', '目前置放了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1991, 'P59', 'en', 'comment', 'This property links an area to the instance of E18 Physical Thing upon which it is found.
It is typically used when a named E46 Section Definition is not appropriate.
E18 Physical Thing may be subdivided into arbitrary regions. 
P59 has section (is located on or within) is a shortcut. If the E53 Place is identified by a Section Definition, a more detailed representation can make use of the fully developed (i.e. indirect) path from E18 Physical Thing through P58 has section definition (defines section), E46 Section Definition, P87 is identified by (identifies) to E53 Place. A Place can only be located on or within one Physical Object.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1992, 'P55', 'en', 'comment', 'This property records the location of an E19 Physical Object at the time of validity of the record or database containing the statement that uses this property. 
	This property is a specialisation of P53 has former or current location (is former or current location of). It indicates that the E53 Place associated with the E19 Physical Object is the current location of the object. The property does not allow any indication of how long the Object has been at the current location. 
P55 has current location (currently holds) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P25 moved (moved by), E9 Move P26 moved to (was destination of) to E53 Place if and only if this Move is the most recent.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1993, 'P56', 'ru', 'name', 'несет признак', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1994, 'P56', 'de', 'name', 'trägt Merkmal', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1995, 'P56', 'fr', 'name', 'présente pour caractéristique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1996, 'P56', 'el', 'name', 'φέρει μόρφωμα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1997, 'P56', 'en', 'name', 'bears feature', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1998, 'P56', 'pt', 'name', 'possui característica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (1999, 'P56', 'cn', 'name', '有外貌表征', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2000, 'P56', 'el', 'name_inverse', 'βρίσκεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2001, 'P56', 'fr', 'name_inverse', 'se trouve sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2002, 'P56', 'de', 'name_inverse', 'wird gefunden auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2003, 'P56', 'en', 'name_inverse', 'is found on', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2004, 'P56', 'ru', 'name_inverse', 'найден на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2005, 'P56', 'pt', 'name_inverse', 'é encontrada em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2006, 'P56', 'cn', 'name_inverse', '被见於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2140, 'P71', 'pt', 'name_inverse', 'é definido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2141, 'P71', 'cn', 'name_inverse', '被条列於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2142, 'P71', 'en', 'comment', 'This property documents a source E32 Authority Document for an instance of an E1 CRM Entity.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2143, 'P72', 'fr', 'name', 'est en langue', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2144, 'P72', 'ru', 'name', 'имеет язык', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2007, 'P56', 'en', 'comment', 'This property describes a E26 Physical Feature found on a E19 Physical Object It does not specify the location of the feature on the object.
P56 bears feature (is found on) is a shortcut. A more detailed representation can make use of the fully developed (i.e. indirect) path from E19 Physical Object through P59 has section (is located on or within), E53 Place, P53 has former or current location (is former or current location of) to E26 Physical Feature.
A Physical Feature can only exist on one object. One object may bear more than one Physical Feature. An E27 Site should be considered as an E26 Physical Feature on the surface of the Earth.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2008, 'P57', 'en', 'name', 'has number of parts', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2009, 'P57', 'ru', 'name', 'имеет число частей', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2010, 'P57', 'el', 'name', 'έχει αριθμό μερών', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2011, 'P57', 'fr', 'name', 'a pour nombre de parties', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2012, 'P57', 'de', 'name', 'hat Anzahl Teile', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2013, 'P57', 'pt', 'name', 'tem número de partes', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2014, 'P57', 'cn', 'name', '有组件数目', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2015, 'P57', 'en', 'comment', 'This property documents the E60 Number of parts of which an instance of E19 Physical Object is composed.
This may be used as a method of checking inventory counts with regard to aggregate or collective objects. What constitutes a part or component depends on the context and requirements of the documentation. Normally, the parts documented in this way would not be considered as worthy of individual attention.
For a more complete description, objects may be decomposed into their components and constituents using P46 is composed of (forms parts of) and P45 consists of (is incorporated in). This allows each element to be described individually.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2016, 'P58', 'en', 'name', 'has section definition', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2017, 'P58', 'de', 'name', 'hat Abschittsdefinition', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2018, 'P58', 'ru', 'name', 'имеет определение района', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2019, 'P58', 'el', 'name', 'έχει ορισμό τμήματος', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2020, 'P58', 'fr', 'name', 'a pour désignation de section', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2021, 'P58', 'pt', 'name', 'tem designação de seção', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2022, 'P58', 'cn', 'name', '有区域定义', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2023, 'P58', 'ru', 'name_inverse', 'определяет район', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2024, 'P58', 'en', 'name_inverse', 'defines section', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2025, 'P58', 'de', 'name_inverse', 'definiert Abschitt auf oder von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2026, 'P58', 'fr', 'name_inverse', 'définit une section de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2027, 'P58', 'el', 'name_inverse', 'ορίζει τμήμα σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2028, 'P58', 'pt', 'name_inverse', 'define uma seção de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2029, 'P58', 'cn', 'name_inverse', '界定了区域於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2030, 'P58', 'en', 'comment', 'This property links an area (section) named by a E46 Section Definition to the instance of E18 Physical Thing upon which it is found.
The CRM handles sections as locations (instances of E53 Place) within or on E18 Physical Thing that are identified by E46 Section Definitions. Sections need not be discrete and separable components or parts of an object.
This is part of a more developed path from E18 Physical Thing through P58, E46 Section Definition, P87 is identified by (identifies) that allows a more precise definition of a location found on an object than the shortcut P59 has section (is located on or within).
A particular instance of a Section Definition only applies to one instance of Physical Thing.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2031, 'P59', 'en', 'name', 'has section', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2032, 'P59', 'el', 'name', 'έχει τομέα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2033, 'P59', 'de', 'name', 'hat Bereich', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2034, 'P59', 'ru', 'name', 'имеет район', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2035, 'P59', 'fr', 'name', 'a pour section', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2036, 'P59', 'pt', 'name', 'tem seção', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2037, 'P59', 'cn', 'name', '有区域', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2038, 'P59', 'ru', 'name_inverse', 'находится на или внутри', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2039, 'P59', 'de', 'name_inverse', 'befindet sich auf oder in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2040, 'P59', 'el', 'name_inverse', 'βρίσκεται σε ή εντός', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2041, 'P59', 'fr', 'name_inverse', 'se situe sur ou dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2042, 'P59', 'en', 'name_inverse', 'is located on or within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2043, 'P59', 'pt', 'name_inverse', 'está localizada sobre ou dentro de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2044, 'P59', 'cn', 'name_inverse', '位於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2045, 'P62', 'de', 'name', 'bildet ab', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2046, 'P62', 'ru', 'name', 'описывает', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2047, 'P62', 'en', 'name', 'depicts', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2048, 'P62', 'el', 'name', 'απεικονίζει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2049, 'P62', 'fr', 'name', 'figure', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2050, 'P62', 'pt', 'name', 'retrata', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2051, 'P62', 'cn', 'name', '描绘', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2052, 'P62', 'el', 'name_inverse', 'απεικονίζεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2053, 'P62', 'de', 'name_inverse', 'wird abgebildet durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2054, 'P62', 'en', 'name_inverse', 'is depicted by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2055, 'P62', 'ru', 'name_inverse', 'описан посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2056, 'P62', 'fr', 'name_inverse', 'est figurée sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2057, 'P62', 'pt', 'name_inverse', 'é retratada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2058, 'P62', 'cn', 'name_inverse', '被描绘於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2059, 'P62', 'en', 'comment', 'This property identifies something that is depicted by an instance of E24 Physical Man-Made Thing.
This property is a shortcut of the more fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1CRM Entity. P62.1 mode of depiction allows the nature of the depiction to be refined.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2060, 'P65', 'fr', 'name', 'présente l''item visuel', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2061, 'P65', 'en', 'name', 'shows visual item', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2062, 'P65', 'de', 'name', 'zeigt Bildliches', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2063, 'P65', 'ru', 'name', 'показывает визуальный предмет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2064, 'P65', 'el', 'name', 'εμφανίζει οπτικό στοιχείο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2065, 'P65', 'pt', 'name', 'apresenta item visual', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2066, 'P65', 'cn', 'name', '显示视觉项目', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2067, 'P65', 'de', 'name_inverse', 'wird gezeigt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2068, 'P65', 'fr', 'name_inverse', 'est présenté par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2069, 'P65', 'en', 'name_inverse', 'is shown by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2070, 'P65', 'el', 'name_inverse', 'εμφανίζεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2071, 'P65', 'ru', 'name_inverse', 'показан посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2072, 'P65', 'pt', 'name_inverse', 'é apresentado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2073, 'P65', 'cn', 'name_inverse', '被显示於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2145, 'P72', 'en', 'name', 'has language', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2146, 'P72', 'de', 'name', 'hat Sprache', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2147, 'P72', 'el', 'name', 'έχει γλώσσα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2148, 'P72', 'pt', 'name', 'é da língua ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2149, 'P72', 'cn', 'name', '使用语言', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2074, 'P65', 'en', 'comment', 'This property documents an E36 Visual Item shown by an instance of E24 Physical Man-Made Thing.
This property is similar to P62 depicts (is depicted by) in that it associates an item of E24 Physical Man-Made Thing with a visual representation. However, P65 shows visual item (is shown by) differs from the P62 depicts (is depicted by) property in that it makes no claims about what the E36 Visual Item is deemed to represent. E36 Visual Item identifies a recognisable image or visual symbol, regardless of what this image may or may not represent.
For example, all recent British coins bear a portrait of Queen Elizabeth II, a fact that is correctly documented using P62 depicts (is depicted by). Different portraits have been used at different periods, however. P65 shows visual item (is shown by) can be used to refer to a particular portrait.
P65 shows visual item (is shown by) may also be used for Visual Items such as signs, marks and symbols, for example the ''Maltese Cross'' or the ''copyright symbol’ that have no particular representational content. 
This property is part of the fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1 CRM Entity which is shortcut by, P62 depicts (is depicted by).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2075, 'P67', 'el', 'name', 'αναφέρεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2076, 'P67', 'en', 'name', 'refers to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2077, 'P67', 'ru', 'name', 'ссылается на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2078, 'P67', 'fr', 'name', 'fait référence à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2079, 'P67', 'de', 'name', 'verweist auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2080, 'P67', 'pt', 'name', 'referencia', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2081, 'P67', 'cn', 'name', '论及', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2082, 'P67', 'fr', 'name_inverse', 'est référencé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2083, 'P67', 'el', 'name_inverse', 'αναφέρεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2084, 'P67', 'de', 'name_inverse', 'wird angeführt von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2085, 'P67', 'en', 'name_inverse', 'is referred to by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2086, 'P67', 'ru', 'name_inverse', 'имеет ссылку на себя от', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2087, 'P67', 'pt', 'name_inverse', 'é referenciado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2088, 'P67', 'cn', 'name_inverse', '被论及於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2089, 'P67', 'en', 'comment', 'This property documents that an E89 Propositional Object makes a statement about an instance of E1 CRM Entity. P67 refers to (is referred to by) has the P67.1 has type link to an instance of E55 Type. This is intended to allow a more detailed description of the type of reference. This differs from P129 is about (is subject of), which describes the primary subject or subjects of the E89 Propositional Object.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2090, 'P68', 'en', 'name', 'foresees use of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2091, 'P68', 'de', 'name', ' sieht den Gebrauch vor von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2092, 'P68', 'ru', 'name', 'обычно применяет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2093, 'P68', 'fr', 'name', 'utilise habituellement', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2094, 'P68', 'el', 'name', 'συνήθως χρησιμοποιεί', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2095, 'P68', 'pt', 'name', 'normalmente emprega', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2096, 'P68', 'cn', 'name', '指定使用材料', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2097, 'P68', 'el', 'name_inverse', 'συνήθως χρησιμοποιείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2098, 'P68', 'de', 'name_inverse', 'vorgesehen für Gebrauch durch defined', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2099, 'P68', 'fr', 'name_inverse', 'est habituellement utilisé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2100, 'P68', 'ru', 'name_inverse', 'обычно используется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2101, 'P68', 'en', 'name_inverse', 'use foreseen by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2102, 'P68', 'pt', 'name_inverse', 'é empregado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2103, 'P68', 'cn', 'name_inverse', '被指定使用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2104, 'P68', 'en', 'comment', 'This property identifies an E57 Material foreseeen to be used by an E29 Design or Procedure. 
E29 Designs and procedures commonly foresee the use of particular E57 Materials. The fabrication of adobe bricks, for example, requires straw, clay and water. This property enables this to be documented.
This property is not intended for the documentation of E57 Materials that were used on a particular occasion when an instance of E29 Design or Procedure was executed.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2105, 'P69', 'fr', 'name', 'est associée à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2106, 'P69', 'el', 'name', 'σχετίζεται με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2107, 'P69', 'ru', 'name', 'ассоциирован с', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2108, 'P69', 'de', 'name', 'ist verbunden mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2109, 'P69', 'en', 'name', 'is associated with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2110, 'P69', 'pt', 'name', 'é associado com', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2111, 'P69', 'cn', 'name', '相关於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2112, 'P69', 'en', 'comment', 'This symmetric property describes the association of an E29 Design or Procedure with other Designs or Procedures.
Any instance of E29 Design or Procedure may be associated with other designs or procedures. The P69.1 has type property of P69 is associated with allows the nature of the association to be specified; examples of types of association between instances of E29 Design or Procedure include: whole-part, sequence, prerequisite, etc.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2113, 'P70', 'fr', 'name', 'mentionne', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2114, 'P70', 'ru', 'name', 'документирует', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2115, 'P70', 'el', 'name', 'τεκμηριώνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2116, 'P70', 'en', 'name', 'documents', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2117, 'P70', 'de', 'name', 'belegt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2118, 'P70', 'pt', 'name', 'documenta', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2119, 'P70', 'cn', 'name', '记录了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2120, 'P70', 'en', 'name_inverse', 'is documented in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2121, 'P70', 'el', 'name_inverse', 'τεκμηριώνεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2122, 'P70', 'de', 'name_inverse', 'wird belegt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2123, 'P70', 'fr', 'name_inverse', 'est mentionnée dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2124, 'P70', 'ru', 'name_inverse', 'документирован в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2125, 'P70', 'pt', 'name_inverse', 'é documentado em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2126, 'P70', 'cn', 'name_inverse', '被记录於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2127, 'P70', 'en', 'comment', 'This property describes the CRM Entities documented by instances of E31 Document.
Documents may describe any conceivable entity, hence the link to the highest-level entity in the CRM hierarchy. This property is intended for cases where a reference is regarded as being of a documentary character, in the scholarly or scientific sense.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2128, 'P71', 'de', 'name', 'listet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2129, 'P71', 'ru', 'name', 'перечисляет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2130, 'P71', 'en', 'name', 'lists', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2131, 'P71', 'el', 'name', 'περιλαμβάνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2132, 'P71', 'fr', 'name', 'définit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2133, 'P71', 'pt', 'name', 'define', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2134, 'P71', 'cn', 'name', '条列出', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2135, 'P71', 'el', 'name_inverse', 'περιλαμβάνεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2136, 'P71', 'de', 'name_inverse', 'wird aufgelistet in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2137, 'P71', 'en', 'name_inverse', 'is listed in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2138, 'P71', 'ru', 'name_inverse', 'перечислен в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2139, 'P71', 'fr', 'name_inverse', 'est défini par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2150, 'P72', 'de', 'name_inverse', 'ist Sprache von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2151, 'P72', 'el', 'name_inverse', 'είναι γλώσσα του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2152, 'P72', 'fr', 'name_inverse', 'est la langue de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2153, 'P72', 'ru', 'name_inverse', 'является языком для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2154, 'P72', 'en', 'name_inverse', 'is language of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2155, 'P72', 'pt', 'name_inverse', 'é a língua de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2156, 'P72', 'cn', 'name_inverse', '被用来撰写', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2157, 'P72', 'en', 'comment', 'This property describes the E56 Language of an E33 Linguistic Object. 
Linguistic Objects are composed in one or more human Languages. This property allows these languages to be documented.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2158, 'P73', 'el', 'name', 'έχει μετάφραση', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2159, 'P73', 'de', 'name', 'hat Übersetzung', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2160, 'P73', 'ru', 'name', 'имеет перевод', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2161, 'P73', 'en', 'name', 'has translation', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2162, 'P73', 'fr', 'name', 'a pour traduction', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2163, 'P73', 'pt', 'name', 'tem tradução', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2164, 'P73', 'cn', 'name', '有译文', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2165, 'P73', 'fr', 'name_inverse', 'est la traduction de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2166, 'P73', 'ru', 'name_inverse', 'является переводом', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2167, 'P73', 'el', 'name_inverse', 'είναι μετάφραση του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2168, 'P73', 'de', 'name_inverse', 'ist Übersetzung von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2169, 'P73', 'en', 'name_inverse', 'is translation of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2170, 'P73', 'pt', 'name_inverse', 'é tradução de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2171, 'P73', 'cn', 'name_inverse', '翻译自', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2172, 'P73', 'en', 'comment', 'This property describes the source and target of instances of E33Linguistic Object involved in a translation.
When a Linguistic Object is translated into a new language it becomes a new Linguistic Object, despite being conceptually similar to the source object.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2173, 'P74', 'ru', 'name', 'имеет текущее или бывшее местожительства', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2174, 'P74', 'en', 'name', 'has current or former residence', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2175, 'P74', 'de', 'name', 'hat derzeitigen oder früheren Sitz', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2176, 'P74', 'el', 'name', 'έχει ή είχε κατοικία', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2177, 'P74', 'fr', 'name', 'réside ou a résidé à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2178, 'P74', 'pt', 'name', 'reside ou residiu em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2179, 'P74', 'cn', 'name', '目前或曾经居住於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2180, 'P74', 'el', 'name_inverse', 'είναι ή ήταν κατοικία του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2181, 'P74', 'de', 'name_inverse', 'ist derzeitiger oder früherer Sitz von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2182, 'P74', 'fr', 'name_inverse', 'est ou a été la résidence de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2183, 'P74', 'ru', 'name_inverse', 'является текущим или бывшим местом жительства для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2184, 'P74', 'en', 'name_inverse', 'is current or former residence of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2185, 'P74', 'pt', 'name_inverse', 'é ou foi residência de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2186, 'P74', 'cn', 'name_inverse', '历年来的居住者包括', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2187, 'P74', 'en', 'comment', 'This property describes the current or former E53 Place of residence of an E39 Actor. 
The residence may be either the Place where the Actor resides, or a legally registered address of any kind.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2188, 'P75', 'ru', 'name', 'владеет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2189, 'P75', 'el', 'name', 'κατέχει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2190, 'P75', 'de', 'name', 'besitzt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2191, 'P75', 'fr', 'name', 'est détenteur de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2192, 'P75', 'en', 'name', 'possesses', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2193, 'P75', 'pt', 'name', 'é detentor de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2194, 'P75', 'cn', 'name', '拥有', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2195, 'P75', 'el', 'name_inverse', 'κατέχεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2196, 'P75', 'ru', 'name_inverse', 'принадлежит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2197, 'P75', 'de', 'name_inverse', 'sind im Besitz von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2198, 'P75', 'fr', 'name_inverse', 'est détenu par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2199, 'P75', 'en', 'name_inverse', 'is possessed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2200, 'P75', 'pt', 'name_inverse', 'são detidos por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2201, 'P75', 'cn', 'name_inverse', '有拥有者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2202, 'P75', 'en', 'comment', 'This property identifies former or current instances of E30 Rights held by an E39 Actor.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2203, 'P76', 'en', 'name', 'has contact point', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2204, 'P76', 'ru', 'name', 'имеет контакт', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2205, 'P76', 'fr', 'name', 'a pour coordonnées individuelles', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2206, 'P76', 'el', 'name', 'έχει σημείο επικοινωνίας', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2207, 'P76', 'de', 'name', 'hat Kontaktpunkt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2208, 'P76', 'pt', 'name', 'possui ponto de contato', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2209, 'P76', 'cn', 'name', '有联系方式', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2210, 'P76', 'fr', 'name_inverse', 'permettent de contacter', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2211, 'P76', 'de', 'name_inverse', 'bietet Zugang zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2212, 'P76', 'en', 'name_inverse', 'provides access to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2213, 'P76', 'el', 'name_inverse', 'παρέχει πρόσβαση σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2214, 'P76', 'ru', 'name_inverse', 'предоставляет доступ к', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2215, 'P76', 'pt', 'name_inverse', 'é ponto de contado de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2216, 'P76', 'cn', 'name_inverse', '被用来联系', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2217, 'P76', 'en', 'comment', 'This property identifies an E51 Contact Point of any type that provides access to an E39 Actor by any communication method, such as e-mail or fax.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2218, 'P78', 'el', 'name', 'αναγνωρίζεται ως', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2219, 'P78', 'fr', 'name', 'est identifiée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2220, 'P78', 'en', 'name', 'is identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2221, 'P78', 'ru', 'name', 'идентифицируется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2222, 'P78', 'de', 'name', 'wird bezeichnet als', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2223, 'P78', 'pt', 'name', 'é identificado por ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2224, 'P78', 'cn', 'name', '有识别称号', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2225, 'P78', 'en', 'name_inverse', 'identifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2226, 'P78', 'de', 'name_inverse', 'bezeichnet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2227, 'P78', 'fr', 'name_inverse', 'identifie', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2228, 'P78', 'el', 'name_inverse', 'είναι αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2229, 'P78', 'ru', 'name_inverse', 'идентифицирует', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2230, 'P78', 'pt', 'name_inverse', 'identifica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2231, 'P78', 'cn', 'name_inverse', '被用来识别', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2232, 'P78', 'en', 'comment', 'This property identifies an E52 Time-Span using an E49Time Appellation.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2233, 'P79', 'el', 'name', 'αρχή προσδιορίζεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2234, 'P79', 'ru', 'name', 'начало ограничено', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2235, 'P79', 'de', 'name', 'hat Anfangsbegründung', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3097, 'P146', 'de', 'name', 'entließ von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2236, 'P79', 'en', 'name', 'beginning is qualified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2237, 'P79', 'fr', 'name', 'début est qualifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2238, 'P79', 'pt', 'name', 'início é qualificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2239, 'P79', 'cn', 'name', '起点认定的性质是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2240, 'P79', 'en', 'comment', 'This property qualifies the beginning of an E52 Time-Span in some way. 
The nature of the qualification may be certainty, precision, source etc.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2241, 'P80', 'el', 'name', 'τέλος προσδιορίζεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2242, 'P80', 'fr', 'name', 'fin est qualifiée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2243, 'P80', 'de', 'name', 'hat Begründung des Endes', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2244, 'P80', 'ru', 'name', 'конец ограничен', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2245, 'P80', 'en', 'name', 'end is qualified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2246, 'P80', 'pt', 'name', 'final é qualificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2247, 'P80', 'cn', 'name', '终点认定的性质是', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2248, 'P80', 'en', 'comment', 'This property qualifies the end of an E52 Time-Span in some way. 
The nature of the qualification may be certainty, precision, source etc.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2249, 'P81', 'en', 'name', 'ongoing throughout', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2250, 'P81', 'el', 'name', 'καθόλη τη διάρκεια του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2251, 'P81', 'de', 'name', 'andauernd während', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2252, 'P81', 'fr', 'name', 'couvre au moins', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2253, 'P81', 'ru', 'name', 'длится в течение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2254, 'P81', 'pt', 'name', 'abrange no mínimo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2255, 'P81', 'cn', 'name', '时段的数值至少涵盖', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2256, 'P81', 'en', 'comment', 'This property describes the minimum period of time covered by an E52 Time-Span.
Since Time-Spans may not have precisely known temporal extents, the CRM supports statements about the minimum and maximum temporal extents of Time-Spans. This property allows a Time-Span’s minimum temporal extent (i.e. its inner boundary) to be assigned an E61 Time Primitive value. Time Primitives are treated by the CRM as application or system specific date intervals, and are not further analysed.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2257, 'P82', 'el', 'name', 'κάποτε εντός', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2258, 'P82', 'ru', 'name', 'некоторое время в течение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2259, 'P82', 'de', 'name', 'irgendwann innerhalb von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2260, 'P82', 'fr', 'name', 'couvre au plus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2261, 'P82', 'en', 'name', 'at some time within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2262, 'P82', 'pt', 'name', 'abrange no máximo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2263, 'P82', 'cn', 'name', '时段的数值不会超越', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2264, 'P82', 'en', 'comment', 'This property describes the maximum period of time within which an E52 Time-Span falls.
Since Time-Spans may not have precisely known temporal extents, the CRM supports statements about the minimum and maximum temporal extents of Time-Spans. This property allows a Time-Span’s maximum temporal extent (i.e. its outer boundary) to be assigned an E61 Time Primitive value. Time Primitives are treated by the CRM as application or system specific date intervals, and are not further analysed.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2265, 'P83', 'fr', 'name', 'a duré au moins', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2266, 'P83', 'el', 'name', 'είχε ελάχιστη διάρκεια', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2267, 'P83', 'de', 'name', 'hatte Mindestdauer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2268, 'P83', 'en', 'name', 'had at least duration', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2269, 'P83', 'ru', 'name', 'имеет длительность по крайней мере больше чем', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2270, 'P83', 'pt', 'name', 'durou no mínimo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2271, 'P83', 'cn', 'name', '时间最少持续了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2272, 'P83', 'el', 'name_inverse', 'είναι ελάχιστη διάρκεια του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2273, 'P83', 'fr', 'name_inverse', 'a été la durée minimum de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2274, 'P83', 'ru', 'name_inverse', 'был минимальной длительностью для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2275, 'P83', 'en', 'name_inverse', 'was minimum duration of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2276, 'P83', 'de', 'name_inverse', 'war Mindestdauer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2277, 'P83', 'pt', 'name_inverse', 'foi a duração mínima de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2278, 'P83', 'en', 'comment', 'This property describes the minimum length of time covered by an E52 Time-Span. 
It allows an E52 Time-Span to be associated with an E54 Dimension representing it’s minimum duration (i.e. it’s inner boundary) independent from the actual beginning and end.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2279, 'P84', 'el', 'name', 'είχε μέγιστη διάρκεια', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2280, 'P84', 'en', 'name', 'had at most duration', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2281, 'P84', 'de', 'name', 'hatte Höchstdauer', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2282, 'P84', 'ru', 'name', 'имеет длительность меньше чем', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2283, 'P84', 'fr', 'name', 'a duré au plus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2284, 'P84', 'pt', 'name', 'durou no máximo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2285, 'P84', 'cn', 'name', '时间最多持续了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2286, 'P84', 'ru', 'name_inverse', 'был максимальной длительностью для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2287, 'P84', 'de', 'name_inverse', 'war längste Dauer von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2288, 'P84', 'en', 'name_inverse', 'was maximum duration of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2289, 'P84', 'el', 'name_inverse', 'είναι μέγιστη διάρκεια του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2290, 'P84', 'fr', 'name_inverse', 'a été la durée maximum de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2291, 'P84', 'pt', 'name_inverse', 'foi a duração máxima de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2292, 'P84', 'cn', 'name_inverse', '', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2293, 'P84', 'en', 'comment', 'This property describes the maximum length of time covered by an E52 Time-Span. 
It allows an E52 Time-Span to be associated with an E54 Dimension representing it’s maximum duration (i.e. it’s outer boundary) independent from the actual beginning and end.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2294, 'P86', 'en', 'name', 'falls within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2295, 'P86', 'ru', 'name', 'содержится в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2296, 'P86', 'el', 'name', 'περιέχεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2297, 'P86', 'fr', 'name', 's’insère dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2298, 'P86', 'de', 'name', 'fällt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2299, 'P86', 'pt', 'name', 'está contido em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2300, 'P86', 'cn', 'name', '时间上被涵盖於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2301, 'P86', 'fr', 'name_inverse', 'inclut', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2302, 'P86', 'de', 'name_inverse', 'enthält', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2303, 'P86', 'en', 'name_inverse', 'contains', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2304, 'P86', 'el', 'name_inverse', 'περιέχει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2305, 'P86', 'ru', 'name_inverse', 'содержит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2306, 'P86', 'pt', 'name_inverse', 'contém', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2307, 'P86', 'cn', 'name_inverse', '时间上涵盖了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2308, 'P86', 'en', 'comment', 'This property describes the inclusion relationship between two instances of E52 Time-Span.
This property supports the notion that a Time-Span’s temporal extent falls within the temporal extent of another Time-Span. It addresses temporal containment only, and no contextual link between the two instances of Time-Span is implied.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2309, 'P87', 'el', 'name', 'αναγνωρίζεται ως', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2310, 'P87', 'en', 'name', 'is identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2311, 'P87', 'ru', 'name', 'идентифицируется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2312, 'P87', 'fr', 'name', 'est identifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2313, 'P87', 'de', 'name', 'wird bezeichnet als', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2314, 'P87', 'pt', 'name', 'é identificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2315, 'P87', 'cn', 'name', '有辨认码', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2316, 'P87', 'de', 'name_inverse', 'bezeichnet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2317, 'P87', 'el', 'name_inverse', 'είναι αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2318, 'P87', 'ru', 'name_inverse', 'идентифицирует', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2319, 'P87', 'fr', 'name_inverse', 'identifie', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2320, 'P87', 'en', 'name_inverse', 'identifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2321, 'P87', 'pt', 'name_inverse', 'identifica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2322, 'P87', 'cn', 'name_inverse', '被用来辨认', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2323, 'P87', 'en', 'comment', 'This property identifies an E53 Place using an E44 Place Appellation. 
Examples of Place Appellations used to identify Places include instances of E48 Place Name, addresses, E47 Spatial Coordinates etc.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2324, 'P89', 'fr', 'name', 's’insère dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2325, 'P89', 'en', 'name', 'falls within', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2326, 'P89', 'ru', 'name', 'содержится в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2327, 'P89', 'de', 'name', 'fällt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2328, 'P89', 'el', 'name', 'περιέχεται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2329, 'P89', 'pt', 'name', 'está contido em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2330, 'P89', 'cn', 'name', '空间上被包围於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2331, 'P89', 'fr', 'name_inverse', 'inclut', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2332, 'P89', 'ru', 'name_inverse', 'содержит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2333, 'P89', 'el', 'name_inverse', 'περιέχει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2334, 'P89', 'de', 'name_inverse', 'enthält', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2335, 'P89', 'en', 'name_inverse', 'contains', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2336, 'P89', 'pt', 'name_inverse', 'contém', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2337, 'P89', 'cn', 'name_inverse', '空间上包含了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2338, 'P89', 'en', 'comment', 'This property identifies the instances of E53 Places that fall within the area covered by another Place.
It addresses spatial containment only, and no ‘whole-part’ relationship between the two places is implied.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2339, 'P90', 'de', 'name', 'hat Wert', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2340, 'P90', 'el', 'name', 'έχει τιμή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2341, 'P90', 'fr', 'name', 'a la valeur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2342, 'P90', 'ru', 'name', 'имеет значение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2343, 'P90', 'en', 'name', 'has value', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2344, 'P90', 'pt', 'name', 'tem valor', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2345, 'P90', 'cn', 'name', '有数值', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2346, 'P90', 'en', 'comment', 'This property allows an E54 Dimension to be approximated by an E60 Number primitive.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2347, 'P91', 'ru', 'name', 'имеет единицу', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2348, 'P91', 'el', 'name', 'έχει μονάδα μέτρησης', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2349, 'P91', 'fr', 'name', 'a pour unité', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2350, 'P91', 'de', 'name', 'hat Einheit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2351, 'P91', 'en', 'name', 'has unit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2352, 'P91', 'pt', 'name', 'tem unidade', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2353, 'P91', 'cn', 'name', '有单位', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2354, 'P91', 'ru', 'name_inverse', 'является единицей для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2355, 'P91', 'fr', 'name_inverse', 'est l''unité de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2356, 'P91', 'de', 'name_inverse', 'ist Einheit von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2357, 'P91', 'el', 'name_inverse', 'αποτελεί μονάδα μέτρησης του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2358, 'P91', 'en', 'name_inverse', 'is unit of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2359, 'P91', 'pt', 'name_inverse', 'é unidade de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2360, 'P91', 'cn', 'name_inverse', '被当做单位来表示', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2361, 'P91', 'en', 'comment', 'This property shows the type of unit an E54 Dimension was expressed in.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2362, 'P92', 'fr', 'name', 'a fait exister', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2363, 'P92', 'en', 'name', 'brought into existence', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2364, 'P92', 'ru', 'name', 'создал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2365, 'P92', 'de', 'name', 'brachte in Existenz', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2366, 'P92', 'el', 'name', 'γέννησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2367, 'P92', 'pt', 'name', 'trouxe à existência', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2368, 'P92', 'cn', 'name', '开始了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2369, 'P92', 'en', 'name_inverse', 'was brought into existence by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2370, 'P92', 'el', 'name_inverse', 'γεννήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2371, 'P92', 'de', 'name_inverse', 'wurde in Existenz gebracht durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2372, 'P92', 'fr', 'name_inverse', 'a commencé à exister du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2373, 'P92', 'ru', 'name_inverse', 'был создан посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2374, 'P92', 'pt', 'name_inverse', 'passou a existir por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2375, 'P92', 'cn', 'name_inverse', '被开始於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2376, 'P92', 'en', 'comment', 'This property allows an E63 Beginning of Existence event to be linked to the E77 Persistent Item brought into existence by it.
It allows a “start” to be attached to any Persistent Item being documented i.e. E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation, E51 Contact Point and E55 Type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2377, 'P93', 'fr', 'name', 'a fait cesser d’exister', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2378, 'P93', 'ru', 'name', 'положил конец существованию', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2379, 'P93', 'de', 'name', 'beendete die Existenz von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2380, 'P93', 'en', 'name', 'took out of existence', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2381, 'P93', 'el', 'name', 'αναίρεσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2382, 'P93', 'pt', 'name', 'cessou a existência de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2383, 'P93', 'cn', 'name', '结束了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2384, 'P93', 'ru', 'name_inverse', 'прекратил существование посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2385, 'P93', 'fr', 'name_inverse', 'a cessé d’exister du fait de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2386, 'P93', 'en', 'name_inverse', 'was taken out of existence by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2387, 'P93', 'el', 'name_inverse', 'αναιρέθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2388, 'P93', 'de', 'name_inverse', 'wurde seiner Existenz beraubt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2389, 'P93', 'pt', 'name_inverse', 'deixou de existir', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2390, 'P93', 'cn', 'name_inverse', '被结束於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2466, 'P98', 'en', 'comment', 'This property links an E67Birth event to an E21 Person in the role of offspring.
Twins, triplets etc. are brought into life by the same Birth event. This is not intended for use with general Natural History material, only people. There is no explicit method for modelling conception and gestation except by using extensions.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2467, 'P99', 'el', 'name', 'διέλυσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2468, 'P99', 'ru', 'name', 'распустил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2469, 'P99', 'fr', 'name', 'a dissous', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2470, 'P99', 'en', 'name', 'dissolved', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2471, 'P99', 'de', 'name', 'löste auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2391, 'P93', 'en', 'comment', 'This property allows an E64 End of Existence event to be linked to the E77 Persistent Item taken out of existence by it.
In the case of immaterial things, the E64 End of Existence is considered to take place with the destruction of the last physical carrier.
This allows an “end” to be attached to any Persistent Item being documented i.e. E70 Thing, E72 Legal Object, E39 Actor, E41 Appellation, E51 Contact Point and E55 Type. For many Persistent Items we know the maximum life-span and can infer, that they must have ended to exist. We assume in that case an End of Existence, which may be as unnoticeable as forgetting the secret knowledge by the last representative of some indigenous nation.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2392, 'P94', 'el', 'name', 'δημιούργησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2393, 'P94', 'ru', 'name', 'создал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2394, 'P94', 'en', 'name', 'has created', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2395, 'P94', 'de', 'name', 'hat erschaffen', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2396, 'P94', 'fr', 'name', 'a créé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2397, 'P94', 'pt', 'name', 'criou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2398, 'P94', 'cn', 'name', '创造了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2399, 'P94', 'el', 'name_inverse', 'δημιουργήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2400, 'P94', 'fr', 'name_inverse', 'a été créé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2401, 'P94', 'ru', 'name_inverse', 'был создан посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2402, 'P94', 'en', 'name_inverse', 'was created by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2403, 'P94', 'de', 'name_inverse', 'wurde erschaffen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2404, 'P94', 'pt', 'name_inverse', 'foi criado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2405, 'P94', 'cn', 'name_inverse', '被创造於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2406, 'P94', 'en', 'comment', 'This property allows a conceptual E65 Creation to be linked to the E28 Conceptual Object created by it. 
It represents the act of conceiving the intellectual content of the E28 Conceptual Object. It does not represent the act of creating the first physical carrier of the E28 Conceptual Object. As an example, this is the composition of a poem, not its commitment to paper.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2407, 'P95', 'fr', 'name', 'a fondé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2408, 'P95', 'ru', 'name', 'сформировал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2409, 'P95', 'de', 'name', 'hat gebildet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2410, 'P95', 'en', 'name', 'has formed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2411, 'P95', 'el', 'name', 'σχημάτισε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2412, 'P95', 'pt', 'name', 'formou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2413, 'P95', 'cn', 'name', '组成了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2414, 'P95', 'fr', 'name_inverse', 'a été fondé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2415, 'P95', 'de', 'name_inverse', 'wurde gebildet von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2416, 'P95', 'el', 'name_inverse', 'σχηματίστηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2417, 'P95', 'en', 'name_inverse', 'was formed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2418, 'P95', 'ru', 'name_inverse', 'была сформирована посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2419, 'P95', 'pt', 'name_inverse', 'foi formado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2420, 'P95', 'cn', 'name_inverse', '被组成於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2421, 'P95', 'en', 'comment', 'This property links the founding or E66 Formation for an E74 Group with the Group itself.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2422, 'P96', 'ru', 'name', 'посредством матери', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2423, 'P96', 'de', 'name', 'durch Mutter', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2424, 'P96', 'fr', 'name', 'de mère', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2425, 'P96', 'en', 'name', 'by mother', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2426, 'P96', 'el', 'name', 'είχε μητέρα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2427, 'P96', 'pt', 'name', 'pela mãe', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2428, 'P96', 'cn', 'name', '来自生母', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2429, 'P96', 'el', 'name_inverse', 'ήταν μητέρα του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2430, 'P96', 'fr', 'name_inverse', 'a donné naissance à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2431, 'P96', 'en', 'name_inverse', 'gave birth', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2432, 'P96', 'ru', 'name_inverse', 'дал рождение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2433, 'P96', 'de', 'name_inverse', 'gebar', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2434, 'P96', 'pt', 'name_inverse', 'deu nascimento', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2435, 'P96', 'cn', 'name_inverse', '成为生母於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2436, 'P96', 'en', 'comment', 'This property links an E67 Birth event to an E21 Person as a participant in the role of birth-giving mother.

Note that biological fathers are not necessarily participants in the Birth (see P97 from father (was father for)). The Person being born is linked to the Birth with the property P98 brought into life (was born). This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions. This is a sub-property of P11 had participant (participated in).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2437, 'P97', 'de', 'name', 'gab Vaterschaft', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2438, 'P97', 'ru', 'name', 'от отца', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2439, 'P97', 'en', 'name', 'from father', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2440, 'P97', 'el', 'name', 'είχε πατέρα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2441, 'P97', 'fr', 'name', 'de père', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2442, 'P97', 'pt', 'name', 'pelo pai', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2443, 'P97', 'cn', 'name', '来自父亲', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2444, 'P97', 'en', 'name_inverse', 'was father for', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2445, 'P97', 'el', 'name_inverse', 'ήταν πατέρας του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2446, 'P97', 'fr', 'name_inverse', 'a été père dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2447, 'P97', 'de', 'name_inverse', 'war Vater für', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2448, 'P97', 'ru', 'name_inverse', 'был отцом для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2449, 'P97', 'pt', 'name_inverse', 'foi pai para', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2450, 'P97', 'cn', 'name_inverse', '成为生父於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2451, 'P97', 'en', 'comment', 'This property links an E67 Birth event to an E21 Person in the role of biological father.
Note that biological fathers are not seen as necessary participants in the Birth, whereas birth-giving mothers are (see P96 by mother (gave birth)). The Person being born is linked to the Birth with the property P98 brought into life (was born).
This is not intended for use with general natural history material, only people. There is no explicit method for modelling conception and gestation except by using extensions. 
A Birth event is normally (but not always) associated with one biological father.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2452, 'P98', 'fr', 'name', 'a donné vie à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2453, 'P98', 'de', 'name', 'brachte zur Welt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2454, 'P98', 'en', 'name', 'brought into life', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2455, 'P98', 'ru', 'name', 'породил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2456, 'P98', 'el', 'name', 'έφερε στη ζωή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2457, 'P98', 'pt', 'name', 'trouxe à vida', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2458, 'P98', 'cn', 'name', '诞生了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2459, 'P98', 'fr', 'name_inverse', 'est né', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2460, 'P98', 'el', 'name_inverse', 'γεννήθηκε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2461, 'P98', 'de', 'name_inverse', 'wurde geboren durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2462, 'P98', 'en', 'name_inverse', 'was born', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2463, 'P98', 'ru', 'name_inverse', 'был рожден', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2464, 'P98', 'pt', 'name_inverse', 'veio à vida pelo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2465, 'P98', 'cn', 'name_inverse', '诞生於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2472, 'P99', 'pt', 'name', 'dissolveu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2473, 'P99', 'cn', 'name', '解散了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2474, 'P99', 'de', 'name_inverse', 'wurde aufgelöst durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2475, 'P99', 'ru', 'name_inverse', 'был распущен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2476, 'P99', 'fr', 'name_inverse', 'a été dissous par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2477, 'P99', 'el', 'name_inverse', 'διαλύθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2478, 'P99', 'en', 'name_inverse', 'was dissolved by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2479, 'P99', 'pt', 'name_inverse', 'foi dissolvido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2480, 'P99', 'cn', 'name_inverse', '被解散於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2481, 'P99', 'en', 'comment', 'This property links the disbanding or E68 Dissolution of an E74 Group to the Group itself.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2482, 'P100', 'en', 'name', 'was death of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2483, 'P100', 'fr', 'name', 'a été la mort de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2484, 'P100', 'el', 'name', 'ήταν θάνατος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2485, 'P100', 'de', 'name', 'Tod von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2486, 'P100', 'ru', 'name', 'был смертью для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2487, 'P100', 'pt', 'name', 'foi a morte para ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2488, 'P100', 'cn', 'name', '灭亡了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2489, 'P100', 'de', 'name_inverse', 'starb in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2490, 'P100', 'fr', 'name_inverse', 'est mort par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2491, 'P100', 'en', 'name_inverse', 'died in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2492, 'P100', 'el', 'name_inverse', 'πέθανε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2493, 'P100', 'ru', 'name_inverse', 'умер в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2494, 'P100', 'pt', 'name_inverse', 'morreu em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2495, 'P100', 'cn', 'name_inverse', '死亡於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2496, 'P100', 'en', 'comment', 'This property property links an E69 Death event to the E21 Person that died.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2497, 'P101', 'en', 'name', 'had as general use', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2498, 'P101', 'fr', 'name', 'avait comme utilisation générale', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2499, 'P101', 'el', 'name', 'είχε ως γενική χρήση', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2500, 'P101', 'de', 'name', 'hatte die allgemeine Verwendung', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2501, 'P101', 'ru', 'name', 'имел основное применение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2502, 'P101', 'pt', 'name', 'tem como uso geral', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2503, 'P101', 'cn', 'name', '被惯用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2504, 'P101', 'de', 'name_inverse', 'war die Verwendung von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2505, 'P101', 'en', 'name_inverse', 'was use of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2506, 'P101', 'fr', 'name_inverse', 'était l’utilisation de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2507, 'P101', 'ru', 'name_inverse', 'был применением для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2508, 'P101', 'el', 'name_inverse', 'ήταν χρήση του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2509, 'P101', 'pt', 'name_inverse', 'foi uso de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2510, 'P101', 'cn', 'name_inverse', '可使用', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2511, 'P101', 'en', 'comment', 'This property links an instance of E70 Thing to an E55 Type of usage.
It allows the relationship between particular things, both physical and immaterial, and general methods and techniques of use to be documented. Thus it can be asserted that a baseball bat had a general use for sport and a specific use for threatening people during the Great Train Robbery.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2512, 'P102', 'en', 'name', 'has title', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2513, 'P102', 'ru', 'name', 'имеет заголовок', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2514, 'P102', 'de', 'name', 'trägt den Titel', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2515, 'P102', 'fr', 'name', 'a pour titre', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2516, 'P102', 'el', 'name', 'έχει τίτλο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2517, 'P102', 'pt', 'name', 'tem título', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2518, 'P102', 'cn', 'name', '有标题', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2519, 'P102', 'en', 'name_inverse', 'is title of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2520, 'P102', 'de', 'name_inverse', 'ist der Titel von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2521, 'P102', 'el', 'name_inverse', 'είναι τίτλος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2522, 'P102', 'fr', 'name_inverse', 'est le titre de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2523, 'P102', 'ru', 'name_inverse', 'является заголовком для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2524, 'P102', 'pt', 'name_inverse', 'é título de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2525, 'P102', 'cn', 'name_inverse', '被用为标题来称呼', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2526, 'P102', 'en', 'comment', 'This property describes the E35 Title applied to an instance of E71 Man-Made Thing. The E55 Type of Title is assigned in a sub property.
The P102.1 has type property of the P102 has title (is title of) property enables the relationship between the Title and the thing to be further clarified, for example, if the Title was a given Title, a supplied Title etc.
It allows any man-made material or immaterial thing to be given a Title. It is possible to imagine a Title being created without a specific object in mind.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2527, 'P103', 'fr', 'name', 'était destiné à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2528, 'P103', 'en', 'name', 'was intended for', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2529, 'P103', 'de', 'name', 'bestimmt für', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2530, 'P103', 'ru', 'name', 'был задуман для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2531, 'P103', 'el', 'name', 'προοριζόταν για', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2532, 'P103', 'pt', 'name', 'era destinado à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2533, 'P103', 'cn', 'name', '被制作来用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2534, 'P103', 'de', 'name_inverse', 'war Bestimmung von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2535, 'P103', 'en', 'name_inverse', 'was intention of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2536, 'P103', 'ru', 'name_inverse', 'был интенцией для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2537, 'P103', 'el', 'name_inverse', 'ήταν προορισμός του', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2538, 'P103', 'fr', 'name_inverse', 'était la raison d''être de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2539, 'P103', 'pt', 'name_inverse', 'era a destinação de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2540, 'P103', 'en', 'comment', 'This property links an instance of E71 Man-Made Thing to an E55 Type of usage. 
It creates a property between specific man-made things, both physical and immaterial, to Types of intended methods and techniques of use. Note: A link between specific man-made things and a specific use activity should be expressed using P19 was intended use of (was made for).', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2541, 'P104', 'fr', 'name', 'est sujet à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2542, 'P104', 'en', 'name', 'is subject to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2543, 'P104', 'ru', 'name', 'является объектом для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2544, 'P104', 'el', 'name', 'υπόκειται σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2545, 'P104', 'de', 'name', 'Gegenstand von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2546, 'P104', 'pt', 'name', 'está sujeito à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2547, 'P104', 'cn', 'name', '受制於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2548, 'P104', 'el', 'name_inverse', 'ισχύει για', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2549, 'P104', 'fr', 'name_inverse', 's’applique à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2550, 'P104', 'de', 'name_inverse', 'findet Anwendung auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2551, 'P104', 'ru', 'name_inverse', 'применяется к', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2552, 'P104', 'en', 'name_inverse', 'applies to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2553, 'P104', 'pt', 'name_inverse', 'se aplicam à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2554, 'P104', 'cn', 'name_inverse', '被应用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2555, 'P104', 'en', 'comment', 'This property links a particular E72 Legal Object to the instances of E30 Right to which it is subject.
The Right is held by an E39 Actor as described by P75 possesses (is possessed by).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2556, 'P105', 'ru', 'name', 'право принадлежит', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2557, 'P105', 'fr', 'name', 'droit détenu par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2558, 'P105', 'de', 'name', 'Rechte stehen zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2559, 'P105', 'el', 'name', 'δικαίωμα κατέχεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2560, 'P105', 'en', 'name', 'right held by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2561, 'P105', 'pt', 'name', 'são direitos de ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2562, 'P105', 'cn', 'name', '有权限持有者', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2563, 'P105', 'de', 'name_inverse', 'hat Rechte an', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2564, 'P105', 'ru', 'name_inverse', 'владеет правом на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2565, 'P105', 'en', 'name_inverse', 'has right on', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2566, 'P105', 'fr', 'name_inverse', 'détient un droit sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2567, 'P105', 'el', 'name_inverse', 'έχει δικαίωμα σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2568, 'P105', 'pt', 'name_inverse', 'possui direitos sobre', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2569, 'P105', 'cn', 'name_inverse', '持有权限来管制', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2570, 'P105', 'en', 'comment', 'This property identifies the E39 Actor who holds the instances of E30 Right to an E72 Legal Object.
	It is a superproperty of P52 has current owner (is current owner of) because ownership is a right that is held on the owned object.
P105 right held by (has right on) is a shortcut of the fully developed path from E72 Legal Object through P104 is subject to (applies to), E30 Right, P75 possesses (is possessed by) to E39 Actor.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2571, 'P106', 'de', 'name', ' ist zusammengesetzt aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2572, 'P106', 'ru', 'name', 'составлен из', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2573, 'P106', 'en', 'name', 'is composed of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2574, 'P106', 'fr', 'name', 'est composé de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2575, 'P106', 'el', 'name', 'αποτελείται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2576, 'P106', 'pt', 'name', 'é composto de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2577, 'P106', 'cn', 'name', '有组成元素', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2578, 'P106', 'ru', 'name_inverse', 'формирует часть', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2579, 'P106', 'el', 'name_inverse', 'αποτελεί μέρος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2580, 'P106', 'de', 'name_inverse', 'bildet Teil von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2581, 'P106', 'fr', 'name_inverse', 'fait partie de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2582, 'P106', 'en', 'name_inverse', 'forms part of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2583, 'P106', 'pt', 'name_inverse', 'faz parte de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2584, 'P106', 'cn', 'name_inverse', '组成了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2585, 'P106', 'en', 'comment', 'This property associates an instance of E90 Symbolic Object with a part of it that is by itself an instance of E90 Symbolic Object, such as fragments of texts or clippings from an image.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2586, 'P107', 'fr', 'name', 'a pour membre actuel ou ancien', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2587, 'P107', 'en', 'name', 'has current or former member', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2588, 'P107', 'el', 'name', 'έχει ή είχε μέλος', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2589, 'P107', 'ru', 'name', 'имеет действующего или бывшего члена', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2590, 'P107', 'de', 'name', 'hat derzeitiges oder früheres Mitglied', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2591, 'P107', 'pt', 'name', 'tem ou teve membro', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2592, 'P107', 'cn', 'name', '有现任或前任成员', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2593, 'P107', 'el', 'name_inverse', 'είναι ή ήταν μέλος του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2594, 'P107', 'en', 'name_inverse', 'is current or former member of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2595, 'P107', 'de', 'name_inverse', 'ist derzeitiges oder früheres Mitglied von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2596, 'P107', 'ru', 'name_inverse', 'является действующим или бывшим членом', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2597, 'P107', 'fr', 'name_inverse', 'est actuel ou ancien membre de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2598, 'P107', 'pt', 'name_inverse', 'é ou foi membro de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2599, 'P107', 'cn', 'name_inverse', '目前或曾经加入群组', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2600, 'P107', 'en', 'comment', 'This property relates an E39 Actor to the E74 Group of which that E39 Actor is a member.
Groups, Legal Bodies and Persons, may all be members of Groups. A Group necessarily consists of more than one member.
This property is a shortcut of the more fully developed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor
The property P107.1 kind of member can be used to specify the type of membership or the role the member has in the group. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2601, 'P108', 'el', 'name', 'παρήγαγε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2602, 'P108', 'fr', 'name', 'a produit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2603, 'P108', 'ru', 'name', 'произвел', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2604, 'P108', 'de', 'name', 'hat hergestellt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2605, 'P108', 'en', 'name', 'has produced', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2606, 'P108', 'pt', 'name', 'produziu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2607, 'P108', 'cn', 'name', '有产出物', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2608, 'P108', 'el', 'name_inverse', 'παρήχθη από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2609, 'P108', 'fr', 'name_inverse', 'a été produit par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2610, 'P108', 'de', 'name_inverse', 'wurde hergestellt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2611, 'P108', 'ru', 'name_inverse', 'был произведен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2612, 'P108', 'en', 'name_inverse', 'was produced by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2613, 'P108', 'pt', 'name_inverse', 'foi produzido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2614, 'P108', 'cn', 'name_inverse', '被制作於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2615, 'P108', 'en', 'comment', 'This property identifies the E24 Physical Man-Made Thing that came into existence as a result of an E12 Production.
The identity of an instance of E24 Physical Man-Made Thing is not defined by its matter, but by its existence as a subject of documentation. An E12 Production can result in the creation of multiple instances of E24 Physical Man-Made Thing.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2616, 'P109', 'fr', 'name', 'a pour conservateur actuel ou ancien', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2617, 'P109', 'de', 'name', 'hat derzeitigen oder früheren Kurator', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2618, 'P109', 'en', 'name', 'has current or former curator', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2619, 'P109', 'el', 'name', 'έχει ή είχε επιμελητή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2620, 'P114', 'pt', 'name', 'é temporalmente igual a', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2621, 'P109', 'ru', 'name', 'имеет действующего или бывшего хранителя', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2622, 'P109', 'pt', 'name', 'tem ou teve curador', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2623, 'P109', 'cn', 'name', '有现任或前任典藏管理员', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2624, 'P109', 'ru', 'name_inverse', 'является действующим или бывшим хранителем', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2625, 'P109', 'el', 'name_inverse', 'είναι ή ήταν επιμελητής του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2626, 'P109', 'fr', 'name_inverse', 'est ou a été le conservateur de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2627, 'P109', 'de', 'name_inverse', 'ist derzeitiger oder früherer Kurator von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2628, 'P109', 'en', 'name_inverse', 'is current or former curator of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2629, 'P109', 'pt', 'name_inverse', 'é ou foi curador de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2630, 'P109', 'cn', 'name_inverse', '目前或曾经典藏管理', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2786, 'P120', 'pt', 'name_inverse', 'ocorre depois', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2631, 'P109', 'en', 'comment', 'This property identifies the E39 Actor or Actors who assume or have assumed overall curatorial responsibility for an E78 Collection.
This property is effectively a short-cut. It does not allow a history of curation to be recorded. This would require use of an Event assigning responsibility for a Collection to a curator.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2632, 'P110', 'ru', 'name', 'увеличил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2633, 'P110', 'fr', 'name', 'a augmenté', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2634, 'P110', 'de', 'name', 'erweiterte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2635, 'P110', 'el', 'name', 'επαύξησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2636, 'P110', 'en', 'name', 'augmented', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2637, 'P110', 'pt', 'name', 'aumentou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2638, 'P110', 'cn', 'name', '扩增了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2639, 'P110', 'fr', 'name_inverse', 'a été augmenté par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2640, 'P110', 'en', 'name_inverse', 'was augmented by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2641, 'P110', 'ru', 'name_inverse', 'был увеличен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2642, 'P110', 'el', 'name_inverse', 'επαυξήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2643, 'P110', 'de', 'name_inverse', 'wurde erweitert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2644, 'P110', 'pt', 'name_inverse', 'foi aumentada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2645, 'P110', 'cn', 'name_inverse', '被扩增於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2646, 'P110', 'en', 'comment', 'This property identifies the E24 Physical Man-Made Thing that is added to (augmented) in an E79 Part Addition.
Although a Part Addition event normally concerns only one item of Physical Man-Made Thing, it is possible to imagine circumstances under which more than one item might be added to (augmented). For example, the artist Jackson Pollock trailing paint onto multiple canvasses.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2647, 'P111', 'de', 'name', 'fügte hinzu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2648, 'P111', 'el', 'name', 'προσέθεσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2649, 'P111', 'fr', 'name', 'a ajouté', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2650, 'P111', 'en', 'name', 'added', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2651, 'P111', 'ru', 'name', 'добавил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2652, 'P111', 'pt', 'name', 'adicionou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2653, 'P111', 'cn', 'name', '附加上部件', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2654, 'P111', 'fr', 'name_inverse', 'a été ajouté par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2655, 'P111', 'de', 'name_inverse', 'wurde hinzugefügt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2656, 'P111', 'en', 'name_inverse', 'was added by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2657, 'P111', 'el', 'name_inverse', 'προστέθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2658, 'P111', 'ru', 'name_inverse', 'был добавлен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2659, 'P111', 'pt', 'name_inverse', 'foi adicionado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2660, 'P111', 'cn', 'name_inverse', '被附加於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2661, 'P111', 'en', 'comment', 'This property identifies the E18 Physical Thing that is added during an E79 Part Addition activity
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2662, 'P112', 'ru', 'name', 'уменьшил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2663, 'P112', 'en', 'name', 'diminished', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2664, 'P112', 'de', 'name', 'verminderte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2665, 'P112', 'fr', 'name', 'a diminué', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2666, 'P112', 'el', 'name', 'εξάλειψε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2667, 'P112', 'pt', 'name', 'diminuiu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2668, 'P112', 'cn', 'name', '缩减了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2669, 'P112', 'en', 'name_inverse', 'was diminished by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2670, 'P112', 'el', 'name_inverse', 'εξαλείφθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2671, 'P112', 'fr', 'name_inverse', 'a été diminué par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2672, 'P112', 'ru', 'name_inverse', 'был уменьшен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2673, 'P112', 'de', 'name_inverse', 'wurde vermindert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2674, 'P112', 'pt', 'name_inverse', 'foi diminuído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2675, 'P112', 'cn', 'name_inverse', '被缩减於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2676, 'P112', 'en', 'comment', 'This property identifies the E24 Physical Man-Made Thing that was diminished by E80 Part Removal.
Although a Part removal activity normally concerns only one item of Physical Man-Made Thing, it is possible to imagine circumstances under which more than one item might be diminished by a single Part Removal activity. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2677, 'P113', 'ru', 'name', 'удален', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2678, 'P113', 'de', 'name', 'entfernte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2679, 'P113', 'en', 'name', 'removed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2680, 'P113', 'el', 'name', 'αφαίρεσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2681, 'P113', 'fr', 'name', 'a enlevé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2682, 'P113', 'pt', 'name', 'removeu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2683, 'P113', 'cn', 'name', '移除了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2684, 'P113', 'el', 'name_inverse', 'αφαιρέθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2685, 'P113', 'de', 'name_inverse', 'wurde entfernt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2686, 'P113', 'en', 'name_inverse', 'was removed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2687, 'P113', 'fr', 'name_inverse', 'a été enlevée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2688, 'P113', 'ru', 'name_inverse', 'был удален посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2689, 'P113', 'pt', 'name_inverse', 'foi removido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2690, 'P113', 'cn', 'name_inverse', '被移除於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2691, 'P113', 'en', 'comment', 'This property identifies the E18 Physical Thing that is removed during an E80 Part Removal activity.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2692, 'P114', 'fr', 'name', 'est temporellement égale à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2693, 'P114', 'de', 'name', 'zeitgleich zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2694, 'P114', 'el', 'name', 'συμπίπτει χρονικά με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2695, 'P114', 'ru', 'name', 'равен по времени', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2696, 'P114', 'en', 'name', 'is equal in time to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2697, 'P114', 'cn', 'name', '时段相同於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2698, 'P114', 'en', 'comment', 'This symmetric property allows the instances of E2 Temporal Entity with the same E52 Time-Span to be equated. 
This property is only necessary if the time span is unknown (otherwise the equivalence can be calculated).
This property is the same as the "equal" relationship of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2699, 'P115', 'en', 'name', 'finishes', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2700, 'P115', 'ru', 'name', 'заканчивает', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2701, 'P115', 'de', 'name', 'beendet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2702, 'P115', 'fr', 'name', 'termine', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2703, 'P115', 'el', 'name', 'περατώνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2704, 'P115', 'pt', 'name', 'finaliza', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2705, 'P115', 'cn', 'name', '结束了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2706, 'P115', 'fr', 'name_inverse', 'est terminée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2707, 'P115', 'ru', 'name_inverse', 'заканчивается', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2708, 'P115', 'el', 'name_inverse', 'περατώνεται με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2709, 'P115', 'de', 'name_inverse', 'wurde beendet mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2710, 'P115', 'en', 'name_inverse', 'is finished by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2711, 'P115', 'pt', 'name_inverse', 'é finalizada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2712, 'P115', 'cn', 'name_inverse', '被结束于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2787, 'P120', 'cn', 'name_inverse', '发生时段后於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3095, 'P145', 'en', 'comment', 'This property identifies the instance of E39 Actor that leaves an instance of E74 Group through an instance of E86 Leaving.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2713, 'P115', 'en', 'comment', 'This property allows the ending point for a E2 Temporal Entity to be situated by reference to the ending point of another temporal entity of longer duration.  
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "finishes / finished-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2714, 'P116', 'fr', 'name', 'commence', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2715, 'P116', 'en', 'name', 'starts', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2716, 'P116', 'ru', 'name', 'начинает', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2717, 'P116', 'de', 'name', 'beginnt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2718, 'P116', 'el', 'name', 'αρχίζει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2719, 'P116', 'pt', 'name', 'inicia', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2720, 'P116', 'cn', 'name', '开始了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2721, 'P116', 'fr', 'name_inverse', 'est commencée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2722, 'P116', 'de', 'name_inverse', 'wurde begonnen mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2723, 'P116', 'el', 'name_inverse', 'αρχίζει με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2724, 'P116', 'ru', 'name_inverse', 'начинается', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2725, 'P116', 'en', 'name_inverse', 'is started by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2726, 'P116', 'pt', 'name_inverse', 'é iniciada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2727, 'P116', 'cn', 'name_inverse', '被开始于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2728, 'P116', 'en', 'comment', 'This property allows the starting point for a E2 Temporal Entity to be situated by reference to the starting point of another temporal entity of longer duration.  
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "starts / started-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2729, 'P117', 'de', 'name', 'fällt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2730, 'P117', 'el', 'name', 'εμφανίζεται κατά τη διάρκεια', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2731, 'P117', 'ru', 'name', 'появляется во течение', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2732, 'P117', 'en', 'name', 'occurs during', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2733, 'P117', 'fr', 'name', 'a lieu pendant', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2734, 'P117', 'pt', 'name', 'ocorre durante', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2735, 'P117', 'cn', 'name', '时段被涵盖於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2736, 'P117', 'el', 'name_inverse', 'περιλαμβάνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2737, 'P117', 'ru', 'name_inverse', 'включает', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2738, 'P117', 'fr', 'name_inverse', 'comporte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2739, 'P117', 'en', 'name_inverse', 'includes', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2740, 'P117', 'de', 'name_inverse', 'beinhaltet', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2741, 'P117', 'pt', 'name_inverse', 'inclui', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2742, 'P117', 'cn', 'name_inverse', '时段涵盖了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2743, 'P117', 'en', 'comment', 'This property allows the entire E52 Time-Span of an E2 Temporal Entity to be situated within the Time-Span of another temporal entity that starts before and ends after the included temporal entity.   
This property is only necessary if the time span is unknown (otherwise the relationship can be calculated). This property is the same as the "during / includes" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2744, 'P118', 'en', 'name', 'overlaps in time with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2745, 'P118', 'ru', 'name', 'перекрывает во времени', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2746, 'P118', 'el', 'name', 'προηγείται μερικώς επικαλύπτοντας', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2747, 'P118', 'de', 'name', 'überlappt zeitlich mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2748, 'P118', 'fr', 'name', 'est partiellement recouverte dans le temps par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2749, 'P118', 'pt', 'name', 'sobrepõe temporalmente', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2750, 'P118', 'cn', 'name', '时段重叠了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2751, 'P118', 'de', 'name_inverse', 'wird zeitlich überlappt von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2752, 'P118', 'ru', 'name_inverse', 'перекрывается во времени', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2753, 'P118', 'fr', 'name_inverse', 'recouvre partiellement dans le temps', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2754, 'P118', 'en', 'name_inverse', 'is overlapped in time by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2755, 'P118', 'el', 'name_inverse', 'έπεται μερικώς επικαλυπτόμενο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2756, 'P118', 'pt', 'name_inverse', 'é sobreposto temporalmente por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2757, 'P118', 'cn', 'name_inverse', '时段被重叠于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2758, 'P118', 'en', 'comment', 'This property identifies an overlap between the instances of E52 Time-Span of two instances of E2 Temporal Entity. 
It implies a temporal order between the two entities: if A overlaps in time B, then A must start before B, and B must end after A. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated).
This property is the same as the "overlaps / overlapped-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2759, 'P119', 'en', 'name', 'meets in time with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2760, 'P119', 'el', 'name', 'προηγείται', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2761, 'P119', 'de', 'name', 'trifft zeitlich auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2762, 'P119', 'ru', 'name', 'следует во времени за', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2763, 'P119', 'fr', 'name', 'est temporellement contiguë avec', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2764, 'P119', 'pt', 'name', 'é temporalmente contíguo com', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2765, 'P119', 'cn', 'name', '紧接续了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2766, 'P119', 'fr', 'name_inverse', 'est immédiatement précédé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2767, 'P119', 'el', 'name_inverse', 'έπεται', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2768, 'P119', 'en', 'name_inverse', 'is met in time by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2769, 'P119', 'de', 'name_inverse', 'wird zeitlich getroffen von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2770, 'P119', 'ru', 'name_inverse', 'предшествует во времени', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2771, 'P119', 'pt', 'name_inverse', 'é imediatamente precedido por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2772, 'P119', 'cn', 'name_inverse', '紧接续於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2773, 'P119', 'en', 'comment', 'This property indicates that one E2 Temporal Entity immediately follows another. 
It implies a particular order between the two entities: if A meets in time with B, then A must precede B. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated). 
This property is the same as the "meets / met-by" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2774, 'P120', 'ru', 'name', 'появляется до', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2775, 'P120', 'fr', 'name', 'a lieu avant', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2776, 'P120', 'el', 'name', 'εμφανίζεται πριν', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2777, 'P120', 'en', 'name', 'occurs before', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2778, 'P120', 'de', 'name', 'kommt vor', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2779, 'P120', 'pt', 'name', 'ocorre antes', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2780, 'P120', 'cn', 'name', '发生时段先於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2781, 'P120', 'fr', 'name_inverse', 'a lieu après', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2782, 'P120', 'el', 'name_inverse', 'εμφανίζεται μετά', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2783, 'P120', 'ru', 'name_inverse', 'появляется после', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2784, 'P120', 'de', 'name_inverse', 'kommt nach', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2785, 'P120', 'en', 'name_inverse', 'occurs after', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2788, 'P120', 'en', 'comment', 'This property identifies the relative chronological sequence of two temporal entities. 
It implies that a temporal gap exists between the end of A and the start of B. This property is only necessary if the relevant time spans are unknown (otherwise the relationship can be calculated).
This property is the same as the "before / after" relationships of Allen’s temporal logic (Allen, 1983, pp. 832-843).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2789, 'P121', 'el', 'name', 'επικαλύπτεται με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2790, 'P121', 'de', 'name', 'überlappt mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2791, 'P121', 'fr', 'name', 'chevauche', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2792, 'P121', 'ru', 'name', 'пересекается с', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2793, 'P121', 'en', 'name', 'overlaps with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2794, 'P121', 'pt', 'name', 'sobrepõe com', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2795, 'P121', 'cn', 'name', '空间重叠于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2796, 'P121', 'en', 'comment', 'This symmetric property allows the instances of E53 Place with overlapping geometric extents to be associated with each other. 
It does not specify anything about the shared area. This property is purely spatial, in contrast to Allen operators, which are purely temporal.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2797, 'P122', 'ru', 'name', 'граничит с', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2798, 'P122', 'en', 'name', 'borders with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2799, 'P122', 'fr', 'name', 'jouxte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2800, 'P122', 'de', 'name', 'grenzt an', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2801, 'P122', 'el', 'name', 'συνορεύει με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2802, 'P122', 'pt', 'name', 'fronteira com', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2803, 'P122', 'cn', 'name', '接壤于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2804, 'P122', 'en', 'comment', 'This symmetric property allows the instances of E53 Place which share common borders to be related as such. 
This property is purely spatial, in contrast to Allen operators, which are purely temporal.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2805, 'P123', 'fr', 'name', 'a eu pour résultat', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2806, 'P123', 'de', 'name', 'ergab', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2807, 'P123', 'el', 'name', 'είχε ως αποτέλεσμα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2808, 'P123', 'ru', 'name', 'повлек появление', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2809, 'P123', 'en', 'name', 'resulted in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2810, 'P123', 'pt', 'name', 'resultou em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2811, 'P123', 'cn', 'name', '转变出', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2812, 'P123', 'fr', 'name_inverse', 'est le résultat de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2813, 'P123', 'el', 'name_inverse', 'προέκυψε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2814, 'P123', 'ru', 'name_inverse', 'был результатом', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2815, 'P123', 'de', 'name_inverse', 'ergab sich aus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2816, 'P123', 'en', 'name_inverse', 'resulted from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2817, 'P123', 'pt', 'name_inverse', 'resultado de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2818, 'P123', 'cn', 'name_inverse', '肇因於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2819, 'P123', 'en', 'comment', 'This property identifies the E77 Persistent Item or items that are the result of an E81 Transformation. 
New items replace the transformed item or items, which cease to exist as units of documentation. The physical continuity between the old and the new is expressed by the link to the common Transformation.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2820, 'P124', 'en', 'name', 'transformed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2821, 'P124', 'de', 'name', 'wandelte um', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2822, 'P124', 'el', 'name', 'μετέτρεψε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2823, 'P124', 'ru', 'name', 'трансформировал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2824, 'P124', 'fr', 'name', 'a transformé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2825, 'P124', 'pt', 'name', 'transformou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2826, 'P124', 'cn', 'name', '转变了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2827, 'P124', 'fr', 'name_inverse', 'a été transformé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2828, 'P124', 'ru', 'name_inverse', 'был трансформирован посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2829, 'P124', 'el', 'name_inverse', 'μετατράπηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2830, 'P124', 'en', 'name_inverse', 'was transformed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2831, 'P124', 'de', 'name_inverse', 'wurde umgewandelt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2832, 'P124', 'pt', 'name_inverse', 'foi transformado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2833, 'P124', 'cn', 'name_inverse', '被转变於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2834, 'P129', 'en', 'comment', 'This property documents that an E89 Propositional Object has as subject an instance of E1 CRM Entity. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2835, 'P130', 'el', 'name', 'παρουσιάζει χαρακτηριστικά του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2836, 'P124', 'en', 'comment', 'This property identifies the E77 Persistent Item or items that cease to exist due to a E81 Transformation. 
It is replaced by the result of the Transformation, which becomes a new unit of documentation. The continuity between both items, the new and the old, is expressed by the link to the common Transformation.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2837, 'P125', 'en', 'name', 'used object of type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2838, 'P125', 'fr', 'name', 'a employé un objet du type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2839, 'P125', 'ru', 'name', 'использовал объект типа', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2840, 'P125', 'de', 'name', 'benutzte Objekt des Typus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2841, 'P125', 'el', 'name', 'χρησιμοποίησε αντικείμενο τύπου', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2842, 'P125', 'pt', 'name', 'usou objeto do tipo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2843, 'P125', 'cn', 'name', '有使用物件类型', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2844, 'P125', 'ru', 'name_inverse', 'был типом объекта использованного в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2845, 'P125', 'en', 'name_inverse', 'was type of object used in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2846, 'P125', 'de', 'name_inverse', 'Objekt des Typus ... wurde benutzt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2847, 'P125', 'fr', 'name_inverse', 'était le type d’objet employé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2848, 'P125', 'el', 'name_inverse', 'ήταν o τύπος αντικείμενου που χρησιμοποιήθηκε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2849, 'P125', 'pt', 'name_inverse', 'foi tipo do objeto usado em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2850, 'P125', 'cn', 'name_inverse', '被使用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2851, 'P125', 'en', 'comment', 'This property defines the kind of objects used in an E7 Activity, when the specific instance is either unknown or not of interest, such as use of "a hammer".
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2852, 'P126', 'fr', 'name', 'a employé', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2853, 'P126', 'de', 'name', 'verwendete', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2854, 'P126', 'en', 'name', 'employed', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2855, 'P126', 'ru', 'name', 'использовал', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2856, 'P126', 'el', 'name', 'χρησιμοποίησε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2857, 'P126', 'pt', 'name', 'empregou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2858, 'P126', 'cn', 'name', '采用了材料', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2859, 'P126', 'en', 'name_inverse', 'was employed in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2860, 'P126', 'de', 'name_inverse', 'wurde verwendet bei', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2861, 'P126', 'ru', 'name_inverse', 'использовался в', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2862, 'P126', 'el', 'name_inverse', 'χρησιμοποιήθηκε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2863, 'P126', 'fr', 'name_inverse', 'a été employé dans', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2864, 'P126', 'pt', 'name_inverse', 'foi empregado em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2865, 'P126', 'cn', 'name_inverse', '被使用於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3026, 'P138', 'de', 'name_inverse', 'wird dargestellt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2866, 'P126', 'en', 'comment', 'This property identifies E57 Material employed in an E11 Modification.
The E57 Material used during the E11 Modification does not necessarily become incorporated into the E24 Physical Man-Made Thing that forms the subject of the E11 Modification.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2867, 'P127', 'el', 'name', 'έχει ευρύτερο όρο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2868, 'P127', 'fr', 'name', 'a pour terme générique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2869, 'P127', 'de', 'name', 'hat den Oberbegriff', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2870, 'P127', 'en', 'name', 'has broader term', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2871, 'P127', 'ru', 'name', 'имеет вышестоящий термин', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2872, 'P127', 'pt', 'name', 'tem termo genérico', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2873, 'P127', 'cn', 'name', '有广义术语', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2874, 'P127', 'fr', 'name_inverse', 'a pour terme spécifique', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2875, 'P127', 'de', 'name_inverse', 'hat den Unterbegriff', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2876, 'P127', 'en', 'name_inverse', 'has narrower term', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2877, 'P127', 'el', 'name_inverse', 'έχει στενότερο όρο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2878, 'P127', 'pt', 'name_inverse', 'tem termo específico', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2879, 'P127', 'cn', 'name_inverse', '有狭义术语', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2880, 'P127', 'en', 'comment', 'This property identifies a super-Type to which an E55 Type is related. 
		It allows Types to be organised into hierarchies. This is the sense of "broader term generic  		(BTG)" as defined in ISO 2788
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2881, 'P128', 'en', 'name', 'carries', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2882, 'P128', 'fr', 'name', 'est le support de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2883, 'P128', 'ru', 'name', 'несет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2884, 'P128', 'el', 'name', 'φέρει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2885, 'P128', 'de', 'name', 'trägt', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2886, 'P128', 'pt', 'name', 'é o suporte de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2887, 'P128', 'cn', 'name', '承载信息', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2888, 'P128', 'el', 'name_inverse', 'φέρεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2889, 'P128', 'en', 'name_inverse', 'is carried by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2890, 'P128', 'ru', 'name_inverse', 'переносится посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2891, 'P128', 'fr', 'name_inverse', 'a pour support', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2892, 'P128', 'de', 'name_inverse', 'wird getragen von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2893, 'P128', 'pt', 'name_inverse', 'é suportado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2894, 'P128', 'cn', 'name_inverse', '被承载于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2895, 'P128', 'en', 'comment', 'This property identifies an E90 Symbolic Object carried by an instance of E24 Physical Man-Made Thing.
In general this would be an E84 Information Carrier P65 shows visual item (is shown by) is a specialisation of P128 carries (is carried by) which should be used for carrying visual items.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2896, 'P129', 'fr', 'name', 'est au sujet de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2897, 'P129', 'en', 'name', 'is about', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2898, 'P129', 'ru', 'name', 'касается', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2899, 'P129', 'el', 'name', 'έχει ως θέμα', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2900, 'P129', 'de', 'name', 'handelt über', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2901, 'P129', 'pt', 'name', 'é sobre', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2902, 'P129', 'cn', 'name', '陈述关於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2903, 'P129', 'fr', 'name_inverse', 'est le sujet de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2904, 'P129', 'de', 'name_inverse', 'wird behandelt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2905, 'P129', 'ru', 'name_inverse', 'является предметом для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2906, 'P129', 'el', 'name_inverse', 'είναι θέμα  του/της', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2907, 'P129', 'en', 'name_inverse', 'is subject of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2908, 'P129', 'pt', 'name_inverse', 'é assunto de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2909, 'P129', 'cn', 'name_inverse', '被陈述於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2910, 'P130', 'en', 'name', 'shows features of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2911, 'P130', 'ru', 'name', 'демонстрирует признаки', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2912, 'P130', 'fr', 'name', 'présente des caractéristiques de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2913, 'P130', 'de', 'name', 'zeigt Merkmale von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2914, 'P130', 'pt', 'name', 'apresenta características de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2915, 'P130', 'cn', 'name', '外观特征原出现於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2916, 'P130', 'el', 'name_inverse', 'χαρακτηριστικά του βρίσκονται επίσης σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2917, 'P130', 'fr', 'name_inverse', 'a des caractéristiques se trouvant aussi sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2918, 'P130', 'de', 'name_inverse', 'Merkmale auch auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2919, 'P130', 'ru', 'name_inverse', 'признаки также найдены на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2920, 'P130', 'en', 'name_inverse', 'features are also found on', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2921, 'P130', 'pt', 'name_inverse', 'características são também encontradas em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2922, 'P130', 'cn', 'name_inverse', '外观特征被复制於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2923, 'P130', 'en', 'comment', 'This property generalises the notions of  "copy of" and "similar to" into a dynamic, asymmetric relationship, where the domain expresses the derivative, if such a direction can be established.
Otherwise, the relationship is symmetric. It is a short-cut of P15 was influenced by (influenced) in a creation or production, if such a reason for the similarity can be verified. Moreover it expresses similarity in cases that can be stated between two objects only, without historical knowledge about its reasons.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2924, 'P131', 'el', 'name', 'αναγνωρίζεται ως', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2925, 'P131', 'de', 'name', 'wird identifziert durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2926, 'P131', 'en', 'name', 'is identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2927, 'P131', 'fr', 'name', 'est identifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2928, 'P131', 'ru', 'name', 'идентифицируется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2929, 'P131', 'pt', 'name', 'é identificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2930, 'P131', 'cn', 'name', '有称号', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2931, 'P131', 'fr', 'name_inverse', 'identifie', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2932, 'P131', 'en', 'name_inverse', 'identifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2933, 'P131', 'el', 'name_inverse', 'είναι αναγνωριστικό', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2934, 'P131', 'ru', 'name_inverse', 'идентифицирует', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2935, 'P131', 'de', 'name_inverse', 'identifiziert', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2936, 'P131', 'pt', 'name_inverse', 'identifica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2937, 'P131', 'cn', 'name_inverse', '被用来识别', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2938, 'P131', 'en', 'comment', 'This property identifies a name used specifically to identify an E39 Actor. 
This property is a specialisation of P1 is identified by (identifies) is identified by.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2939, 'P132', 'el', 'name', 'επικαλύπτεται με', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2940, 'P132', 'de', 'name', 'überlappt mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2941, 'P132', 'fr', 'name', 'chevauche', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2942, 'P132', 'ru', 'name', 'пересекается с', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2943, 'P132', 'en', 'name', 'overlaps with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2944, 'P132', 'pt', 'name', 'sobrepõe', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2945, 'P132', 'cn', 'name', '时空重叠于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3027, 'P138', 'pt', 'name_inverse', 'tem representação', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3028, 'P138', 'cn', 'name_inverse', '有图像描绘', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2946, 'P132', 'en', 'comment', 'This symmetric property allows instances of E4 Period that overlap both temporally and spatially to be related, i,e. they share some spatio-temporal extent.
This property does not imply any ordering or sequence between the two periods, either spatial or temporal.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2947, 'P133', 'de', 'name', 'getrennt von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2948, 'P133', 'en', 'name', 'is separated from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2949, 'P133', 'el', 'name', 'διαχωρίζεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2950, 'P133', 'fr', 'name', 'est séparée de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2951, 'P133', 'ru', 'name', 'отделен от', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2952, 'P133', 'pt', 'name', 'é separado de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2953, 'P133', 'cn', 'name', '时空不重叠于', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2954, 'P133', 'en', 'comment', 'This symmetric property allows instances of E4 Period that do not overlap both temporally and spatially, to be related i,e. they do not share any spatio-temporal extent.
This property does not imply any ordering or sequence between the two periods either spatial or temporal.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2955, 'P134', 'de', 'name', 'setzte sich fort in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2956, 'P134', 'el', 'name', 'συνέχισε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2957, 'P134', 'ru', 'name', 'продолжил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2958, 'P134', 'fr', 'name', 'est la suite de', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2959, 'P134', 'en', 'name', 'continued', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2960, 'P134', 'pt', 'name', 'continuou', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2961, 'P134', 'cn', 'name', '延续了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2962, 'P134', 'de', 'name_inverse', 'wurde fortgesetzt durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2963, 'P134', 'ru', 'name_inverse', 'был продолжен', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2964, 'P134', 'fr', 'name_inverse', 'a été continuée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2965, 'P134', 'en', 'name_inverse', 'was continued by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2966, 'P134', 'el', 'name_inverse', 'συνεχίστηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2967, 'P134', 'pt', 'name_inverse', 'foi continuada por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2968, 'P134', 'cn', 'name_inverse', '有延续活动', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2969, 'P134', 'en', 'comment', 'This property allows two activities to be related where the domain is considered as an intentional continuation of the range.
Used multiple times, this allows a chain of related activities to be created which follow each other in sequence.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2970, 'P135', 'en', 'name', 'created type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2971, 'P135', 'de', 'name', 'erschuf Typus', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2972, 'P135', 'el', 'name', 'δημιούργησε τύπο', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2973, 'P135', 'fr', 'name', 'a créé le type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2974, 'P135', 'ru', 'name', 'создал тип', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2975, 'P135', 'pt', 'name', 'criou tipo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2976, 'P135', 'cn', 'name', '创造了类型', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2977, 'P135', 'en', 'name_inverse', 'was created by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2978, 'P135', 'de', 'name_inverse', 'wurde geschaffen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2979, 'P135', 'fr', 'name_inverse', 'a été créé par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2980, 'P135', 'el', 'name_inverse', 'δημιουργήθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2981, 'P135', 'ru', 'name_inverse', 'был создан посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2982, 'P135', 'pt', 'name_inverse', 'foi criado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2983, 'P135', 'cn', 'name_inverse', '被创造於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2984, 'P135', 'en', 'comment', 'This property identifies the E55 Type, which is created in an E83Type Creation activity.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2985, 'P136', 'fr', 'name', 's’est fondée sur', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2986, 'P136', 'ru', 'name', 'был основан на', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2987, 'P136', 'de', 'name', 'stützte sich auf', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2988, 'P136', 'el', 'name', 'βασίστηκε σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2989, 'P136', 'en', 'name', 'was based on', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2990, 'P136', 'pt', 'name', 'foi baseado em', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2991, 'P136', 'cn', 'name', '根据了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2992, 'P136', 'en', 'name_inverse', 'supported type creation', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2993, 'P136', 'el', 'name_inverse', 'υποστήριξε τη δημιουργία τύπου', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2994, 'P136', 'fr', 'name_inverse', 'a justifié la création de type', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2995, 'P136', 'de', 'name_inverse', 'belegte', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2996, 'P136', 'ru', 'name_inverse', 'поддержал создание типа', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2997, 'P136', 'pt', 'name_inverse', 'suportou a criação de tipo', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2998, 'P136', 'cn', 'name_inverse', '提供證據给类型创造', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (2999, 'P136', 'en', 'comment', 'This property identifies one or more items that were used as evidence to declare a new E55 Type.
The examination of these items is often the only objective way to understand the precise characteristics of a new Type. Such items should be deposited in a museum or similar institution for that reason. The taxonomic role renders the specific relationship of each item to the Type, such as "holotype" or "original element".
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3000, 'P137', 'en', 'name', 'exemplifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3001, 'P137', 'fr', 'name', 'exemplifie', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3002, 'P137', 'el', 'name', 'δειγματίζει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3003, 'P137', 'ru', 'name', 'поясняет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3004, 'P137', 'de', 'name', 'erläutert', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3005, 'P137', 'pt', 'name', 'é exemplificado por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3006, 'P137', 'cn', 'name', '例示了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3007, 'P137', 'ru', 'name_inverse', 'поясняется посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3008, 'P137', 'de', 'name_inverse', 'erläutert durch Beispiel', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3009, 'P137', 'en', 'name_inverse', 'is exemplified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3010, 'P137', 'el', 'name_inverse', 'δειγματίζεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3011, 'P137', 'fr', 'name_inverse', 'est exemplifié par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3012, 'P137', 'pt', 'name_inverse', 'exemplifica', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3013, 'P137', 'cn', 'name_inverse', '有例示', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3014, 'P137', 'en', 'comment', 'This property allows an item to be declared as a particular example of an E55 Type or taxon
	The P137.1 in the taxonomic role property of P137 exemplifies (is exemplified by) allows differentiation of taxonomic roles. The taxonomic role renders the specific relationship of this example to the Type, such as "prototypical", "archetypical", "lectotype", etc. The taxonomic role "lectotype" is not associated with the Type Creation (E83) itself, but selected in a later phase.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3015, 'P138', 'el', 'name', 'παριστάνει', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3016, 'P138', 'en', 'name', 'represents', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3017, 'P138', 'ru', 'name', 'представляет', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3018, 'P138', 'de', 'name', 'stellt dar', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3019, 'P138', 'fr', 'name', 'représente', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3020, 'P138', 'pt', 'name', 'representa', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3021, 'P138', 'cn', 'name', '描绘了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3022, 'P138', 'en', 'name_inverse', 'has representation', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3023, 'P138', 'ru', 'name_inverse', 'имеет представление', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3024, 'P138', 'fr', 'name_inverse', 'est représentée par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3025, 'P138', 'el', 'name_inverse', 'παριστάνεται από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3029, 'P138', 'en', 'comment', 'This property establishes the relationship between an E36 Visual Item and the entity that it visually represents.
Any entity may be represented visually. This property is part of the fully developed path from E24 Physical Man-Made Thing through P65 shows visual item (is shown by), E36 Visual Item, P138 represents (has representation) to E1 CRM Entity, which is shortcut by P62depicts (is depicted by). P138.1 mode of representation allows the nature of the representation to be refined.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3030, 'P139', 'fr', 'name', 'a pour autre forme', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3031, 'P139', 'ru', 'name', 'имеет альтернативную форму', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3032, 'P139', 'en', 'name', 'has alternative form', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3033, 'P139', 'de', 'name', 'hat alternative Form', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3034, 'P139', 'el', 'name', 'έχει εναλλακτική μορφή', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3035, 'P139', 'pt', 'name', 'tem forma alternativa', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3036, 'P139', 'cn', 'name', '有替代称号', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3037, 'P139', 'en', 'comment', 'This property establishes a relationship of equivalence between two instances of E41 Appellation independent from any item identified by them. It is a dynamic asymmetric relationship, where the range expresses the derivative, if such a direction can be established. Otherwise, the relationship is symmetric. The relationship is not transitive.
The equivalence applies to all cases of use of an instance of E41 Appellation. Multiple names assigned to an object, which are not equivalent for all things identified with a specific instance of E41 Appellation, should be modelled as repeated values of P1 is identified by (identifies). 
P139.1 has type allows the type of derivation, such as “transliteration from Latin 1 to ASCII” be refined..
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3038, 'P140', 'de', 'name', 'wies Merkmal zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3039, 'P140', 'el', 'name', 'απέδωσε ιδιότητα σε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3040, 'P140', 'en', 'name', 'assigned attribute to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3041, 'P140', 'fr', 'name', 'a affecté un attribut à', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3042, 'P140', 'ru', 'name', 'присвоил атрибут для', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3043, 'P140', 'pt', 'name', 'atribuiu atributo para', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3044, 'P140', 'cn', 'name', '指定属性给', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3045, 'P140', 'en', 'name_inverse', 'was attributed by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3046, 'P140', 'fr', 'name_inverse', 'a reçu un attribut par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3047, 'P140', 'ru', 'name_inverse', 'получил атрибут посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3048, 'P140', 'de', 'name_inverse', 'bekam Merkmal zugewiesen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3049, 'P140', 'el', 'name_inverse', 'χαρακτηρίστηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3050, 'P140', 'pt', 'name_inverse', 'foi atribuído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3051, 'P140', 'cn', 'name_inverse', '被指定属性於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3052, 'P140', 'en', 'comment', 'This property indicates the item to which an attribute or relation is assigned. ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3053, 'P141', 'en', 'name', 'assigned', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3054, 'P141', 'ru', 'name', 'присвоил', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3055, 'P141', 'de', 'name', 'wies zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3056, 'P141', 'el', 'name', 'απέδωσε', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3057, 'P141', 'fr', 'name', 'a attribué', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3058, 'P141', 'pt', 'name', 'atribuiu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3059, 'P141', 'cn', 'name', '指定了属性值', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3060, 'P141', 'ru', 'name_inverse', 'был присвоен посредством', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3061, 'P141', 'de', 'name_inverse', 'wurde zugewiesen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3062, 'P141', 'fr', 'name_inverse', 'a été attribué par', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3063, 'P141', 'en', 'name_inverse', 'was assigned by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3064, 'P141', 'el', 'name_inverse', 'αποδόθηκε από', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3065, 'P141', 'pt', 'name_inverse', 'foi atribuído por', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3066, 'P141', 'cn', 'name_inverse', '被指定了属性值於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3067, 'P141', 'en', 'comment', 'This property indicates the attribute that was assigned or the item that was related to the item denoted by a property P140 assigned attribute to in an Attribute assignment action.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3068, 'P142', 'en', 'name', 'used constituent', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3069, 'P142', 'de', 'name', 'benutzte Bestandteil', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3070, 'P142', 'cn', 'name', '使用称号构成部分', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3071, 'P142', 'de', 'name_inverse', 'wurde benutzt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3072, 'P142', 'en', 'name_inverse', 'was used in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3073, 'P142', 'cn', 'name_inverse', '被用来构成称号於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3074, 'P142', 'en', 'comment', 'This property associates the event of assigning an instance of E42 Identifier to an entity, with  the instances of E41 Appellation that were used as elements of the identifier.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3075, 'P143', 'en', 'name', 'joined', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3076, 'P143', 'de', 'name', 'verband', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3077, 'P143', 'cn', 'name', '加入了成员', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3078, 'P143', 'en', 'name_inverse', 'was joined by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3079, 'P143', 'de', 'name_inverse', 'wurde verbunden durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3080, 'P143', 'cn', 'name_inverse', '被加入为成员於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3081, 'P143', 'en', 'comment', 'This property identifies the instance of E39 Actor that becomes member of a E74 Group in an E85 Joining.
 	Joining events allow for describing people becoming members of a group with a more detailed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3082, 'P144', 'en', 'name', 'joined with', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3083, 'P144', 'de', 'name', 'verband mit', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3084, 'P144', 'cn', 'name', '加入成员到', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3085, 'P144', 'en', 'name_inverse', 'gained member by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3086, 'P144', 'de', 'name_inverse', 'erwarb Mitglied durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3087, 'P144', 'cn', 'name_inverse', '获得成员於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3088, 'P144', 'en', 'comment', 'This property identifies the instance of E74 Group of which an instance of E39 Actor becomes a member through an instance of E85 Joining.
Although a Joining activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which becoming member of one Group implies becoming member of another Group as well. 
Joining events allow for describing people becoming members of a group with a more detailed path from E74 Group through P144 joined with (gained member by), E85 Joining, P143 joined (was joined by) to E39 Actor, compared to the shortcut offered by P107 has current or former member (is current or former member of).
The property P144.1 kind of member can be used to specify the type of membership or the role the member has in the group. 
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3089, 'P145', 'en', 'name', 'separated', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3090, 'P145', 'de', 'name', 'entließ', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3091, 'P145', 'cn', 'name', '分离了成员', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3092, 'P145', 'en', 'name_inverse', 'left by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3093, 'P145', 'de', 'name_inverse', 'wurde entlassen durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3094, 'P145', 'cn', 'name_inverse', '脱离群组於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3098, 'P146', 'cn', 'name', '脱离了群组', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3099, 'P146', 'en', 'name_inverse', 'lost member by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3100, 'P146', 'de', 'name_inverse', 'verlor Mitglied durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3101, 'P146', 'cn', 'name_inverse', '失去成员於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3102, 'P146', 'en', 'comment', 'This property identifies the instance of E74 Group an instance of E39 Actor leaves through an instance of E86 Leaving.
Although a Leaving activity normally concerns only one instance of E74 Group, it is possible to imagine circumstances under which leaving one E74 Group implies leaving another E74 Group as well.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3103, 'P147', 'en', 'name', 'curated', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3104, 'P147', 'de', 'name', 'betreute kuratorisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3105, 'P147', 'cn', 'name', '典藏管理了', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3106, 'P147', 'en', 'name_inverse', 'was curated by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3107, 'P147', 'de', 'name_inverse', 'wurde kuratorisch betreut durch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3108, 'P147', 'cn', 'name_inverse', '被典藏管理於', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3109, 'P147', 'en', 'comment', 'This property associates an instance of E87 Curation Activity with the instance of E78 Collection that is subject of that  curation activity.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3110, 'P148', 'en', 'name', 'has component', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3111, 'P148', 'de', 'name', 'hat Bestandteil', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3112, 'P148', 'cn', 'name', '有组件', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3113, 'P148', 'en', 'name_inverse', 'is component of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3114, 'P148', 'de', 'name_inverse', 'ist Bestandteil von', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3115, 'P148', 'cn', 'name_inverse', '被用来组成', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3116, 'OA9', '0', 'name', 'erscheint zuletzt in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3117, 'P148', 'en', 'comment', 'This property associates an instance of E89 Propositional Object with a structural part of it that is by itself an instance of E89 Propositional Object.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3118, 'P149', 'en', 'name', 'is identified by', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3119, 'P149', 'en', 'name_inverse', 'identifies', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3120, 'P149', 'en', 'comment', 'This property identifies an instance of E28 Conceptual Object using an instance of E75 Conceptual Object Appellation.', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3121, 'P150', 'en', 'name', 'defines typical parts of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3122, 'P150', 'en', 'name_inverse', 'defines typical wholes for', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3123, 'P150', 'en', 'comment', 'The property "broaderPartitive" associates an instance of E55 Type “A” with an instance of E55 Type “B”, when items of type “A” typically form part of items of type “B”, such as “car motors” and “cars”.
It allows Types to be organised into hierarchies. This is the sense of "broader term partitive (BTP)" as defined in ISO 2788 and “broaderPartitive” in SKOS.
', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3124, 'P151', 'en', 'name', 'was formed from', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3125, 'P151', 'en', 'name_inverse', 'participated in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3126, 'P151', 'en', 'comment', 'This property associates an instance of E66 Formation with an instance of E74 Group from which the new group was formed preserving a sense of continuity such as in mission, membership or tradition.
	', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3127, 'P152', 'en', 'name', 'has parent', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3128, 'P152', 'en', 'name_inverse', 'is parent of', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3129, 'P152', 'en', 'comment', 'It appears that there is a notion of events justifying parenthood relationships in a biological or legal sense. There is a notion of legal parenthood being equal to or equivalent to biological parenthood. The fact that the legal system may not acknowledge biological parenthood is not a contradiction to a more general concept comprising both biological and legal sense. In particular, such a notion should imply as default children being heirs, if the society supports such concept. Superproperty of paths for was born – gave birth, was born, by father
	', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3130, 'OA1', 'en', 'name', 'begins chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3131, 'OA1', 'de', 'name', 'beginnt chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3132, 'OA1', 'en', 'comment', 'OA1 is used to link the beginning of a persistent item''s (E77) life span (or time of usage)
    with a certain date in time. E77 (Persistent Item) - P92i (was brought into existence by) - E63 (Beginning of Existence)
    - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [Holy Lance (E22)] was brought into existence by [forging of Holy Lance (E12)] has time span
    [Moment/Duration of Forging of Holy Lance (E52)] ongoing througout [0770-12-24 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3133, 'OA2', 'en', 'name', 'ends chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3134, 'OA2', 'de', 'name', 'endet chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3135, 'OA2', 'en', 'comment', 'OA2 is used to link the end of a persistent item''s (E77) life span (or time of usage) with
    a certain date in time.
    E77 (Persistent Item) - P93i (was taken out of existence by) - E64 (End of Existence) - P4 (has time span) -
    E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [The one ring (E22)] was destroyed by [Destruction of the one ring (E12)] has time span
    [Moment of throwing it down the lava (E52)] ongoing througout [3019-03-25 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3136, 'OA3', 'en', 'name', 'born chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3137, 'OA3', 'de', 'name', 'geboren chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3138, 'OA3', 'en', 'comment', 'OA3 is used to link the birth of a person with a certain date in time.
    21 (Person) - P98i (was born) by - E67 (Birth) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) -
    E61 (Time Primitive)
    Example: [Stefan (E21)] was born by [birth of Stefan (E12)] has time span
    [Moment/Duration of Stefan''s birth (E52)] ongoing througout [1981-11-23 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3139, 'OA4', 'en', 'name', 'died chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3140, 'OA4', 'de', 'name', 'gestorben chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3141, 'OA4', 'en', 'comment', 'OA4 is used to link the death of a person with a certain date in time.
    E21 (Person) - P100i (died in) - E69 (Death) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) -
    E61 (Time Primitive)
    Example: [Lady Diana (E21)] died in [death of Diana (E69)] has time span [Moment/Duration of Diana''s death (E52)]
    ongoing througout [1997-08-31 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3142, 'OA5', 'en', 'name', 'begins chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3143, 'OA5', 'de', 'name', 'beginnt chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3144, 'OA5', 'en', 'comment', 'OA5 is used to link the beginning of a temporal entity (E2) with a certain date in time.
    It can also be used to determine the beginning of a property''s duration.
    E2 (Temporal Entity) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [ Thirty Years'' War (E7)] has time span [Moment/Duration of Beginning of Thirty Years'' War (E52)] ongoing
    througout [1618-05-23 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3145, 'OA6', 'en', 'name', 'ends chronologically', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3146, 'OA6', 'de', 'name', 'endet chronologisch', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3147, 'OA6', 'en', 'comment', 'OA6 is used to link the end of a temporal entity''s (E2) with a certain date in time.
    It can also be used to determine the end of a property''s duration.
    E2 (temporal entity) - P4 (has time span) - E52 (Time Span) - P81 (ongoing throughout) - E61 (Time Primitive)
    Example: [ Thirty Years'' War (E7)] has time span [Moment/Duration of End of Thirty Years'' War (E52)] ongoing
    througout [1648-10-24 (E61)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3148, 'OA7', 'en', 'name', 'has relationship to', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3149, 'OA7', 'de', 'name', 'hat Beziehung zu', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3150, 'OA7', 'en', 'comment', 'OA7 is used to link two Actors (E39) via a certain relationship E39 Actor linked with
    E39 Actor: E39 (Actor) - P11i (participated in) - E5 (Event) - P11 (had participant) - E39 (Actor) Example:
    [ Stefan (E21)] participated in [ Relationship from Stefan to Joachim (E5)] had participant [Joachim (E21)] The
    connecting event is defined by an entity of class E55 (Type): [Relationship from Stefan to Joachim (E5)] has type
    [Son to Father (E55)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3151, 'OA8', 'en', 'name', 'appears for the first time in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3152, 'OA8', 'de', 'name', 'erscheint erstes mal in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3153, 'OA8', 'en', 'comment', 'OA9 is used to link the beginning of a persistent item''s (E77) life span (or time of
    usage) with a certain place. E.g to document the birthplace of a person. E77 Persistent Item linked with a E53
    Place: E77 (Persistent Item) - P92i (was brought into existence by) - E63 (Beginning of Existence) - P7 (took
    place at) - E53 (Place) Example: [Albert Einstein (E21)] was brought into existence by [Birth of Albert Einstein
    (E12)] took place at [Ulm (E53)]', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3154, 'OA9', 'en', 'name', 'appears for the last time in', '2017-11-28 16:37:16.558907', NULL);
INSERT INTO property_i18n VALUES (3155, 'OA9', 'en', 'comment', 'OA10 is used to link the end of a persistent item''s (E77) life span (or time of usage)
    with a certain place. E.g to document a person''s place of death. E77 Persistent Item linked with a E53 Place:
    E77 (Persistent Item) - P93i (was taken out of existence by) - E64 (End of Existence) - P7 (took place at) - E53
    (Place) Example: [Albert Einstein (E21)] was taken out of by [Death of Albert Einstein (E12)] took place at
    [Princeton (E53)]', '2017-11-28 16:37:16.558907', NULL);


--
-- Name: property_i18n_id_seq; Type: SEQUENCE SET; Schema: model; Owner: blade
--

SELECT pg_catalog.setval('property_i18n_id_seq', 3155, true);


--
-- Name: property_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('property_id_seq', 149, true);


--
-- Data for Name: property_inheritance; Type: TABLE DATA; Schema: model; Owner: openatlas
--

INSERT INTO property_inheritance VALUES (1, 'P12', 'P11', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (2, 'P93', 'P13', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (3, 'P11', 'P14', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (4, 'P12', 'P16', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (5, 'P15', 'P16', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (6, 'P15', 'P17', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (7, 'P14', 'P22', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (8, 'P14', 'P23', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (9, 'P12', 'P25', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (10, 'P7', 'P26', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (11, 'P7', 'P27', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (12, 'P14', 'P28', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (13, 'P14', 'P29', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (14, 'P12', 'P31', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (15, 'P125', 'P32', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (16, 'P16', 'P33', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (17, 'P140', 'P34', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (18, 'P141', 'P35', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (19, 'P141', 'P37', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (20, 'P141', 'P38', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (21, 'P140', 'P39', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (22, 'P141', 'P40', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (23, 'P140', 'P41', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (24, 'P141', 'P42', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (25, 'P1', 'P48', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (26, 'P49', 'P50', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (27, 'P51', 'P52', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (28, 'P105', 'P52', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (29, 'P53', 'P55', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (30, 'P46', 'P56', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (31, 'P128', 'P65', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (32, 'P67', 'P68', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (33, 'P67', 'P70', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (34, 'P67', 'P71', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (35, 'P130', 'P73', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (36, 'P1', 'P78', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (37, 'P3', 'P79', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (38, 'P3', 'P80', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (39, 'P1', 'P87', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (40, 'P12', 'P92', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (41, 'P12', 'P93', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (42, 'P92', 'P94', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (43, 'P92', 'P95', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (44, 'P11', 'P96', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (45, 'P92', 'P98', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (46, 'P11', 'P99', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (47, 'P93', 'P99', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (48, 'P93', 'P100', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (49, 'P1', 'P102', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (50, 'P31', 'P108', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (51, 'P92', 'P108', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (52, 'P49', 'P109', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (53, 'P31', 'P110', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (54, 'P16', 'P111', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (55, 'P12', 'P111', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (56, 'P31', 'P112', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (57, 'P12', 'P113', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (58, 'P92', 'P123', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (59, 'P93', 'P124', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (60, 'P130', 'P128', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (61, 'P67', 'P129', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (62, 'P1', 'P131', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (63, 'P15', 'P134', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (64, 'P94', 'P135', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (65, 'P15', 'P136', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (66, 'P2', 'P137', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (67, 'P67', 'P138', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (68, 'P16', 'P142', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (69, 'P11', 'P143', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (70, 'P11', 'P144', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (71, 'P11', 'P145', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (72, 'P11', 'P146', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (73, 'P1', 'P149', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');
INSERT INTO property_inheritance VALUES (74, 'P11', 'P151', '2015-06-11 19:26:28.25822', '2017-11-28 15:21:37.316625');


--
-- Name: property_inheritance_id_seq; Type: SEQUENCE SET; Schema: model; Owner: openatlas
--

SELECT pg_catalog.setval('property_inheritance_id_seq', 74, true);


--
-- PostgreSQL database dump complete
--

