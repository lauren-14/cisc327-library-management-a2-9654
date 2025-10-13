from datetime import datetime, timedelta
from database import (
    get_book_by_id, get_patron_borrowed_books
)
from library_service import (
    get_patron_status_report
)
print(get_patron_status_report("121212"))
#days_overdue = (datetime.now() - borrowed_books[0]['due_date']).days
#print(days_overdue)
print()

start_time = datetime(2025, 1, 1, 9, 0, 0)
end_time = datetime(2025, 1, 1, 9, 0, 0)
time_difference = end_time - start_time
print(f"Time difference: {time_difference.days + 1}")