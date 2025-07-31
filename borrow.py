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

def return_book_window():
    return_win = tk.Toplevel()
    return_win.title("Return Book")
    return_win.geometry("700x400")

    tk.Label(return_win, text="📚 Return Book", font=("Helvetica", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(return_win, columns=("ID", "Student", "Book", "Borrowed On", "Return By"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Student", text="Student Name")
    tree.heading("Book", text="Book Title")
    tree.heading("Borrowed On", text="Borrowed On")
    tree.heading("Return By", text="Return By")
    tree.pack(pady=10, fill="both", expand=True)

    # Load borrowed books from database
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, student_name, book_title, borrow_date, return_date FROM borrow WHERE returned = 0")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        tree.insert("", tk.END, values=row)

    def return_selected_book():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("No selection", "Please select a book to return.")
            return

        item = tree.item(selected)
        borrow_id = item["values"][0]

        conn = sqlite3.connect("library.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE borrow SET returned = 1 WHERE id = ?", (borrow_id,))
        conn.commit()
        conn.close()

        tree.delete(selected)
        messagebox.showinfo("Success", "Book marked as returned.")

    tk.Button(return_win, text="✅ Mark as Returned", command=return_selected_book).pack(pady=10)

def view_borrowed_books_window():
    view_win = tk.Toplevel()
    view_win.title("All Borrowed Books")
    view_win.geometry("800x400")

    tk.Label(view_win, text="📖 All Borrowed Books", font=("Helvetica", 14, "bold")).pack(pady=10)

    tree = ttk.Treeview(view_win, columns=("ID", "Student", "Book", "Borrowed On", "Return By", "Status"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Student", text="Student Name")
    tree.heading("Book", text="Book Title")
    tree.heading("Borrowed On", text="Borrowed On")
    tree.heading("Return By", text="Return By")
    tree.heading("Status", text="Status")
    tree.pack(pady=10, fill="both", expand=True)

    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT id, student_name, book_title, borrow_date, return_date, returned FROM borrow")
    rows = cursor.fetchall()
    conn.close()

    for row in rows:
        status = "✅ Returned" if row[5] == 1 else "❌ Pending"
        tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], status))
