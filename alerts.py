import datetime
from playsound import playsound
import os
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, timedelta
from datetime import date

import sqlite3

# def view_upcoming_returns():
#     conn = sqlite3.connect("library.db")
#     cursor = conn.cursor()

#     today = datetime.today().date()
#     upcoming_date = today + timedelta(days=3)

#     cursor.execute("SELECT student_name, admission_no, class, stream, book_title, return_date FROM borrow WHERE return_date BETWEEN ? AND ?", (today, upcoming_date))
#     rows = cursor.fetchall()
#     conn.close()

#     if not rows:
#         messagebox.showinfo("Upcoming Returns", "No books are due for return in the next 3 days.")
#         return

#     popup = tk.Toplevel()
#     popup.title("📅 Upcoming Book Returns")

#     tk.Label(popup, text="Books due for return within next 3 days", font=("Helvetica", 14, "bold")).pack(pady=10)

#     for row in rows:
#         student, adm, cls, stream, title, due = row
#         due_date = datetime.strptime(due, "%Y-%m-%d").strftime("%d %b %Y")
#         info = f"{student} ({adm}, {cls}-{stream}) → '{title}' by {due_date}"
#         tk.Label(popup, text=info, anchor="w", justify="left").pack(anchor="w", padx=10)

# Hii function ina-check due dates na inatoa alert
def check_due_alerts():
    today = date.today()
    tomorrow = today + timedelta(days=1)

    if not os.path.exists("borrowed_books.txt"):
        print("No borrowed books file found.")
        return

    try:
        with open("borrowed_books.txt", "r") as file:
            for line in file:
                data = line.strip().split(",")
                if len(data) < 5:
                    continue

                # Assuming return_date is the 5th value (index 4)
                return_date_str = data[4]
                try:
                    return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()

                    if return_date == tomorrow:
                        print(f"🔔 Reminder: Book due tomorrow for {data[0]}")
                        playsound("alert_tomorrow.mp3")

                    elif return_date == today:
                        print(f"🚨 ALERT: Book due today for {data[0]}")
                        playsound("alert_today.mp3")

                except ValueError as ve:
                    print(f"Invalid date format in line: {line}")
    except Exception as e:
        print(f"Error reading borrowed books file: {e}")
