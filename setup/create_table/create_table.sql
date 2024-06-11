CREATE TABLE ServiceUser (
    user_id INT GENERATED ALWAYS AS IDENTITY,
    username VARCHAR(50) NOT NULL,
    email VARCHAR(50) NOT NULL,
    password VARCHAR(64) NOT NULL,
    created_at DATE NOT NULL,
        PRIMARY KEY(user_id)
);



CREATE TABLE Problem (
    problem_id INT GENERATED ALWAYS AS IDENTITY,
    title VARCHAR(50),
    description TEXT,
    created_by INT,
    created_at DATE NOT NULL,
        PRIMARY KEY(problem_id),
        FOREIGN KEY(created_by) REFERENCES ServiceUser(user_id) ON DELETE SET NULL
);

CREATE TABLE TestCase (
    testcase_id INT GENERATED ALWAYS AS IDENTITY,
    problem_id INT,
    input TEXT,
    output TEXT,
    FOREIGN KEY(problem_id) REFERENCES Problem(problem_id) ON DELETE CASCADE
);

CREATE TABLE Role (
    role_id INT GENERATED ALWAYS AS IDENTITY,
    role_name TEXT,

    PRIMARY KEY(role_id)
);

CREATE TABLE UserRole (
    user_id INT,
    role_id INT,

    FOREIGN KEY(user_id) REFERENCES ServiceUser(user_id) ON DELETE CASCADE,
    FOREIGN KEY(role_id) REFERENCES Role(role_id) ON DELETE SET NULL,
    PRIMARY KEY(user_id, role_id)
);

CREATE TABLE ContestParticipant (
    contest_id INT,
    score INT,
    user_id INT,
    
    FOREIGN KEY(contest_id) REFERENCES Contest(contest_id) ON DELETE CASCADE,
    FOREIGN KEY(user_id) REFERENCES ServiceUser(user_id) ON DELETE CASCADE,
    PRIMARY KEY(contest_id, user_id)
);

CREATE TABLE Permission (
    permission_id INT GENERATED ALWAYS AS IDENTITY,
    permission_name TEXT,

    PRIMARY_KEY(permission_id)
);

