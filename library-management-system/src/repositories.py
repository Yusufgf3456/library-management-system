"""Data access layer (Repository pattern).

Each repository performs CRUD (Create/Read/Update/Delete) operations for one
table using SQL queries. Business rules live in services.py, NOT here; this
layer is responsible only for database access. This separation keeps the code
modular.
"""
from typing import List, Optional

from .models import Book, Member, Loan


class BookRepository:
    """CRUD operations for the books table."""

    def __init__(self, db):
        self.conn = db.conn

    def add(self, book: Book) -> Book:
        cur = self.conn.execute(
            """INSERT INTO books
               (title, author, isbn, published_year, total_copies, available_copies)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (book.title, book.author, book.isbn, book.published_year,
             book.total_copies, book.available_copies),
        )
        self.conn.commit()
        book.id = cur.lastrowid
        return book

    def get(self, book_id: int) -> Optional[Book]:
        row = self.conn.execute(
            "SELECT * FROM books WHERE id = ?", (book_id,)
        ).fetchone()
        return self._row_to_book(row) if row else None

    def list_all(self) -> List[Book]:
        rows = self.conn.execute("SELECT * FROM books ORDER BY id").fetchall()
        return [self._row_to_book(r) for r in rows]

    def search(self, keyword: str) -> List[Book]:
        like = f"%{keyword}%"
        rows = self.conn.execute(
            "SELECT * FROM books WHERE title LIKE ? OR author LIKE ? ORDER BY id",
            (like, like),
        ).fetchall()
        return [self._row_to_book(r) for r in rows]

    def update(self, book: Book) -> Book:
        self.conn.execute(
            """UPDATE books
               SET title = ?, author = ?, isbn = ?, published_year = ?,
                   total_copies = ?, available_copies = ?
               WHERE id = ?""",
            (book.title, book.author, book.isbn, book.published_year,
             book.total_copies, book.available_copies, book.id),
        )
        self.conn.commit()
        return book

    def delete(self, book_id: int) -> None:
        self.conn.execute("DELETE FROM books WHERE id = ?", (book_id,))
        self.conn.commit()

    @staticmethod
    def _row_to_book(row) -> Book:
        return Book(
            id=row["id"], title=row["title"], author=row["author"],
            isbn=row["isbn"], published_year=row["published_year"],
            total_copies=row["total_copies"],
            available_copies=row["available_copies"],
        )


class MemberRepository:
    """CRUD operations for the members table."""

    def __init__(self, db):
        self.conn = db.conn

    def add(self, member: Member) -> Member:
        cur = self.conn.execute(
            "INSERT INTO members (name, email, phone) VALUES (?, ?, ?)",
            (member.name, member.email, member.phone),
        )
        self.conn.commit()
        member.id = cur.lastrowid
        # joined_date is assigned automatically by the database; read it back
        saved = self.get(member.id)
        return saved if saved else member

    def get(self, member_id: int) -> Optional[Member]:
        row = self.conn.execute(
            "SELECT * FROM members WHERE id = ?", (member_id,)
        ).fetchone()
        return self._row_to_member(row) if row else None

    def get_by_email(self, email: str) -> Optional[Member]:
        row = self.conn.execute(
            "SELECT * FROM members WHERE email = ?", (email,)
        ).fetchone()
        return self._row_to_member(row) if row else None

    def list_all(self) -> List[Member]:
        rows = self.conn.execute("SELECT * FROM members ORDER BY id").fetchall()
        return [self._row_to_member(r) for r in rows]

    def update(self, member: Member) -> Member:
        self.conn.execute(
            "UPDATE members SET name = ?, email = ?, phone = ? WHERE id = ?",
            (member.name, member.email, member.phone, member.id),
        )
        self.conn.commit()
        return member

    def delete(self, member_id: int) -> None:
        self.conn.execute("DELETE FROM members WHERE id = ?", (member_id,))
        self.conn.commit()

    @staticmethod
    def _row_to_member(row) -> Member:
        return Member(
            id=row["id"], name=row["name"], email=row["email"],
            phone=row["phone"], joined_date=row["joined_date"],
        )


class LoanRepository:
    """CRUD operations for the loans table."""

    def __init__(self, db):
        self.conn = db.conn

    def add(self, loan: Loan) -> Loan:
        cur = self.conn.execute(
            "INSERT INTO loans (book_id, member_id, due_date) VALUES (?, ?, ?)",
            (loan.book_id, loan.member_id, loan.due_date),
        )
        self.conn.commit()
        loan.id = cur.lastrowid
        saved = self.get(loan.id)
        return saved if saved else loan

    def get(self, loan_id: int) -> Optional[Loan]:
        row = self.conn.execute(
            "SELECT * FROM loans WHERE id = ?", (loan_id,)
        ).fetchone()
        return self._row_to_loan(row) if row else None

    def list_all(self) -> List[Loan]:
        rows = self.conn.execute("SELECT * FROM loans ORDER BY id").fetchall()
        return [self._row_to_loan(r) for r in rows]

    def list_active(self) -> List[Loan]:
        """Loan records that have not been returned (active)."""
        rows = self.conn.execute(
            "SELECT * FROM loans WHERE return_date IS NULL ORDER BY id"
        ).fetchall()
        return [self._row_to_loan(r) for r in rows]

    def active_loans_for_book(self, book_id: int) -> List[Loan]:
        rows = self.conn.execute(
            "SELECT * FROM loans WHERE book_id = ? AND return_date IS NULL",
            (book_id,),
        ).fetchall()
        return [self._row_to_loan(r) for r in rows]

    def active_loans_for_member(self, member_id: int) -> List[Loan]:
        rows = self.conn.execute(
            "SELECT * FROM loans WHERE member_id = ? AND return_date IS NULL",
            (member_id,),
        ).fetchall()
        return [self._row_to_loan(r) for r in rows]

    def mark_returned(self, loan_id: int, return_date: str) -> None:
        self.conn.execute(
            "UPDATE loans SET return_date = ? WHERE id = ?",
            (return_date, loan_id),
        )
        self.conn.commit()

    @staticmethod
    def _row_to_loan(row) -> Loan:
        return Loan(
            id=row["id"], book_id=row["book_id"], member_id=row["member_id"],
            loan_date=row["loan_date"], due_date=row["due_date"],
            return_date=row["return_date"],
        )
