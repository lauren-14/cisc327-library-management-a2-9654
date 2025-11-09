"""
This testing suite is used to test the R7 requirement:

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history
"""

import pytest
from services import library_service 

def test_patron_status_valid():
    """Test patron status valid input."""
    success, message = library_service.get_patron_status_report("123456")
    
    assert success == True
    assert "success" in message.lower()

# def test_patron_status_invalid_not_in_db():
#     """Test patron status not in database."""
#     success, message = get_patron_status_report("5")
    
#     assert success == False
#     assert "patron must be in database" in message

def test_patron_status_invalid_patron_too_long():
    """Test too long patron ID."""
    success, message = library_service.get_patron_status_report("1234567")
    
    assert success == False
    assert "6 digits" in message

def test_patron_status_invalid_patron_too_short():
    """Test too short patron ID."""
    success, message = library_service.get_patron_status_report("12345")
    
    assert success == False
    assert "6 digits" in message

def test_patron_status_invalid_patron_with_letters():
    """Test patron_status for letters in patron ID."""
    success, message = library_service.get_patron_status_report("12345X")
    
    assert success == False
    assert "6 digits" in message

def test_patron_status_invalid_negative_patron():
    """Test patron_status for negative patron."""
    success, message = library_service.get_patron_status_report("-12345")
    
    assert success == False
    assert "6 digits and positive" in message

# if __name__ == "__main__":
#     test_patron_status_valid()
#     #test_patron_status_invalid_not_in_db()
#     test_patron_status_invalid_patron_too_long()
#     test_patron_status_invalid_patron_too_short()
#     test_patron_status_invalid_patron_with_letters()
#     test_patron_status_invalid_negative_patron()