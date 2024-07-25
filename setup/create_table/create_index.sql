-- Role table
CREATE UNIQUE INDEX idx_role_role_id ON Role (role_id);
CREATE CLUSTERED INDEX idx_role_role_name ON Role (role_name);

-- Permission table
CREATE UNIQUE INDEX idx_permission_permission_id ON Permission (permission_id);
CREATE CLUSTERED INDEX idx_permission_name ON Permission (name);

-- RolePermission table
CREATE UNIQUE INDEX idx_rolepermission_role_permission ON RolePermission (role_id, permission_id);
CREATE NONCLUSTERED INDEX idx_rolepermission_permission_id ON RolePermission (permission_id);

-- ServiceUser table
CREATE UNIQUE INDEX idx_serviceuser_user_id ON ServiceUser (user_id);
CREATE CLUSTERED INDEX idx_serviceuser_username ON ServiceUser (username);
CREATE NONCLUSTERED INDEX idx_serviceuser_email ON ServiceUser (email);
CREATE NONCLUSTERED INDEX idx_serviceuser_role_id ON ServiceUser (role_id);

-- Problem table
CREATE UNIQUE INDEX idx_problem_problem_id ON Problem (problem_id);
CREATE CLUSTERED INDEX idx_problem_title ON Problem (title);
CREATE NONCLUSTERED INDEX idx_problem_created_by ON Problem (created_by);

-- TestCase table
CREATE UNIQUE INDEX idx_testcase_testcase_id ON TestCase (testcase_id);
CREATE CLUSTERED INDEX idx_testcase_problem_id ON TestCase (problem_id);

-- Tag table
CREATE UNIQUE INDEX idx_tag_tag_id ON Tag (tag_id);
CREATE CLUSTERED INDEX idx_tag_type_content ON Tag (type, content);

-- ProblemTag table
CREATE UNIQUE INDEX idx_problem_tag ON ProblemTag (problem_id, tag_id);
CREATE NONCLUSTERED INDEX idx_problem_tag_problem_id ON ProblemTag (problem_id);
CREATE NONCLUSTERED INDEX idx_problem_tag_tag_id ON ProblemTag (tag_id);

-- Discussion table
CREATE UNIQUE INDEX idx_discussion_discussion_id ON Discussion (discussion_id);
CREATE CLUSTERED INDEX idx_discussion_problem_id ON Discussion (problem_id);
CREATE NONCLUSTERED INDEX idx_discussion_user_id ON Discussion (user_id);
CREATE NONCLUSTERED INDEX idx_discussion_parentdiscussion_id ON Discussion (parentdiscussion_id);

-- Contest table
CREATE UNIQUE INDEX idx_contest_contest_id ON Contest (contest_id);
CREATE CLUSTERED INDEX idx_contest_title ON Contest (title);
CREATE NONCLUSTERED INDEX idx_contest_created_by ON Contest (created_by);
CREATE NONCLUSTERED INDEX idx_contest_winner ON Contest (winner);
CREATE NONCLUSTERED INDEX idx_contest_start_time ON Contest (start_time);
CREATE NONCLUSTERED INDEX idx_contest_end_time ON Contest (end_time);

-- ContestProblem table
CREATE UNIQUE INDEX idx_contest_problem ON ContestProblem (contest_id, problem_id);
CREATE CLUSTERED INDEX idx_contestproblem_contest_id ON ContestProblem (contest_id);
CREATE NONCLUSTERED INDEX idx_contestproblem_problem_id ON ContestProblem (problem_id);

-- ContestParticipant table
CREATE UNIQUE INDEX idx_contest_participant ON ContestParticipant (contest_id, participant_id);
CREATE CLUSTERED INDEX idx_contestparticipant_contest_id ON ContestParticipant (contest_id);
CREATE NONCLUSTERED INDEX idx_contestparticipant_participant_id ON ContestParticipant (participant_id);

-- ContestProblemSubmission table
CREATE UNIQUE INDEX idx_submission_id ON ContestProblemSubmission (submission_id);
CREATE CLUSTERED INDEX idx_contestproblemsubmission_participant_id ON ContestProblemSubmission (participant_id);
CREATE NONCLUSTERED INDEX idx_contestproblemsubmission_problem_id ON ContestProblemSubmission (problem_id);

-- PopupResource table
CREATE UNIQUE INDEX idx_popupresource_resource_id ON PopupResource (resource_id);
CREATE CLUSTERED INDEX idx_popupresource_resource_name ON PopupResource (resource_name);
CREATE NONCLUSTERED INDEX idx_popupresource_resource_url ON PopupResource (resource_url);
CREATE NONCLUSTERED INDEX idx_popupresource_homepage ON PopupResource (homepage);
CREATE NONCLUSTERED INDEX idx_popupresource_resource_language ON PopupResource (resource_language);

-- Materialized view index
CREATE UNIQUE INDEX idx_popupresourcesview_resource_id ON PopupResourcesView (resource_id);
CREATE CLUSTERED INDEX idx_popupresourcesview_resource_name ON PopupResourcesView (resource_name);
CREATE NONCLUSTERED INDEX idx_popupresourcesview_resource_url ON PopupResourcesView (resource_url);
CREATE NONCLUSTERED INDEX idx_popupresourcesview_homepage ON PopupResourcesView (homepage);
CREATE NONCLUSTERED INDEX idx_popupresourcesview_resource_language ON PopupResourcesView (resource_language);
