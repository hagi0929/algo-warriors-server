INSERT INTO ContestProblem (problem_id, contest_id)
VALUES (1, 1);
INSERT INTO ContestProblem (problem_id, contest_id)
VALUES (2, 1);
INSERT INTO ContestProblem (problem_id, contest_id)
VALUES (3, 1);
INSERT INTO ContestProblem (problem_id, contest_id)
VALUES (4, 1);
INSERT INTO ContestProblem (problem_id, contest_id)
VALUES (4, 1);

SELECT cp.problem_id, p.title, p.description
FROM ContestProblem cp
JOIN Problem p ON cp.problem_id = p.problem_id
WHERE cp.contest_id = 1;
