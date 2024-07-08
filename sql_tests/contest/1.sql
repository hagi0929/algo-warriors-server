INSERT INTO contest (title, description, start_time, end_time, created_by)
VALUES ('Coding Challenge June 2024', 'Join our coding challenge this June and test your skills!', '2024-06-25T09:00:00Z', '2024-06-25T12:00:00Z', 1)
RETURNING contest_id, created_at;

INSERT INTO contest (title, description, start_time, end_time, created_by)
VALUES ('Coding Challenge July 2024', 'Join our coding challenge this July and test your skills!', '2024-07-25T09:00:00Z', '2024-07-25T12:00:00Z', 1)
RETURNING contest_id, created_at;

SELECT * FROM Contest;

SELECT * FROM Contest 
WHERE contest_id = 1;

SELECT * 
FROM Contest
WHERE start_time BETWEEN "2024-06-15 09:00:00+00" AND "2024-06-30 09:00:00+00"
ORDER BY start_time;
