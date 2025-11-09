"""
This testing suite is used to test the R4 requirement:

The system shall provide a return interface that includes:

- Accepts patron ID and book ID as form parameters
- Verifies the book was borrowed by the patron
- Updates available copies and records return date
- Calculates and displays any late fees owed
"""

import pytest
from services import library_service 


def test_return_book_valid_input():
    """Test returning a book with valid input."""
    # 1984 ISBN
    success, message = library_service.return_book_by_patron("123456", "9780451524935")
    
    assert success == True
    assert "successfully added" in message.lower()

def test_return_book_invalid_isbn_too_long():
    """Test returning a book with too long ISBN."""
    success, message = library_service.return_book_by_patron("123456", "12345678901234")
    
    assert success == False
    assert "13 digits" in message

def test_return_book_invalid_isbn_too_short():
    """Test returning a book with too short ISBN."""
    success, message = library_service.return_book_by_patron("123456", "123456789012")
    
    assert success == False
    assert "13 digits" in message

def test_return_book_invalid_isbn_with_letters():
    """Test returning a book with letters in ISBN."""
    success, message = library_service.return_book_by_patron("123456", "1234567890LOL")
    
    assert success == False
    assert "13 digits" in message

def test_return_book_invalid_negative_isbn():
    """Test returning a book with negative ISBN."""
    success, message = library_service.return_book_by_patron("123456", "-123456789012")
    
    assert success == False
    assert "13 digits and positive" in message

def test_return_book_invalid_isbn_not_in_db():
    """Test returning a book with ISBN not in database."""
    success, message = library_service.return_book_by_patron("123456", "1234567890123")
    
    assert success == False
    assert "ISBN must be in database" in message

def test_return_book_invalid_patron_too_long():
    """Test returning a book with too long patron ID."""
    success, message = library_service.return_book_by_patron("1234567", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_patron_too_short():
    """Test returning a book with too short patron ID."""
    success, message = library_service.return_book_by_patron("12345", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_patron_with_letters():
    """Test returning a book with letters in patron ID."""
    success, message = library_service.return_book_by_patron("12345X", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_negative_patron():
    """Test returning a book with negative ISBN."""
    success, message = library_service.return_book_by_patron("-12345", "9780451524935")
    
    assert success == False
    assert "6 digits and positive" in message

def test_return_book_invalid_incorrect_patron():
    """Test returning a book from different patron."""
    # 1984 ISBN
    success, message = library_service.return_book_by_patron("000001", "9780451524935 ")
    
    assert success == False
    assert "different patron" in message

# if __name__ == "__main__":
#     test_return_book_valid_input()
#     test_return_book_invalid_isbn_too_long()
#     test_return_book_invalid_isbn_too_short()
#     test_return_book_invalid_isbn_with_letters()
#     test_return_book_invalid_negative_isbn()
#     test_return_book_invalid_isbn_not_in_db()
#     test_return_book_invalid_patron_too_long()
#     test_return_book_invalid_patron_too_short()
#     test_return_book_invalid_patron_with_letters()
#     test_return_book_invalid_negative_patron()
#     test_return_book_invalid_incorrect_patron()
