from sqlalchemy.sql import text
from .. import db
from ..model.tag import Tag


class TagRepos:
    @staticmethod
    def get_tag_list() -> list[Tag]:
        query = text("""
        SELECT tag_id, type, content FROM Tag
        """)
        result = db.session.execute(query)
        tags = []
        for row in result:
            tags.append(Tag(
                tag_id=row[0],
                type=row[1],
                content=row[2],
            ))
        return tags

    @staticmethod
    def get_tag_by_id(tag_id: int) -> Tag:
        query = text("""
        SELECT tag_id, type, content FROM Tag
        WHERE tag_id = :tid
        """)
        parameters = {'tid': tag_id}
        result = db.session.execute(query, parameters)
        row = result.fetchone()
        if row:
            return Tag(
                tag_id=row[0],
                type=row[1],
                content=row[2],
            )
        return None

    @staticmethod
    def create_tag(tag: Tag) -> int:
        query = text("""
            INSERT INTO Tag (type, content)
            VALUES (:type, :content)
            RETURNING tag_id
        """)
        result = db.session.execute(query, {
            'type': tag.type,
            'content': tag.content,
        })
        tag_id = result.fetchone()[0]

        db.session.commit()
        return tag_id

    @staticmethod
    def delete_tag(tag_id: int) -> bool:
        query = text("""
            DELETE FROM Tag
            WHERE tag_id = :tid
        """)
        result = db.session.execute(query, {'tid': tag_id})
        db.session.commit()
        return result.rowcount > 0
