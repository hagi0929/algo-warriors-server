SELECT p.problem_id,
       p.title,
       STRING_AGG(d.content, ', ') AS difficulty,
       STRING_AGG(s.content, ', ') AS subcategory
FROM Problem p
LEFT JOIN ProblemTag pt ON p.problem_id = pt.problem_id
LEFT JOIN Tag d ON pt.tag_id = d.tag_id AND d.type = 'difficulty'
LEFT JOIN Tag s ON pt.tag_id = s.tag_id AND s.type = 'subcategory'
GROUP BY p.problem_id, p.title
ORDER BY p.problem_id LIMIT 300;