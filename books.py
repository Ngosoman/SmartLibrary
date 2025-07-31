import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

def add_book():
    add_window = tk.Toplevel()
    add_window.title("Add New Book")
    add_window.geometry("400x400")

    tk.Label(add_window, text="Add New Book", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Book Title
    tk.Label(add_window, text="Title:").pack()
    title_entry = tk.Entry(add_window, width=40)
    title_entry.pack(pady=5)

    # Author
    tk.Label(add_window, text="Author:").pack()
    author_entry = tk.Entry(add_window, width=40)
    author_entry.pack(pady=5)

    # Category Dropdown
    tk.Label(add_window, text="Category:").pack()
    category = ttk.Combobox(add_window, values=["Textbook", "Novel", "Setbook", "Storybook"], state="readonly")
    category.pack(pady=5)
    category.set("Textbook")

    # Quantity
    tk.Label(add_window, text="Quantity:").pack()
    quantity_entry = tk.Entry(add_window, width=10)
    quantity_entry.pack(pady=5)

    def save_book():
        title = title_entry.get().strip()
        author = author_entry.get().strip()
        cat = category.get().strip()
        qty = quantity_entry.get().strip()

        if not title or not author or not qty.isdigit():
            messagebox.showerror("Error", "Please fill all fields correctly.")
            return

        qty = int(qty)

        file_exists = os.path.isfile("books.csv")
        with open("books.csv", "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Title", "Author", "Category", "Quantity"])
            writer.writerow([title, author, cat, qty])

        messagebox.showinfo("Success", f"{qty} book(s) recorded successfully!")
        add_window.destroy()

    tk.Button(add_window, text="Save Book", command=save_book).pack(pady=15)

def view_books():
    if not os.path.isfile("books.csv"):
        messagebox.showerror("Error", "No books found.")
        return

    view_window = tk.Toplevel()
    view_window.title("View All Books")
    view_window.geometry("700x400")

    tk.Label(view_window, text="Library Books", font=("Helvetica", 14, "bold")).pack(pady=10)

    # Treeview to show books
    columns = ("Title", "Author", "Category", "Quantity")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")
    
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(expand=True, fill="both", padx=20, pady=10)

    # Load books from CSV
    with open("books.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tree.insert("", "end", values=(row["Title"], row["Author"], row["Category"], row["Quantity"]))
            