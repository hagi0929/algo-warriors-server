# Repository for Contest model
# Author: Vidhi Ruparel
from sqlalchemy.sql import text
from .. import db
from ..model.contest import Contest
from typing import List, Optional

class ContestRepos:
    # Get all contests
    @staticmethod
    def get_all_contests() -> List[Contest]:
        query = text("""
        SELECT * FROM Contest
        """)
        result = db.session.execute(query)
        contests = []
        for row in result:
            contest = Contest(
                contest_id=row[0],
                title=row[1],
                description=row[2],
                start_time=row[3],
                end_time=row[4],
                created_by=row[5],
                created_at=row[6],
                winner=row[7]
            )
            contests.append(contest)        
        return contests
    
    # Get contest by id
    @staticmethod
    def get_contest_by_id(contest_id: int) -> Optional[Contest]:
        query = text("""
        SELECT * FROM Contest 
        WHERE contest_id = :cid
        """)
        parameters = {'cid': contest_id}
        result = db.session.execute(query, parameters)
        row = result.first()

        if row is None:
            return None
        contest = Contest(
            contest_id=row[0],
            title=row[1],
            description=row[2],
            start_time=row[3],
            end_time=row[4],
            created_by=row[5],
            created_at=row[6],
            winner=row[7]
        )
        return contest
    
    # Add new contest
    @staticmethod
    def create_contest(contest: Contest) -> Contest:
        query = text("""
            INSERT INTO contest (title, description, start_time, end_time, created_by)
            VALUES (:title, :description, :start_time, :end_time, :created_by)
            RETURNING contest_id, created_at
        """)
        result = db.session.execute(query, {
            'title': contest.title,
            'description': contest.description,
            'start_time': contest.start_time,
            'end_time': contest.end_time,
            'created_by': contest.created_by,
        })
        contest_id = result.fetchone()[0]
        created_at = result.fetchone()[1]
        
        db.session.commit()
        
        # Return the contest object with the assigned contest_id
        contest.contest_id = contest_id
        contest.created_at = created_at
        return contest
    
    # Delete contest by id
    @staticmethod
    def delete_contest(contest_id: int) -> None:
        query = text("""
        DELETE FROM Contest
        WHERE contest_id = :cid
        """)
        parameters = {'cid': contest_id}
        db.session.execute(query, parameters)
        db.session.commit()

    # Register user to contest
    @staticmethod
    def register_user_to_contest(contest_id: int, user_id: int) -> None:
        query = text("""
            INSERT INTO ContestParticipant (contest_id, participant_id)
            VALUES (:contest_id, :user_id)
        """)
        db.session.execute(query, {'contest_id': contest_id, 'user_id': user_id})
        db.session.commit()
    
    # Add problem to contest
    @staticmethod
    def add_problem_to_contest(contest_id: int, problem_id: int) -> None:
        query = text("""
            INSERT INTO ContestProblem (problem_id, contest_id)
            VALUES (:problem_id, :contest_id)
        """)
        db.session.execute(query, {'problem_id': problem_id, 'contest_id': contest_id})
        db.session.commit()

    # Get contest problems
    @staticmethod
    def get_contest_problems(contest_id: int) -> List[dict]:
        query = text("""
            SELECT cp.problem_id, p.title, p.description
            FROM ContestProblem cp
            JOIN Problem p ON cp.problem_id = p.problem_id
            WHERE cp.contest_id = :contest_id
        """)
        result = db.session.execute(query, {'contest_id': contest_id})
        problems = [
            {
                'problem_id': row['problem_id'],
                'title': row['title'],
                'description': row['description']
            } for row in result
        ]
        return problems
    
    # Get contest participants
    @staticmethod
    def get_contest_participants(contest_id: int) -> List[dict]:
        query = text("""
            SELECT u.user_id, u.username
            FROM ContestParticipant cp
            JOIN ServiceUser u ON cp.participant_id = u.user_id
            WHERE cp.contest_id = :contest_id
        """)
        result = db.session.execute(query, {'contest_id': contest_id})
        participants = [
            {
                'user_id': row['user_id'],
                'username': row['username']
            } for row in result
        ]
        return participants
    
    # Get contests the user is participating in
    @staticmethod
    def get_contests_participating(user_id: int) -> List[Contest]:
        query = text("""
            SELECT c.contest_id, c.title, c.description, c.start_time, c.end_time, c.created_by, c.created_at, c.winner
            FROM Contest c
            JOIN ContestParticipant cp ON c.contest_id = cp.contest_id
            WHERE cp.participant_id = :user_id AND c.start_time <= NOW() AND c.end_time >= NOW()
        """)
        result = db.session.execute(query, {'user_id': user_id})
        contests = [
            Contest(
                contest_id=row['contest_id'],
                title=row['title'],
                description=row['description'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                created_by=row['created_by'],
                created_at=row['created_at'],
                winner=row['winner']
            ) for row in result
        ]
        return contests

    # Submit contest problem
    @staticmethod
    def submit_contest_problem(participant_id: int, problem_id: int, submission: str) -> int:
        query = text("""
            INSERT INTO ContestProblemSubmission (participant_id, problem_id, submission)
            VALUES (:participant_id, :problem_id, :submission)
            RETURNING submission_id
        """)
        result = db.session.execute(query, {
            'participant_id': participant_id,
            'problem_id': problem_id,
            'submission': submission
        })
        submission_id = result.fetchone()[0]
        db.session.commit()
        return submission_id

    # Get contest within a time range
    @staticmethod
    def get_contests_within_date_range(start_date: str, end_date: str) -> List[Contest]:
        query = text("""
            SELECT * 
            FROM Contest
            WHERE start_time BETWEEN :start_date AND :end_date
            ORDER BY start_time
        """)
        result = db.session.execute(query, {'start_date': start_date, 'end_date': end_date})
        contests = [
            Contest(
                contest_id=row['contest_id'],
                title=row['title'],
                description=row['description'],
                start_time=row['start_time'],
                end_time=row['end_time'],
                created_by=row['created_by'],
                created_at=row['created_at'],
                winner=row['winner']
            ) for row in result
        ]
        return contests
    
    # Get users participating in a contest ranked by highest score and earliest submission time
    @staticmethod
    def get_contest_participants_ranked(contest_id: int, n: int) -> List[dict]:
        query = text("""
            WITH UserSubmissions AS (
                SELECT
                    cps.participant_id,
                    COUNT(DISTINCT cps.problem_id) AS score,
                    MAX(cps.created_at) AS last_submission
                FROM
                    ContestProblemSubmission cps
                JOIN ContestParticipant cp ON cps.participant_id = cp.participant_id
                JOIN ContestProblem pr ON cps.problem_id = pr.problem_id
                WHERE cp.contest_id = :contest_id AND pr.contest_id = :contest_id
                GROUP BY cps.participant_id
            )
            SELECT u.user_id, u.username, us.score, us.last_submission
            FROM UserSubmissions us
            JOIN ServiceUser u ON us.participant_id = u.user_id
            ORDER BY
                us.score DESC,
                us.last_submission ASC
            LIMIT :n;
        """)
        result = db.session.execute(query, {'contest_id': contest_id, 'n': n})
        users = [
            {
                'user_id': row['user_id'],
                'username': row['username'],
                'score': row['score'],
                'last_submission': row['last_submission']
            } for row in result
        ]
        return users
    
    # Get user's score and rank in a contest
    @staticmethod
    def get_user_score_and_rank(contest_id: int, user_id: int) -> Optional[dict]:
        query = text("""
            WITH RankedParticipants AS (
                SELECT
                    cps.participant_id,
                    COUNT(DISTINCT cps.problem_id) AS score,
                    MAX(cps.created_at) AS last_submission,
                    RANK() OVER (ORDER BY COUNT(DISTINCT cps.problem_id) DESC, MAX(cps.created_at) ASC) AS rank
                FROM
                    ContestProblemSubmission cps
                JOIN ContestParticipant cp ON cps.participant_id = cp.participant_id
                JOIN ContestProblem pr ON cps.problem_id = pr.problem_id
                WHERE cp.contest_id = :contest_id AND pr.contest_id = :contest_id
                GROUP BY cps.participant_id
            )
            SELECT rp.participant_id AS user_id, su.username, rp.score, rp.rank
            FROM RankedParticipants rp
            JOIN ServiceUser su ON rp.participant_id = su.user_id
            WHERE rp.participant_id = :user_id;
        """)
        
        result = db.session.execute(query, {'contest_id': contest_id, 'user_id': user_id})
        row = result.fetchone()
        if row:
            return {
                'user_id': row['user_id'],
                'username': row['username'],
                'score': row['score'],
                'rank': row['rank']
            }
        return None

    # Declare contest winner
    @staticmethod
    def declare_winner(contest_id: int) -> None:
        # Get the top scorer (limit to 1)
        top_scorer = ContestRepos.get_contest_participants_ranked(contest_id, n=1)
        
        if not top_scorer:
            raise ValueError("No participants found for this contest")
        
        winner_id = top_scorer[0]['user_id']
        
        update_query = text("""
            UPDATE Contest
            SET winner = :winner_id
            WHERE contest_id = :contest_id;
        """)
        
        db.session.execute(update_query, {'winner_id': winner_id, 'contest_id': contest_id})
        db.session.commit()
