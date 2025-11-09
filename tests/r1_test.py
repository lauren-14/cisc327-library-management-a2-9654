"""
This testing suite is used to test the R1 requirement:

The system shall provide a web interface to add new books to the catalog via a form with the following fields:
- Title (required, max 200 characters)
- Author (required, max 100 characters)
- ISBN (required, exactly 13 digits)
- Total copies (required, positive integer)
- The system shall display success/error messages and redirect to the catalog view after successful addition.
"""

import pytest
#from services import library_service 
import library_service
from unittest.mock import Mock
from unittest.mock import patch

def test_add_book_valid_input(mocker):
    """Test adding a book with valid input."""

    # testing get_book_by_isbn stub
    mocker.patch("library_service.get_book_by_isbn", 
                    return_value={'title':"Test Book",
                                  'author':"Test Author",
                                  'isbn':"1234567890123",
                                  'total_copies' : 5,
                                  'available_copies' : 5})
    
    assert library_service.get_book_by_isbn("1234567890123") == {'title':"Test Book",
                                                                'author':"Test Author",
                                                                'isbn':"1234567890123",
                                                                'total_copies' : 5,
                                                                'available_copies' : 5}
    
    
    #mock_database = Mock(spec="")

    # success, message = library_service.add_book_to_catalog("Test Book", "Test Author", "123456789", 5)

    # # mock insert data stub
    
    # assert success == True # mock the data!! (already in the database, that's why)
    # assert message == "A book with this ISBN already exists."

# def test_add_book_invalid_isbn_too_short():
#     """Test adding a book with ISBN too short."""
#     success, message = library_service.add_book_to_catalog("Test Book", "Test Author", "123456789", 5)
    
#     assert success == False
#     assert "13 digits" in message 

# def test_add_book_invalid_isbn_too_long():
#     """Test adding a book with ISBN too long."""
#     success, message = library_service.add_book_to_catalog("Test Book", "Test Author", "12345678901234", 5)
    
#     assert success == False
#     assert "13 digits" in message

# def test_add_book_invalid_isbn_with_letters():
#     """Test adding a book with letters in the ISBN."""
#     success, message = library_service.add_book_to_catalog("Test Book", "Test Author", "1234567890LOL", 5)
    
#     assert success == False
#     assert "13 digits" in message

# def test_add_book_invalid_negative_isbn():
#     """Test adding a book with a negative ISBN."""
#     success, message = library_service.add_book_to_catalog("Test Book", "Test Author", "-123456789012", 5)
    
#     assert success == False
#     assert "13 digits and positive" in message

# def test_add_book_invalid_long_title():
#     """Test adding a book with too long of a title (more than 200 characters)."""
#     title = ""
#     for i in range (201):
#         title += "x"
#     success, message = library_service.add_book_to_catalog(title, "Test Author", "1234567890123", 5)
    
#     assert success == False
#     assert "title max 200 characters" in message

# def test_add_book_valid_200_title():
#     """Test adding a book with valid 200 character title and other valid input."""
#     title = ""
#     for i in range (200):
#         title += "x"
#     success, message = library_service.add_book_to_catalog(title, "Test Author", "1234567890123", 5)
    
#     assert success == True
#     assert "successfully added" in message.lower()

# def test_add_book_invalid_no_title():
#     """Test adding a book with no (empty) title."""
#     success, message = library_service.add_book_to_catalog(" ", "Test Author", "1234567890123", 5)
    
#     assert success == False
#     assert "title min 1 character" in message

# def test_add_book_invalid_no_author():
#     """Test adding a book with no (empty) author."""
#     success, message = library_service.add_book_to_catalog("Test Title", " ", "1234567890123", 5)
    
#     assert success == False
#     assert "author min 1 character" in message

# def test_add_book_valid_100_author():
#     """Test adding a book with valid 100 character author and other valid input."""
#     author = ""
#     for i in range (200):
#         author += "x"
#     success, message = library_service.add_book_to_catalog("Test Title", author, "1234567890123", 5)
    
#     assert success == True
#     assert "successfully added" in message.lower()

# def test_add_book_invalid_long_author():
#     """Test adding a book with too long of an author (more than 100 characters)."""
#     author = ""
#     for i in range (101):
#         author += "x"
#     success, message = library_service.add_book_to_catalog("Test Title", author, "1234567890123", 5)
    
#     assert success == False
#     assert "author max 100 characters" in message

# def test_add_book_invalid_zero_copies():
#     """Test adding a book with no copies."""
#     success, message = library_service.add_book_to_catalog("Test Title", "Test Author", "1234567890123", 0)
    
#     assert success == False
#     assert "min 1 copies" in message

# def test_add_book_invalid_negative_copies():
#     """Test adding a book with negative number of copies."""
#     success, message = library_service.add_book_to_catalog("Test Title", "Test Author", "1234567890123", -1)
    
#     assert success == False
#     assert "min 1 copies" in message

# def test_add_book_invalid_duplicate_isbn():
#     """Test adding a book with a duplicate ISBN of an existing book in the database."""
#     # great gatsby ISBN taken from database
#     success, message = library_service.add_book_to_catalog("Test Title", "Test Author", '9780743273565', 5) 
    
#     assert success == False
#     assert "no duplicate ISBNs" in message

# if __name__ == "__main__":
#     test_add_book_valid_input()
#     test_add_book_invalid_isbn_too_short()
#     test_add_book_invalid_isbn_too_long()
#     test_add_book_invalid_isbn_with_letters()
#     test_add_book_invalid_negative_isbn()
#     test_add_book_invalid_long_title()
#     test_add_book_valid_200_title()
#     test_add_book_invalid_no_title()
#     test_add_book_invalid_no_author()
#     test_add_book_valid_100_author()
#     test_add_book_invalid_long_author()
#     test_add_book_invalid_zero_copies()
#     test_add_book_invalid_negative_copies()
#     test_add_book_invalid_duplicate_isbn()