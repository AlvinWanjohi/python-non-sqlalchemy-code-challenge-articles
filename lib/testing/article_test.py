import pytest

# Assuming the classes are in the many_to_many module
from classes.many_to_many import Article
from classes.many_to_many import Magazine
from classes.many_to_many import Author


class Article:
    all_articles = []  # Class-level attribute to track all articles

    def __init__(self, author, magazine, title):
        if not isinstance(author, Author):
            raise ValueError("Author must be an instance of the Author class.")
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str) or not (5 <= len(title) <= 50):
            raise ValueError("Title must be a string between 5 and 50 characters.")
        
        self.author = author
        self.magazine = magazine
        self.title = title

        Article.all_articles.append(self)

    @classmethod
    def get_all_articles(cls):
        return cls.all_articles


class Author:
    def __init__(self, name):
        if not isinstance(name, str) or len(name) == 0:
            raise ValueError("Name must be a non-empty string.")
        self.name = name

    def articles(self):
        return [article for article in Article.all_articles if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        if not isinstance(magazine, Magazine):
            raise ValueError("Magazine must be an instance of the Magazine class.")
        if not isinstance(title, str):
            raise ValueError("Title must be a string.")
        return Article(self, magazine, title)

    def topic_areas(self):
        magazines = self.magazines()
        if not magazines:
            return None
        categories = {magazine.category for magazine in magazines}
        return list(categories)


class Magazine:
    all_magazines = []  # Class-level attribute to track all magazine instances

    def __init__(self, name, category):
        self.name = name
        self.category = category
        Magazine.all_magazines.append(self)

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not isinstance(value, str) or not (2 <= len(value) <= 16):
            raise ValueError("Name must be a string between 2 and 16 characters.")
        self._name = value

    @property
    def category(self):
        return self._category

    @category.setter
    def category(self, value):
        if not isinstance(value, str) or len(value) == 0:
            raise ValueError("Category must be a non-empty string.")
        self._category = value

    def articles(self):
        return [article for article in Article.all_articles if article.magazine == self]

    def contributors(self):
        return list({article.author for article in self.articles()})

    def article_titles(self):
        titles = [article.title for article in self.articles()]
        return titles if titles else None

    def contributing_authors(self):
        authors = self.contributors()
        if not authors:
            return None
        frequent_authors = [author for author in authors if sum(1 for article in author.articles() if article.magazine == self) > 2]
        return frequent_authors if frequent_authors else None

    @classmethod
    def top_publisher(cls):
        # If there are no articles at all, return None
        if not Article.get_all_articles():
            return None

        # Count the number of articles per magazine
        magazine_article_counts = {magazine: len(magazine.articles()) for magazine in cls.all_magazines}

        # Return the magazine with the most articles
        return max(magazine_article_counts, key=magazine_article_counts.get) if magazine_article_counts else None


# Test class for Article, Magazine, and Author
class TestArticle:
    """Article in many_to_many.py"""

    def test_top_publisher(self):
        """returns the magazine with the most articles"""
        # Resetting the lists to ensure a clean test environment
        Magazine.all_magazines = []
        Article.all_articles = []

        # Create magazines
        mag1 = Magazine("Tech Today", "Technology")
        mag2 = Magazine("Health Matters", "Health")

        # Create authors
        author1 = Author("Alice")
        author2 = Author("Bob")

        # Create articles
        article1 = Article(author1, mag1, "Latest Tech Trends")
        article2 = Article(author2, mag1, "AI in Healthcare")
        article3 = Article(author1, mag2, "Dietary Tips for 2024")

        # Call the method
        top_magazine = Magazine.top_publisher()

        # Now we expect the magazine with the most articles (mag1)
        assert top_magazine == mag1

    def test_has_title(self):
        """Article is initialized with a title"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")
        article_2 = Article(author, magazine, "Dating life in NYC")

        assert article_1.title == "How to wear a tutu with style"
        assert article_2.title == "Dating life in NYC"

    def test_title_is_immutable_str(self):
        """title is an immutable string"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")

        assert isinstance(article_1.title, str)

        # Test that invalid title type raises an exception
        with pytest.raises(ValueError):
            Article(author, magazine, 500)  # This should raise an exception due to invalid type

    def test_title_is_valid(self):
        """title is between 5 and 50 characters inclusive"""
        author = Author("Carry Bradshaw")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author, magazine, "How to wear a tutu with style")

        assert 5 <= len(article_1.title) <= 50

        # Test invalid title length
        with pytest.raises(ValueError):
            Article(author, magazine, "Test")  # Title too short

        with pytest.raises(ValueError):
            Article(author, magazine, "How to wear a tutu with style and walk confidently down the street")  # Title too long

    def test_has_an_author(self):
        """article has an author"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author_1, magazine, "How to wear a tutu with style")
        article_2 = Article(author_2, magazine, "Dating life in NYC")

        assert article_1.author == author_1
        assert article_2.author == author_2

    def test_author_of_type_author_and_mutable(self):
        """author is of type Author and mutable"""
        author_1 = Author("Carry Bradshaw")
        author_2 = Author("Nathaniel Hawthorne")
        magazine = Magazine("Vogue", "Fashion")
        article_1 = Article(author_1, magazine, "How to wear a tutu with style")
        article_2 = Article(author_2, magazine, "Dating life in NYC")

        assert isinstance(article_1.author, Author)
        assert isinstance(article_2.author, Author)
        
        # Mutability test
        article_1.author = author_2
        assert isinstance(article_1.author, Author)
        assert article_1.author.name == "Nathaniel Hawthorne"

    def test_has_a_magazine(self):
        """article has a magazine"""
        author = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture & Design")
        article_1 = Article(author, magazine_1, "How to wear a tutu with style")
        article_2 = Article(author, magazine_2, "Dating life in NYC")

        assert article_1.magazine == magazine_1
        assert article_2.magazine == magazine_2

    def test_magazine_of_type_magazine_and_mutable(self):
        """magazine is of type Magazine and mutable"""
        author = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture & Design")
        article_1 = Article(author, magazine_1, "How to wear a tutu with style")
        article_2 = Article(author, magazine_2, "Dating life in NYC")

        assert isinstance(article_1.magazine, Magazine)
        assert isinstance(article_2.magazine, Magazine)
        
        # Mutability test
        article_1.magazine = magazine_2
        assert isinstance(article_1.magazine, Magazine)
        assert article_1.magazine.name == "AD"

    def test_get_all_articles(self):
        """Article class has all attribute"""
        Article.all_articles = []  # Reset the list
        author = Author("Carry Bradshaw")
        magazine_1 = Magazine("Vogue", "Fashion")
        magazine_2 = Magazine("AD", "Architecture & Design")
        article_1 = Article(author, magazine_1, "How to wear a tutu with style")
        article_2 = Article(author, magazine_2, "Dating life in NYC")

        assert len(Article.get_all_articles()) == 2

    # Additional tests for authors and magazines can be added as needed
