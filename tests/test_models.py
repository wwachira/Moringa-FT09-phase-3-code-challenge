import unittest
from unittest.mock import MagicMock
from models.author import Author
from models.article import Article
from models.magazine import Magazine

# Define a test suite for the models
class TestModels(unittest.TestCase):
    def setUp(self):
        # Create a mock cursor for database operations
        self.cursor = MagicMock()

    def test_author_creation(self):
        # Creates Author object
        author = Author(1, "John Doe")
        # Check if the author's name matches the expected value
        self.assertEqual(author.name, "John Doe")

    def test_article_creation(self):
        # Creates Article object
        article = Article(1, "Test Title", "Test Content", 1, 1)
        # Check if the article's title matches the expected value
        self.assertEqual(article.title, "Test Title")

    def test_magazine_creation(self):
        # Creates Magazine object
        magazine = Magazine(1, "Tech Weekly", "Technology")
        # Check if the magazine's name matches the expected value
        self.assertEqual(magazine.name, "Tech Weekly")

    def test_create_author(self):
        # Creates Author object
        author = Author(None, "John Doe")
        # Call the create_author method on the author object
        author.create_author(self.cursor)
        # Check if the cursor's execute method was called with the correct SQL query and parameters
        self.cursor.execute.assert_called_once_with("INSERT INTO authors (name) VALUES (?)", ("John Doe",))

# Run the test suite
if __name__ == "__main__":
    unittest.main()