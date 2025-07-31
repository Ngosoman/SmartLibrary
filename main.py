import tkinter as tk
from tkinter import messagebox
from login import login_screen
from books import add_book, view_books

# Start the main app after login
def start_dashboard():
    root = tk.Tk()
    root.title("School Library System - Admin Dashboard")
    root.geometry("400x300")

    tk.Label(root, text="Welcome Admin", font=("Helvetica", 16, "bold")).pack(pady=20)

    tk.Button(root, text="Add Book", width=20, command=add_book).pack(pady=10)
    tk.Button(root, text="View All Books", width=20, command=view_books).pack(pady=10)
    # We'll add Borrow, Return, Search, Edit, Delete later here

    tk.Button(root, text="Logout", width=20, command=lambda: [root.destroy(), login_screen()]).pack(pady=20)
    root.mainloop()

if __name__ == "__main__":
    login_screen()
