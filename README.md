Library Management System

A small command-line (CLI) library app I built with Python and SQLite. It
basically does all the usual CRUD stuff — create / list / update / delete — for
books, members and loan records.


OSTIM Technical University — WAP 228 Workplace Practice, Project 1.
Stack: Python + SQL (SQLite) + GitHub.



I tried to keep things simple and readable instead of over-engineering it, since
the whole point was to practice the basics properly.

What it does


Books: add, list, search by title/author, update, delete
Members: add (with email check), list, delete
Loans: borrow a book and return it later


And there are a few business rules baked in so the data doesn't get messy:


You can't borrow a book if there are no available copies left
Available copies go down when you borrow and go back up when you return
Loan period is always 14 days — the due date gets calculated automaticaly
A book or member that has an active loan can't be deleted
Two members can't be registered with the same email adress


I also wrote 16 unit tests (with unittest) to make sure none of these rules
quietly break later. No external dependencies either — just the Python standard
library.

Project structure

library-management-system/
├── main.py                 # Entry point
├── requirements.txt        # No external deps, but kept it anyway
├── README.md
├── .gitignore
├── sql/
│   ├── schema.sql          # Tables (books, members, loans)
│   └── seed_data.sql       # Sample data
├── src/
│   ├── __init__.py
│   ├── database.py         # SQLite connection + schema setup
│   ├── models.py           # Data models (Book, Member, Loan)
│   ├── repositories.py     # Data access layer (the SQL queries)
│   ├── services.py         # Business logic (rules + validation)
│   └── cli.py              # The menu you actually see
└── tests/
    ├── __init__.py
    └── test_library.py     # Unit tests

About the layers

I seperated the code into three layers so each part has one job and nothing gets
tangled together:


Repository layer (repositories.py) — only talks to the database, runs SQL.
Service layer (services.py) — holds the business rules and validation.
CLI layer (cli.py) — handles the user and just calls the service.


The nice thing is that if I ever wanted to swap the CLI for a web interface, the
service and repository layers wouldn't really need to change.

Setup & running

You only need Python 3.8+, nothing to install.

bash# Clone the repo
git clone <YOUR_REPO_LINK>
cd library-management-system

# Run it
python main.py

# First time and want some sample data to play with?
python main.py --seed

When you run it, a SQLite file called library.db gets created and your data
lives there, so it sticks around between runs.

Tests

bashpython -m unittest discover -s tests -v

The tests run on a temporary in-memory (:memory:) database, so they never
touch your real library.db. You can run them as many times as you want without
messing anything up.

Database schema

TableWhat's in itbooksBook info and copy countsmembersMember infoloansLoan records (which book, which member, dates)

The loans table is connected to books and members with foreign keys, so a
book or member that still has a loan can't accidentaly get deleted.

Quick example

--- MAIN MENU ---
 1) Add book
 2) List books
 9) Borrow book
10) Return book
...
Your choice: 9
Book id: 1
Member id: 1
  + Book borrowed (loan id=1, due: 2026-07-02).

That's pretty much it. Feel free to poke around the code — I left a few comments
in the trickier spots.