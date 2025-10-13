"""
This testing suite is used to test the R1 requirement:

The system shall display all books in the catalog in a table format showing:
- Book ID, Title, Author, ISBN
- Available copies / Total copies
- Actions (Borrow button for available books)
"""

import pytest
import sys
import os

# NEED 4-5 TEST CASES

def test_display():
    """Test adding a book with valid input."""
    success, message = add_book_to_catalog("Test Book", "Test Author", "1234567890123", 5)
    
    assert success == True
    assert "successfully added" in message.lower()

# if __name__ == "__main__":
#     test_display()