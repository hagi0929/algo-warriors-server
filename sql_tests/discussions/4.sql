INSERT INTO Discussion (parentdiscussion_id, problem_id, user_id, content, created_at, updated_at)
    VALUES (NULL, 4, 1, ‘This is a new comment’, NOW(), NOW())
    RETURNING discussion_id;