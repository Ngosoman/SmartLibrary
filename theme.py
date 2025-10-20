# theme.py
import tkinter as tk
from tkinter import ttk

# Global theme state
current_theme = "light"

def configure_styles(theme="light"):
    global current_theme
    current_theme = theme
    style = ttk.Style()
    style.theme_use('clam')

    if theme == "dark":
        # Dark theme colors
        primary_color = "#5dade2"  # Light blue
        secondary_color = "#58d68d"  # Light green
        danger_color = "#ec7063"  # Light red
        background_color = "#2c3e50"  # Dark gray
        card_background = "#34495e"  # Slightly lighter dark
        text_color = "#ecf0f1"  # Light text
    else:
        # Light theme colors
        primary_color = "#3498db"  # Blue
        secondary_color = "#2ecc71"  # Green
        danger_color = "#e74c3c"  # Red
        background_color = "#f5f5f5"  # Light gray
        card_background = "white"
        text_color = "#2c3e50"

    # Configure root style
    style.configure('.',
                   background=background_color,
                   foreground=text_color,
                   font=('Segoe UI', 10))

    # Frame styles
    style.configure('TFrame', background=background_color)
    style.configure('Card.TFrame',
                   background=card_background,
                   relief=tk.RAISED,
                   borderwidth=1)

    # Button styles
    style.configure('TButton',
                   padding=6,
                   font=('Segoe UI', 10, 'bold'))
    style.map('TButton',
             background=[('active', primary_color)],
             foreground=[('active', 'white')])

    style.configure('Primary.TButton',
                    foreground="white",
                    background="#222f3e",
                    font=("Segoe UI", 12, "bold"),
                    padding=8)
    style.map("Primary.TButton",
              background=[("active", primary_color)])

    style.configure('Success.TButton',
                   background=secondary_color,
                   foreground="white")
    style.configure('Danger.TButton',
                   background=danger_color,
                   foreground="white")

    # Entry styles
    style.configure('TEntry',
                   padding=5,
                   relief=tk.SOLID,
                   fieldbackground=card_background,
                   foreground=text_color)

    # Label styles
    style.configure('Header1.TLabel',
                   font=('Segoe UI', 16, 'bold'),
                   foreground=text_color)
    style.configure('Header2.TLabel',
                   font=('Segoe UI', 14),
                   foreground=text_color)

    # Treeview styles
    style.configure('Treeview',
                   rowheight=25,
                   fieldbackground=card_background,
                   background=card_background,
                   foreground=text_color)
    style.configure('Treeview.Heading',
                   font=('Segoe UI', 10, 'bold'),
                   background=background_color,
                   foreground=text_color)
    style.map('Treeview',
             background=[('selected', primary_color)])

def toggle_theme():
    global current_theme
    new_theme = "dark" if current_theme == "light" else "light"
    configure_styles(new_theme)
    return new_theme
