class Tag:
    def __init__(self, tag_id: int, type: str, content: str):
        self.tag_id = tag_id
        self.type = type
        self.content = content

    def to_dict(self) -> dict:
        return {
            'tag_id': self.tag_id,
            'type': self.type,
            'content': self.content
        }
