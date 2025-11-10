"""
This testing suite is used to test the R4 requirement:

The system shall provide a return interface that includes:

- Accepts patron ID and book ID as form parameters
- Verifies the book was borrowed by the patron
- Updates available copies and records return date
- Calculates and displays any late fees owed
"""

import pytest
import services.library_service as library_service 


def test_return_book_valid_input(mocker):
    """Test returning a book with valid input."""

    # testing get_book_by_id stub
    mocker.patch("library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrowed_books stub
    mocker.patch("library_service.get_patron_borrowed_books", return_value=[{'book_id':1}])
    assert library_service.get_patron_borrowed_books("123456") == [{'book_id':1}]

    # testing calculate_late_fee_for_book stub
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    assert library_service.calculate_late_fee_for_book("123456", 1) == {
                        'fee_amount': 15,
                        'days_overdue': 21
                    }

    # testing update_borrow_record_return_date stub
    mocker.patch("library_service.update_borrow_record_return_date", return_value=True)
    mocker.patch("library_service.update_book_availability", return_value=True)

    # 1984 ISBN
    success, message = library_service.return_book_by_patron("123456", 1)
    
    assert success == True
    assert "success" in message

def test_return_book_invalid_patron_too_long():
    """Test returning a book with too long patron ID."""
    success, message = library_service.return_book_by_patron("1234567", 1)
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_patron_too_short():
    """Test returning a book with too short patron ID."""
    success, message = library_service.return_book_by_patron("12345", 1)
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_patron_with_letters():
    """Test returning a book with letters in patron ID."""
    success, message = library_service.return_book_by_patron("12345X", 1)
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_negative_patron():
    """Test returning a book with negative ISBN."""
    success, message = library_service.return_book_by_patron("-12345", 1)
    
    assert success == False
    assert "6 digits" in message

def test_return_book_invalid_incorrect_patron(mocker):
    """Test returning a book from different patron."""

    # testing get_book_by_id stub
    mocker.patch("library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrowed_books stub
    mocker.patch("library_service.get_patron_borrowed_books", return_value=[])
    assert library_service.get_patron_borrowed_books("123456") == []
    
    # 1984 ISBN
    success, message = library_service.return_book_by_patron("000001", 1)
    
    assert success == False
    assert "not borrowed book with ID" in message

# update return date database error

# update avail copies database error

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
