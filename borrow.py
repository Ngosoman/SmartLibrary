import tkinter as tk
from tkinter import messagebox, ttk
import csv
import sqlite3
from datetime import datetime

def record_borrowing_window():
    def submit_borrow():
        student = entry_student.get().strip()
        admission = entry_admission.get().strip()
        student_class = entry_class.get().strip()
        stream = entry_stream.get().strip()
        book_title = entry_book.get().strip()
        date_borrowed = entry_borrow_date.get().strip()
        date_due = entry_due_date.get().strip()

        if not all([student, admission, student_class, stream, book_title, date_borrowed, date_due]):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        with open('borrowed_books.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([student, admission, student_class, stream, book_title, date_borrowed, date_due])
        messagebox.showinfo("Success", "Book borrowing recorded successfully.")
        window.destroy()

    window = tk.Toplevel()
    window.title("Record Book Borrowing")

    tk.Label(window, text="Student Name").grid(row=0, column=0, padx=10, pady=5)
    entry_student = tk.Entry(window)
    entry_student.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Admission Number").grid(row=1, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Class").grid(row=2, column=0, padx=10, pady=5)
    entry_class = tk.Entry(window)
    entry_class.grid(row=2, column=1, padx=10, pady=5)

    tk.Label(window, text="Stream").grid(row=3, column=0, padx=10, pady=5)
    entry_stream = tk.Entry(window)
    entry_stream.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(window, text="Book Title").grid(row=4, column=0, padx=10, pady=5)
    entry_book = tk.Entry(window)
    entry_book.grid(row=4, column=1, padx=10, pady=5)

    tk.Label(window, text="Date Borrowed (YYYY-MM-DD)").grid(row=5, column=0, padx=10, pady=5)
    entry_borrow_date = tk.Entry(window)
    entry_borrow_date.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(window, text="Return Date (YYYY-MM-DD)").grid(row=6, column=0, padx=10, pady=5)
    entry_due_date = tk.Entry(window)
    entry_due_date.grid(row=6, column=1, padx=10, pady=5)

    tk.Button(window, text="Submit", command=submit_borrow).grid(row=7, column=0, columnspan=2, pady=10)

def return_book_window():
    def return_book():
        admission_number = entry_admission.get().strip()
        book_title = entry_book.get().strip()

        rows = []
        returned = False

        try:
            with open('borrowed_books.csv', 'r') as file:
                reader = csv.reader(file)
                for row in reader:
                    if row[1] == admission_number and row[4] == book_title:
                        returned = True
                        continue
                    rows.append(row)

            if returned:
                with open('borrowed_books.csv', 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerows(rows)
                messagebox.showinfo("Success", "Book returned successfully.")
                window.destroy()
            else:
                messagebox.showerror("Error", "No matching borrowed book found.")
        except FileNotFoundError:
            messagebox.showerror("Error", "Borrowed books file not found.")

    window = tk.Toplevel()
    window.title("Return Book")

    tk.Label(window, text="Admission Number").grid(row=0, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Book Title").grid(row=1, column=0, padx=10, pady=5)
    entry_book = tk.Entry(window)
    entry_book.grid(row=1, column=1, padx=10, pady=5)

    tk.Button(window, text="Return Book", command=return_book).grid(row=2, column=0, columnspan=2, pady=10)

def view_borrowed_books_window():
    window = tk.Toplevel()
    window.title("Borrowed Books")

    columns = ("Student", "Admission", "Class", "Stream", "Book", "Borrow Date", "Due Date")
    tree = ttk.Treeview(window, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100)
    tree.pack(padx=10, pady=10, fill="both", expand=True)

    try:
        with open('borrowed_books.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                tree.insert('', tk.END, values=row)
    except FileNotFoundError:
        messagebox.showinfo("Info", "No borrowed books recorded yet.")

def check_due_books():
    today = datetime.now().date()
    due_books = []

    try:
        with open('borrowed_books.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                try:
                    due_date = datetime.strptime(row[6], "%Y-%m-%d").date()
                    if due_date == today:
                        due_books.append(row)
                except (IndexError, ValueError):
                    continue
    except FileNotFoundError:
        return

    if due_books:
        msg = "Books due today:\n\n"
        for book in due_books:
            msg += f"{book[0]} ({book[1]}) - {book[4]}\n"
        messagebox.showinfo("Due Books", msg)
