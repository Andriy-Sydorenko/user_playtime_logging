import tkinter as tk
from tkinter import ttk
from entry_with_placeholder import EntryWithPlaceholder

def update_label():
  username = username_var.get()
  date_range = date_range_var.get()
  label.config(text=f"Username: {username}\nDate Range: {date_range}")

# Create the main window
app = tk.Tk()
app.geometry("500x300")
app.title("Get user playtime statistic")
app.iconbitmap("misc/tkinter_app_icon.ico")

# Create a label widget
label = tk.Label(app, text="Welcome to Tkinter!")
label.pack(pady=10)



# Create input field for username
username_label = tk.Label(app, text="Username:")
username_label.pack(pady=5)

username_var = tk.StringVar()
username_entry = EntryWithPlaceholder(app, placeholder="Enter username please")
username_entry.pack(pady=5)

# Create input field for date range
date_range_label = tk.Label(app, text="Choose the date range:")
date_range_label.pack(pady=5)

date_range_var = tk.StringVar()
date_range_combobox = ttk.Combobox(app, textvariable=date_range_var, values=["Today", "This Week", "This Month"])
date_range_combobox.set("Select date range")
date_range_combobox.pack(pady=5)

# Create a label widget
label = tk.Label(app, text="Welcome to Tkinter!")
label.pack(pady=10)

# Create a button widget
button = tk.Button(app, text="Update Label", command=update_label)
button.pack(pady=10)


# Run the Tkinter event loop
app.mainloop()
