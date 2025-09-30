import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
from plyer import notification
import winsound
import os
from tkcalendar import DateEntry
import csv
from notifications import notifier

# Configuration
DB_FILE = "library.db"
SOUND_FILE = "alert_tomorrow.mp3.mp3"

class LibraryDB:
    """Database handler for borrowing operations"""
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.create_tables()

    def create_tables(self):
        cursor = self.conn.cursor()
        # Do NOT recreate/override books schema here (books.py owns it).
        # Only ensure borrowed_books exists and uses TEXT book_id to match books.id (TEXT).
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id TEXT NOT NULL,
            student_name TEXT NOT NULL,
            admission_number TEXT NOT NULL,
            class TEXT NOT NULL,
            stream TEXT NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned INTEGER DEFAULT 0
        )
        """)
        self.conn.commit()

    # ---- CORE OPERATIONS ----
    def borrow_book(self, student_data, book_title, due_date):
        """Process book borrowing by title (kept for compatibility)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, quantity FROM books WHERE title=?", (book_title,))
        book = cursor.fetchone()
        if not book or int(book[1]) <= 0:
            raise ValueError("Book not available")

        # Check borrow limit
        cursor.execute("""
        SELECT COUNT(*) FROM borrowed_books
        WHERE admission_number=? AND returned=0
        """, (student_data['admission'],))
        if cursor.fetchone()[0] >= 3:
            raise ValueError("Maximum borrow limit (3 books) reached")

        borrow_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO borrowed_books (
            book_id, student_name, admission_number, class, stream,
            borrow_date, due_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            book[0], student_data['name'], student_data['admission'],
            student_data['class'], student_data['stream'],
            borrow_date, due_date
        ))

        # Update inventory
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id=?", (book[0],))
        self.conn.commit()
        return True

    def borrow_book_by_id(self, student_data, book_id, due_date):
        """Borrow using book ID (string)"""
        cursor = self.conn.cursor()
        # Check availability + get title
        cursor.execute("SELECT title, quantity FROM books WHERE id=?", (book_id,))
        row = cursor.fetchone()
        if not row or int(row[1]) <= 0:
            raise ValueError("Book not available")
        title, qty = row

        # Check borrow limit
        cursor.execute("""
        SELECT COUNT(*) FROM borrowed_books
        WHERE admission_number=? AND returned=0
        """, (student_data['admission'],))
        if cursor.fetchone()[0] >= 3:
            raise ValueError("Maximum borrow limit (3 books) reached")

        # Record borrowing
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        cursor.execute("""
        INSERT INTO borrowed_books (
            book_id, student_name, admission_number, class, stream,
            borrow_date, due_date
        ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            book_id, student_data['name'], student_data['admission'],
            student_data['class'], student_data['stream'],
            borrow_date, due_date
        ))

        # Update inventory and check post-update stock
        cursor.execute("UPDATE books SET quantity = quantity - 1 WHERE id=?", (book_id,))
        cursor.execute("SELECT quantity FROM books WHERE id=?", (book_id,))
        new_qty = int(cursor.fetchone()[0])
        self.conn.commit()

        # Low stock notification after borrow (threshold <= 2)
        try:
            if new_qty <= 2 and notifier:
                notifier.add_notification(
                    f"Low stock alert: {title} (only {new_qty} left)",
                    urgent=True
                )
        except Exception:
            pass

        return True

    def return_book(self, admission_number, book_title):
        """Process book return by title"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT bb.id, bb.book_id FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.admission_number=? AND b.title=? AND bb.returned=0
        """, (admission_number, book_title))
        record = cursor.fetchone()

        if not record:
            raise ValueError("No matching active borrowing found")

        # Mark as returned
        cursor.execute("UPDATE borrowed_books SET returned=1 WHERE id=?", (record[0],))
        # Restock
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id=?", (record[1],))
        self.conn.commit()
        return True

    def return_book_by_id(self, admission_number, book_id):
        """Return a book using its ID (string)"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT id FROM borrowed_books
        WHERE admission_number=? AND book_id=? AND returned=0
        """, (admission_number, book_id))
        record = cursor.fetchone()
        if not record:
            raise ValueError("No matching active borrowing found")
        cursor.execute("UPDATE borrowed_books SET returned=1 WHERE id=?", (record[0],))
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id=?", (book_id,))
        self.conn.commit()
        return True

    # ---- QUERY METHODS ----
    def get_available_books(self):
        """Get books with quantity > 0, return list of (id, title)"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT id, title FROM books WHERE quantity > 0")
        return cursor.fetchall()

    def get_borrowed_books(self):
        """Get all active borrowings"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT b.title, bb.student_name, bb.admission_number,
               bb.class, bb.stream, bb.borrow_date, bb.due_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.returned = 0
        """)
        return cursor.fetchall()

    def get_upcoming_returns(self, days=2):
        """Get books due between today and today+days"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        cursor.execute("""
        SELECT b.title, bb.student_name, bb.due_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.returned=0 AND bb.due_date BETWEEN ? AND ?
        ORDER BY bb.due_date ASC
        """, (today, future_date))
        return cursor.fetchall()

    def get_overdue_books(self):
        """Get books whose due_date is before today"""
        cursor = self.conn.cursor()
        cursor.execute("""
        SELECT b.title, bb.student_name, bb.due_date
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.returned=0 AND date(bb.due_date) < date('now')
        ORDER BY bb.due_date ASC
        """)
        return cursor.fetchall()

# --------------------------
# DASHBOARD-COMPATIBLE FUNCTIONS
# --------------------------
def record_borrowing_window():
    db = LibraryDB()
    all_books = db.get_available_books()  # List of (id, title)

    def update_book_options(*args):
        search_term = search_var.get().lower()
        filtered = [f"{bid} - {title}" for bid, title in all_books if search_term in title.lower() or search_term in str(bid)]
        book_menu['menu'].delete(0, 'end')
        if filtered:
            for opt in filtered:
                book_menu['menu'].add_command(label=opt, command=tk._setit(book_var, opt))
            book_var.set(filtered[0])
        else:
            book_menu['menu'].add_command(label="No books found", command=tk._setit(book_var, "No books found"))
            book_var.set("No books found")

    def submit_borrow():
        student_data = {
            'name': entry_name.get(),
            'admission': entry_admission.get(),
            'class': class_var.get(),
            'stream': entry_stream.get()
        }
        selected = book_var.get()
        if not selected or selected == "No books found":
            messagebox.showerror("Error", "No book selected!")
            return

        book_id = selected.split(" - ")[0]
        book_title = selected.split(" - ")[1]
        due_date_str = due_date_entry.get_date().strftime("%Y-%m-%d")

        try:
            if db.borrow_book_by_id(student_data, book_id, due_date_str):
                messagebox.showinfo("Success", "Book borrowed successfully!")
                record_borrowing_to_csv(student_data, book_id, book_title, datetime.now().strftime("%Y-%m-%d"), due_date_str)
                window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    window = tk.Toplevel()
    window.title("Record Borrowing")
    window.geometry("400x500")

    # Form fields
    tk.Label(window, text="Student Name").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Admission Number").grid(row=1, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Class").grid(row=2, column=0, padx=10, pady=5)
    class_var = tk.StringVar(value="Grade 1")
    class_menu = tk.OptionMenu(window, class_var, *[f"Grade {i}" for i in range(1, 9)] + [f"Form {i}" for i in range(1, 5)])
    class_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(window, text="Stream").grid(row=3, column=0, padx=10, pady=5)
    entry_stream = tk.Entry(window)
    entry_stream.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(window, text="Search Book").grid(row=4, column=0, padx=10, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(window, textvariable=search_var)
    search_entry.grid(row=4, column=1, padx=10, pady=5)
    search_var.trace("w", update_book_options)

    tk.Label(window, text="Book (ID - Title)").grid(row=5, column=0, padx=10, pady=5)
    book_var = tk.StringVar()
    book_options = [f"{bid} - {title}" for bid, title in all_books]
    if book_options:
        book_var.set(book_options[0])
        book_menu = tk.OptionMenu(window, book_var, *book_options)
    else:
        book_var.set("No books available")
        book_menu = tk.OptionMenu(window, book_var, "No books available")
    book_menu.grid(row=5, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(window, text="Borrow Date").grid(row=6, column=0, padx=10, pady=5)
    borrow_date = tk.Label(window, text=datetime.now().strftime("%Y-%m-%d"))
    borrow_date.grid(row=6, column=1, padx=10, pady=5)

    tk.Label(window, text="Due Date").grid(row=7, column=0, padx=10, pady=5)
    due_date_entry = DateEntry(window, date_pattern="yyyy-mm-dd",
                               mindate=datetime.now(),
                               width=18)
    due_date_entry.set_date(datetime.now() + timedelta(days=14))
    due_date_entry.grid(row=7, column=1, padx=10, pady=5)

    submit_btn = tk.Button(window, text="Submit", command=submit_borrow)
    submit_btn.grid(row=8, columnspan=2, pady=15)

    if not all_books:
        submit_btn.config(state="disabled")
        tk.Label(window, text="No books available to borrow.", fg="red").grid(row=9, columnspan=2, pady=10)

def return_book_window():
    """Book return window (dashboard-compatible)"""
    db = LibraryDB()

    def update_books(*args):
        admission = entry_admission.get()
        if not admission:
            book_menu['menu'].delete(0, 'end')
            book_var.set("")
            return
        cursor = db.conn.cursor()
        cursor.execute("""
            SELECT b.id, b.title FROM borrowed_books bb
            JOIN books b ON bb.book_id = b.id
            WHERE bb.admission_number=? AND bb.returned=0
        """, (admission,))
        borrowed = cursor.fetchall()
        book_options = [f"{bid} - {title}" for bid, title in borrowed]
        book_menu['menu'].delete(0, 'end')
        for opt in book_options:
            book_menu['menu'].add_command(label=opt, command=tk._setit(book_var, opt))
        if book_options:
            book_var.set(book_options[0])
        else:
            book_var.set("")

    def submit_return():
        admission = entry_admission.get()
        selected = book_var.get()
        if not selected:
            messagebox.showerror("Error", "No book selected!")
            return
        book_id = selected.split(" - ")[0]
        try:
            if db.return_book_by_id(admission, book_id):
                messagebox.showinfo("Success", "Book returned successfully!")
                window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

        # Optional: re-check overdues to notify (non-blocking)
        try:
            overdue_list = db.get_overdue_books()
            if overdue_list and notifier:
                for book_title, student_name, due_date in overdue_list:
                    notifier.add_notification(
                        f"{student_name} has overdue book: {book_title} (Due: {due_date})",
                        urgent=True
                    )
        except Exception:
            pass

    window = tk.Toplevel()
    window.title("Return Book")
    window.geometry("300x200")
    window.resizable(True, True)

    tk.Label(window, text="Admission Number").grid(row=0, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=0, column=1, padx=10, pady=5)
    entry_admission.bind("<FocusOut>", update_books)
    entry_admission.bind("<KeyRelease>", update_books)

    tk.Label(window, text="Book (ID - Title)").grid(row=1, column=0, padx=10, pady=5)
    book_var = tk.StringVar()
    book_menu = tk.OptionMenu(window, book_var, "")
    book_menu.grid(row=1, column=1, padx=10, pady=5, sticky="ew")

    tk.Button(window, text="Return Book", command=submit_return).grid(row=2, columnspan=2, pady=15)

def view_borrowed_books_window():
    """Display all borrowed books (dashboard-compatible)"""
    db = LibraryDB()
    borrowed_books = db.get_borrowed_books()

    window = tk.Toplevel()
    window.title("Borrowed Books")
    window.geometry("800x400")

    tree = ttk.Treeview(window, columns=("Title", "Student", "Admission", "Class", "Stream", "Borrowed", "Due"))
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)

    for i, col in enumerate(("Title", "Student", "Admission", "Class", "Stream", "Borrowed", "Due"), 1):
        tree.heading(f"#{i}", text=col)
        tree.column(f"#{i}", width=100)

    for book in borrowed_books:
        tree.insert("", tk.END, values=book)

    tree.pack(fill="both", expand=True)

def view_upcoming_returns():
    """Show upcoming returns (dashboard-compatible)"""
    db = LibraryDB()
    upcoming = db.get_upcoming_returns()

    if not upcoming:
        messagebox.showinfo("Upcoming Returns", "No books due in the next 2 days")
        return

    window = tk.Toplevel()
    window.title("Upcoming Returns")
    window.geometry("500x300")

    tree = ttk.Treeview(window, columns=("Title", "Student", "Due Date"))
    tree.heading("#0", text="ID")
    tree.column("#0", width=50)

    for i, col in enumerate(("Title", "Student", "Due Date"), 1):
        tree.heading(f"#{i}", text=col)
        tree.column(f"#{i}", width=150)

    for i, book in enumerate(upcoming, 1):
        tree.insert("", tk.END, text=str(i), values=book)

    tree.pack(fill="both", expand=True)

def check_due_alerts():
    """Check for overdue books and notify (dashboard-compatible)"""
    try:
        db = LibraryDB()
        overdue = db.get_overdue_books()  # strictly due_date < today

        if overdue:
            # In-app bell notifications (one per overdue)
            if notifier:
                for book_title, student_name, due_date in overdue:
                    try:
                        notifier.add_notification(
                            "Overdue Books",
                            f"{student_name} has overdue book: {book_title} (Due: {due_date})",
                            urgent=True
                        )
                    except Exception:
                        pass

            # System toast summary
            try:
                notification.notify(
                    title="Overdue Books",
                    message=f"{len(overdue)} books are overdue!",
                    timeout=10
                )
            except Exception:
                pass

            # Optional sound if file exists
            if os.path.exists(SOUND_FILE):
                try:
                    winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)
                except Exception:
                    pass
    except Exception:
        pass

def record_borrowing_to_csv(student_data, book_id, book_title, borrow_date, due_date):
    with open("borrowed_books.csv", "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([
            book_id,
            student_data['name'],
            student_data['admission'],
            student_data['class'],
            student_data['stream'],
            book_title,
            borrow_date,
            due_date
        ])
