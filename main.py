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

tk.Label(root, text="Password:").pack()
pass_entry = tk.Entry(root, show="*", width=30)
pass_entry.pack(pady=5)

tk.Button(root, text="Login", command=login, width=15, bg="blue", fg="white").pack(pady=15)

root.mainloop()
