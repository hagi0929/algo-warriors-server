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