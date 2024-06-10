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
