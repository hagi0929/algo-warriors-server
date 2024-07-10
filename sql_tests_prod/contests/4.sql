SELECT u.user_id, u.username
FROM ContestParticipant cp
JOIN ServiceUser u ON cp.participant_id = u.user_id
WHERE cp.contest_id = 50;
