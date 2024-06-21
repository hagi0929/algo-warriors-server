SELECT DISTINCT P.problem_id, P.title, P.created_by, P.created_at
        FROM Problem P
        JOIN ProblemTag PT ON P.problem_id = PT.problem_id
        JOIN Tag T ON PT.tag_id = T.tag_id
        WHERE P.problem_id != :pid
        AND (T.type = 'difficulty'
        AND T.content IN (
        SELECT T.content FROM ProblemTag PT_diff
        JOIN Tag T ON PT_diff.tag_id = T.tag_id
        WHERE PT_diff.problem_id = :pid
        AND T.type = 'difficulty'
        )
        OR(
        T.type = 'subcategory'
        AND T.content IN (
            SELECT T.content FROM ProblemTag PT_sub
            JOIN Tag T ON PT_sub.tag_id = T.tag_id
            WHERE PT_sub.problem_id = :pid
            AND T.type = 'subcategory'
            )
        ))
        LIMIT 5;