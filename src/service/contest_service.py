# Service layer for contest
# Author: Vidhi Ruparel
from typing import List, Optional
from ..model.contest import Contest
from ..repos.contest_repos import ContestRepos

class ContestService:
    # Get all contests
    @staticmethod
    def get_all_contests() -> List[Contest]:
        return ContestRepos.get_all_contests()
    
    # Get contest by id
    @staticmethod
    def get_contest_by_id(contest_id: int) -> Optional[Contest]:
        return ContestRepos.get_contest_by_id(contest_id)
    
    # Create contest
    @staticmethod
    def create_contest(data) -> Contest:
        return ContestRepos.create_contest(data)
    
    # Delete contest by id
    @staticmethod
    def delete_contest(contest_id: int) -> None:
        ContestRepos.delete_contest(contest_id)

    # Register user to contest
    @staticmethod
    def register_user_to_contest(contest_id: int, user_id: int) -> None:
        ContestRepos.register_user_to_contest(contest_id, user_id)

    # Add problem to contest
    @staticmethod
    def add_problem_to_contest(contest_id: int, problem_id: int) -> None:
        ContestRepos.add_problem_to_contest(contest_id, problem_id)

    # Get contest problems
    @staticmethod
    def get_contest_problems(contest_id: int) -> List[dict]:
        return ContestRepos.get_contest_problems(contest_id)
    
    # Get contest participants
    @staticmethod
    def get_contest_participants(contest_id: int) -> List[dict]:
        return ContestRepos.get_contest_participants(contest_id)
    
    # Get contests the user is participating in
    @staticmethod
    def get_contests_participating(user_id: int) -> List[Contest]:
        return ContestRepos.get_contests_participating(user_id)
    
    # Submit contest problem
    @staticmethod
    def submit_contest_problem(participant_id: int, problem_id: int, submission: str) -> int:
        return ContestRepos.submit_contest_problem(participant_id, problem_id, submission)
    
    # Get contest within a time range
    @staticmethod
    def get_contests_within_date_range(start_date: str, end_date: str) -> List[Contest]:
        return ContestRepos.get_contests_within_date_range(start_date, end_date)
    
    # Get contest participants ranked
    @staticmethod
    def get_contest_participants_ranked(contest_id: int, n: int) -> List[dict]:
        return ContestRepos.get_contest_participants_ranked(contest_id, n)

    # Get user's score and rank in contest
    @staticmethod
    def get_user_score_and_rank(contest_id: int, user_id: int) -> Optional[dict]:
        return ContestRepos.get_user_score_and_rank(contest_id, user_id)
    
    # Declare contest winner
    @staticmethod
    def declare_winner(contest_id: int) -> None:
        ContestRepos.declare_winner(contest_id)
