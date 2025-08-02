import json
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from datetime import datetime
from fpdf import FPDF
from tkinter import *
from tkinter import messagebox
import webbrowser
import csv

def generate_report():
    filename = f"BorrowedBooksReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open("borrowed_books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)

            if not data:
                print("CSV file is empty.")
                return

            # If no header row, add headers manually
            headers = ["Student Name", "Admission No", "Class", "Stream", "Book Title", "Borrow Date", "Return Date"]

            c = canvas.Canvas(filepath, pagesize=A4)
            c.setFont("Helvetica-Bold", 14)
            c.drawString(200, 800, "Borrowed Books Report")

            c.setFont("Helvetica", 10)
            y = 770

            # Print headers
            for i, header in enumerate(headers):
                c.drawString(50 + i * 80, y, header)

            y -= 20

            # Print data rows
            for row in data:
                for i, cell in enumerate(row):
                    c.drawString(50 + i * 80, y, str(cell))
                y -= 20
                if y < 50:
                    c.showPage()
                    y = 800

            c.save()
            print(f"Report saved as {filename}")
            webbrowser.open_new(rf"{filepath}")

    except FileNotFoundError:
        print("borrowed_books.csv file not found.")

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
