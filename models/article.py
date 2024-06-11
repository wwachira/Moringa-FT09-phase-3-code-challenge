from database.connection import get_db_connection
from models.author import Author
from models.magazine import Magazine

class Article:
    def __init__(self, id, title, content, author_id, magazine_id):
        self._id = id
        self.title = title
        self.content = content
        self._author_id = author_id
        self._magazine_id = magazine_id

    @property
    def id(self):
        return self._id

    @property
    def author_id(self):
        return self._author_id

    @property
    def magazine_id(self):
        return self._magazine_id

    @property
    def author(self):
        if self._author_id is None:
            return None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors WHERE id = ?', (self.author_id,))
        author = cursor.fetchone()
        conn.close()

        if author:
            return Author(author['id'], author['name'])
        else:
            return None

    @property
    def magazine(self):
        if self._magazine_id is None:
            return None

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines WHERE id = ?', (self.magazine_id,))
        magazine = cursor.fetchone()
        conn.close()

        if magazine:
            return Magazine(magazine['id'], magazine['name'], magazine['category'])
        else:
            return None

    def __repr__(self):
        return f'<Article {self.title}>'
