"""
This testing suite is used to test the R6 requirement:

The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display
"""

import pytest
import sys
import os
# sys.path.insert(1, "C:/Users/laure/OneDrive/Documents!/CISC 327/CISC327-CMPE327-F25")
from library_service import (
    search_books_in_catalog
)

def test_search_book_valid_title():
    """Test book valid title input (partial matching)."""
    success, message = search_books_in_catalog("the great gatsby","title")
    
    assert success == True
    assert "success" in message.lower()

def test_search_book_valid_author():
    """Test book valid author input (partial matching)."""
    success, message = search_books_in_catalog("george orwell","author")
    
    assert success == True
    assert "success" in message.lower()

def test_search_book_valid_isbn():
    """Test book valid isbn input (exact matching)."""
    success, message = search_books_in_catalog("9780743273565","isbn") # gatsby isbn
    
    assert success == True
    assert "success" in message.lower()

def test_search_book_invalid_title_not_in_db():
    """Test book not in database."""
    success, message = search_books_in_catalog("Six of Crows","title")
    
    assert success == False
    assert "book title must be in database" in message

def test_search_book_invalid_author_not_in_db():
    """Test book not in database."""
    success, message = search_books_in_catalog("Leigh Bardugo","author")
    
    assert success == False
    assert "book author must be in database" in message

def test_search_book_invalid_isbn_not_in_db():
    """Test book not in database."""
    success, message = search_books_in_catalog("5","isbn")
    
    assert success == False
    assert "book ISBN must be in database" in message

def test_search_book_invalid_search_type():
    """Test book not in database."""
    success, message = search_books_in_catalog("5","search type")
    
    assert success == False
    assert "search type must be 'author', 'title', or 'isbn'" in message

# if __name__ == "__main__":
#     test_search_book_valid_title()
#     test_search_book_valid_author()
#     test_search_book_valid_isbn()
#     test_search_book_invalid_title_not_in_db()
#     test_search_book_invalid_author_not_in_db()
#     test_search_book_invalid_isbn_not_in_db()
#     test_search_book_invalid_search_type()
#     # test_search_book_invalid_isbn_too_short()
#     # test_search_book_invalid_isbn_too_long()
#     # test_search_book_invalid_isbn_with_letters()
#     # test_search_book_invalid_negative_isbn()
#     # test_search_book_invalid_long_title()
#     # test_search_book_valid_200_title()
#     # test_search_book_invalid_no_title()
#     # test_search_book_invalid_no_author()
#     # test_search_book_valid_100_author()
#     # test_search_book_invalid_long_author()