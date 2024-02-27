import datetime
import tkinter as tk
import webbrowser
from tkinter import filedialog as fd
from tkinter import ttk

import babel.numbers  # noqa
import customtkinter as ctk
from CTkMessagebox import CTkMessagebox
from PIL import Image
from tkcalendar import DateEntry

import main
import utils

DARK_MODE = "Dark mode"
DEFAULT_DARK_MODE = "Dark mode"
utils.set_default_appearance_mode(DEFAULT_DARK_MODE)


def dark_theme_switch():
    global DARK_MODE
    theme = switch_var.get()
    if theme == "Dark mode":
        ctk.set_appearance_mode("dark")
        DARK_MODE = "Dark mode"
    elif theme == "Light mode":
        ctk.set_appearance_mode("light")
        DARK_MODE = "Light mode"


def on_enter(event):  # noqa
    calculate_button.configure(fg_color="grey")


def on_leave(event):  # noqa
    calculate_button.configure(fg_color="black")


def open_url(event):  # noqa
    webbrowser.open("https://github.com/Andriy-Sydorenko")


def submit():
    try:
        with open("users.txt", "w") as file:
            file.write(username_input_widget.get("1.0", "end").strip("\n"))
    except IOError:
        CTkMessagebox(
            title="Unable to save the file",
            message="Something went wrong when saved username file",
            icon="warning",
            option_1="Damn!"
        )
    start_date = datetime.datetime.strptime(start_date_var.get(), main.DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date_var.get(), main.DATE_FORMAT)
    usernames_list = [username for username in username_input_widget.get("1.0", "end").split("\n") if username]
    if start_date > end_date:
        CTkMessagebox(title="Date input error!",
                      message="This date range is invalid! First date should be less than second",
                      icon="warning",
                      option_1="Ok")
        return
    if not usernames_list:
        CTkMessagebox(title="User list is empty!",
                      message="You haven't chosen any users!",
                      icon="warning",
                      option_1="Ok")
        return

    result = main.get_users_playtime(usernames_list=usernames_list,
                                     start_date=start_date_var.get(),
                                     end_date=end_date_var.get(),
                                     server_name=server_choice.get())

    table.delete(*table.get_children())
    try:
        for username, user_data in result.items():
            data = [username, ]
            data.extend(list(user_data.values()))
            table.insert(parent="", index=0, values=data)
    except (AttributeError, ValueError, TypeError):
        return


def calculate_event_winners():
    start_date = datetime.datetime.strptime(start_date_var.get(), main.DATE_FORMAT)
    end_date = datetime.datetime.strptime(end_date_var.get(), main.DATE_FORMAT)
    if start_date > end_date:
        CTkMessagebox(title="Date input error!",
                      message="This date range is invalid! First date should be less than second",
                      icon="warning",
                      option_1="Ok")
        return
    result = main.get_user_event_wins(start_date=start_date_var.get(),
                                      end_date=end_date_var.get(),
                                      server_name=server_choice.get())
    app.clipboard_clear()
    app.clipboard_append(result)

    CTkMessagebox(title="Data with event winners is copied to the clipboard",
                  message="Now you can paste the data whenever you want",
                  option_1="Ok")


def copy_selected_item(event):
    selected_items = table.selection()  # This will get all selected items, not just one
    all_text_to_copy = []

    for item in selected_items:
        item_values = table.item(item)["values"]  # Extract values for each selected item
        if item_values:
            text_to_copy = " ".join(map(str, item_values))  # Create a string from the item values
            all_text_to_copy.append(text_to_copy)  # Add this string to the list of texts to copy

    final_text_to_copy = "\n".join(all_text_to_copy)  # Join all item texts with a newline
    if final_text_to_copy:  # Check if there's anything to copy
        app.clipboard_clear()
        app.clipboard_append(final_text_to_copy)
        app.update()


def select_all_table_rows(event):
    for item in table.get_children():
        table.selection_add(item)


def open_text_file():
    filetypes = (
        ("text files", "*.txt"),
    )

    file_path = fd.askopenfilename(
        title="Open a file",
        initialdir="/",
        filetypes=filetypes
    )

    if file_path:
        usernames = utils.parse_usernames_from_file(file_path)
        username_input_widget.delete("1.0", "end")
        for username in usernames:
            username_input_widget.insert("end", username + "\n")


app = ctk.CTk()
app.resizable(False, False)
app.geometry("700x480")
app.title("Get user playtime statistic")
app.iconbitmap("tkinter_app_icon.ico")

main_frame = ctk.CTkFrame(app)
main_frame.pack(side=ctk.LEFT, anchor=ctk.N, padx=20, pady=20)

dark_mode_frame = ctk.CTkFrame(main_frame, width=20)
dark_mode_frame.pack(pady=10)
switch_var = ctk.StringVar(value="Dark mode")
dark_mode_switch = ctk.CTkSwitch(master=dark_mode_frame,
                                 text="",
                                 variable=switch_var,
                                 command=dark_theme_switch,
                                 onvalue="Dark mode",
                                 offvalue="Light mode")
dark_mode_switch.grid(row=0, column=0, pady=5)
theme_image = ctk.CTkImage(light_image=Image.open("light_mode.webp"),
                           dark_image=Image.open("dark_mode.webp"),
                           size=(25, 25))
dark_mode_label = ctk.CTkLabel(master=dark_mode_frame, text="", image=theme_image)
dark_mode_label.grid(row=0, column=1, padx=(5, 0))

# Username input frame
username_frame = ctk.CTkFrame(main_frame, width=200, height=200)
username_frame.pack(side=ctk.LEFT)

# Create input field for username
username_label = ctk.CTkLabel(username_frame, text="Usernames:")
username_label.grid(row=0, pady=1)

username_input_widget = ctk.CTkTextbox(username_frame)
username_input_widget.configure()
username_input_widget.grid(row=1)

try:
    with open("users.txt", "r") as file:
        usernames = file.read()
        username_input_widget.insert("1.0", usernames)
except IOError:
    CTkMessagebox(
        title="Unable to load the file",
        message="Something went wrong when loaded username file",
        icon="warning",
        option_1="Damn!"
    )

open_file_button = ctk.CTkButton(username_frame, text="Open a file", command=open_text_file)
open_file_button.grid(row=2, pady=5)

calculate_button = ctk.CTkButton(username_frame, text="Calculate data", command=submit, fg_color="black")
calculate_button.grid()
calculate_button.bind("<Enter>", on_enter)
calculate_button.bind("<Leave>", on_leave)

event_winners_button = ctk.CTkButton(username_frame,
                                     text="Get event winners",
                                     command=calculate_event_winners,
                                     fg_color="#46008b")
event_winners_button.grid(pady=5)

footer_frame = ctk.CTkFrame(username_frame)
footer_frame.grid(column=0, pady=10)

made_by_label = ctk.CTkLabel(footer_frame, text="© Made by deficiente")
made_by_label.pack(side=tk.LEFT, padx=10)

github_image = ctk.CTkImage(light_image=Image.open("github_light_mode.webp"),
                            dark_image=Image.open("github_light_mode.webp"),
                            size=(35, 35))
github_label = ctk.CTkLabel(master=footer_frame, text="", image=github_image, cursor="hand2")
github_label.bind("<Button-1>", open_url)
github_label.pack()

date_frame = ctk.CTkFrame(app, width=100, height=50)
date_frame.pack(pady=20, side=ctk.LEFT, anchor=ctk.N)

# Create DateEntry widgets for start and end dates
week_ago_date = datetime.date.today() - datetime.timedelta(days=6)
start_date_var = ctk.StringVar()
start_date_entry = DateEntry(date_frame,
                             textvariable=start_date_var,
                             date_pattern="dd-mm-yyyy",
                             maxdate=datetime.date.today(),
                             year=week_ago_date.year,
                             month=week_ago_date.month,
                             day=week_ago_date.day)
start_date_entry.grid(row=0, column=0, pady=10, padx=10)
start_date_entry.configure()

hyphen_label = ctk.CTkLabel(date_frame, text="-")
hyphen_label.grid(row=0, column=1, padx=5)

end_date_var = ctk.StringVar()
end_date_entry = DateEntry(date_frame,
                           textvariable=end_date_var,
                           date_pattern="dd-mm-yyyy",
                           maxdate=datetime.date.today())
end_date_entry.grid(row=0, column=2, pady=10, padx=10)
end_date_entry.configure()

server_choice = ctk.CTkOptionMenu(app, values=list(main.SERVERS.keys()))
server_choice.pack(padx=10, pady=25, side=ctk.LEFT, anchor=ctk.N)

table = ttk.Treeview(app, columns=("username", "total", "average"), show="headings", height=16, selectmode="extended")
table.heading("username", text="Username")
table.heading("total", text="Total playtime")
table.heading("average", text="Average playtime")
table.tag_configure("dark_mode", foreground="white", background="#2d2d2d")
for item_id in table.get_children():
    table.item(item_id, tags=("dark_mode",))
table.place(relx=0.655, rely=0.515, anchor=ctk.CENTER)
table.column("username", width=150)
table.column("total", width=150)
table.column("average", width=150)
table.bind("<Control-c>", copy_selected_item)
table.bind("<Double-1>", select_all_table_rows)

app.mainloop()
