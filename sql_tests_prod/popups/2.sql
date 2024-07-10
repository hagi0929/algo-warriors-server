SELECT *
FROM PopupResourcesView
WHERE resource_name ILIKE '%python%'
   OR topics ILIKE '%python%'
ORDER BY stars DESC;
