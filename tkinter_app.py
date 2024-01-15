import tkinter as tk
import datetime
from tkcalendar import DateEntry
from PIL import Image
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
import main
import utils
import webbrowser

usernames_list = []
DARK_MODE = "Dark mode"
DEFAULT_DARK_MODE = "Dark mode"
utils.set_default_appearance_mode(DEFAULT_DARK_MODE)


def add_username():
    username = username_var.get()
    if username:
        username_input_widget.configure(state=ctk.NORMAL)
        username_input_widget.insert(ctk.END, f"{username}\n")
        username_input_widget.configure(state=ctk.DISABLED)
        username_var.set("")
        usernames_list.append(username)


def clear_text():
    username_input_widget.configure(state=ctk.NORMAL)
    username_input_widget.delete(1.0, ctk.END)
    username_input_widget.configure(state=ctk.DISABLED)
    usernames_list.clear()


def delete_last_username():
    if usernames_list:
        username_input_widget.configure(state=ctk.NORMAL)
        last_username = usernames_list.pop()
        username_input_widget.delete(f"{len(usernames_list) + 1}.0", ctk.END)
        username_input_widget.configure(state=ctk.DISABLED)


def dark_theme_switch():
    global DARK_MODE
    theme = switch_var.get()
    if theme == "Dark mode":
        ctk.set_appearance_mode("dark")
        DARK_MODE = "Dark mode"
    elif theme == "Light mode":
        ctk.set_appearance_mode("light")
        DARK_MODE = "Light mode"


def open_url(event):
    webbrowser.open("https://github.com/Andriy-Sydorenko")


def submit():
    if start_date_var.get() > end_date_var.get():
        CTkMessagebox(message="This date range is valid! First date should be less than second",
                      icon="warning",
                      option_1="Ok")
        return
    main.main(usernames_list, start_date_var.get(), end_date_var.get())


# Create the main window
app = ctk.CTk()
app.resizable(False, False)
app.geometry("700x530")
app.title("Get user playtime statistic")
app.iconbitmap("misc/tkinter_app_icon.ico")

main_frame = ctk.CTkFrame(app)
main_frame.pack(side=ctk.LEFT, anchor=ctk.N, padx=20, pady=20)

# Dark mode switch frame
dark_mode_frame = ctk.CTkFrame(main_frame, width=20)
dark_mode_frame.pack(pady=10)
switch_var = ctk.StringVar(value="Dark mode")
dark_mode_switch = ctk.CTkSwitch(master=dark_mode_frame, text="", variable=switch_var, command=dark_theme_switch, onvalue="Dark mode", offvalue="Light mode")
dark_mode_switch.grid(row=0, column=0, pady=5)
theme_image = ctk.CTkImage(light_image=Image.open("misc/light_mode.webp"), dark_image=Image.open("misc/dark_mode.webp"), size=(25, 25))
dark_mode_label = ctk.CTkLabel(master=dark_mode_frame, text="", image=theme_image)
dark_mode_label.grid(row=0, column=1, padx=(5, 0))

# Username input frame
username_frame = ctk.CTkFrame(main_frame, width=200, height=200)
username_frame.pack(side=ctk.LEFT)

# Create input field for username
username_label = ctk.CTkLabel(username_frame, text="Username:")
username_label.grid(row=0)

username_var = ctk.StringVar()
username_entry = ctk.CTkEntry(username_frame, textvariable=username_var)
username_entry.grid(row=1)

# Buttons for username operations
add_button = ctk.CTkButton(username_frame, text="Add", command=add_username, width=50, height=40)
add_button.grid(pady=5, column=0, row=2, padx=(0, 90))

clear_button = ctk.CTkButton(username_frame, text="Clear", command=clear_text, width=50, height=40)
clear_button.grid(pady=5, column=0, row=2, padx=(90, 0))

delete_button = ctk.CTkButton(username_frame, text="Delete Last Username", command=delete_last_username)
delete_button.grid(pady=5, row=3)

get_button = ctk.CTkButton(username_frame, text="Get all data", command=submit)
get_button.grid(pady=5)

# Text widget to display usernames (initially disabled)
username_input_widget = ctk.CTkTextbox(username_frame)
username_input_widget.configure(state=ctk.DISABLED)
username_input_widget.grid()

# Date frame (moved vertically)
date_frame = ctk.CTkFrame(app)
date_frame.pack(pady=20)  # Adjust the pady value as needed

# Create DateEntry widgets for start and end dates
week_ago_date = datetime.date.today() - datetime.timedelta(days=7)
start_date_var = ctk.StringVar()
start_date_entry = DateEntry(date_frame, textvariable=start_date_var, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today(), year=week_ago_date.year, month=week_ago_date.month, day=week_ago_date.day)
start_date_entry.grid(row=0, column=0, pady=10, padx=10)
start_date_entry.configure()

# Add a hyphen between start and end dates
hyphen_label = ctk.CTkLabel(date_frame, text="-")
hyphen_label.grid(row=0, column=1, padx=5)

end_date_var = ctk.StringVar()
end_date_entry = DateEntry(date_frame, textvariable=end_date_var, date_pattern="dd-mm-yyyy", maxdate=datetime.date.today())
end_date_entry.grid(row=0, column=2, pady=10, padx=10)
end_date_entry.configure()

footer_frame = ctk.CTkFrame(app)
footer_frame.pack(side=ctk.BOTTOM, pady=10)

made_by_label = ctk.CTkLabel(footer_frame, text="© Made by deficiente")
made_by_label.pack(side=tk.LEFT, padx=10)

github_image = ctk.CTkImage(light_image=Image.open("misc/github_light_mode.webp"), dark_image=Image.open("misc/github_light_mode.webp"), size=(35, 35))
github_label = ctk.CTkLabel(master=footer_frame, text="", image=github_image, cursor="hand2")
github_label.bind("<Button-1>", open_url)
github_label.pack()

app.mainloop()
