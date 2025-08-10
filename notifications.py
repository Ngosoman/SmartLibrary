import tkinter as tk
from tkinter import ttk
from plyer import notification
import winsound
from datetime import datetime

class NotificationManager:
    def __init__(self, root):
        self.root = root
        self.notifications = []
        self.setup_ui()
        
    def setup_ui(self):
        self.bell_btn = ttk.Button(self.root, text="🔔", 
                                 command=self.show_notification_center)
        self.bell_btn.pack(side=tk.RIGHT, padx=10)
        
        self.counter_var = tk.StringVar(value="0")
        ttk.Label(self.root, textvariable=self.counter_var).pack(side=tk.RIGHT)
        
    def add_notification(self, message, urgent=False):
        timestamp = datetime.now().strftime("%H:%M")
        self.notifications.append((timestamp, message, urgent))
        self.counter_var.set(str(len(self.notifications)))
        
        notification.notify(
            title="Library Alert",
            message=message,
            timeout=10
        )
        
        if urgent:
            winsound.PlaySound("alert_tomorrow.mp3.mp3", winsound.SND_ASYNC)
    
    def show_notification_center(self):
        window = tk.Toplevel(self.root)
        window.title("Notification Center")
        window.geometry("600x400")
        
        # Simple list without matplotlib
        tree = ttk.Treeview(window, columns=("Time", "Message", "Urgent"), show="headings")
        tree.heading("Time", text="Time")
        tree.heading("Message", text="Message")
        tree.heading("Urgent", text="Urgent")
        tree.column("Time", width=80)
        tree.column("Message", width=400)
        tree.column("Urgent", width=80)
        
        for note in self.notifications:
            tree.insert("", tk.END, values=(note[0], note[1], "⚠️" if note[2] else ""))
        
        scrollbar = ttk.Scrollbar(window, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)


notifier = None

def init_notifications(root):
    global notifier
    notifier = NotificationManager(root)
    return notifier