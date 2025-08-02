from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import sqlite3
from datetime import datetime

def generate_report():
    conn = sqlite3.connect("library.db")
    cursor = conn.cursor()
    cursor.execute("SELECT student_name, admission_no, class, stream, book_title, borrow_date, return_date FROM borrow")
    records = cursor.fetchall()
    conn.close()

    if not records:
        print("No records found.")
        return

    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"Borrowing_Report_{now}.pdf"
    c = canvas.Canvas(filename, pagesize=A4)
    width, height = A4

    c.setFont("Helvetica-Bold", 16)
    c.drawCentredString(width / 2.0, height - 50, "📚 Borrowing Report")
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 80, f"Generated on: {datetime.now().strftime('%d %b %Y, %I:%M %p')}")

    c.setFont("Helvetica-Bold", 10)
    headers = ["Name", "Adm No", "Class", "Stream", "Book", "Borrowed", "Due"]
    x_offsets = [50, 150, 220, 270, 330, 430, 500]

    y = height - 110
    for i, header in enumerate(headers):
        c.drawString(x_offsets[i], y, header)

    y -= 20
    c.setFont("Helvetica", 9)
    for record in records:
        if y < 40:
            c.showPage()
            y = height - 50
        for i, item in enumerate(record):
            c.drawString(x_offsets[i], y, str(item))
        y -= 15

    c.save()
    print(f"✅ Report saved as {filename}")
