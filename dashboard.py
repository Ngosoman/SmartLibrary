import tkinter as tk
from tkinter import messagebox
import books
import borrow

def dashboard_window():
    dashboard = tk.Tk()
    dashboard.title("Library Dashboard")
    dashboard.geometry("400x400")
    
    tk.Label(dashboard, text="Welcome to the Library System", font=("Helvetica", 16, "bold")).pack(pady=20)

    # BOOKS SECTION
    tk.Button(dashboard, text="Add Book", width=25, command=books.add_book_window).pack(pady=5)
    tk.Button(dashboard, text="View Books", width=25, command=books.view_books_window).pack(pady=5)
    tk.Button(dashboard, text="Edit Book", width=25, command=books.edit_book_window).pack(pady=5)
    tk.Button(dashboard, text="Delete Book", width=25, command=books.delete_book_window).pack(pady=5)

    # BORROW SECTION
    tk.Button(dashboard, text="Record Borrowing", width=25, command=borrow.record_borrowing_window).pack(pady=5)

    # TODO: Future features
    tk.Button(dashboard, text="Return Book", width=25, command=borrow.return_book_window).pack(pady=5)

    tk.Button(dashboard, text="View Borrowed Books (Coming Soon)", width=25, state="disabled").pack(pady=5)

    # Exit
    tk.Button(dashboard, text="Logout", width=25, command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()
