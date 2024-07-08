WITH temp AS (
    SELECT P.problem_id, P.title, P.created_by, P.created_at
    FROM Problem P
    JOIN ProblemTag PT ON P.problem_id = PT.problem_id
    JOIN Tag T ON PT.tag_id = T.tag_id
    WHERE T.type = 'difficulty' AND T.content IN ('1')
),

temp2 as (
SELECT P.problem_id, P.title, P.created_by, P.created_at
FROM temp P
JOIN ProblemTag PT ON P.problem_id = PT.problem_id
JOIN Tag T ON PT.tag_id = T.tag_id
WHERE T.type = 'subcategory' AND T.content IN('graphs')
)

SELECT P.problem_id, P.title, P.created_by, P.created_at
FROM temp2 P
JOIN ProblemTag PT ON P.problem_id = PT.problem_id
JOIN Tag T ON PT.tag_id = T.tag_id
WHERE T.type = 'source' AND T.content IN ('2')