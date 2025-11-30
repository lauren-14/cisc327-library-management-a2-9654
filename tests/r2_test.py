"""
This testing suite is used to test the R2 requirement:

The system shall display all books in the catalog in a table format showing:
- Book ID, Title, Author, ISBN
- Available copies / Total copies
- Actions (Borrow button for available books)
"""

import pytest
import sys
sys.path.append('services')
#sys.path.append('../services')
import services.library_service as library_service

import re
from playwright.sync_api import Page, expect

def test_catalog_display(page: Page):
    page.goto("http://127.0.0.1:5000")

    # Expect a title "to contain" a substring.
    expect(page).to_have_title(re.compile("Library Management System"))

    # tests that table of books is displayed
    table = page.locator("table")
    headers = table.locator("thead th").all_inner_texts()
    assert headers == ["ID","Title","Author","ISBN","Availability","Actions"]