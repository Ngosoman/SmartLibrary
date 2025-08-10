import tkinter as tk
from tkinter import messagebox

# Function to verify credentials
def login():
    username = username_entry.get()
    password = password_entry.get()

    if username == "Admin" and password == "AdminLibrary":
        messagebox.showinfo("Success", "Login successful!")
        login_window.destroy()
        open_library_dashboard()

        
    else:
        messagebox.showerror("Error", "Invalid username or password.")


    
# Function to simulate opening the main dashboard
def open_library_dashboard():
    dashboard = tk.Tk()
    dashboard.title("Library Management System")
    dashboard.geometry("500x300")
    tk.Label(dashboard, text="Welcome to the Library Management System!", font=("Helvetica", 14)).pack(pady=20)
    dashboard.mainloop()

# Main Login Window
login_window = tk.Tk()
login_window.title("Library Login")
login_window.geometry("400x250")

tk.Label(login_window, text="Username:").pack(pady=(20, 5))
username_entry = tk.Entry(login_window)
username_entry.pack()

tk.Label(login_window, text="Password:").pack(pady=(10, 5))
password_entry = tk.Entry(login_window, show="*")
password_entry.pack()

tk.Button(login_window, text="Login", command=login).pack(pady=20)

login_window.mainloop()
