# borrow.py
import tkinter as tk
from tkinter import messagebox
import csv
from datetime import datetime

def record_borrowing_window():
    def submit_borrow():
        student = entry_student.get()
        book_title = entry_book.get()
        date_borrowed = entry_borrow_date.get()
        date_due = entry_due_date.get()

        if not student or not book_title or not date_borrowed or not date_due:
            messagebox.showerror("Missing Info", "Please fill in all fields")
            return

        # Check if the book exists and has stock
        found = False
        updated_books = []
        with open('books.csv', 'r', newline='') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0].lower() == book_title.lower():
                    found = True
                    try:
                        quantity = int(row[4])
                        if quantity > 0:
                            row[4] = str(quantity - 1)
                        else:
                            messagebox.showerror("Out of Stock", "No copies available.")
                            return
                    except ValueError:
                        messagebox.showerror("Invalid Quantity", "Book quantity error.")
                        return
                updated_books.append(row)

        if not found:
            messagebox.showerror("Not Found", "Book not found in library.")
            return

        # Save borrow record
        with open("borrowed_books.csv", "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([student, book_title, date_borrowed, date_due])

        # Update books.csv stock
        with open("books.csv", "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(updated_books)

        messagebox.showinfo("Success", "Borrowing recorded successfully.")
        borrow_window.destroy()

    borrow_window = tk.Toplevel()
    borrow_window.title("Record Borrowing")
    borrow_window.geometry("400x300")

    tk.Label(borrow_window, text="Student Name").pack()
    entry_student = tk.Entry(borrow_window)
    entry_student.pack()

    tk.Label(borrow_window, text="Book Title").pack()
    entry_book = tk.Entry(borrow_window)
    entry_book.pack()

    tk.Label(borrow_window, text="Date Borrowed (YYYY-MM-DD)").pack()
    entry_borrow_date = tk.Entry(borrow_window)
    entry_borrow_date.insert(0, datetime.now().strftime("%Y-%m-%d"))
    entry_borrow_date.pack()

    tk.Label(borrow_window, text="Return Date (YYYY-MM-DD)").pack()
    entry_due_date = tk.Entry(borrow_window)
    entry_due_date.pack()

    tk.Button(borrow_window, text="Submit", command=submit_borrow).pack(pady=10)
