SET search_path = web;

INSERT INTO web."user" (group_id, username, password, active, email) VALUES (
    (SELECT id FROM web."group" WHERE name = 'admin'),
    'test',
    '$2b$12$yPQCBsSQdZxESEz79SFiOOZBLG2GZ9Cc2rzVMgZxXyW2y3T499LYK',
    True,
    'test@test.org'
);
