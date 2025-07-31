from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
import datetime

def generate_report():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM borrow")
    records = cursor.fetchall()

    if not records:
        print("No borrow records found.")
        return

    filename = f"Borrow_Report_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Borrowed Books Report")

    c.setFont("Helvetica-Bold", 12)
    headers = ["ID", "Book ID", "Student", "Date Borrowed", "Due Date", "Returned"]
    x_positions = [30, 80, 150, 250, 370, 470]
    y = height - 80

    for i, header in enumerate(headers):
        c.drawString(x_positions[i], y, header)

    c.setFont("Helvetica", 10)
    y -= 20
    for row in records:
        if y < 50:
            c.showPage()
            y = height - 50
        for i, item in enumerate(row):
            c.drawString(x_positions[i], y, str(item))
        y -= 20

    c.save()
    print(f"Report saved as {filename}")
    conn.close()
