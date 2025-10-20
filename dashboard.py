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
from theme import configure_styles, toggle_theme

# Run alerts check on launch (legacy alerts module, leaves as-is)
alerts.check_due_alerts()

def open_dashboard():
    # Configure styles
    configure_styles()

    # Create main dashboard window
    dashboard = tk.Toplevel()
    dashboard.title("📚 SmartLibrary Dashboard")
    dashboard.geometry("1400x800")
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

    # Main container with sidebar and content
    main_container = ttk.Frame(dashboard)
    main_container.pack(fill=tk.BOTH, expand=True)

    # Sidebar
    sidebar_expanded = tk.BooleanVar(value=True)
    sidebar_width = 250

    def toggle_sidebar():
        if sidebar_expanded.get():
            # Collapse
            sidebar.config(width=60)
            sidebar_expanded.set(False)
            collapse_btn.config(text="▶")
            # Hide text, show icons
            menu_label.pack_forget()
            dark_mode_btn.config(text="🌙")
            notification_label.pack_forget()
            bell_btn.config(text="🔔")
            recent_label.pack_forget()
            preview_frame.pack_forget()
        else:
            # Expand
            sidebar.config(width=250)
            sidebar_expanded.set(True)
            collapse_btn.config(text="◀")
            # Show text, hide icons
            menu_label.pack(pady=(20, 10))
            dark_mode_btn.config(text="🌙 Dark Mode")
            notification_label.pack(pady=(20, 10))
            bell_btn.config(text="🔔 Notifications")
            recent_label.pack(pady=(10, 5))
            preview_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

    sidebar = ttk.Frame(main_container, width=sidebar_width, style="Card.TFrame")
    sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10), pady=10)
    sidebar.pack_propagate(False)

    # Collapse button at top
    collapse_btn = ttk.Button(sidebar, text="◀", command=toggle_sidebar, width=2)
    collapse_btn.pack(anchor="ne", padx=5, pady=5)

    # Sidebar title
    menu_label = ttk.Label(sidebar, text="Menu", style="Header2.TLabel", font=("Segoe UI", 14, "bold"))
    menu_label.pack(pady=(20, 10))

    # Dark mode toggle
    def toggle_dark_mode():
        new_theme = toggle_theme()
        # Refresh the dashboard styles
        dashboard.update_idletasks()

    dark_mode_btn = ttk.Button(sidebar, text="🌙 Dark Mode", style="TButton", command=toggle_dark_mode)
    dark_mode_btn.pack(fill=tk.X, padx=20, pady=5)

    # Notifications in sidebar
    notification_label = ttk.Label(sidebar, text="Notifications", style="Header2.TLabel")
    notification_label.pack(pady=(20, 10))

    # Notification bell with counter
    notification_frame = ttk.Frame(sidebar)
    notification_frame.pack(fill=tk.X, padx=20, pady=5)

    # Create and pack the bell button
    bell_btn = ttk.Button(notification_frame, text="🔔 Notifications", style="Primary.TButton",
                          command=lambda: notifier.show_notification_center())
    bell_btn.pack(side=tk.TOP, fill=tk.X, pady=(0, 5))

    # Pack the counter label
    counter_label = ttk.Label(notification_frame, textvariable=notifier.counter_var, font=("Segoe UI", 12, "bold"))
    counter_label.pack(side=tk.TOP)

    # Add a small preview of recent notifications
    recent_label = ttk.Label(sidebar, text="Recent Alerts", style="Header2.TLabel", font=("Segoe UI", 10))
    recent_label.pack(pady=(10, 5))

    preview_frame = ttk.Frame(sidebar)
    preview_frame.pack(fill=tk.X, padx=20, pady=(0, 10))

    # Show up to 3 recent notifications
    recent_notifications = []
    for category, notes in notifier.notifications.items():
        for i, note in enumerate(notes[-3:]):  # Last 3
            recent_notifications.append((category, note, i))

    for category, note, idx in recent_notifications[-3:]:
        is_read = idx in notifier.read_status[category]
        status_icon = "✓" if is_read else "●"
        preview_text = f"{status_icon} {note[1][:30]}..." if len(note[1]) > 30 else f"{status_icon} {note[1]}"
        ttk.Label(preview_frame, text=preview_text, font=("Segoe UI", 9), foreground="#7f8c8d").pack(anchor="w", pady=1)

    # Main content area
    content_frame = ttk.Frame(main_container, padding=20)
    content_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    # Header section
    header_frame = ttk.Frame(content_frame)
    header_frame.pack(fill=tk.X, pady=(0, 20))

    # Dashboard title
    ttk.Label(header_frame,
              text="SmartLibrary System",
              style="Header1.TLabel").pack(side=tk.LEFT)

    # Stats summary cards (real-time data)
    stats_frame = ttk.Frame(content_frame)
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
    panel_frame = ttk.Frame(content_frame)
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
    status_frame = ttk.Frame(content_frame, style="Card.TFrame", padding=10)
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
