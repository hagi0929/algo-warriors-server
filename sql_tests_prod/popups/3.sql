SELECT *
FROM PopupResourcesView
WHERE resource_name ILIKE '%artificial-intelligence%'
   OR topics ILIKE '%artificial-intelligence%'
ORDER BY stars DESC;
