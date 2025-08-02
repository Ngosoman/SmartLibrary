import json
import os
from datetime import datetime
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
import webbrowser

import csv

def generate_report():
    file_path = "borrowed_books.csv"

    if not os.path.exists(file_path):
        messagebox.showerror("Error", "No borrowed books CSV file found.")
        return

    data = []
    with open(file_path, "r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)

    if not data:
        messagebox.showinfo("Info", "No borrowed books to include in the report.")
        return

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", "B", 14)
    pdf.cell(200, 10, "SmartLibrary Borrowed Books Report", ln=True, align="C")

    pdf.set_font("Arial", size=10)
    pdf.ln(10)

    # Table headers
    headers = ["Name", "Adm No", "Class", "Stream", "Book Title", "Borrow Date", "Return Date"]
    col_widths = [30, 25, 20, 20, 40, 30, 30]

    for i, header in enumerate(headers):
        pdf.cell(col_widths[i], 10, header, 1, 0, 'C')
    pdf.ln()

    # Table rows
    for record in data:
        pdf.cell(col_widths[0], 10, record.get("student_name", ""), 1)
        pdf.cell(col_widths[1], 10, record.get("admission_number", ""), 1)
        pdf.cell(col_widths[2], 10, record.get("student_class", ""), 1)
        pdf.cell(col_widths[3], 10, record.get("student_stream", ""), 1)
        pdf.cell(col_widths[4], 10, record.get("book_title", "")[:20], 1)
        pdf.cell(col_widths[5], 10, record.get("borrow_date", ""), 1)
        pdf.cell(col_widths[6], 10, record.get("return_date", ""), 1)
        pdf.ln()

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"BorrowedBooksReport_{timestamp}.pdf"
    pdf.output(filename)
    webbrowser.open_new(rf"{filename}")

    messagebox.showinfo("Report Generated", f"Report saved as {filename}")


# Tkinter UI
def open_report_window():
    window = Tk()
    window.title("Generate Borrowed Books Report")
    window.geometry("400x200")
    window.configure(bg="#f2f2f2")

    label = Label(window, text="Click below to generate report:", font=("Arial", 12), bg="#f2f2f2")
    label.pack(pady=30)

    button = Button(window, text="Generate Report", command=generate_report, bg="green", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    button.pack()

    window.mainloop()

if __name__ == "__main__":
    open_report_window()
