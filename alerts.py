import os
import datetime
from datetime import date, timedelta
from playsound import playsound
from tkinter import messagebox, Tk

# Function to check for due alerts
def check_due_alerts():
    today = date.today()
    tomorrow = today + timedelta(days=1)
    file_path = "borrowed_books.txt"

    if not os.path.exists(file_path):
        print("❌ No borrowed_books.txt file found.")
        return

    try:
        with open(file_path, "r") as file:
            for line_number, line in enumerate(file, start=1):
                data = line.strip().split(",")

                if len(data) < 5:
                    print(f"⚠️ Skipping line {line_number}: Not enough fields.")
                    continue

                student_name = data[0].strip()
                return_date_str = data[4].strip()

                try:
                    return_date = datetime.datetime.strptime(return_date_str, "%Y-%m-%d").date()

                    if return_date == tomorrow:
                        print(f"🔔 Reminder: Book due tomorrow for {student_name}")
                        show_ui_alert(f"Reminder: Book due tomorrow for {student_name}")
                        playsound("alert_tomorrow.mp3")

                    elif return_date == today:
                        print(f"🚨 ALERT: Book due TODAY for {student_name}")
                        show_ui_alert(f"ALERT: Book due TODAY for {student_name}")
                        playsound("alert_today.mp3")

                except ValueError:
                    print(f"❌ Invalid date format on line {line_number}: '{return_date_str}'")

    except Exception as e:
        print(f"🔥 Error reading file: {e}")

# Optional GUI pop-up using Tkinter
def show_ui_alert(message):
    try:
        root = Tk()
        root.withdraw()  # Hide the main window
        messagebox.showinfo("Book Return Alert", message)
        root.destroy()
    except Exception as e:
        print(f"⚠️ Unable to show popup: {e}")

# For testing purposes (you can call this from main dashboard or scheduler)
if __name__ == "__main__":
    check_due_alerts()
