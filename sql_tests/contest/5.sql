WITH UserSubmissions AS (
    SELECT
        cps.participant_id,
        COUNT(DISTINCT cps.problem_id) AS score,
        MAX(cps.created_at) AS last_submission
    FROM
        ContestProblemSubmission cps
    JOIN ContestParticipant cp ON cps.participant_id = cp.participant_id
    JOIN ContestProblem pr ON cps.problem_id = pr.problem_id
    WHERE cp.contest_id = 1 AND pr.contest_id = 1
    GROUP BY cps.participant_id
)
SELECT u.user_id, u.username, us.score, us.last_submission
FROM UserSubmissions us
JOIN ServiceUser u ON us.participant_id = u.user_id
ORDER BY
    us.score DESC,
    us.last_submission ASC
LIMIT 3;
