import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime, timedelta
from plyer import notification
import winsound
import os

# Configuration
DB_FILE = "library.db"
SOUND_FILE = "alert_tomorrow.mp3.mp3"

class LibraryDB:
    """Database handler for all library operations"""
    
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.create_tables()
        
    def create_tables(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            quantity INTEGER DEFAULT 1 CHECK(quantity >= 0)
        )""")
        
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS borrowed_books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            book_id INTEGER NOT NULL,
            student_name TEXT NOT NULL,
            admission_number TEXT NOT NULL,
            class TEXT NOT NULL,
            stream TEXT NOT NULL,
            borrow_date TEXT NOT NULL,
            due_date TEXT NOT NULL,
            returned INTEGER DEFAULT 0,
            FOREIGN KEY(book_id) REFERENCES books(id)
        )""")
        self.conn.commit()

    # ---- CORE OPERATIONS ----
    def borrow_book(self, student_data, book_title):
        """Process book borrowing"""
        cursor = self.conn.cursor()
        
        # Get book ID and check availability
        cursor.execute("SELECT id, quantity FROM books WHERE title=?", (book_title,))
        book = cursor.fetchone()
        if not book or book[1] <= 0:
            raise ValueError("Book not available")
        
        # Check borrow limit
        cursor.execute("""
        SELECT COUNT(*) FROM borrowed_books 
        WHERE admission_number=? AND returned=0
        """, (student_data['admission'],))
        if cursor.fetchone()[0] >= 3:
            raise ValueError("Maximum borrow limit (3 books) reached")
        
        # Record borrowing
        borrow_date = datetime.now().strftime("%Y-%m-%d")
        due_date = (datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d")
        
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

    def return_book(self, admission_number, book_title):
        """Process book return"""
        cursor = self.conn.cursor()
        
        # Find the borrowing record
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
        
        # Restock book
        cursor.execute("UPDATE books SET quantity = quantity + 1 WHERE id=?", (record[1],))
        self.conn.commit()
        return True

    # ---- QUERY METHODS ----
    def get_available_books(self):
        """Get books with quantity > 0"""
        cursor = self.conn.cursor()
        cursor.execute("SELECT title FROM books WHERE quantity > 0")
        return [book[0] for book in cursor.fetchall()]
    
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
        """Get books due in next X days"""
        cursor = self.conn.cursor()
        today = datetime.now().strftime("%Y-%m-%d")
        future_date = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
        
        cursor.execute("""
        SELECT b.title, bb.student_name, bb.due_date 
        FROM borrowed_books bb
        JOIN books b ON bb.book_id = b.id
        WHERE bb.returned=0 AND bb.due_date BETWEEN ? AND ?
        """, (today, future_date))
        return cursor.fetchall()

# --------------------------
# DASHBOARD-COMPATIBLE FUNCTIONS
# --------------------------
def record_borrowing_window():
    """Main borrowing window (dashboard-compatible)"""
    db = LibraryDB()
    available_books = db.get_available_books()

    def submit_borrow():
        student_data = {
            'name': entry_name.get(),
            'admission': entry_admission.get(),
            'class': class_var.get(),
            'stream': entry_stream.get()
        }
        book_title = book_var.get()
        if not book_title:
            messagebox.showerror("Error", "No book selected!")
            return
        try:
            if db.borrow_book(student_data, book_title):
                messagebox.showinfo("Success", "Book borrowed successfully!")
                window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    window = tk.Toplevel()
    window.title("Record Borrowing")
    window.geometry("400x450")

    # Form fields
    tk.Label(window, text="Student Name").grid(row=0, column=0, padx=10, pady=5)
    entry_name = tk.Entry(window)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(window, text="Admission Number").grid(row=1, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(window, text="Class").grid(row=2, column=0, padx=10, pady=5)
    class_var = tk.StringVar(value="Grade 1")
    class_menu = tk.OptionMenu(window, class_var, *[f"Grade {i}" for i in range(1,9)] + [f"Form {i}" for i in range(1,5)])
    class_menu.grid(row=2, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(window, text="Stream").grid(row=3, column=0, padx=10, pady=5)
    entry_stream = tk.Entry(window)
    entry_stream.grid(row=3, column=1, padx=10, pady=5)

    tk.Label(window, text="Book Title").grid(row=4, column=0, padx=10, pady=5)
    book_var = tk.StringVar()
    if available_books:
        book_var.set(available_books[0])  # Set default selection
    book_menu = tk.OptionMenu(window, book_var, *available_books)
    book_menu.grid(row=4, column=1, padx=10, pady=5, sticky="ew")

    tk.Label(window, text="Borrow Date").grid(row=5, column=0, padx=10, pady=5)
    borrow_date = tk.Label(window, text=datetime.now().strftime("%Y-%m-%d"))
    borrow_date.grid(row=5, column=1, padx=10, pady=5)

    tk.Label(window, text="Due Date").grid(row=6, column=0, padx=10, pady=5)
    due_date = tk.Label(window, text=(datetime.now() + timedelta(days=14)).strftime("%Y-%m-%d"))
    due_date.grid(row=6, column=1, padx=10, pady=5)

    submit_btn = tk.Button(window, text="Submit", command=submit_borrow)
    submit_btn.grid(row=7, columnspan=2, pady=15)

    if not available_books:
        submit_btn.config(state="disabled")
        tk.Label(window, text="No books available to borrow.", fg="red").grid(row=8, columnspan=2, pady=10)

def return_book_window():
    """Book return window (dashboard-compatible)"""
    db = LibraryDB()
    
    def submit_return():
        admission = entry_admission.get()
        book_title = book_var.get()
        
        try:
            if db.return_book(admission, book_title):
                messagebox.showinfo("Success", "Book returned successfully!")
                window.destroy()
        except Exception as e:
            messagebox.showerror("Error", str(e))
    
    window = tk.Toplevel()
    window.title("Return Book")
    window.geometry("300x200")
    
    tk.Label(window, text="Admission Number").grid(row=0, column=0, padx=10, pady=5)
    entry_admission = tk.Entry(window)
    entry_admission.grid(row=0, column=1, padx=10, pady=5)
    
    tk.Label(window, text="Book Title").grid(row=1, column=0, padx=10, pady=5)
    book_var = tk.StringVar()
    book_menu = tk.OptionMenu(window, book_var, *db.get_available_books())
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
    """Check for overdue books (dashboard-compatible)"""
    db = LibraryDB()
    overdue = db.get_upcoming_returns(days=0)  # Books due yesterday or earlier
    
    if overdue:
        notification.notify(
            title="Overdue Books",
            message=f"{len(overdue)} books are overdue!",
            timeout=10
        )
        if os.path.exists(SOUND_FILE):
            winsound.PlaySound(SOUND_FILE, winsound.SND_ASYNC)