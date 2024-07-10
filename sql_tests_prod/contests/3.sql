SELECT cp.problem_id, p.title, p.description
FROM ContestProblem cp
JOIN Problem p ON cp.problem_id = p.problem_id
WHERE cp.contest_id = 50;
