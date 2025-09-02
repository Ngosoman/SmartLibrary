import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
import datetime
from datetime import datetime
import os
from uuid import uuid4
from notifications import notifier



DB_FILE = "library.db"

class BookManager:
    def __init__(self):
        self.conn = sqlite3.connect(DB_FILE)
        self.create_table()
    
    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            category TEXT NOT NULL,
            quantity INTEGER NOT NULL CHECK(quantity >= 0),
            date_added TEXT NOT NULL
        )
        """)
        self.conn.commit()
    
    def add_book(self, book_data):
        cursor = self.conn.cursor()
        try:
            cursor.execute("""
            INSERT INTO books (id, title, author, category, quantity, date_added)
            VALUES (?, ?, ?, ?, ?, ?)
            """, (
                book_data['id'],
                book_data['title'],
                book_data['author'],
                book_data['category'],
                book_data['quantity'],
                datetime.now().strftime("%Y-%m-%d")
            ))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def get_all_books(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM books ORDER BY title")
        return cursor.fetchall()
    
    def update_book(self, book_id, updates):
        cursor = self.conn.cursor()
        cursor.execute("""
        UPDATE books 
        SET title=?, author=?, category=?, quantity=?
        WHERE id=?
        """, (
            updates['title'],
            updates['author'],
            updates['category'],
            updates['quantity'],
            book_id
        ))
        self.conn.commit()
        return cursor.rowcount > 0
        if updates['quantity'] < 5:  # Threshold for low stock
         notifier.add_notification(
            f"Low stock alert: {book_title} (only {updates['quantity']} left)",
            urgent=True
        )
    
    def delete_book(self, book_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM books WHERE id=?", (book_id,))
        self.conn.commit()
        return cursor.rowcount > 0

# ------------------- Add Book Window -------------------
def add_book_window():
    def generate_book_id():
        return str(uuid4())[:8].upper()  # Short unique ID

    def save_book():
        # Automatic ID generation if not provided
        book_id = id_entry.get().strip() or generate_book_id()
        book_data = {
            'id': book_id,
            'title': title_entry.get().strip(),
            'author': author_entry.get().strip(),
            'category': category.get(),
            'quantity': quantity_entry.get().strip()
        }

        # Validation
        if not all([book_data['id'], book_data['title'], book_data['author'], book_data['category'], book_data['quantity']]):
            messagebox.showerror("Error", "All fields are required!")
            return

        try:
            book_data['quantity'] = int(book_data['quantity'])
            if book_data['quantity'] < 1:
                messagebox.showerror("Error", "Quantity must be at least 1")
                return
        except ValueError:
            messagebox.showerror("Error", "Quantity must be a number")
            return

        # Save to database
        db = BookManager()
        if db.add_book(book_data):
            messagebox.showinfo("Success", 
                f"Book added successfully!\nBook ID: {book_data['id']}")
            add_win.destroy()
        else:
            messagebox.showerror("Error", "Failed to add book. ID may already exist.")

    add_win = tk.Toplevel()
    add_win.title("Add New Book")
    add_win.geometry("400x450")

    # Form fields
    tk.Label(add_win, text="Add New Book", font=("Helvetica", 14, "bold")).pack(pady=10)

    tk.Label(add_win, text="Book ID (optional):").pack()
    id_entry = tk.Entry(add_win, width=20)
    id_entry.insert(0, generate_book_id())
    id_entry.pack(pady=5)

    tk.Label(add_win, text="Title:").pack()
    title_entry = tk.Entry(add_win, width=40)
    title_entry.pack(pady=5)

    tk.Label(add_win, text="Author:").pack()
    author_entry = tk.Entry(add_win, width=40)
    author_entry.pack(pady=5)

    tk.Label(add_win, text="Category:").pack()
    category = ttk.Combobox(add_win, 
                          values=["Textbook", "Novel", "Setbook", "Storybook", "Reference"],
                          state="readonly")
    category.set("Textbook")
    category.pack(pady=5)

    tk.Label(add_win, text="Quantity:").pack()
    quantity_entry = tk.Entry(add_win, width=10)
    quantity_entry.insert(0, "1")
    quantity_entry.pack(pady=5)

    tk.Button(add_win, text="Generate New ID", 
             command=lambda: id_entry.delete(0, tk.END) or id_entry.insert(0, generate_book_id())).pack(pady=5)

    tk.Button(add_win, text="Save Book", command=save_book).pack(pady=15)

# ------------------- View Books Window -------------------
def view_books():
    db = BookManager()
    all_books = db.get_all_books()
    
    view_win = tk.Toplevel()
    view_win.title("Library Books")
    view_win.geometry("1000x500")
    
    # Treeview setup
    tree = ttk.Treeview(view_win, columns=("id", "title", "author", "category", "quantity", "date_added"), show="headings")
    tree.heading("id", text="Book ID")
    tree.heading("title", text="Title")
    tree.heading("author", text="Author")
    tree.heading("category", text="Category")
    tree.heading("quantity", text="Qty")
    tree.heading("date_added", text="Date Added")
    
    tree.column("id", width=100, anchor="center")
    tree.column("title", width=250)
    tree.column("author", width=200)
    tree.column("category", width=120, anchor="center")
    tree.column("quantity", width=60, anchor="center")
    tree.column("date_added", width=100, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Populate data
    for book in all_books:
        tree.insert("", "end", values=book)
    
    # Action buttons frame
    btn_frame = tk.Frame(view_win)
    btn_frame.pack(pady=10)
    
    def edit_book():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return
        
        book_data = tree.item(selected)['values']
        edit_win = tk.Toplevel()
        edit_win.title(f"Edit Book {book_data[0]}")
        edit_win.geometry("400x450")
        
        # Form fields with current values
        tk.Label(edit_win, text=f"Edit Book: {book_data[0]}", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        tk.Label(edit_win, text="Book ID:").pack()
        tk.Label(edit_win, text=book_data[0]).pack(pady=5)
        
        tk.Label(edit_win, text="Title:").pack()
        title_entry = tk.Entry(edit_win, width=40)
        title_entry.insert(0, book_data[1])
        title_entry.pack(pady=5)
        
        tk.Label(edit_win, text="Author:").pack()
        author_entry = tk.Entry(edit_win, width=40)
        author_entry.insert(0, book_data[2])
        author_entry.pack(pady=5)
        
        tk.Label(edit_win, text="Category:").pack()
        category = ttk.Combobox(edit_win, 
                              values=["Textbook", "Novel", "Setbook", "Storybook", "Reference"],
                              state="readonly")
        category.set(book_data[3])
        category.pack(pady=5)
        
        tk.Label(edit_win, text="Quantity:").pack()
        quantity_entry = tk.Entry(edit_win, width=10)
        quantity_entry.insert(0, book_data[4])
        quantity_entry.pack(pady=5)
        
        def save_changes():
            updates = {
                'title': title_entry.get().strip(),
                'author': author_entry.get().strip(),
                'category': category.get(),
                'quantity': quantity_entry.get().strip()
            }
            
            # Validation
            if not all(updates.values()):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                updates['quantity'] = int(updates['quantity'])
                if updates['quantity'] < 0:
                    messagebox.showerror("Error", "Quantity cannot be negative")
                    return
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
                return
            
            if db.update_book(book_data[0], updates):
                messagebox.showinfo("Success", "Book updated successfully!")
                edit_win.destroy()
                view_win.destroy()
                view_books()
            else:
                messagebox.showerror("Error", "Failed to update book")
        
        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=15)
    
    def delete_book():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return
        
        book_id = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete book {book_id}?")
        if confirm:
            if db.delete_book(book_id):
                messagebox.showinfo("Success", "Book deleted successfully")
                view_win.destroy()
                view_books()
            else:
                messagebox.showerror("Error", "Failed to delete book")
    
    # Action buttons
    tk.Button(btn_frame, text="Edit Selected", command=edit_book, 
             bg="orange", fg="white").pack(side="left", padx=10)
    tk.Button(btn_frame, text="Delete Selected", command=delete_book,
             bg="red", fg="white").pack(side="left", padx=10)
    tk.Button(btn_frame, text="Refresh List", 
             command=lambda: [view_win.destroy(), view_books()]).pack(side="left", padx=10)

# Helper function to get current datetime
def datetime_now():
    from datetime import datetime
    return datetime.now()


# ------------------- View Books Window -------------------
def view_books():
    db = BookManager()
    all_books = db.get_all_books()
    
    view_win = tk.Toplevel()
    view_win.title("Library Books")
    view_win.geometry("1000x500")
    
    # Treeview setup
    tree = ttk.Treeview(view_win, columns=("id", "title", "author", "category", "quantity", "date_added"), show="headings")
    tree.heading("id", text="Book ID")
    tree.heading("title", text="Title")
    tree.heading("author", text="Author")
    tree.heading("category", text="Category")
    tree.heading("quantity", text="Qty")
    tree.heading("date_added", text="Date Added")
    
    tree.column("id", width=100, anchor="center")
    tree.column("title", width=250)
    tree.column("author", width=200)
    tree.column("category", width=120, anchor="center")
    tree.column("quantity", width=60, anchor="center")
    tree.column("date_added", width=100, anchor="center")
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(view_win, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    scrollbar.pack(side="right", fill="y")
    tree.pack(fill="both", expand=True, padx=10, pady=10)
    
    # Populate data
    for book in all_books:
        tree.insert("", "end", values=book)
    
    # Action buttons frame
    btn_frame = tk.Frame(view_win)
    btn_frame.pack(pady=10)
    
    def edit_book():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return
        
        book_data = tree.item(selected)['values']
        edit_win = tk.Toplevel()
        edit_win.title(f"Edit Book {book_data[0]}")
        edit_win.geometry("400x450")
        
        # Form fields with current values
        tk.Label(edit_win, text=f"Edit Book: {book_data[0]}", font=("Helvetica", 14, "bold")).pack(pady=10)
        
        tk.Label(edit_win, text="Book ID:").pack()
        tk.Label(edit_win, text=book_data[0]).pack(pady=5)
        
        tk.Label(edit_win, text="Title:").pack()
        title_entry = tk.Entry(edit_win, width=40)
        title_entry.insert(0, book_data[1])
        title_entry.pack(pady=5)
        
        tk.Label(edit_win, text="Author:").pack()
        author_entry = tk.Entry(edit_win, width=40)
        author_entry.insert(0, book_data[2])
        author_entry.pack(pady=5)
        
        tk.Label(edit_win, text="Category:").pack()
        category = ttk.Combobox(edit_win, 
                              values=["Textbook", "Novel", "Setbook", "Storybook", "Reference"],
                              state="readonly")
        category.set(book_data[3])
        category.pack(pady=5)
        
        tk.Label(edit_win, text="Quantity:").pack()
        quantity_entry = tk.Entry(edit_win, width=10)
        quantity_entry.insert(0, book_data[4])
        quantity_entry.pack(pady=5)
        
        def save_changes():
            updates = {
                'title': title_entry.get().strip(),
                'author': author_entry.get().strip(),
                'category': category.get(),
                'quantity': quantity_entry.get().strip()
            }
            
            # Validation
            if not all(updates.values()):
                messagebox.showerror("Error", "All fields are required!")
                return
            
            try:
                updates['quantity'] = int(updates['quantity'])
                if updates['quantity'] < 0:
                    messagebox.showerror("Error", "Quantity cannot be negative")
                    return
            except ValueError:
                messagebox.showerror("Error", "Quantity must be a number")
                return
            
            if db.update_book(book_data[0], updates):
                messagebox.showinfo("Success", "Book updated successfully!")
                edit_win.destroy()
                view_win.destroy()
                view_books()
            else:
                messagebox.showerror("Error", "Failed to update book")
        
        tk.Button(edit_win, text="Save Changes", command=save_changes).pack(pady=15)
    
    def delete_book():
        selected = tree.focus()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book first")
            return
        
        book_id = tree.item(selected)['values'][0]
        confirm = messagebox.askyesno("Confirm Delete", 
                                    f"Are you sure you want to delete book {book_id}?")
        if confirm:
            if db.delete_book(book_id):
                messagebox.showinfo("Success", "Book deleted successfully")
                view_win.destroy()
                view_books()
            else:
                messagebox.showerror("Error", "Failed to delete book")
    
    # Action buttons
    tk.Button(btn_frame, text="Edit Selected", command=edit_book, 
             bg="orange", fg="white").pack(side="left", padx=10)
    tk.Button(btn_frame, text="Delete Selected", command=delete_book,
             bg="red", fg="white").pack(side="left", padx=10)
    tk.Button(btn_frame, text="Refresh List", 
             command=lambda: [view_win.destroy(), view_books()]).pack(side="left", padx=10)

# Helper function to get current datetime
def datetime_now():
    from datetime import datetime
    return datetime.now()

def check_stock_levels():
    db = BookManager()
    low_stock = db.get_low_stock_books(threshold=3)

    for book in low_stock:
        # book tuple: (id, title, author, category, quantity, date_added)
        try:
            if notifier:
                notifier.add_notification(
                    f"Low stock alert: {book[1]} (only {book[4]} left)",
                    urgent=True
                )
        except Exception:
            pass