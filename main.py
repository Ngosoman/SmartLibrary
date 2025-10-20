import tkinter as tk
from tkinter import messagebox
from dashboard import open_dashboard
from theme import configure_styles

# Function to handle login
def login():
    username = user_entry.get()
    password = pass_entry.get()

    if username == "Admin" and password == "AdminLibrary":
        messagebox.showinfo("Login Success", "Welcome to the School Library System!")
        root.destroy()
        open_dashboard()
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

# Function to toggle password visibility
def toggle_password():
    if pass_entry.cget('show') == '*':
        pass_entry.config(show='')
        eye_btn.config(text='🙈')
    else:
        pass_entry.config(show='*')
        eye_btn.config(text='👁️')

# Function to handle Enter key press
def on_enter(event):
    login()

# GUI
root = tk.Tk()
root.title("Library Login")
root.geometry("350x250")
root.resizable(True, True)
# Apply theme
configure_styles()

tk.Label(root, text="Library Management Login", font=("Helvetica", 14, "bold")).pack(pady=15)

tk.Label(root, text="Username:").pack()
user_entry = tk.Entry(root, width=30)
user_entry.pack(pady=5)
user_entry.bind('<Return>', on_enter)

tk.Label(root, text="Password:").pack()
password_frame = tk.Frame(root)
password_frame.pack(pady=5)
pass_entry = tk.Entry(password_frame, show="*", width=25)
pass_entry.pack(side=tk.LEFT)
pass_entry.bind('<Return>', on_enter)
eye_btn = tk.Button(password_frame, text='👁️', command=toggle_password, width=3)
eye_btn.pack(side=tk.RIGHT)

tk.Button(root, text="Login", command=login, width=15, bg="blue", fg="white").pack(pady=15)

root.mainloop()
