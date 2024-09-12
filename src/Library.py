from src.Book import Book
from src.User import User
from typing import List, Tuple, Optional

class Library:
    def __init__(self) -> None:
        self.__books: List[Book] = []
        self.__users: List[User] = []
        self.__checked_out_books: List[Tuple[Book, User, str]] = []
        self.__checked_in_books: List[Tuple[Book, User, str]] = []

    # Getters
    def get_books(self) -> List[Book]:
        return self.__books

    def get_users(self) -> List[User]:
        return self.__users

    def get_checked_out_books(self) -> List[Tuple[Book, User, str]]:
        return self.__checked_out_books

    def get_checked_in_books(self) -> List[Tuple[Book, User, str]]:
        return self.__checked_in_books

    def add_book(self, isbn: str, title: str, author: str) -> None:
        """Add a book to the library."""
        new_book = Book(isbn, title, author)
        self.__books.append(new_book)

    def list_all_books(self) -> None:
        """List all books in the library."""
        for book in self.__books:
            print(f"ISBN: {book.get_isbn()}, Title: {book.get_title()}, Author: {book.get_author()}")

    def check_out_book(self, isbn: str, dni: int, due_date: str) -> str:
        book = next((b for b in self.__books if b.get_isbn() == isbn and b.is_available()), None)
        if book is None:
            return f"Book {isbn} is not available"

        user = next((u for u in self.__users if u.get_dni() == dni), None)
        if user is None:
            return f"User {dni} not found"

        book.set_available(False)
        self.__checked_out_books.append((book, user, due_date))
        user.increment_checkouts()
        return f"User {dni} checked out book {isbn}"

    def check_in_book(self, isbn: str, dni: int, returned_date: str) -> str:
        for record in self.__checked_out_books:
            book, user, _ = record
            if book.get_isbn() == isbn and user.get_dni() == dni:
                book.set_available(True)
                self.__checked_out_books.remove(record)
                self.__checked_in_books.append((book, user, returned_date))
                user.increment_checkins()
                return f"Book {isbn} checked in by user {dni}"

        return f"Book {isbn} was not checked out by user {dni}"

    def add_user(self, dni: int, name: str) -> None:
        new_user = User(dni, name)
        self.__users.append(new_user)
