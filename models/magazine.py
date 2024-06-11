from database.connection import get_db_connection

class Magazine:
    def __init__(self, name, category):
        self._id = None
        self.name = name
        self.category = category
        self.save()

    def save(self):
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('INSERT INTO magazines (name, category) VALUES (?, ?)', (self.name, self.category))
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
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string")
        self._category = value

    @staticmethod
    def fetch_all():
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM magazines')
        magazines = cursor.fetchall()
        conn.close()
        return [Magazine(magazine['name'], magazine['category']) for magazine in magazines]

    def articles(self):
        from models.article import Article  # Import inside method to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT * FROM articles
            WHERE magazine_id = ?
        ''', (self.id,))
        articles = cursor.fetchall()
        conn.close()
        return [Article(article["id"], article["title"], article["content"]) for article in articles]

    def contributors(self):
        from models.author import Author  # Import inside method to avoid circular import
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            SELECT DISTINCT a.* FROM authors a
            JOIN articles ar ON a.id = ar.author_id
            WHERE ar.magazine_id = ?
        ''', (self.id,))
        authors = cursor.fetchall()
        conn.close()
        return [Author(author["name"]) for author in authors]

    def __repr__(self):
        return f'<Magazine {self.name}>'
