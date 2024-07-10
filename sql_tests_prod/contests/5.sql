SELECT c.contest_id, c.title, c.description, c.start_time, c.end_time, c.created_by, c.created_at, c.winner
FROM Contest c
JOIN ContestParticipant cp ON c.contest_id = cp.contest_id
WHERE cp.participant_id = 25;
