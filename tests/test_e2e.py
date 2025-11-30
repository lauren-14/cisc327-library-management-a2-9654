import re
from playwright.sync_api import Page, expect
import pytest
import sys
sys.path.append('services')
#sys.path.append('../services')
import services.library_service as library_service 

# https://playwright.dev/python/docs/api/class-locator#locator-fill
# https://www.neovasolutions.com/wp-content/uploads/2023/02/js_alerts.png

def test_user_flow_add_and_borrow_book(page: Page):
    """
    Tests successful adding, searching, and borrowing of a book.
    """
    page.goto("http://127.0.0.1:5000/catalog")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Library Management System"))
    expect(page).to_have_url("http://127.0.0.1:5000/catalog")

    # add new book to catalog (removed from database before added)
    page.get_by_role("link", name="Add Book").click()
    expect(page).to_have_url("http://127.0.0.1:5000/add_book")
    expect(page.get_by_role("heading", name="Add New Book")).to_be_visible()
    page.get_by_role("textbox", name="Title *").fill("Test Book")
    page.get_by_role("textbox", name="Author *").fill("Test Author")
    page.get_by_role("textbox", name="ISBN *").fill("1234567890123")
    page.get_by_role("spinbutton", name="Total Copies *").fill("1")
    page.get_by_role("button", name="Add Book to Catalog").click()

    # verify book appears in catalog
    expect(page).to_have_url("http://127.0.0.1:5000/catalog")
    expect(page.get_by_role("heading", name="Book Catalog")).to_be_visible()
    expect(page.get_by_text("Book \"Test Book\" has been successfully added to the catalog.")).to_be_visible()
    expect(page.get_by_text("1234567890123")).to_be_visible()
    
    # navigate to search book page
    page.get_by_role("link", name="Search").click()
    expect(page).to_have_url("http://127.0.0.1:5000/search")
    expect(page.get_by_role("heading", name="Search Books")).to_be_visible()
    page.get_by_role("textbox", name="Search Term").fill("test book")
    page.select_option("#type",value="title")
    page.get_by_role("button", name="Search").click()

    # borrow the book
    expect(page.get_by_text("1234567890123")).to_be_visible()
    page.get_by_role("textbox", name="Patron ID").fill("000000")
    page.get_by_role("button", name="Borrow").click()

    # verify the borrow confirmation message appears
    expect(page).to_have_url("http://127.0.0.1:5000/catalog")
    expect(page.get_by_role("heading", name="Book Catalog")).to_be_visible()
    expect(page.get_by_text("Successfully borrowed \"Test Book\".")).to_be_visible()

def test_user_flow_return_book_and_add_duplicate_book(page: Page):
    """
    Tests successful return of a book and unsuccessful adding of
    a duplicate book (relies on borrowed book from previous test)
    """
    page.goto("http://127.0.0.1:5000/catalog")

    # Expect title to contain "Library Management System"
    expect(page).to_have_title(re.compile("Library Management System"))
    expect(page).to_have_url("http://127.0.0.1:5000/catalog")
    expect(page.get_by_text("Test Book")).to_be_visible()

    # return the book
    page.get_by_role("link", name="Return Book").click()
    expect(page).to_have_url("http://127.0.0.1:5000/return")
    expect(page.get_by_role("heading", name="Return Book")).to_be_visible()
    page.get_by_role("textbox", name="Patron ID *").fill("000000")

    book_id = library_service.get_book_by_isbn("1234567890123")['id']
    page.get_by_role("spinbutton", name="Book ID *").fill(str(book_id))
    page.get_by_role("button", name="Process Return").click()

    # verify the return confirmation message appears
    expect(page).to_have_url("http://127.0.0.1:5000/return")
    expect(page.get_by_role("heading", name="Return Book")).to_be_visible()
    expect(page.get_by_text("Book return successful with $0.00 in late fees due.")).to_be_visible()

    # add new book to catalog (already added)
    page.get_by_role("link", name="Add Book").click()
    expect(page).to_have_url("http://127.0.0.1:5000/add_book")
    expect(page.get_by_role("heading", name="Add New Book")).to_be_visible()
    page.get_by_role("textbox", name="Title *").fill("Test Book")
    page.get_by_role("textbox", name="Author *").fill("Test Author")
    page.get_by_role("textbox", name="ISBN *").fill("1234567890123")
    page.get_by_role("spinbutton", name="Total Copies *").fill("1")
    page.get_by_role("button", name="Add Book to Catalog").click()

    # verify book was not added
    expect(page).to_have_url("http://127.0.0.1:5000/add_book")
    expect(page.get_by_role("heading", name="Add New Book")).to_be_visible()
    expect(page.get_by_text("A book with this ISBN already exists.")).to_be_visible()

    # confirm it is already in the catalog
    page.get_by_role("link", name="Cancel").click()
    expect(page).to_have_url("http://127.0.0.1:5000/catalog")
    expect(page.get_by_role("heading", name="Catalog")).to_be_visible()
    expect(page.get_by_text("1234567890123")).to_be_visible()