"""Unit tests for LibraryService (unittest).

Each test uses a fresh in-memory (:memory:) database so that tests do not
affect one another and nothing is written to disk.

To run, from the project root:
    python -m unittest discover -s tests -v
"""
import unittest
from datetime import date, timedelta

from src.database import Database
from src.services import LibraryService, LibraryError


class BaseTest(unittest.TestCase):
    def setUp(self):
        self.db = Database(":memory:")
        self.service = LibraryService(self.db)

    def tearDown(self):
        self.db.close()


class TestBookCRUD(BaseTest):
    def test_add_and_get_book(self):
        book = self.service.add_book("Test Book", "Author A", total_copies=2)
        self.assertIsNotNone(book.id)
        fetched = self.service.books.get(book.id)
        self.assertEqual(fetched.title, "Test Book")
        self.assertEqual(fetched.available_copies, 2)

    def test_add_book_empty_title_raises(self):
        with self.assertRaises(LibraryError):
            self.service.add_book("   ", "Author")

    def test_list_and_search(self):
        self.service.add_book("Python Basics", "A. Author")
        self.service.add_book("Java Basics", "B. Author")
        self.assertEqual(len(self.service.list_books()), 2)
        results = self.service.search_books("python")
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].title, "Python Basics")

    def test_update_book(self):
        book = self.service.add_book("Old Title", "Author")
        book.title = "New Title"
        self.service.update_book(book)
        self.assertEqual(self.service.books.get(book.id).title, "New Title")

    def test_delete_book(self):
        book = self.service.add_book("To Be Deleted", "Author")
        self.service.delete_book(book.id)
        self.assertIsNone(self.service.books.get(book.id))


class TestMemberCRUD(BaseTest):
    def test_add_member(self):
        m = self.service.add_member("Ali Veli", "ali@example.com")
        self.assertIsNotNone(m.id)
        self.assertIsNotNone(m.joined_date)  # auto-assigned by the database

    def test_invalid_email_raises(self):
        with self.assertRaises(LibraryError):
            self.service.add_member("Ali", "invalid-email")

    def test_duplicate_email_raises(self):
        self.service.add_member("Ali", "same@example.com")
        with self.assertRaises(LibraryError):
            self.service.add_member("Veli", "same@example.com")


class TestLoanFlow(BaseTest):
    def setUp(self):
        super().setUp()
        self.book = self.service.add_book("Loanable Book", "Author", total_copies=1)
        self.member = self.service.add_member("Member One", "member@example.com")

    def test_borrow_decrements_available(self):
        self.service.borrow_book(self.book.id, self.member.id)
        updated = self.service.books.get(self.book.id)
        self.assertEqual(updated.available_copies, 0)

    def test_borrow_when_unavailable_raises(self):
        self.service.borrow_book(self.book.id, self.member.id)  # only copy taken
        with self.assertRaises(LibraryError):
            self.service.borrow_book(self.book.id, self.member.id)

    def test_return_increments_available(self):
        loan = self.service.borrow_book(self.book.id, self.member.id)
        self.service.return_book(loan.id)
        updated = self.service.books.get(self.book.id)
        self.assertEqual(updated.available_copies, 1)

    def test_double_return_raises(self):
        loan = self.service.borrow_book(self.book.id, self.member.id)
        self.service.return_book(loan.id)
        with self.assertRaises(LibraryError):
            self.service.return_book(loan.id)

    def test_due_date_is_two_weeks(self):
        loan = self.service.borrow_book(self.book.id, self.member.id)
        expected = (date.today() + timedelta(days=14)).isoformat()
        self.assertEqual(loan.due_date, expected)

    def test_cannot_delete_book_with_active_loan(self):
        self.service.borrow_book(self.book.id, self.member.id)
        with self.assertRaises(LibraryError):
            self.service.delete_book(self.book.id)

    def test_cannot_delete_member_with_active_loan(self):
        self.service.borrow_book(self.book.id, self.member.id)
        with self.assertRaises(LibraryError):
            self.service.delete_member(self.member.id)

    def test_active_loans_listing(self):
        loan = self.service.borrow_book(self.book.id, self.member.id)
        self.assertEqual(len(self.service.list_active_loans()), 1)
        self.service.return_book(loan.id)
        self.assertEqual(len(self.service.list_active_loans()), 0)


if __name__ == "__main__":
    unittest.main()
