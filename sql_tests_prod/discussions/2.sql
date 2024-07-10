SELECT discussion_id, 
        parentdiscussion_id, 
        problem_id, 
        user_id, 
        title,
        content, 
        created_at, 
        updated_at
FROM Discussion
WHERE discussion_id = 3;