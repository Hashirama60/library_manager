import json
import logging
from pathlib import Path
from book import Book

logger = logging.getLogger(__name__)

class LibraryInventory:
    def __init__(self):
        self.books = []

    def add_book(self, book):
        # Check for duplicate ISBN
        if any(b.isbn == book.isbn for b in self.books):
            raise ValueError(f"Book with ISBN {book.isbn} already exists.")
        self.books.append(book)
        logger.info(f"Added book: {book.title}")

    def search_by_title(self, title):
        return [book for book in self.books if title.lower() in book.title.lower()]

    def search_by_isbn(self, isbn):
        for book in self.books:
            if book.isbn == isbn:
                return book
        return None

    def display_all(self):
        if not self.books:
            print("No books in inventory.")
        else:
            for book in self.books:
                print(book)

    def save_to_file(self, filename="books.json"):
        try:
            path = Path(filename)
            data = [book.to_dict() for book in self.books]
            with path.open('w') as f:
                json.dump(data, f, indent=4)
            logger.info(f"Inventory saved to {filename}")
        except Exception as e:
            logger.error(f"Error saving to file: {e}")
            raise

    def load_from_file(self, filename="books.json"):
        try:
            path = Path(filename)
            if not path.exists():
                logger.warning(f"File {filename} does not exist. Starting with empty inventory.")
                return
            with path.open('r') as f:
                data = json.load(f)
            self.books = [Book(**item) for item in data]
            logger.info(f"Inventory loaded from {filename}")
        except json.JSONDecodeError:
            logger.error(f"Corrupted JSON file: {filename}. Starting with empty inventory.")
            self.books = []
        except Exception as e:
            logger.error(f"Error loading from file: {e}")
            raise