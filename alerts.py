import datetime
from playsound import playsound
import os
from tkinter import messagebox
import tkinter as tk
from datetime import datetime, timedelta
from datetime import date

import sqlite3

# Function to check due alerts
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
