"""
This testing suite is used to test the R5 requirement:

The system shall provide an API endpoint GET `/api/late_fee/<patron_id>/<book_id>` that includes the following.
- Calculates late fees for overdue books based on:
  - Books due 14 days after borrowing
  - $0.50/day for first 7 days overdue
  - $1.00/day for each additional day after 7 days
  - Maximum $15.00 per book
- Returns JSON response with fee amount and days overdue
"""

import pytest
import sys
sys.path.append('services')
#sys.path.append('../services')
from datetime import datetime, timedelta
import services.library_service as library_service

def test_late_fee_valid_input_14_or_less(mocker):
    """Test late fee for book with valid input."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'is_overdue': False})

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[{'book_id':1,'is_overdue': False}])
    assert library_service.get_patron_borrowed_books("123456") == [{'book_id':1, 'is_overdue': False}]

    values, message = library_service.calculate_late_fee_for_book("123456", 1)
    
    assert values['fee_amount'] == 0
    assert values['days_overdue'] == 0
    assert "Not Overdue" in message

def test_late_fee_valid_input_15_to_21(mocker):
    """Test late fee for book with valid input."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'is_overdue': True})
    
    time_difference = timedelta(days=2)

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[{'book_id':1,
                                                                             'is_overdue': True,
                                                                             'due_date':(datetime.now() - time_difference)}])
    values, message = library_service.calculate_late_fee_for_book("123456", 1)
    
    assert values['fee_amount'] == values['days_overdue']*0.5
    assert values['days_overdue'] <= 7
    assert "Success" in message

def test_late_fee_valid_input_22_or_more(mocker):
    """Test late fee for book with valid input."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'is_overdue': True})
    
    time_difference = timedelta(days=8)

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[{'book_id':1,
                                                                             'is_overdue': True,
                                                                             'due_date':(datetime.now() - time_difference)}])
    
    values, message = library_service.calculate_late_fee_for_book("123456", 1)
    
    assert values['fee_amount'] <= 15
    assert values['fee_amount'] == values['days_overdue'] + 3.5
    assert values['days_overdue'] > 7
    assert "Success" in message

def test_late_fee_valid_over_15_fee(mocker):
    """Test late fee for book with valid input."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'is_overdue': True})
    
    time_difference = timedelta(days=100)

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[{'book_id':1,
                                                                             'is_overdue': True,
                                                                             'due_date':(datetime.now() - time_difference)}])
    
    values, message = library_service.calculate_late_fee_for_book("123456", 1)
    
    assert values['fee_amount'] == 15
    assert values['days_overdue'] > 7
    assert "Success" in message

def test_late_fee_invalid_patron_too_long():
    """Test late fee for book with too long patron ID."""
    success, message = library_service.calculate_late_fee_for_book("1234567", 1)
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_patron_too_short():
    """Test late fee for book with too short patron ID."""
    success, message = library_service.calculate_late_fee_for_book("12345", 1)
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_patron_with_letters():
    """Test late fee for book with letters in patron ID."""
    success, message = library_service.calculate_late_fee_for_book("12345X", 1)
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_negative_patron():
    """Test late fee for book with negative ISBN."""
    success, message = library_service.calculate_late_fee_for_book("-12345", 1)
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_incorrect_patron(mocker):
    """Test late fee for book from different patron."""

    # testing get_book_by_id stub
    mocker.patch("services.library_service.get_book_by_id", 
                    return_value={'title':'sample_title',
                                  'is_overdue': False})

    # testing get_patron_borrowed_books stub
    mocker.patch("services.library_service.get_patron_borrowed_books", return_value=[])
    assert library_service.get_patron_borrowed_books("123456") == []

    # 1984 ISBN
    values, message = library_service.calculate_late_fee_for_book("000001", 1)

    assert values['fee_amount'] == 0
    assert values['days_overdue'] == 0
    assert "Not borrowed" in message

# if __name__ == "__main__":
#     test_late_fee_valid_input_14_or_less()
#     test_late_fee_valid_input_15_to_21()
#     test_late_fee_valid_input_22_or_more()
#     test_late_fee_invalid_isbn_too_long()
#     test_late_fee_invalid_isbn_too_short()
#     test_late_fee_invalid_isbn_with_letters()
#     test_late_fee_invalid_negative_isbn()
#     test_late_fee_invalid_isbn_not_in_db()
#     test_late_fee_invalid_patron_too_long()
#     test_late_fee_invalid_patron_too_short()
#     test_late_fee_invalid_patron_with_letters()
#     test_late_fee_invalid_negative_patron()
#     test_late_fee_invalid_incorrect_patron()