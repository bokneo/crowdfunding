CREATE TABLE auth_user (
    id SERIAL PRIMARY KEY
    first_name VARCHAR(64) NOT NULL,
    last_name VARCHAR(64) NOT NULL,
    password VARCHAR(255) NOT NULL,
    email VARCHAR(128),
    total_amount NUMERIC(12,2) DEFAULT 0
);

CREATE TABLE project(
    project_name VARCHAR(255) PRIMARY KEY,
    email VARCHAR(128) NOT NULL,
    project_description TEXT,
    start_date DATE NOT NULL,
    end_data DATE NOT NULL,
    pledged NUMERIC(12,2) DEFAULT 0,
    FOREIGN KEY(email) REFERENCES users(email)
);

CREATE TABLE investor(
    investor_id SERIAL PRIMARY KEY,
    project_name VARCHAR(255),
    email VARCHAR(128) REFERENCES users(email),
    pledged NUMERIC(12,2) DEFAULT 0,
    ts  TIMESTAMP,
    FOREIGN KEY(project_name) REFERENCES project(project_name)
);