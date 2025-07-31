import tkinter as tk
from tkinter import messagebox
import books
import borrow
from reports import generate_report

def open_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Library Management System")
    dashboard.geometry("500x500")

    tk.Label(dashboard, text="📚 Library Management System", font=("Helvetica", 16, "bold")).pack(pady=20)

    # BOOK FUNCTIONS
    tk.Button(dashboard, text="➕ Add Book", width=30, command=books.add_book_window).pack(pady=5)
    tk.Button(dashboard, text="📚 View Books", width=30, command=books.view_books_window).pack(pady=5)
    tk.Button(dashboard, text="✏️ Edit Book", width=30, command=books.edit_book_window).pack(pady=5)
    tk.Button(dashboard, text="❌ Delete Book", width=30, command=books.delete_book_window).pack(pady=5)

    # BORROW FUNCTIONS
    tk.Button(dashboard, text="👤 Record Borrowing", width=30, command=borrow.record_borrowing_window).pack(pady=5)
    tk.Button(dashboard, text="📤 Return Book", width=30, command=borrow.return_book_window).pack(pady=5)
    tk.Button(dashboard, text="📆 Upcoming Returns", width=30, command=borrow.check_due_books).pack(pady=5)
    tk.Button(dashboard, text="📋 View Borrowed Books", width=30, command=borrow.view_borrowed_books_window).pack(pady=5)

    # REPORT
    tk.Button(dashboard, text="🧾 Generate Report", width=30, command=generate_report).pack(pady=5)

    # EXIT
    tk.Button(dashboard, text="🚪 Logout", width=30, command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

# Optionally remove this if unused
# def dashboard_window():
#     ...
