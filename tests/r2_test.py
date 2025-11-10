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