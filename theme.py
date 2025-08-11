# theme.py
import tkinter as tk
from tkinter import ttk

def configure_styles():
    style = ttk.Style()
    style.theme_use('clam')
    
    # Main colors
    primary_color = "#3498db"  # Blue
    secondary_color = "#2ecc71"  # Green
    danger_color = "#e74c3c"  # Red
    background_color = "#f5f5f5"  # Light gray
    
    # Configure root style
    style.configure('.', 
                   background=background_color,
                   foreground="#2c3e50",
                   font=('Segoe UI', 10))
    
    # Frame styles
    style.configure('TFrame', background=background_color)
    style.configure('Card.TFrame', 
                   background="white",
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
              background=[("active", "#1a242f")])  
    
    style.configure('Success.TButton',
                   background=secondary_color,
                   foreground="white")
    style.configure('Danger.TButton',
                   background=danger_color,
                   foreground="white")
    
    # Entry styles
    style.configure('TEntry',
                   padding=5,
                   relief=tk.SOLID)
    
    # Label styles
    style.configure('Header1.TLabel',
                   font=('Segoe UI', 16, 'bold'),
                   foreground="#2c3e50")
    style.configure('Header2.TLabel',
                   font=('Segoe UI', 14),
                   foreground="#34495e")
    
    # Treeview styles
    style.configure('Treeview',
                   rowheight=25,
                   fieldbackground="white")
    style.configure('Treeview.Heading',
                   font=('Segoe UI', 10, 'bold'))
    style.map('Treeview',
             background=[('selected', primary_color)])