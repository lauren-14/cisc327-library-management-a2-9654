"""
This testing suite is used to test the refund_late_fees function in library_service.py
"""

import pytest
import sys
sys.path.append('services')
from unittest.mock import Mock
from unittest.mock import patch
import services.library_service as library_service 
from services.payment_service import (
    PaymentGateway
)

# successful refund
def test_refund_late_fee_success():
    """ Test successful refund """

    # testing refund_late_fee_payment with mocked PaymentGateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = (True, "Success")
    success, msg = library_service.refund_late_fee_payment("txn_123", 15, mock_gateway)

    assert success == True
    assert msg == "Success"
    mock_gateway.refund_payment.assert_called_once()

# invalid transaction ID rejections (verifies mock is NOT called)
def test_refund_late_fee_invalid_transactionID():
    """ Tests invalid transaction ID (doesn't start with "txn_") """

    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since transaction ID is rejected before
    # payment gateway is even accessed
    success, msg = library_service.refund_late_fee_payment("txn123", 15, mock_gateway)

    assert success == False
    assert msg == "Invalid transaction ID."
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_empty_transactionID():
    """ Tests empty transaction ID"""

    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since transaction ID is rejected before
    # payment gateway is even accessed
    success, msg = library_service.refund_late_fee_payment(None, 15, mock_gateway)

    assert success == False
    assert msg == "Invalid transaction ID."
    mock_gateway.refund_payment.assert_not_called()

# invalid refund amounts (negative, 0, exceeds $15 max)
def test_refund_late_fee_negative_refund_amount():
    """ Tests negative (invalid) refund amount """

    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since refund amount is rejected before
    # payment gateway is even accessed
    success, msg = library_service.refund_late_fee_payment("txn_123", -1, mock_gateway)

    assert success == False
    assert msg == "Refund amount must be greater than 0."
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_zero_refund_amount():
    """ Tests $0 (invalid) refund amount """

    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since refund amount is rejected before
    # payment gateway is even accessed
    success, msg = library_service.refund_late_fee_payment("txn_123", 0, mock_gateway)

    assert success == False
    assert msg == "Refund amount must be greater than 0."
    mock_gateway.refund_payment.assert_not_called()

def test_refund_late_fee_over_15_refund_amount():
    """ Tests over $15 (invalid) refund amount """

    mock_gateway = Mock(spec=PaymentGateway)
    # process payment return value not mocked since refund amount is rejected before
    # payment gateway is even accessed
    success, msg = library_service.refund_late_fee_payment("txn_123", 16, mock_gateway)

    assert success == False
    assert msg == "Refund amount exceeds maximum late fee."
    mock_gateway.refund_payment.assert_not_called()

# refund processing error (exception handling)
def test_refund_late_fee_processing_error():
    """ Tests refund processing error """

    # testing refund_late_fee_payment with mocked PaymentGateway
    mock_gateway = Mock(spec=PaymentGateway)
    mock_gateway.refund_payment.return_value = ("")
    success, msg = library_service.refund_late_fee_payment("txn_123", 15, mock_gateway)

    assert success == False
    assert "Refund processing error" in msg
    mock_gateway.refund_payment.assert_called_once()