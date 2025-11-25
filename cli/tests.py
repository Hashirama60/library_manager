import unittest
from book import Book
from inventory import LibraryInventory
import tempfile
import os

class TestLibrarySystem(unittest.TestCase):
    def setUp(self):
        self.inventory = LibraryInventory()
        self.book1 = Book("1984", "George Orwell", "1234567890")
        self.book2 = Book("To Kill a Mockingbird", "Harper Lee", "0987654321")

    def test_book_creation(self):
        self.assertEqual(self.book1.title, "1984")
        self.assertTrue(self.book1.is_available())

    def test_book_issue_return(self):
        self.assertTrue(self.book1.issue())
        self.assertFalse(self.book1.is_available())
        self.assertTrue(self.book1.return_book())
        self.assertTrue(self.book1.is_available())

    def test_inventory_add_search(self):
        self.inventory.add_book(self.book1)
        self.inventory.add_book(self.book2)
        self.assertEqual(len(self.inventory.books), 2)
        result = self.inventory.search_by_isbn("1234567890")
        self.assertEqual(result.title, "1984")
        results = self.inventory.search_by_title("1984")
        self.assertEqual(len(results), 1)

    def test_duplicate_isbn(self):
        self.inventory.add_book(self.book1)
        with self.assertRaises(ValueError):
            self.inventory.add_book(Book("Duplicate", "Author", "1234567890"))

    def test_file_persistence(self):
        self.inventory.add_book(self.book1)
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json') as f:
            temp_file = f.name
        try:
            self.inventory.save_to_file(temp_file)
            new_inventory = LibraryInventory()
            new_inventory.load_from_file(temp_file)
            self.assertEqual(len(new_inventory.books), 1)
            self.assertEqual(new_inventory.books[0].title, "1984")
        finally:
            os.unlink(temp_file)

if __name__ == "__main__":
    unittest.main()