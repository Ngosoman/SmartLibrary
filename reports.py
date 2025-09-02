import os
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime, date
from tkinter import *
from tkinter import messagebox
import webbrowser
import csv

def generate_report(selected_grade="All", selected_stream="All"):
    filename = f"BorrowedBooksReport_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    filepath = os.path.join(os.getcwd(), filename)

    try:
        with open("borrowed_books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            data = list(reader)

            if not data or len(data) < 2:
                messagebox.showwarning("Warning", "No borrowed book records found.")
                return

            headers = ["Book ID", "Student Name", "Admission No", "Class", "Stream", "Book Title", "Borrow Date", "Due Date"]

            # Borrowing History Filter
            filtered_history = []
            for row in data[1:]:  # skip headers
                grade = row[3] if len(row) > 3 else ""
                stream = row[4] if len(row) > 4 else ""
                grade_match = (selected_grade == "All") or (grade == selected_grade)
                stream_match = (selected_stream == "All") or (stream == selected_stream)
                if grade_match and stream_match:
                    filtered_history.append(row)

            # Overdue Filter
            overdue = []
            today = date.today()
            for row in filtered_history:
                try:
                    due_date = datetime.strptime(row[7], "%Y-%m-%d").date()
                    if due_date < today:
                        overdue.append(row)
                except Exception:
                    continue

            # Build PDF
            doc = SimpleDocTemplate(filepath, pagesize=A4)
            styles = getSampleStyleSheet()
            elements = []

            # Title
            elements.append(Paragraph("📚 Borrowed Books Report", styles["Title"]))
            elements.append(Spacer(1, 12))

            # Borrowing History Section
            elements.append(Paragraph("Borrowing History", styles["Heading2"]))
            if filtered_history:
                history_table = Table([headers] + filtered_history, repeatRows=1)
                history_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.grey),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(history_table)
            else:
                elements.append(Paragraph("No borrowing records found for this filter.", styles["Normal"]))

            elements.append(Spacer(1, 20))

            # Overdue Section
            elements.append(Paragraph("Overdue Books", styles["Heading2"]))
            if overdue:
                overdue_table = Table([headers] + overdue, repeatRows=1)
                overdue_table.setStyle(TableStyle([
                    ('BACKGROUND', (0,0), (-1,0), colors.red),
                    ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                    ('ALIGN', (0,0), (-1,-1), 'LEFT'),
                    ('GRID', (0,0), (-1,-1), 0.5, colors.black),
                ]))
                elements.append(overdue_table)
            else:
                elements.append(Paragraph("No overdue books for this filter.", styles["Normal"]))

            doc.build(elements)
            messagebox.showinfo("Success", f"Report saved as {filename}")
            webbrowser.open_new(rf"{filepath}")

    except FileNotFoundError:
        messagebox.showerror("Error", "borrowed_books.csv file not found.")


def open_report_window():
    window = Tk()
    window.title("Generate Borrowed Books Report")
    window.geometry("400x300")
    window.configure(bg="#f2f2f2")

    Label(window, text="Generate Borrowed Books Report", font=("Arial", 14, "bold"), bg="#f2f2f2").pack(pady=10)

    # Read CSV to get available Grades & Streams dynamically
    grades = {"All"}
    streams = {"All"}
    try:
        with open("borrowed_books.csv", "r", newline="", encoding="utf-8") as file:
            reader = csv.reader(file)
            next(reader)  # skip header
            for row in reader:
                if len(row) > 3: grades.add(row[3])
                if len(row) > 4: streams.add(row[4])
    except:
        pass

    filter_frame = Frame(window, bg="#f2f2f2")
    filter_frame.pack(pady=10)

    Label(filter_frame, text="Grade:", bg="#f2f2f2").grid(row=0, column=0, padx=5)
    grade_var = StringVar(value="All")
    grade_menu = OptionMenu(filter_frame, grade_var, *sorted(grades))
    grade_menu.grid(row=0, column=1, padx=5)

    Label(filter_frame, text="Stream:", bg="#f2f2f2").grid(row=0, column=2, padx=5)
    stream_var = StringVar(value="All")
    stream_menu = OptionMenu(filter_frame, stream_var, *sorted(streams))
    stream_menu.grid(row=0, column=3, padx=5)

    def on_generate():
        generate_report(grade_var.get(), stream_var.get())

    button = Button(window, text="Generate Report", command=on_generate, bg="green", fg="white", font=("Arial", 12, "bold"), padx=10, pady=5)
    button.pack(pady=20)

    window.mainloop()


if __name__ == "__main__":
    open_report_window()
