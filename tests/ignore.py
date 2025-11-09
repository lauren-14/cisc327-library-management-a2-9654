"""
DELETE THIS
This testing suite is used to test the pay_late_fees function in library_service.py
"""
import pytest
import sys, os
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(parent_dir)
from unittest.mock import Mock
from unittest.mock import patch
from services.payment_service import (
    PaymentGateway
)
from services.library_service import (
    calculate_late_fee_for_book, pay_late_fees
)
from database import get_book_by_id

# successful payment
@patch ('library_service.calculate_late_fee_for_book',return_value={})
def test_successful_payment(mocker):
    # with patch ("library_service.calculate_late_fee_for_book",return_value={
    #                     'fee_amount': 15,
    #                     'days_overdue': 21
    #                 }):
    #     result = library_service.calculate_late_fee_for_book("123456", 1)
    #     assert result == {
    #                     'fee_amount': 15,
    #                     'days_overdue': 21
    #                 }
    mock_get_book_by_id = mocker.patch('library_service.get_book_by_id', 
                    return_value={} # does nothing (test like calcuate_late_fee func)
            )
    mock_calculate_late_fee_for_book = mocker.patch("services.library_service.calculate_late_fee_for_book", 
                    return_value=
                    {
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    mock_process_payment = mocker.patch("services.payment_service.PaymentGateway.process_payment", return_value=(True, "txn_123", "Success"))
    mock_calculate_late_fee = mocker.Mock()
    mock_calculate_late_fee.return_value = {
                        'fee_amount': 15,
                        'days_overdue': 21
                    }
    # #values = mock_calculate_late_fee_for_book("123456", "1789051524935")
    # # assert values['fee_amount'] == 15
    # # assert values['days_overdue'] == 21

    assert calculate_late_fee_for_book("123456", 1) == {
                        'fee_amount': 15,
                        'days_overdue': 21
                    }
    # value = get_book_by_id(0)
    # assert value == {}



    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (True, "txn_123", "Success")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)
    #mock_gateway.assert_called_once()

    # assert success == True
    # assert txn == "txn_123"

# payment declined by gateway
def test_payment_decline(mocker):
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = (False, "", "Invalid amount: must be greater than 0")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert txn == None
    assert "Payment failed:" in msg

# invalid patron ID (verfiy mock NOT called)
def test_patron_status_invalid_patron_too_long():
    """Test too long patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    success, msg, txn = pay_late_fees("1234567", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."

def test_patron_status_invalid_patron_too_short():
    """Test too long patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    success, msg, txn = pay_late_fees("12345", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."

def test_patron_status_invalid_patron_with_letters():
    """Test patron_status for letters in patron ID."""
    mock_gateway = Mock(spec=PaymentGateway)
    success, msg, txn = pay_late_fees("12345X", 1, mock_gateway)
    
    assert success == False
    assert msg == "Invalid patron ID. Must be exactly 6 digits."

# network error exception handling
def test_network_error(mocker):
    """ Test network error from process payment (incorrect return values) """
    mock_get_book_id = mocker.patch("database.get_book_by_id", 
                    return_value=1 # does nothing (test like calcuate_late_fee func)
            )
    mock_calculate_late_fee_for_book = mocker.patch("services.library_service.calculate_late_fee_for_book", 
                    return_value=
                    {
                        'fee_amount': 15,
                        'days_overdue': 21
                    })
    
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.process_payment.return_value = ("")
    success, msg, txn = pay_late_fees("123456", 1, mock_gateway)

    assert success == False
    assert "Payment processing error" in msg