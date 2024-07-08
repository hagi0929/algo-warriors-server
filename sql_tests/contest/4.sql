INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (1, 2, 1, 'Solution code for problem 1 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (2, 2, 2, 'Solution code for problem 2 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (3, 2, 3, 'Solution code for problem 3 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (4, 2, 4, 'Solution code for problem 4 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (5, 2, 5, 'Solution code for problem 5 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (6, 3, 1, 'Solution code for problem 1 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (7, 3, 2, 'Solution code for problem 2 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (8, 3, 3, 'Solution code for problem 3 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (9, 4, 1, 'Solution code for problem 1 submission', NOW());

INSERT INTO ContestProblemSubmission (submission_id, participant_id, problem_id, submission, created_at) 
VALUES (10, 4, 2, 'Solution code for problem 2 submission', NOW());

WITH RankedParticipants AS (
    SELECT
        cps.participant_id,
        COUNT(DISTINCT cps.problem_id) AS score,
        MAX(cps.created_at) AS last_submission,
        RANK() OVER (ORDER BY COUNT(DISTINCT cps.problem_id) DESC, MAX(cps.created_at) ASC) AS rank
    FROM
        ContestProblemSubmission cps
    JOIN ContestParticipant cp ON cps.participant_id = cp.participant_id
    JOIN ContestProblem pr ON cps.problem_id = pr.problem_id
    WHERE cp.contest_id = 1 AND pr.contest_id = 1
    GROUP BY cps.participant_id
)
SELECT rp.participant_id AS user_id, su.username, rp.score, rp.rank
FROM RankedParticipants rp
JOIN ServiceUser su ON rp.participant_id = su.user_id
WHERE rp.participant_id = 2;
