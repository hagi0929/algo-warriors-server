WITH RECURSIVE subthreads AS (
    SELECT 
        discussion_id, 
        parentdiscussion_id, 
        problem_id, 
        user_id, 
        title, 
        content, 
        created_at, 
        updated_at
    FROM 
        Discussion
    WHERE 
        discussion_id = 1
    UNION ALL
    SELECT 
        d.discussion_id, 
        d.parentdiscussion_id, 
        d.problem_id, 
        d.user_id, 
        d.title, 
        d.content, 
        d.created_at, 
        d.updated_at
    FROM 
        Discussion d
    INNER JOIN 
        subthreads s 
    ON 
        d.parentdiscussion_id = s.discussion_id
)
SELECT DISTINCT discussion_id, 
        parentdiscussion_id, 
        problem_id, 
        user_id, 
        title, 
        content, 
        created_at, 
        updated_at
FROM 
    subthreads
ORDER BY 
    created_at;