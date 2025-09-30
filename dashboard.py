import tkinter as tk
from tkinter import ttk, messagebox
import books
from books import BookManager
import borrow
from borrow import LibraryDB
import reports
import alerts
from notifications import NotificationManager
from notifications import init_notifications
from datetime import datetime
from theme import configure_styles

# Run alerts check on launch (legacy alerts module, leaves as-is)
alerts.check_due_alerts()

def open_dashboard():
    # Configure styles
    configure_styles()

    # Create main dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("📚 SmartLibrary Dashboard")
    dashboard.geometry("1200x800")
    dashboard.resizable(True, True)

    # Initialize notification manager (sets the global `notifier` inside notifications.py)
    notifier = init_notifications(dashboard)

    # Trigger stock + overdue checks now that notifier is ready
    try:
        books.check_stock_levels()
    except Exception:
        pass

    try:
        borrow.check_due_alerts()
    except Exception:
        pass

    # Main container with padding
    main_frame = ttk.Frame(dashboard, padding=20)
    main_frame.pack(fill=tk.BOTH, expand=True)

    # Header section
    header_frame = ttk.Frame(main_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Dashboard title
    ttk.Label(header_frame,
              text="SmartLibrary System",
              style="Header1.TLabel").pack(side=tk.LEFT)

    # Notification bell with counter
    notification_frame = ttk.Frame(header_frame)
    notification_frame.pack(side=tk.RIGHT)

    # Create and pack the bell button
    bell_btn = ttk.Button(notification_frame, text="🔔 Notifications", style="Primary.TButton",
                          command=lambda: notifier.show_notification_center())
    bell_btn.pack(side=tk.RIGHT, padx=10)

    # Pack the counter label
    ttk.Label(notification_frame, textvariable=notifier.counter_var).pack(side=tk.RIGHT)

    # Stats summary cards (real-time data)
    stats_frame = ttk.Frame(main_frame)
    stats_frame.pack(fill=tk.X, pady=(0, 20))

    # Get real-time data
    book_db = BookManager()
    borrow_db = LibraryDB()
    total_books = sum(book[4] for book in book_db.get_all_books())
    borrowed_books_count = len(borrow_db.get_borrowed_books())
    overdue_books_count = len(borrow_db.get_overdue_books())

    # Card 1: Total Books
    card1 = ttk.Frame(stats_frame, style="Card.TFrame", padding=15)
    card1.grid(row=0, column=0, padx=10, sticky="nsew")
    ttk.Label(card1, text="Total Books", style="Header2.TLabel").pack()
    ttk.Label(card1, text=str(total_books), font=('Segoe UI', 24, 'bold')).pack()

    # Card 2: Books Borrowed
    card2 = ttk.Frame(stats_frame, style="Card.TFrame", padding=15)
    card2.grid(row=0, column=1, padx=10, sticky="nsew")
    ttk.Label(card2, text="Books Borrowed", style="Header2.TLabel").pack()
    ttk.Label(card2, text=str(borrowed_books_count), font=('Segoe UI', 24, 'bold')).pack()

    # Card 3: Overdue Books
    card3 = ttk.Frame(stats_frame, style="Card.TFrame", padding=15)
    card3.grid(row=0, column=2, padx=10, sticky="nsew")
    ttk.Label(card3, text="Overdue Books", style="Header2.TLabel").pack()
    ttk.Label(card3, text=str(overdue_books_count), font=('Segoe UI', 24, 'bold'), foreground="#e74c3c").pack()

    # Configure grid weights
    stats_frame.columnconfigure(0, weight=1)
    stats_frame.columnconfigure(1, weight=1)
    stats_frame.columnconfigure(2, weight=1)

    # Main action panels
    panel_frame = ttk.Frame(main_frame)
    panel_frame.pack(fill=tk.BOTH, expand=True)

    # Left panel - Book Management
    book_panel = ttk.Frame(panel_frame, style="Card.TFrame", padding=15)
    book_panel.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    ttk.Label(book_panel,
              text="Book Management",
              style="Header2.TLabel").pack(anchor="w", pady=(0, 15))

    action_buttons = [
        ("➕ Add Book", books.add_book_window),
        ("📖 View Books", books.view_books),
    ]

    for text, command in action_buttons:
        ttk.Button(book_panel,
                   text=text,
                   style="Primary.TButton",
                   command=command).pack(fill=tk.X, pady=5)

    # Middle panel - Borrow/Return
    borrow_panel = ttk.Frame(panel_frame, style="Card.TFrame", padding=15)
    borrow_panel.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")

    ttk.Label(borrow_panel,
              text="Borrowing Section",
              style="Header2.TLabel").pack(anchor="w", pady=(0, 15))

    borrow_buttons = [
        ("👤 Record Borrowing", borrow.record_borrowing_window),
        ("📤 Return Book", borrow.return_book_window),
        ("📆 Upcoming Returns", borrow.view_upcoming_returns),
        ("📋 View Borrowed Books", borrow.view_borrowed_books_window)
    ]

    for text, command in borrow_buttons:
        ttk.Button(borrow_panel,
                   text=text,
                   style="Secondary.TButton",
                   command=command).pack(fill=tk.X, pady=5)

    # Right panel - Reports & Admin
    admin_panel = ttk.Frame(panel_frame, style="Card.TFrame", padding=15)
    admin_panel.grid(row=0, column=2, padx=10, pady=10, sticky="nsew")

    ttk.Label(admin_panel,
              text="Reports & Admin",
              style="Header2.TLabel").pack(anchor="w", pady=(0, 15))

    admin_buttons = [
        ("🧾 Generate Report", reports.open_report_window),
        ("🚪 Logout", dashboard.destroy)
    ]

    for text, command in admin_buttons:
        btn_style = "Danger.TButton" if text == "🚪 Logout" else "TButton"
        ttk.Button(admin_panel,
                   text=text,
                   style=btn_style,
                   command=command).pack(fill=tk.X, pady=5)

    # Configure grid weights
    panel_frame.columnconfigure(0, weight=1)
    panel_frame.columnconfigure(1, weight=1)
    panel_frame.columnconfigure(2, weight=1)

    # Status bar
    status_frame = ttk.Frame(main_frame, style="Card.TFrame", padding=10)
    status_frame.pack(fill=tk.X, pady=(10, 0))

    ttk.Label(status_frame,
              text="Ready",
              foreground="#7f8c8d").pack(side=tk.LEFT)

    ttk.Label(status_frame,
              text=f"Logged in as: Admin | {datetime.now().strftime('%Y-%m-%d %H:%M')}",
              foreground="#7f8c8d").pack(side=tk.RIGHT)

def show_notifications(notifier):
    """Display notification center"""
    if notifier:
        notifier.show_notification_center()
    else:
        messagebox.showwarning("Notifications", "Notification system not initialized")

# Helper function to get current datetime
def datetime_now():
    from datetime import datetime
    return datetime.now()
