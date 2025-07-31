import tkinter as tk
from tkinter import messagebox

def open_library_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Library Management System")
    dashboard.geometry("500x400")

    tk.Label(dashboard, text="📚 Library Management System", font=("Helvetica", 16, "bold")).pack(pady=20)

    # Button Options
    tk.Button(dashboard, text="➕ Add Book", width=25, command=add_book).pack(pady=5)
    tk.Button(dashboard, text="📚 View All Books", width=25, command=view_books).pack(pady=5)
    tk.Button(dashboard, text="👤 Record Borrowing", width=25, command=record_borrowing).pack(pady=5)
    tk.Button(dashboard, text="📆 Upcoming Returns", width=25, command=upcoming_returns).pack(pady=5)
    tk.Button(dashboard, text="🧾 Generate Report", width=25, command=generate_report).pack(pady=5)
    tk.Button(dashboard, text="🚪 Logout", width=25, command=dashboard.destroy).pack(pady=20)

    dashboard.mainloop()

# Placeholder functions (we'll implement these next)
def add_book():
    messagebox.showinfo("Add Book", "Function to add a new book.")

def view_books():
    messagebox.showinfo("View Books", "Function to view all books.")

def record_borrowing():
    messagebox.showinfo("Borrow Book", "Function to record borrowing.")

def upcoming_returns():
    messagebox.showinfo("Upcoming Returns", "Function to check return dates.")

def generate_report():
    messagebox.showinfo("Reports", "Function to generate reports.")

