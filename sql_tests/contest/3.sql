INSERT INTO ContestParticipant (contest_id, participant_id)
VALUES (1, 2);
INSERT INTO ContestParticipant (contest_id, participant_id)
VALUES (1, 3);
INSERT INTO ContestParticipant (contest_id, participant_id)
VALUES (1, 4);

SELECT u.user_id, u.username
FROM ContestParticipant cp
JOIN ServiceUser u ON cp.participant_id = u.user_id
WHERE cp.contest_id = 1;

SELECT c.contest_id, c.title, c.description, c.start_time, c.end_time, c.created_by, c.created_at, c.winner
FROM Contest c
JOIN ContestParticipant cp ON c.contest_id = cp.contest_id
WHERE cp.participant_id = 2 AND c.start_time <= NOW() AND c.end_time >= NOW();
