import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

BOOKS_FILE = "books.csv"

# ------------------- Add Book -------------------
def add_book():
    add_window = tk.Toplevel()
    add_window.title("Add New Book")
    add_window.geometry("400x400")

    tk.Label(add_window, text="Add New Book", font=("Helvetica", 14, "bold")).pack(pady=10)

    tk.Label(add_window, text="Title:").pack()
    title_entry = tk.Entry(add_window, width=40)
    title_entry.pack(pady=5)

    tk.Label(add_window, text="Author:").pack()
    author_entry = tk.Entry(add_window, width=40)
    author_entry.pack(pady=5)

    tk.Label(add_window, text="Category:").pack()
    category = ttk.Combobox(add_window, values=["Textbook", "Novel", "Setbook", "Storybook"], state="readonly")
    category.pack(pady=5)
    category.set("Textbook")

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

        file_exists = os.path.isfile(BOOKS_FILE)
        with open(BOOKS_FILE, "a", newline="") as file:
            writer = csv.writer(file)
            if not file_exists:
                writer.writerow(["Title", "Author", "Category", "Quantity"])
            writer.writerow([title, author, cat, qty])

        messagebox.showinfo("Success", f"{qty} book(s) recorded successfully!")
        add_window.destroy()

    tk.Button(add_window, text="Save Book", command=save_book).pack(pady=15)

# ------------------- View Books -------------------
def view_books():
    if not os.path.isfile(BOOKS_FILE):
        messagebox.showerror("Error", "No books found.")
        return

    view_window = tk.Toplevel()
    view_window.title("Library Books")
    view_window.geometry("800x400")

    tk.Label(view_window, text="All Books in Library", font=("Helvetica", 14, "bold")).pack(pady=10)

    columns = ("Title", "Author", "Category", "Quantity")
    tree = ttk.Treeview(view_window, columns=columns, show="headings")

    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)

    tree.pack(expand=True, fill="both", padx=20, pady=10)

    # Load data
    with open(BOOKS_FILE, newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            tree.insert("", "end", values=(row["Title"], row["Author"], row["Category"], row["Quantity"]))

    # ---------------- Edit Book ----------------
    def edit_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to edit.")
            return

        item = tree.item(selected[0])
        values = item["values"]
        edit_window = tk.Toplevel()
        edit_window.title("Edit Book")
        edit_window.geometry("400x350")

        tk.Label(edit_window, text="Edit Book", font=("Helvetica", 14, "bold")).pack(pady=10)

        tk.Label(edit_window, text="Title:").pack()
        title_entry = tk.Entry(edit_window, width=40)
        title_entry.insert(0, values[0])
        title_entry.pack(pady=5)

        tk.Label(edit_window, text="Author:").pack()
        author_entry = tk.Entry(edit_window, width=40)
        author_entry.insert(0, values[1])
        author_entry.pack(pady=5)

        tk.Label(edit_window, text="Category:").pack()
        category = ttk.Combobox(edit_window, values=["Textbook", "Novel", "Setbook", "Storybook"], state="readonly")
        category.set(values[2])
        category.pack(pady=5)

        tk.Label(edit_window, text="Quantity:").pack()
        quantity_entry = tk.Entry(edit_window, width=10)
        quantity_entry.insert(0, values[3])
        quantity_entry.pack(pady=5)

        def save_changes():
            new_title = title_entry.get().strip()
            new_author = author_entry.get().strip()
            new_category = category.get().strip()
            new_quantity = quantity_entry.get().strip()

            if not new_title or not new_author or not new_quantity.isdigit():
                messagebox.showerror("Error", "Please fill all fields correctly.")
                return

            # Update in CSV
            updated_rows = []
            with open(BOOKS_FILE, newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    if row[0] == values[0] and row[1] == values[1]:
                        updated_rows.append([new_title, new_author, new_category, new_quantity])
                    else:
                        updated_rows.append(row)

            with open(BOOKS_FILE, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(headers)
                writer.writerows(updated_rows)

            messagebox.showinfo("Success", "Book updated successfully.")
            edit_window.destroy()
            view_window.destroy()
            view_books()

        tk.Button(edit_window, text="Save Changes", command=save_changes).pack(pady=15)

    # ---------------- Delete Book ----------------
    def delete_selected():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Warning", "Please select a book to delete.")
            return

        confirm = messagebox.askyesno("Confirm", "Are you sure you want to delete this book?")
        if not confirm:
            return

        item = tree.item(selected[0])
        values = item["values"]

        updated_rows = []
        with open(BOOKS_FILE, newline="") as file:
            reader = csv.reader(file)
            headers = next(reader)
            for row in reader:
                if row[0] == values[0] and row[1] == values[1]:
                    continue  # skip the book
                updated_rows.append(row)

        with open(BOOKS_FILE, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(headers)
            writer.writerows(updated_rows)

        messagebox.showinfo("Success", "Book deleted successfully.")
        view_window.destroy()
        view_books()

    # Buttons for edit and delete
    btn_frame = tk.Frame(view_window)
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="Edit Selected", command=edit_selected, bg="orange").pack(side="left", padx=10)
    tk.Button(btn_frame, text="Delete Selected", command=delete_selected, bg="red", fg="white").pack(side="left", padx=10)
