DROP TABLE IF EXISTS users;

CREATE TABLE users
(
    id        INTEGER PRIMARY KEY AUTOINCREMENT,
    email     VARCHAR(100) NOT NULL UNIQUE,
    password  VARCHAR(15)  NOT NULL,
    firstname VARCHAR(40)  NOT NULL,
    lastname  VARCHAR(40)  NOT NULL,
    role      VARCHAR(30)  NOT NULL DEFAULT 'student',
    registered_on TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    current_login TIMESTAMP,
    last_login TIMESTAMP,
    postkey VARCHAR(MAX) NOT NULL,
);