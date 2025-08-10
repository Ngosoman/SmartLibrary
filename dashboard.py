import tkinter as tk
from tkinter import messagebox
import books
import borrow
import reports
import alerts

from reports import generate_report
from borrow import view_upcoming_returns
from alerts import check_due_alerts
from notifications import NotificationManager
from notifications import init_notifications

# Run alerts check on launch
check_due_alerts()

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("SmartLibrary Dashboard")
    dashboard.geometry("500x650")
    dashboard.resizable(True, True)

    # Initialize notification system and bell
    notifier = NotificationManager(dashboard)
    init_notifications(dashboard)

    tk.Label(dashboard, text="📚 SmartLibrary System", font=("Helvetica", 16, "bold")).pack(pady=20)

    # BOOK FUNCTIONS
    tk.Button(dashboard, text="➕ Add Book", width=30, command=books.add_book_window).pack(pady=5)
    tk.Button(dashboard, text="📖 View Books", width=30, command=books.view_books).pack(pady=5)

    # BORROW FUNCTIONS
    tk.Label(dashboard, text=" Borrowing Section", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
    tk.Button(dashboard, text="👤 Record Borrowing", width=30, command=borrow.record_borrowing_window).pack(pady=5)
    tk.Button(dashboard, text="📤 Return Book", width=30, command=borrow.return_book_window).pack(pady=5)
    tk.Button(dashboard, text="📆 Upcoming Returns", width=30, command=borrow.view_upcoming_returns).pack(pady=5)
    tk.Button(dashboard, text="📋 View Borrowed Books", width=30, command=borrow.view_borrowed_books_window).pack(pady=5)

    # REPORTS
    tk.Label(dashboard, text="📊 Reports", font=("Helvetica", 12, "bold")).pack(pady=(15, 5))
    tk.Button(dashboard, text="🧾 Generate Report", width=30, command=generate_report).pack(pady=5)

    # EXIT
    tk.Button(dashboard, text="🚪 Logout", width=30, fg="white", bg="red", command=dashboard.destroy).pack(pady=25)
    
    dashboard.mainloop()
