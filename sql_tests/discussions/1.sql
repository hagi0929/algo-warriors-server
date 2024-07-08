SELECT discussion_id, 
        parentdiscussion_id, 
        problem_id, 
        user_id, 
        content, 
        created_at, 
        updated_at
FROM Discussion
WHERE problem_id = 2;