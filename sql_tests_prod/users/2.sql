SELECT role_id, ARRAY_AGG(permission.name) AS permissions
FROM RolePermission
LEFT JOIN Permission ON RolePermission.permission_id = Permission.permission_id
WHERE role_id = 1
GROUP BY role_id;
