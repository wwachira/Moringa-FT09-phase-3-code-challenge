# author.py

from database.connection import get_db_connection

class Author:
    def __init__(self, id, name):
        self._id = id
        self.name = name

    @classmethod
    def fetch_all(cls):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM authors')
        authors = cursor.fetchall()
        conn.close()
        return [cls(author['id'], author['name']) for author in authors]

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO authors (name) VALUES (?)', (self.name,))
        self._id = cursor.lastrowid
        conn.commit()
        conn.close()

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value

    def articles(self):
        from models.article import Article  # Import inside method to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE author_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"]) for article in articles]

    def magazines(self):
        from models.magazine import Magazine  # Import inside method to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT m.* FROM magazines m
            JOIN articles a ON m.id = a.magazine_id
            WHERE a.author_id = ?
        ''', (self.id,))
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine["name"], magazine["category"]) for magazine in magazines]

    def __repr__(self):
        return f'<Author {self.name}>'
