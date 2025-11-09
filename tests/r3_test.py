"""
This testing suite is used to test the R3 requirement:

The system shall provide a borrowing interface to borrow books by patron ID:

- Accepts patron ID and book ID as the form parameters
- Validates patron ID (6-digit format)
- Checks book availability and patron borrowing limits (max 5 books)
- Creates borrowing record and updates available copies
- Displays appropriate success/error messages
"""

import pytest
from services import library_service 

def test_borrow_book_valid_input():
    """Test borrowing a book with valid input."""
    # great gatsby ISBN
    success, message = library_service.borrow_book_by_patron("123456", "9780743273565")
    
    assert success == True
    assert "successfully added" in message.lower()

def test_borrow_book_invalid_isbn_too_long():
    """Test borrowing a book with too long ISBN."""
    success, message = library_service.borrow_book_by_patron("123456", "12345678901234")
    
    assert success == False
    assert "13 digits" in message

def test_borrow_book_invalid_isbn_too_short():
    """Test borrowing a book with too short ISBN."""
    success, message = library_service.borrow_book_by_patron("123456", "123456789012")
    
    assert success == False
    assert "13 digits" in message

def test_borrow_book_invalid_isbn_with_letters():
    """Test borrowing a book with letters in ISBN."""
    success, message = library_service.borrow_book_by_patron("123456", "1234567890OMG")
    
    assert success == False
    assert "13 digits" in message

def test_borrow_book_invalid_negative_isbn():
    """Test borrowing a book with negative ISBN."""
    success, message = library_service.borrow_book_by_patron("123456", "-123456789012")
    
    assert success == False
    assert "13 digits and positive" in message

def test_borrow_book_invalid_isbn_not_in_db():
    """Test borrowing a book with ISBN not in database."""
    success, message = library_service.borrow_book_by_patron("123456", "1234567890123")
    
    assert success == False
    assert "ISBN must be in database" in message

def test_borrow_book_invalid_patron_too_long():
    """Test borrowing a book with too long patron ID."""
    success, message = library_service.borrow_book_by_patron("1234567", "9780743273565")
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_patron_too_short():
    """Test borrowing a book with too short patron ID."""
    success, message = library_service.borrow_book_by_patron("12345", "9780743273565")
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_patron_with_letters():
    """Test borrowing a book with letters in patron ID."""
    success, message = library_service.borrow_book_by_patron("12345X", "9780743273565")
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_negative_patron():
    """Test borrowing a book with negative ISBN."""
    success, message = library_service.borrow_book_by_patron("-12345", "9780743273565")
    
    assert success == False
    assert "6 digits and positive" in message

def test_borrow_book_invalid_borrow_limit():
    """Test borrowing a book with borrow limit of 5 reached."""
    for i in range(5):
        success, message = library_service.borrow_book_by_patron("123456", "9780743273565")
    success, message = library_service.borrow_book_by_patron("123456", "9780743273565")
    
    assert success == False
    assert "borrow limit reached" in message

def test_borrow_book_invalid_no_copies():
    """Test borrowing a book with no copies."""
    # 1984 ISBN
    success, message = library_service.borrow_book_by_patron("123123", "9780451524935 ")
    
    assert success == False
    assert "borrow limit reached" in message

def test_borrow_book_invalid_duplicate():
    """Test borrowing another copy of the same book already borrowed."""
    # 1984 ISBN
    success, message = library_service.borrow_book_by_patron("123456", "9780451524935")
    
    assert success == False
    assert "already borrowed" in message

# if __name__ == "__main__":
#     test_borrow_book_valid_input()
#     test_borrow_book_invalid_isbn_too_long()
#     test_borrow_book_invalid_isbn_too_short()
#     test_borrow_book_invalid_isbn_with_letters()
#     test_borrow_book_invalid_negative_isbn()
#     test_borrow_book_invalid_isbn_not_in_db()
#     test_borrow_book_invalid_patron_too_long()
#     test_borrow_book_invalid_patron_too_short()
#     test_borrow_book_invalid_patron_with_letters()
#     test_borrow_book_invalid_negative_patron()
#     test_borrow_book_invalid_borrow_limit()
#     test_borrow_book_invalid_no_copies()
#     test_borrow_book_invalid_duplicate()
