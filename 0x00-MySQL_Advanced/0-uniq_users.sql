-- 0. We are all unique!
-- SQL script that creates a table users
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INT,
    email VARCHAR(255),
    name VARCHAR(255)
);