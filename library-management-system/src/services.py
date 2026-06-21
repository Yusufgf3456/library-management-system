"""Business logic layer (Service layer).

Uses the repositories to enforce business rules: validation, the
borrow/return flow, pre-delete checks, etc. The core rules of the application
are gathered here; the CLI only calls this layer.
"""
import re
from datetime import date, timedelta
from typing import List

from .database import Database
from .models import Book, Member, Loan
from .repositories import BookRepository, MemberRepository, LoanRepository

EMAIL_REGEX = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


class LibraryError(Exception):
    """Raised when a business rule is violated."""


class LibraryService:
    """Service that manages all library operations."""

    LOAN_PERIOD_DAYS = 14  # Loan period (days)

    def __init__(self, db: Database):
        self.db = db
        self.books = BookRepository(db)
        self.members = MemberRepository(db)
        self.loans = LoanRepository(db)

    # ----- Book operations -----

    def add_book(self, title: str, author: str, isbn: str = None,
                 published_year: int = None, total_copies: int = 1) -> Book:
        if not title or not title.strip():
            raise LibraryError("Book title cannot be empty.")
        if not author or not author.strip():
            raise LibraryError("Author name cannot be empty.")
        if total_copies < 1:
            raise LibraryError("Number of copies must be at least 1.")
        book = Book(
            title=title.strip(), author=author.strip(), isbn=isbn,
            published_year=published_year,
            total_copies=total_copies, available_copies=total_copies,
        )
        return self.books.add(book)

    def list_books(self) -> List[Book]:
        return self.books.list_all()

    def search_books(self, keyword: str) -> List[Book]:
        return self.books.search(keyword)

    def update_book(self, book: Book) -> Book:
        if self.books.get(book.id) is None:
            raise LibraryError(f"Book with id {book.id} not found.")
        return self.books.update(book)

    def delete_book(self, book_id: int) -> None:
        if self.books.get(book_id) is None:
            raise LibraryError(f"Book with id {book_id} not found.")
        if self.loans.active_loans_for_book(book_id):
            raise LibraryError(
                "This book has active loans; it must be returned first."
            )
        self.books.delete(book_id)

    # ----- Member operations -----

    def add_member(self, name: str, email: str, phone: str = None) -> Member:
        if not name or not name.strip():
            raise LibraryError("Member name cannot be empty.")
        if not EMAIL_REGEX.match(email or ""):
            raise LibraryError("Please enter a valid email address.")
        if self.members.get_by_email(email):
            raise LibraryError("A member with this email already exists.")
        member = Member(name=name.strip(), email=email.strip(), phone=phone)
        return self.members.add(member)

    def list_members(self) -> List[Member]:
        return self.members.list_all()

    def update_member(self, member: Member) -> Member:
        if self.members.get(member.id) is None:
            raise LibraryError(f"Member with id {member.id} not found.")
        return self.members.update(member)

    def delete_member(self, member_id: int) -> None:
        if self.members.get(member_id) is None:
            raise LibraryError(f"Member with id {member_id} not found.")
        if self.loans.active_loans_for_member(member_id):
            raise LibraryError(
                "This member has unreturned books; they must be returned first."
            )
        self.members.delete(member_id)

    # ----- Borrow / return operations -----

    def borrow_book(self, book_id: int, member_id: int) -> Loan:
        book = self.books.get(book_id)
        if book is None:
            raise LibraryError(f"Book with id {book_id} not found.")
        member = self.members.get(member_id)
        if member is None:
            raise LibraryError(f"Member with id {member_id} not found.")
        if book.available_copies <= 0:
            raise LibraryError(f"No available copies for '{book.title}'.")

        due = (date.today() + timedelta(days=self.LOAN_PERIOD_DAYS)).isoformat()
        loan = Loan(book_id=book_id, member_id=member_id, due_date=due)
        saved_loan = self.loans.add(loan)

        # Decrease available copy count by one
        book.available_copies -= 1
        self.books.update(book)
        return saved_loan

    def return_book(self, loan_id: int) -> Loan:
        loan = self.loans.get(loan_id)
        if loan is None:
            raise LibraryError(f"Loan record with id {loan_id} not found.")
        if not loan.is_active:
            raise LibraryError("This book has already been returned.")

        self.loans.mark_returned(loan_id, date.today().isoformat())

        # Increase available copy count by one
        book = self.books.get(loan.book_id)
        if book:
            book.available_copies += 1
            self.books.update(book)
        return self.loans.get(loan_id)

    def list_active_loans(self) -> List[Loan]:
        return self.loans.list_active()

    def list_all_loans(self) -> List[Loan]:
        return self.loans.list_all()
