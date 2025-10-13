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
import os
# sys.path.insert(1, "C:/Users/laure/OneDrive/Documents!/CISC 327/CISC327-CMPE327-F25")
from library_service import (
    calculate_late_fee_for_book
)

def test_late_fee_valid_input_14_or_less():
    """Test late fee for book with valid input."""
    # 1984 ISBN
    values, message = calculate_late_fee_for_book("123456", "9780451524935")
    
    assert values['fee_amount'] == 0
    assert values['days_overdue'] <= 14
    assert "successfully added" in message.lower()

def test_late_fee_valid_input_15_to_21():
    """Test late fee for book with valid input."""
    # 1984 ISBN
    values, message = calculate_late_fee_for_book("123456", "9780451524935")
    
    assert values['fee_amount'] == values['days_overdue']*0.5
    assert values['days_overdue'] <= 21
    assert values['days_overdue'] > 14
    assert "successfully added" in message.lower()

def test_late_fee_valid_input_22_or_more():
    """Test late fee for book with valid input."""
    # 1984 ISBN
    values, message = calculate_late_fee_for_book("123456", "9780451524935")
    
    assert values['fee_amount'] <= 15
    assert values['fee_amount'] == values['days_overdue'] 
    assert values['days_overdue'] < 21
    assert "successfully added" in message.lower()

def test_late_fee_invalid_isbn_too_long():
    """Test late fee for book with too long ISBN."""
    success, message = calculate_late_fee_for_book("123456", "12345678901234")
    
    assert success == False
    assert "13 digits" in message

def test_late_fee_invalid_isbn_too_short():
    """Test late fee for book with too short ISBN."""
    success, message = calculate_late_fee_for_book("123456", "123456789012")
    
    assert success == False
    assert "13 digits" in message

def test_late_fee_invalid_isbn_with_letters():
    """Test late fee for book with letters in ISBN."""
    success, message = calculate_late_fee_for_book("123456", "1234567890LOL")
    
    assert success == False
    assert "13 digits" in message

def test_late_fee_invalid_negative_isbn():
    """Test late fee for book with negative ISBN."""
    success, message = calculate_late_fee_for_book("123456", "-123456789012")
    
    assert success == False
    assert "13 digits and positive" in message

def test_late_fee_invalid_isbn_not_in_db():
    """Test late fee for book with ISBN not in database."""
    success, message = calculate_late_fee_for_book("123456", "1234567890123")
    
    assert success == False
    assert "ISBN must be in database" in message

def test_late_fee_invalid_patron_too_long():
    """Test late fee for book with too long patron ID."""
    success, message = calculate_late_fee_for_book("1234567", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_patron_too_short():
    """Test late fee for book with too short patron ID."""
    success, message = calculate_late_fee_for_book("12345", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_patron_with_letters():
    """Test late fee for book with letters in patron ID."""
    success, message = calculate_late_fee_for_book("12345X", "9780451524935")
    
    assert success == False
    assert "6 digits" in message

def test_late_fee_invalid_negative_patron():
    """Test late fee for book with negative ISBN."""
    success, message = calculate_late_fee_for_book("-12345", "9780451524935")
    
    assert success == False
    assert "6 digits and positive" in message

def test_late_fee_invalid_incorrect_patron():
    """Test late fee for book from different patron."""
    # 1984 ISBN
    success, message = calculate_late_fee_for_book("000001", "9780451524935 ")
    
    assert success == False
    assert "different patron" in message

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