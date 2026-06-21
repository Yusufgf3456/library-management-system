"""Command-line interface (CLI).

Menu-driven; lets the user perform book/member/loan operations. All actions
are executed through the LibraryService.
"""
from .services import LibraryService, LibraryError


def _input(prompt: str) -> str:
    return input(prompt).strip()


def _input_optional_int(prompt: str):
    raw = _input(prompt)
    if raw == "":
        return None
    try:
        return int(raw)
    except ValueError:
        print("  ! Not a numeric value, left empty.")
        return None


class LibraryCLI:
    """Menu-driven user interface."""

    def __init__(self, service: LibraryService):
        self.service = service

    def run(self) -> None:
        print("=" * 50)
        print("   LIBRARY MANAGEMENT SYSTEM")
        print("=" * 50)
        while True:
            self._print_menu()
            choice = _input("Your choice: ")
            if choice == "0":
                print("Exiting. Goodbye!")
                break
            self._handle(choice)

    def _print_menu(self) -> None:
        print(
            "\n--- MAIN MENU ---\n"
            " 1) Add book\n"
            " 2) List books\n"
            " 3) Search books\n"
            " 4) Update book\n"
            " 5) Delete book\n"
            " 6) Add member\n"
            " 7) List members\n"
            " 8) Delete member\n"
            " 9) Borrow book\n"
            "10) Return book\n"
            "11) Active loans\n"
            "12) All loan records\n"
            " 0) Exit"
        )

    def _handle(self, choice: str) -> None:
        actions = {
            "1": self._add_book,
            "2": self._list_books,
            "3": self._search_books,
            "4": self._update_book,
            "5": self._delete_book,
            "6": self._add_member,
            "7": self._list_members,
            "8": self._delete_member,
            "9": self._borrow,
            "10": self._return,
            "11": self._list_active_loans,
            "12": self._list_all_loans,
        }
        action = actions.get(choice)
        if action is None:
            print("  ! Invalid choice.")
            return
        try:
            action()
        except LibraryError as e:
            print(f"  ! Error: {e}")
        except Exception as e:  # unexpected errors (e.g. duplicate email)
            print(f"  ! Unexpected error: {e}")

    # ----- Book menu -----

    def _add_book(self) -> None:
        title = _input("Title: ")
        author = _input("Author: ")
        isbn = _input("ISBN (optional): ") or None
        year = _input_optional_int("Published year (optional): ")
        copies = _input_optional_int("Number of copies [1]: ") or 1
        book = self.service.add_book(title, author, isbn, year, copies)
        print(f"  + Book added (id={book.id}).")

    def _list_books(self) -> None:
        books = self.service.list_books()
        if not books:
            print("  No books on record.")
            return
        print(f"  {'id':<4}{'Title':<28}{'Author':<22}{'Available/Total'}")
        for b in books:
            print(f"  {b.id:<4}{b.title[:27]:<28}{b.author[:21]:<22}"
                  f"{b.available_copies}/{b.total_copies}")

    def _search_books(self) -> None:
        kw = _input("Keyword to search: ")
        books = self.service.search_books(kw)
        if not books:
            print("  No results found.")
            return
        for b in books:
            print(f"  [{b.id}] {b.title} - {b.author} "
                  f"({b.available_copies}/{b.total_copies})")

    def _update_book(self) -> None:
        book_id = _input_optional_int("Book id to update: ")
        book = self.service.books.get(book_id) if book_id else None
        if book is None:
            print("  ! Book not found.")
            return
        print("  (Leave a field empty to keep it unchanged.)")
        new_title = _input(f"Title [{book.title}]: ") or book.title
        new_author = _input(f"Author [{book.author}]: ") or book.author
        new_total = _input_optional_int(f"Total copies [{book.total_copies}]: ")
        book.title = new_title
        book.author = new_author
        if new_total is not None:
            # If total changes, adjust available count proportionally
            diff = new_total - book.total_copies
            book.total_copies = new_total
            book.available_copies = max(0, book.available_copies + diff)
        self.service.update_book(book)
        print("  + Book updated.")

    def _delete_book(self) -> None:
        book_id = _input_optional_int("Book id to delete: ")
        if book_id is None:
            print("  ! Invalid id.")
            return
        self.service.delete_book(book_id)
        print("  + Book deleted.")

    # ----- Member menu -----

    def _add_member(self) -> None:
        name = _input("Full name: ")
        email = _input("Email: ")
        phone = _input("Phone (optional): ") or None
        member = self.service.add_member(name, email, phone)
        print(f"  + Member added (id={member.id}).")

    def _list_members(self) -> None:
        members = self.service.list_members()
        if not members:
            print("  No members on record.")
            return
        print(f"  {'id':<4}{'Full name':<24}{'Email':<30}{'Joined'}")
        for m in members:
            print(f"  {m.id:<4}{m.name[:23]:<24}{m.email[:29]:<30}{m.joined_date}")

    def _delete_member(self) -> None:
        member_id = _input_optional_int("Member id to delete: ")
        if member_id is None:
            print("  ! Invalid id.")
            return
        self.service.delete_member(member_id)
        print("  + Member deleted.")

    # ----- Loan menu -----

    def _borrow(self) -> None:
        book_id = _input_optional_int("Book id: ")
        member_id = _input_optional_int("Member id: ")
        if book_id is None or member_id is None:
            print("  ! Book id and member id are required.")
            return
        loan = self.service.borrow_book(book_id, member_id)
        print(f"  + Book borrowed (loan id={loan.id}, "
              f"due: {loan.due_date}).")

    def _return(self) -> None:
        loan_id = _input_optional_int("Loan record id: ")
        if loan_id is None:
            print("  ! Invalid id.")
            return
        loan = self.service.return_book(loan_id)
        print(f"  + Book returned (return date: {loan.return_date}).")

    def _list_active_loans(self) -> None:
        loans = self.service.list_active_loans()
        if not loans:
            print("  No active loans.")
            return
        for ln in loans:
            print(f"  [{ln.id}] book={ln.book_id} member={ln.member_id} "
                  f"borrowed={ln.loan_date} due={ln.due_date}")

    def _list_all_loans(self) -> None:
        loans = self.service.list_all_loans()
        if not loans:
            print("  No loan records.")
            return
        for ln in loans:
            status = "returned" if ln.return_date else "ACTIVE"
            print(f"  [{ln.id}] book={ln.book_id} member={ln.member_id} "
                  f"borrowed={ln.loan_date} status={status}")
