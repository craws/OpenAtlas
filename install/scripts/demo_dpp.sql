-- SQL to filter demo data from DPP

-- To do: remove orphaned gis data and source translations

BEGIN;

-- Disable triggers, otherwise script takes forever and/or run into errors
ALTER TABLE model.entity DISABLE TRIGGER on_delete_entity;
ALTER TABLE model.link_property DISABLE TRIGGER on_delete_link_property;

-- Delete data from other case studies
DELETE FROM model.entity WHERE id NOT IN
    (SELECT e.id FROM model.entity e
    JOIN model.link l ON
        e.id = l.domain_id
        AND l.property_code = 'P2'
        AND l.range_id = (SELECT id FROM model.entity WHERE name = 'Ethnonym of the Vlachs'))
AND class_code IN ('E33', 'E6', 'E7', 'E8', 'E12', 'E21', 'E74', 'E40', 'E31', 'E18', 'E84')
AND (system_type IS NULL OR system_type NOT IN ('source translation'));

-- Delete orphans manually because triggers are disabled
DELETE FROM model.entity WHERE id IN (
   SELECT e.id FROM model.entity e
        LEFT JOIN model.link l1 on e.id = l1.domain_id
        LEFT JOIN model.link l2 on e.id = l2.range_id
        LEFT JOIN model.link_property lp2 on e.id = lp2.range_id
        WHERE
            l1.domain_id IS NULL
            AND l2.range_id IS NULL
            AND lp2.range_id IS NULL
            AND e.class_code IN ('E61', 'E41', 'E53', 'E82'));

-- Delete unrelated user
DELETE FROM web.user WHERE username NOT IN ('admin', 'dschmid', 'bkoschicek', 'mpopovic', 'jnikic');

-- Insert demo user
INSERT INTO web.user (username, real_name, email, active, group_id, password) VALUES (
    'Demolina', 'Demolina', 'demolina@example.com', True, (SELECT id FROM web.group WHERE name = 'editor'),
    '$2b$12$9T05T1IiCnlEiUdf5gSosuSYewK5Rf4T/PwuvbSXEooR95BG2kgvG');

-- Disable email, set sitename and other settings
UPDATE web.settings SET value = '' WHERE name = 'mail';
UPDATE web.settings SET value = '' WHERE name LIKE 'mail_%';
UPDATE web.settings SET value = 'openatlas@craws.net' WHERE name LIKE 'mail_recipients_feedback';
UPDATE web.settings SET value = '1' WHERE name = 'file_upload_max_size';
UPDATE web.settings SET value = 'Development Demo' WHERE name = 'site_name';

-- Update content
UPDATE web.i18n SET text = '<p>Development Demo site for <a href="http://openatlas.eu/">OpenAtlas</a> projects. <a href="/login">Login</a>.</p>
<p>The data will be reset daily around midnight. Demo data kindly provided by:</p>
<p><strong>The Ethnonym of the Vlachs in the Written Sources and the Toponymy in the Historical Region of Macedonia</strong> (11th-16th Cent.) <a href="http://dpp.oeaw.ac.at/index.php?seite=CaseStudies&amp;submenu=skopje" target="_blank" rel="noopener noreferrer">More Information</a></p>
<p>The present demo version is the result of a scholarly project, which was submitted by the digital cluster project &ldquo;Digitising Patterns of Power (<a href="http://dpp.oeaw.ac.at/]" target="_blank" rel="noopener noreferrer">DPP</a>)&rdquo; at the Institute for Medieval Research (Austrian Academy of Sciences, Vienna) and the Ss. Cyril and Methodius University of Skopje (Faculty of Philosophy, Institute for History). It focuses on the interplay between the resident population and the nomads (i.e. the Vlachs) in the historical region of Macedonia from the 11th to the 16th centuries.<br /><br />This region at the crossroads of Orthodoxy, Roman Catholicism and Islam and the question of the origin of the Vlachs, who identify themselves as a separate ethnic group until modern times, as well as the ethnonym "Vlachs" and its derivatives in the form of toponyms and personal names are at the core of the joint research. Hereby, historical and archaeological research is combined with Digital Humanities.<br /><br />The project, which was successfully submitted by the project coordinators Doz. Dr. Mihailo Popović and Prof. Dr. Toni Filiposki, is funded by the Centre for International Cooperation &amp; Mobility (ICM) of the Austrian Agency for International Cooperation in Education and Research (OeAD-GmbH) for two years (2016-18) and forms an additional case study within DPP. <br /><br />Project teams:<br /><br />Toni Filiposki (project leader / Skopje), Boban Petrovski (Skopje), Nikola Minov (Skopje), Vladimir Kuhar (Skopje), Boban Gjorgjievski (Skopje)<br /><br />Mihailo Popović (project leader / Vienna), Jelena Nikić (Vienna), David Schmid (Vienna)</p>
<p><strong>OpenAtlas</strong></p>' WHERE name = 'intro' AND language = 'en';
UPDATE web.i18n SET text = '<p style="text-align: left;">Development Demo Seite f&uuml;r <a href="http://openatlas.eu/">OpenAtlas</a> Projekte. Zum <a href="/login">Login</a>.</p>
<p>Die Daten werden t&auml;glich gegen Mitternacht zur&uuml;ckgesetzt. Demo Daten freundlicherweise zur Verf&uuml;gung gestellt von:</p>
<p><strong>The Ethnonym of the Vlachs in the Written Sources and the Toponymy in the Historical Region of Macedonia</strong> (11th-16th Cent.) <a href="http://dpp.oeaw.ac.at/index.php?seite=CaseStudies&amp;submenu=skopje" target="_blank" rel="noopener noreferrer">More Information</a></p>
<p>The present demo version is the result of a scholarly project, which was submitted by the digital cluster project &ldquo;Digitising Patterns of Power (<a href="http://dpp.oeaw.ac.at/]" target="_blank" rel="noopener noreferrer">DPP</a>)&rdquo; at the Institute for Medieval Research (Austrian Academy of Sciences, Vienna) and the Ss. Cyril and Methodius University of Skopje (Faculty of Philosophy, Institute for History). It focuses on the interplay between the resident population and the nomads (i.e. the Vlachs) in the historical region of Macedonia from the 11th to the 16th centuries.<br /><br />This region at the crossroads of Orthodoxy, Roman Catholicism and Islam and the question of the origin of the Vlachs, who identify themselves as a separate ethnic group until modern times, as well as the ethnonym "Vlachs" and its derivatives in the form of toponyms and personal names are at the core of the joint research. Hereby, historical and archaeological research is combined with Digital Humanities.<br /><br />The project, which was successfully submitted by the project coordinators Doz. Dr. Mihailo Popović and Prof. Dr. Toni Filiposki, is funded by the Centre for International Cooperation &amp; Mobility (ICM) of the Austrian Agency for International Cooperation in Education and Research (OeAD-GmbH) for two years (2016-18) and forms an additional case study within DPP. <br /><br />Project teams:<br /><br />Toni Filiposki (project leader / Skopje), Boban Petrovski (Skopje), Nikola Minov (Skopje), Vladimir Kuhar (Skopje), Boban Gjorgjievski (Skopje)<br /><br />Mihailo Popović (project leader / Vienna), Jelena Nikić (Vienna), David Schmid (Vienna)</p>
<p>&nbsp;<strong>OpenAtlas</strong></p>' WHERE name = 'intro' AND language = 'de';
UPDATE web.i18n SET text = 'Webmaster: alexander.watzinger@craws.net' WHERE name = 'contact' AND language = 'en';
UPDATE web.i18n SET text = 'Webmaster: alexander.watzinger@craws.net' WHERE name = 'contact' AND language = 'de';
UPDATE web.i18n SET text = '' WHERE name = 'legal_notice' AND language = 'en';
UPDATE web.i18n SET text = '' WHERE name = 'legal_notice' AND language = 'de';

-- Re-enable triggers
ALTER TABLE model.entity ENABLE TRIGGER on_delete_entity;
ALTER TABLE model.link_property ENABLE TRIGGER on_delete_link_property;

COMMIT;
