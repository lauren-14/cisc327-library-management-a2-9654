Lauren Hunter
20409654
Section 001 (Fall 2025)

REQ #   | FUNCTION NAME                 | IMPLEMENTATION STATUS | MISSING COMPONENTS
--------|-------------------------------|-----------------------|------------------------------------------------
R1      | add_book_to_catalog()         | Partial               | validate ISBN 
        |                               |                       |
R3      | borrow_book_by_patron()       | Complete              | none
        |                               |                       |
R4      | return_book_by_patron()       | Partial               | validate patron ID, check if book exists and 
        |                               |                       | is unavailable, check if book is borrowed by
        |                               |                       | patron, update available copies, record return
        |                               |                       | date, calculate and display any late fees
        |                               |                       | 
R5      | calculate_late_fee_for_book() | Partial               | check that API is connected, 
        |                               |                       | determine if book is returned more than 14 days
        |                               |                       | after borrowing, calculate $0.50/day late fee
        |                               |                       | if book is returned 15-21 after borrowing, 
        |                               |                       | calculate $1.00/day late fee if book is returned
        |                               |                       | more than 21 days after borrowing, limit the late 
        |                               |                       | fee to $15 if late fees exceed $15
        |                               |                       | 
R6      | search_books_in_catalog()     | Partial               | check if book exists (case insensitive) by title, 
        |                               |                       | check if book exists (case insensitive) by author,
        |                               |                       | check if book exists by ISBN, display results
        |                               |                       | 
R7      | get_patron_status_report()    | Partial               | retrieve and display currently borrowed books,
        |                               |                       | calculate due dates of borrowed books, 
        |                               |                       | calculate late fees for borrowed books, 
        |                               |                       | calculate number of books currently borrowed,
        |                               |                       | retrieve and display borrowing history
        |                               |                       | 
        |                               |                       | ** create menu option to show patron status
        |                               |                       | on catalog page, business logic functions?? **

** SUMMARY OF TEST SCRIPTS **

r1_test.py (testing R1 function add_book_to_catalog): 
    test_add_book_valid_input()
    test_add_book_invalid_isbn_too_short()
    test_add_book_invalid_isbn_too_long()
    test_add_book_invalid_isbn_with_letters()
    test_add_book_invalid_negative_isbn()
    test_add_book_invalid_long_title()
    test_add_book_valid_200_title()
    test_add_book_invalid_no_title()
    test_add_book_invalid_no_author()
    test_add_book_valid_100_author()
    test_add_book_invalid_long_author()
    test_add_book_invalid_zero_copies()
    test_add_book_invalid_negative_copies()
    test_add_book_invalid_duplicate_isbn()

r2_test.py (testing R2 function)


r3_test.py (testing R3 function borrow_book_by_patron):
    test_borrow_book_valid_input()
    test_borrow_book_invalid_isbn_too_long()
    test_borrow_book_invalid_isbn_too_short()
    test_borrow_book_invalid_isbn_with_letters()
    test_borrow_book_invalid_negative_isbn()
    test_borrow_book_invalid_isbn_not_in_db()
    test_borrow_book_invalid_patron_too_long()
    test_borrow_book_invalid_patron_too_short()
    test_borrow_book_invalid_patron_with_letters()
    test_borrow_book_invalid_negative_patron()
    test_borrow_book_invalid_borrow_limit()
    test_borrow_book_invalid_no_copies()
    test_borrow_book_invalid_duplicate()

r4_test.py (testing R4 function return_book_by_patron):
    test_return_book_valid_input()
    test_return_book_invalid_isbn_too_long()
    test_return_book_invalid_isbn_too_short()
    test_return_book_invalid_isbn_with_letters()
    test_return_book_invalid_negative_isbn()
    test_return_book_invalid_isbn_not_in_db()
    test_return_book_invalid_patron_too_long()
    test_return_book_invalid_patron_too_short()
    test_return_book_invalid_patron_with_letters()
    test_return_book_invalid_negative_patron()
    test_return_book_invalid_incorrect_patron()

r5_test.py (testing R5 function calculate_late_fee_for_book):
    test_late_fee_valid_input_14_or_less()
    test_late_fee_valid_input_15_to_21()
    test_late_fee_valid_input_22_or_more()
    test_late_fee_invalid_isbn_too_long()
    test_late_fee_invalid_isbn_too_short()
    test_late_fee_invalid_isbn_with_letters()
    test_late_fee_invalid_negative_isbn()
    test_late_fee_invalid_isbn_not_in_db()
    test_late_fee_invalid_patron_too_long()
    test_late_fee_invalid_patron_too_short()
    test_late_fee_invalid_patron_with_letters()
    test_late_fee_invalid_negative_patron()
    test_late_fee_invalid_incorrect_patron()

r6_test.py (testing R6 function search_books_in_catalog):
    test_search_book_valid_title()
    test_search_book_valid_author()
    test_search_book_valid_isbn()
    test_search_book_invalid_title_not_in_db()
    test_search_book_invalid_author_not_in_db()
    test_search_book_invalid_isbn_not_in_db()

r7_test.py (testing R7 function get_patron_status_report):
    test_patron_status_valid()
    test_patron_status_invalid_not_in_db()
    test_patron_status_invalid_patron_too_long()
    test_patron_status_invalid_patron_too_short()
    test_patron_status_invalid_patron_with_letters()
    test_patron_status_invalid_negative_patron()
