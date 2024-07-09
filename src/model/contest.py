# Description: Model for contest
# Author: Vidhi Ruparel
class Contest:
    def __init__(self, contest_id: int, title: str, description: str, start_time: str, end_time: str, created_by: int, 
             created_at: str, winner: int = None):
        self.contest_id = contest_id
        self.title = title
        self.description = description
        self.start_time = start_time
        self.end_time = end_time
        self.created_by = created_by
        self.created_at = created_at
        self.winner = winner
    
    def to_dict(self) -> dict:
        return {
            'contest_id': self.contest_id,
            'title': self.title,
            'description': self.description,
            'start_time': self.start_time,
            'end_time': self.end_time,
            'created_by': self.created_by,
            'created_at': self.created_at,
            'winner': self.winner
        }