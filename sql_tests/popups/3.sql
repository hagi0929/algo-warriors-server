SELECT resource_language AS language,
       AVG(stars) AS avg_stars,
       COUNT(*) AS resource_count
FROM PopupResourcesView
WHERE resource_language IS NOT NULL
GROUP BY resource_language
ORDER BY avg_stars DESC;
