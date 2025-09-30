import tkinter as tk
from tkinter import ttk
from plyer import notification
import winsound
from datetime import datetime

class NotificationManager:
    def __init__(self, root):
        self.root = root
        self.notifications = {
            "Overdue Books": [],
            "Low Stock": [],
            "System Reminders": []
        }
        self.setup_ui()
        
    def setup_ui(self):
        # Notification bell button
        self.bell_btn = ttk.Button(self.root, text="🔔",
                                   command=self.show_notification_center)

        # Counter for unread notifications
        self.counter_var = tk.StringVar(value="0")
        
    def add_notification(self, category, message, urgent=False):
        """Add a notification under a category"""
        timestamp = datetime.now().strftime("%H:%M")
        
        if category not in self.notifications:
            self.notifications[category] = []
        
        self.notifications[category].append((timestamp, message, urgent))
        
        # Update counter
        total_count = sum(len(v) for v in self.notifications.values())
        self.counter_var.set(str(total_count))
        
        # System tray notification
        notification.notify(
            title=f"Library Alert - {category}",
            message=message,
            timeout=10
        )
        
        # Urgent sound alert
        if urgent:
            winsound.PlaySound("alert_today.mp3", winsound.SND_ASYNC)
    
    def show_notification_center(self):
        window = tk.Toplevel(self.root)
        window.title("Notification Center")
        window.geometry("700x500")
        
        notebook = ttk.Notebook(window)
        notebook.pack(fill="both", expand=True)
        
        # Create tabs for each category
        for category, notes in self.notifications.items():
            frame = ttk.Frame(notebook)
            notebook.add(frame, text=category)
            
            tree = ttk.Treeview(frame, columns=("Time", "Message", "Urgent"), show="headings")
            tree.heading("Time", text="Time")
            tree.heading("Message", text="Message")
            tree.heading("Urgent", text="Urgent")
            tree.column("Time", width=80)
            tree.column("Message", width=450)
            tree.column("Urgent", width=80)
            
            for note in notes:
                tree.insert("", tk.END, values=(note[0], note[1], "⚠️" if note[2] else ""))
            
            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(fill="both", expand=True)


# Global notifier instance
notifier = None

def init_notifications(root):
    global notifier
    notifier = NotificationManager(root)
    return notifier
