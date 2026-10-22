BEGIN;

-- Raise database version
UPDATE web.settings SET value = '9.6.0' WHERE name = 'database_version';

-- #2156: Transform single _from dates (at 00:00:00) into one-day timespans
UPDATE model.entity
SET begin_to = begin_from
WHERE begin_from IS NOT NULL
  AND begin_to IS NULL
  AND begin_from::time = '00:00:00';

UPDATE model.entity
SET end_to = end_from
WHERE end_from IS NOT NULL
  AND end_to IS NULL
  AND end_from::time = '00:00:00';

UPDATE model.link
SET begin_to = begin_from
WHERE begin_from IS NOT NULL
  AND begin_to IS NULL
  AND begin_from::time = '00:00:00';

UPDATE model.link
SET end_to = end_from
WHERE end_from IS NOT NULL
  AND end_to IS NULL
  AND end_from::time = '00:00:00';

-- #2156: Set _to dates with 00:00:00 time to 23:59:59
UPDATE model.entity
SET begin_to = begin_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE begin_to IS NOT NULL
  AND begin_to::time = '00:00:00';

UPDATE model.entity
SET end_to = end_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE end_to IS NOT NULL
  AND end_to::time = '00:00:00';

UPDATE model.link
SET begin_to = begin_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE begin_to IS NOT NULL
  AND begin_to::time = '00:00:00';

UPDATE model.link
SET end_to = end_to + INTERVAL '23 hours 59 minutes 59 seconds'
WHERE end_to IS NOT NULL
  AND end_to::time = '00:00:00';

END;
