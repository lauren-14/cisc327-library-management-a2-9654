"""
This testing suite is used to test the R6 requirement:

The system shall provide search functionality with the following parameters:
- `q`: search term
- `type`: search type (title, author, isbn)
- Support partial matching for title/author (case-insensitive)
- Support exact matching for ISBN
- Return results in same format as catalog display
"""

import pytest
import sys
sys.path.append('services')
#sys.path.append('../services')
import services.library_service as library_service 

def test_search_book_valid_title(mocker):
    """Test book valid title input (partial matching)."""

    # testing get_all_books stub
    mocker.patch("services.library_service.get_all_books", 
                    return_value=[{"title":"the great gatsby"}])
    
    book = library_service.search_books_in_catalog("the great gatsby","title")
    
    assert len(book) > 0
    #assert "success" in message

def test_search_book_valid_author(mocker):
    """Test book valid author input (partial matching)."""
    # testing get_all_books stub
    mocker.patch("services.library_service.get_all_books", 
                    return_value=[{"author":"harper lee"}])
    
    book = library_service.search_books_in_catalog("harper lee","author")
    
    assert len(book) > 0
    #assert "success" in message

def test_search_book_valid_isbn(mocker):
    """Test book valid isbn input (exact matching)."""

    # get_book_by_isbn stub that mocks book being in database
    mocker.patch("services.library_service.get_book_by_isbn", 
                    return_value=True)
    
    assert library_service.get_book_by_isbn("1234567890123") == True
    book = library_service.search_books_in_catalog("9780743273565","isbn")
    
    assert len(book) > 0
    #assert "success" in message

def test_search_book_invalid_title_not_in_db(mocker):
    """Test book not in database."""

    # testing get_all_books stub
    mocker.patch("services.library_service.get_all_books", 
                    return_value=[{"title":"the great gatsby"}])
    
    book = library_service.search_books_in_catalog("Six of Crows","title")
    
    assert len(book) == 0
    #assert "not found" in message

def test_search_book_invalid_author_not_in_db(mocker):
    """Test book not in database."""

    # testing get_all_books stub
    mocker.patch("services.library_service.get_all_books", 
                    return_value=[{"author":"harper lee"}])
    
    book = library_service.search_books_in_catalog("Leigh Bardugo","author")
    
    assert len(book) == 0
    #assert "not found" in message

def test_search_book_invalid_isbn_not_in_db(mocker):
    """Test book not in database."""

    # get_book_by_isbn stub that mocks book being in database
    mocker.patch("services.library_service.get_book_by_isbn", 
                    return_value=False)
    
    assert library_service.get_book_by_isbn("1234567890123") == False

    book = library_service.search_books_in_catalog("5","isbn")
    
    assert book == []
    #assert "ISBN does not exist" in message

def test_search_book_invalid_search_type(mocker):
    """Test book not in database."""

    mocker.patch("services.library_service.get_all_books", 
                    return_value=[])
    book = library_service.search_books_in_catalog("5","search type")
    
    assert book == []
    #assert "invalid search type" in message

# if __name__ == "__main__":
#     test_search_book_valid_title()
#     test_search_book_valid_author()
#     test_search_book_valid_isbn()
#     test_search_book_invalid_title_not_in_db()
#     test_search_book_invalid_author_not_in_db()
#     test_search_book_invalid_isbn_not_in_db()
#     test_search_book_invalid_search_type()
#     # test_search_book_invalid_isbn_too_short()
#     # test_search_book_invalid_isbn_too_long()
#     # test_search_book_invalid_isbn_with_letters()
#     # test_search_book_invalid_negative_isbn()
#     # test_search_book_invalid_long_title()
#     # test_search_book_valid_200_title()
#     # test_search_book_invalid_no_title()
#     # test_search_book_invalid_no_author()
#     # test_search_book_valid_100_author()
#     # test_search_book_invalid_long_author()