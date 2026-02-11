BEGIN;

-- Raise database version
UPDATE web.settings SET value = '8.12.0' WHERE name = 'database_version';

-- Fix for deleting users with API tokens (#2489)
ALTER TABLE IF EXISTS ONLY web.user_tokens DROP CONSTRAINT IF EXISTS user_tokens_creator_id_fkey;
ALTER TABLE IF EXISTS ONLY web.user_tokens DROP CONSTRAINT IF EXISTS user_tokens_user_id_fkey;
ALTER TABLE ONLY web.user_tokens ADD CONSTRAINT user_tokens_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES web."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;
ALTER TABLE ONLY web.user_tokens ADD CONSTRAINT user_tokens_user_id_fkey FOREIGN KEY (user_id) REFERENCES web."user"(id) ON UPDATE CASCADE ON DELETE CASCADE;

END;
