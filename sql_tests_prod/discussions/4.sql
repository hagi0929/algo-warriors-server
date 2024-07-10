INSERT INTO Discussion (parentdiscussion_id, problem_id, user_id, title, content, created_at, updated_at)
    VALUES (NULL, 4, 1, 'Problem 4 Discussion', 'This is a new comment', NOW(), NOW())
--RETURNING discussion_id; available in backend, not here