BEGIN;

DROP TABLE IF EXISTS web.license;
DROP SEQUENCE IF EXISTS license_id_seq;
CREATE SEQUENCE license_id_seq INCREMENT 1 MINVALUE 1 MAXVALUE 2147483647 CACHE 1;

CREATE TABLE web.license (
    "id" integer DEFAULT nextval('license_id_seq') NOT NULL,
    "name" text NOT NULL,
    "description" text,
    "super_id" integer,
    "url" text,
    "created" timestamp NOT NULL,
    "modified" timestamp,
    CONSTRAINT "license_pkey" PRIMARY KEY ("id")
) WITH (oids = false);

INSERT INTO web.license (name, description) VALUES
    ('public', 'Licenses that allow public sharing, e.g. displaying on a website or adding to a public archive.'),
    ('restricted', 'Licenses that restrict the use for public sharing.'),
    ('needs clarification', 'Licenses that have to be clarified.');

INSERT INTO web.license (name, description, url, super_id) VALUES
    ('Public domain', 'When a work is in the public domain, it is free for use by anyone for any purpose without restriction under copyright law.', 'https://wiki.creativecommons.org/wiki/Public_domain', (SELECT id FROM web.license WHERE name = '')),
    ('CC BY 4.0', 'See https://creativecommons.org/licenses/by/4.0/', 'https://creativecommons.org/licenses/by/4.0/', (SELECT id FROM web.license WHERE name = 'public')),
    ('CC BY-SA 4.0', 'See https://creativecommons.org/licenses/by-sa/4.0/', 'https://creativecommons.org/licenses/by-sa/4.0/', (SELECT id FROM web.license WHERE name = 'public')),
    ('Unspecified restricted', 'This is an example entry in case the kind of restriction is not known.', NULL, (SELECT id FROM web.license WHERE name = 'restricted')),
    ('Needs clarification', 'This is an example entry', NULL, (SELECT id FROM web.license WHERE name = 'needs clarification'));

END;
