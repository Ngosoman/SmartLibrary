import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib import colors
from datetime import datetime
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
import webbrowser
import csv

def generate_report(selected_grade="All", selected_class="All"):
    filename = f"BorrowedBooksReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open("borrowed_books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)

            if not data:
                print("CSV file is empty.")
                return

            # Updated headers to include Book ID
            headers = ["Book ID", "Student Name", "Admission No", "Class", "Stream", "Book Title", "Borrow Date", "Due Date"]

            # Filter data
            filtered_data = []
            for row in data:
                row_grade = row[3] if len(row) > 3 else ""  # Adjust index if needed
                row_class = row[3] if len(row) > 3 else ""
                grade_match = (selected_grade == "All") or (row_grade == selected_grade)
                class_match = (selected_class == "All") or (row_class == selected_class)
                if grade_match and class_match:
                    filtered_data.append(row)

            # Prepare table data
            table_data = [headers] + filtered_data

            # Create PDF with table
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            table = Table(table_data, repeatRows=1)
            table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.grey),
                ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 12),
                ('BOTTOMPADDING', (0,0), (-1,0), 8),
                ('GRID', (0,0), (-1,-1), 0.5, colors.black),
            ]))
            elements = [table]
            doc.build(elements)
            print(f"Report saved as {filename}")
            webbrowser.open_new(rf"{filepath}")

    except FileNotFoundError:
        print("borrowed_books.csv file not found.")

# Tkinter UI
def open_report_window():
    window = Tk()
    window.title("Generate Borrowed Books Report")
    window.geometry("400x300")
    window.configure(bg="#f2f2f2")

    Label(window, text="Generate Borrowed Books Report", font=("Arial", 14, "bold"), bg="#f2f2f2").pack(pady=10)

    # Grade/Class filter options
    filter_frame = Frame(window, bg="#f2f2f2")
    filter_frame.pack(pady=10)

    Label(filter_frame, text="Grade:", bg="#f2f2f2").grid(row=0, column=0, padx=5)
    grade_var = StringVar(value="All")
    grades = ["All"] + [f"Grade {i}" for i in range(1, 9)]
    grade_menu = OptionMenu(filter_frame, grade_var, *grades)
    grade_menu.grid(row=0, column=1, padx=5)

    Label(filter_frame, text="Class:", bg="#f2f2f2").grid(row=0, column=2, padx=5)
    class_var = StringVar(value="All")
    classes = ["All"] + [f"Form {i}" for i in range(1, 5)]
    class_menu = OptionMenu(filter_frame, class_var, *classes)
    class_menu.grid(row=0, column=3, padx=5)

    def on_generate():
        generate_report(grade_var.get(), class_var.get())

    button = Button(window, text="Generate Report", command=on_generate, bg="green", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    button.pack(pady=20)

    window.mainloop()

if __name__ == "__main__":
    open_report_window()
