SELECT T.tag_id, T.type, T.content
FROM Tag T
JOIN ProblemTag PT ON T.tag_id = PT.tag_id
WHERE PT.problem_id = 1