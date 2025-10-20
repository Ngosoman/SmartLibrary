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
        self.read_status = {
            "Overdue Books": set(),
            "Low Stock": set(),
            "System Reminders": set()
        }
        self.setup_ui()

    def setup_ui(self):
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
            notebook.add(frame, text=f"{category} ({len(notes)})")

            tree = ttk.Treeview(frame, columns=("Time", "Message", "Status"), show="headings")
            tree.heading("Time", text="Time")
            tree.heading("Message", text="Message")
            tree.heading("Status", text="Status")
            tree.column("Time", width=80)
            tree.column("Message", width=450)
            tree.column("Status", width=80)

            for i, note in enumerate(notes):
                is_read = i in self.read_status[category]
                status = "Read" if is_read else "Unread"
                tree.insert("", tk.END, values=(note[0], note[1], status))

                # Mark as read when clicked
                def mark_read(event, cat=category, idx=i):
                    self.read_status[cat].add(idx)
                    self.update_counter()
                    # Refresh the treeview
                    tree.item(tree.selection()[0], values=(note[0], note[1], "Read"))

                tree.bind("<ButtonRelease-1>", mark_read)

            scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
            tree.configure(yscrollcommand=scrollbar.set)
            scrollbar.pack(side="right", fill="y")
            tree.pack(fill="both", expand=True)

    def update_counter(self):
        """Update the unread counter"""
        unread_count = 0
        for category, notes in self.notifications.items():
            unread_count += len(notes) - len(self.read_status[category])
        self.counter_var.set(str(unread_count))


# Global notifier instance
notifier = None

def init_notifications(root):
    global notifier
    notifier = NotificationManager(root)
    return notifier
