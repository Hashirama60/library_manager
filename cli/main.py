import logging
from inventory import LibraryInventory
from book import Book

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    inventory = LibraryInventory()
    inventory.load_from_file()  # Load on startup

    while True:
        print("\nLibrary Management System")
        print("1. Add Book")
        print("2. Issue Book")
        print("3. Return Book")
        print("4. View All Books")
        print("5. Search Book")
        print("6. Exit")

        try:
            choice = input("Enter your choice (1-6): ").strip()
            if choice == "1":
                title = input("Enter title: ").strip()
                author = input("Enter author: ").strip()
                isbn = input("Enter ISBN: ").strip()
                if not title or not author or not isbn:
                    print("All fields are required.")
                    continue
                book = Book(title, author, isbn)
                inventory.add_book(book)
                print("Book added successfully.")
            elif choice == "2":
                isbn = input("Enter ISBN to issue: ").strip()
                book = inventory.search_by_isbn(isbn)
                if book and book.issue():
                    print("Book issued successfully.")
                else:
                    print("Book not found or already issued.")
            elif choice == "3":
                isbn = input("Enter ISBN to return: ").strip()
                book = inventory.search_by_isbn(isbn)
                if book and book.return_book():
                    print("Book returned successfully.")
                else:
                    print("Book not found or not issued.")
            elif choice == "4":
                inventory.display_all()
            elif choice == "5":
                search_type = input("Search by (1) Title or (2) ISBN: ").strip()
                if search_type == "1":
                    title = input("Enter title: ").strip()
                    results = inventory.search_by_title(title)
                    if results:
                        for book in results:
                            print(book)
                    else:
                        print("No books found.")
                elif search_type == "2":
                    isbn = input("Enter ISBN: ").strip()
                    book = inventory.search_by_isbn(isbn)
                    if book:
                        print(book)
                    else:
                        print("Book not found.")
                else:
                    print("Invalid choice.")
            elif choice == "6":
                inventory.save_to_file()  # Save on exit
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please enter 1-6.")
        except ValueError as e:
            print(f"Error: {e}")
        except Exception as e:
            logging.error(f"Unexpected error: {e}")
            print("An unexpected error occurred. Please try again.")

if __name__ == "__main__":
    main()