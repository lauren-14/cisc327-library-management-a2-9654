"""
This testing suite is used to test the R7 requirement:

The system shall display patron status for a particular patron that includes the following: 

- Currently borrowed books with due dates
- Total late fees owed  
- Number of books currently borrowed
- Borrowing history
"""

import pytest
import services.library_service as library_service 

# test not patron_id, not patron_id.isdigit()

def test_patron_status_valid(mocker):
    """Test patron status valid input."""

    # testing get_patron_borrowed_books stub
    mocker.patch("library_service.get_patron_borrowed_books", return_value=[{'book_id':1}])

    # calculate late fee for book stub
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    
    # testing get_patron_borrow_count stub
    mocker.patch("library_service.get_patron_borrow_count", return_value=1)
    assert library_service.get_patron_borrow_count("123456") == 1

    report, message = library_service.get_patron_status_report("123456")
    
    assert report['borrowed'] == [{'book_id':1}]
    assert report['fee_amount'] == 15
    assert report['borrow_count'] == 1
    assert "Success" in message

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
    assert "6 digits" in message

# if __name__ == "__main__":
#     test_patron_status_valid()
#     #test_patron_status_invalid_not_in_db()
#     test_patron_status_invalid_patron_too_long()
#     test_patron_status_invalid_patron_too_short()
#     test_patron_status_invalid_patron_with_letters()
#     test_patron_status_invalid_negative_patron()