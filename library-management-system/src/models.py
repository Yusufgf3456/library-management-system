"""Data models (domain objects).

Each table is represented by a dataclass. Dataclasses automatically generate
__init__, __repr__ and __eq__, which keeps the code concise.
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class Book:
    """Represents a book."""
    title: str
    author: str
    isbn: Optional[str] = None
    published_year: Optional[int] = None
    total_copies: int = 1
    available_copies: int = 1
    id: Optional[int] = None


@dataclass
class Member:
    """Represents a library member."""
    name: str
    email: str
    phone: Optional[str] = None
    joined_date: Optional[str] = None
    id: Optional[int] = None


@dataclass
class Loan:
    """Represents a loan record."""
    book_id: int
    member_id: int
    due_date: str
    loan_date: Optional[str] = None
    return_date: Optional[str] = None
    id: Optional[int] = None

    @property
    def is_active(self) -> bool:
        """Return True if the book has not been returned yet."""
        return self.return_date is None
