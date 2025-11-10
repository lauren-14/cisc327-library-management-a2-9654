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
import sys
sys.path.append('services')
#sys.path.append('../services')
import services.library_service as library_service 

def test_borrow_book_valid_input(mocker):
    """Test borrowing a book with valid input."""
    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrow_count stub
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=5)
    assert library_service.get_patron_borrow_count("123456") == 5

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    assert library_service.get_patron_borrowed_books("123456") == []

    # insert_borrow_record stub
    mocker.patch("services.library_service.insert_borrow_record", return_value=True)

    # testing update_book_availability stub
    mocker.patch("services.library_service.update_book_availability", return_value=True)
    assert library_service.update_book_availability(1,-1) == True

    success, message = library_service.borrow_book_by_patron("123456", 2)
    
    assert success == True
    assert "Successfully borrowed" in message

def test_borrow_book_not_in_db(mocker):
    """Test borrowing a book not in the database."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value=False)
    
    success, message = library_service.borrow_book_by_patron("123456", 2)
    
    assert success == False
    assert "Book not found" in message

def test_borrow_book_invalid_patron_too_long():
    """Test borrowing a book with too long patron ID."""
    success, message = library_service.borrow_book_by_patron("1234567", 2)
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_patron_too_short():
    """Test borrowing a book with too short patron ID."""
    success, message = library_service.borrow_book_by_patron("12345", 2)
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_patron_with_letters():
    """Test borrowing a book with letters in patron ID."""
    success, message = library_service.borrow_book_by_patron("12345X", 2)
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_negative_patron():
    """Test borrowing a book with negative patron ID."""
    success, message = library_service.borrow_book_by_patron("-12345", 2)
    
    assert success == False
    assert "6 digits" in message

def test_borrow_book_invalid_borrow_limit(mocker):
    """Test borrowing a book with borrow limit of 5 reached."""
    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrow_count stub
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=6)

    assert library_service.get_patron_borrow_count("123456") == 6
    success, message = library_service.borrow_book_by_patron("123456", 2)
    
    assert success == False
    assert "maximum borrowing limit" in message

def test_borrow_book_invalid_no_copies(mocker):
    """Test borrowing a book with no copies."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':0})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':0}
    
    # 1984 ISBN
    success, message = library_service.borrow_book_by_patron("123123", 2)
    
    assert success == False
    assert "currently not available" in message

def test_borrow_book_invalid_duplicate(mocker):
    """Test borrowing another copy of the same book already borrowed."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1,
                                  'book_id:': 1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1,
                                                 'book_id:': 1}

    # testing get_patron_borrow_count stub
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=1)
    assert library_service.get_patron_borrow_count("123456") == 1

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[{'book_id':1}])
    assert library_service.get_patron_borrowed_books("123456") == [{'book_id':1}]

    # 1984 ISBN
    success, message = library_service.borrow_book_by_patron("123456", 1)
    
    assert success == False
    assert "already borrowed" in message

def test_borrow_book_borrow_record_database_error(mocker):
    """Test borrowing a book with borrow record database error."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrow_count stub
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=5)
    assert library_service.get_patron_borrow_count("123456") == 5

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    assert library_service.get_patron_borrowed_books("123456") == []

    # insert_borrow_record stub
    mocker.patch("services.library_service.insert_borrow_record", return_value=False)

    success, message = library_service.borrow_book_by_patron("123456", 2)
    
    assert success == False
    assert "Database error occurred while creating borrow record" in message

def test_borrow_book_update_availability_database_error(mocker):
    """Test borrowing a book with borrow record database error."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'available_copies':1})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title',
                                                 'available_copies':1}

    # testing get_patron_borrow_count stub
    mocker.patch("services.library_service.get_patron_borrow_count", return_value=5)
    assert library_service.get_patron_borrow_count("123456") == 5

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    assert library_service.get_patron_borrowed_books("123456") == []

    # insert_borrow_record stub
    mocker.patch("services.library_service.insert_borrow_record", return_value=True)

    # testing update_book_availability stub
    mocker.patch("services.library_service.update_book_availability", return_value=False)
    assert library_service.update_book_availability(1,-1) == False

    success, message = library_service.borrow_book_by_patron("123456", 2)
    
    assert success == False
    assert "Database error occurred while updating book availability" in message

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
