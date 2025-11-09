"""
This testing suite is used to test the pay_late_fees function in library_service.py
"""
import pytest
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from unittest.mock import Mock
from unittest.mock import patch
from payment_service import (
    PaymentGateway
)
import library_service 

# successful payment
def test_successful_payment(mocker):
    """ Test successful payment """

    # testing calculate_late_fee_for_book stub
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    result = library_service.calculate_late_fee_for_book("123456", 1)
    assert result == {
                        'fee_amount': 15,
                        'days_overdue': 21
                    }
    
    # testing get_book_by_id stub
    mocker.patch("library_service.get_book_by_id", 
                    return_value={'title':'sample_title'})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title'}

    # testing pay_late_fees with mocked PaymentGateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = library_service.pay_late_fees("123456", 1, mock_gateway)

    assert success == True
    assert "Payment successful!" in msg
    assert txn == "txn_123"
    mock_gateway.process_payment.assert_called_once()

# payment declined by gateway
def test_payment_decline(mocker):
    """ Test payment declined from fees exceeding $1000 """
    
    # testing calculate_late_fee_for_book stub
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 2000,
                        'days_overdue': 21
                    })
    result = library_service.calculate_late_fee_for_book("123456", 1)
    assert result == {
                        'fee_amount': 2000,
                        'days_overdue': 21
                    }
    
    # testing get_book_by_id stub
    mocker.patch("library_service.get_book_by_id", 
                    return_value={'title':'sample_title'})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title'}
    
    # testing invalid pay_late_fees with mocked PaymentGateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Payment declined: amount exceeds limit")
    success, msg, txn = library_service.pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "Payment failed:" in msg
    mock_gateway.process_payment.assert_called_once()

# invalid patron IDs (verifies mock is NOT called)
def test_patron_status_invalid_patron_too_long():
    """Test too long patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since patron ID is rejected before
    # payment gateway is even accessed
    success, msg, txn = library_service.pay_late_fees("1234567", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."
    mock_gateway.process_payment.assert_not_called()

def test_patron_status_invalid_patron_too_short():
    """Test too long patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since patron ID is rejected before
    # payment gateway is even accessed
    success, msg, txn = library_service.pay_late_fees("12345", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."
    mock_gateway.process_payment.assert_not_called()

def test_patron_status_invalid_patron_with_letters():
    """Test patron_status for letters in patron ID."""
    """Test too long patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since patron ID is rejected before
    # payment gateway is even accessed
    success, msg, txn = library_service.pay_late_fees("12345X", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."
    mock_gateway.process_payment.assert_not_called()

# zero late fees (verifies mock is NOT called)
def test_zero_fees(mocker):
    # testing calculate_late_fee_for_book stub
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 0,
                        'days_overdue': 21
                    })
    result = library_service.calculate_late_fee_for_book("123456", 1)
    assert result == {
                        'fee_amount': 0,
                        'days_overdue': 21
                    }
    
    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since fee amount is rejected before
    # payment gateway is even accessed
    success, msg, txn = library_service.pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert msg == "No late fees to pay for this book."
    mock_gateway.process_payment.assert_not_called()
    

# network error exception handling
def test_nextwork_error(mocker):
    """ Test network error from process payment (incorrect return values) """
    mocker.patch("library_service.calculate_late_fee_for_book", return_value={
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    result = library_service.calculate_late_fee_for_book("123456", 1)
    assert result == {
                        'fee_amount': 15,
                        'days_overdue': 21
                    }
    
    # testing get_book_by_id stub
    mocker.patch("library_service.get_book_by_id", 
                    return_value={'title':'sample_title'})
    
    assert library_service.get_book_by_id(1) == {'title':'sample_title'}

    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = ("")
    success, msg, txn = library_service.pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "Payment processing error" in msg
    mock_gateway.process_payment.assert_called_once()