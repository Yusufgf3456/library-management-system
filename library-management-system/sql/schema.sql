-- Library Management System - Database Schema
-- Database engine: SQLite

PRAGMA foreign_keys = ON;

-- Books table
CREATE TABLE IF NOT EXISTS books (
    id               INTEGER PRIMARY KEY AUTOINCREMENT,
    title            TEXT    NOT NULL,
    author           TEXT    NOT NULL,
    isbn             TEXT    UNIQUE,
    published_year   INTEGER,
    total_copies     INTEGER NOT NULL DEFAULT 1 CHECK (total_copies >= 0),
    available_copies INTEGER NOT NULL DEFAULT 1 CHECK (available_copies >= 0)
);

-- Members table
CREATE TABLE IF NOT EXISTS members (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT    NOT NULL,
    email       TEXT    NOT NULL UNIQUE,
    phone       TEXT,
    joined_date TEXT    NOT NULL DEFAULT (date('now'))
);

-- Loans table
CREATE TABLE IF NOT EXISTS loans (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    book_id     INTEGER NOT NULL,
    member_id   INTEGER NOT NULL,
    loan_date   TEXT    NOT NULL DEFAULT (date('now')),
    due_date    TEXT    NOT NULL,
    return_date TEXT,
    FOREIGN KEY (book_id)   REFERENCES books(id)   ON DELETE RESTRICT,
    FOREIGN KEY (member_id) REFERENCES members(id) ON DELETE RESTRICT
);

-- Indexes for query performance
CREATE INDEX IF NOT EXISTS idx_loans_book   ON loans(book_id);
CREATE INDEX IF NOT EXISTS idx_loans_member ON loans(member_id);
CREATE INDEX IF NOT EXISTS idx_loans_active ON loans(return_date);
