import tkinter as tk
import customtkinter as ctk

# def set_transparent_placeholder(username_entry):
#   def on_entry_focus_in(event):
#     if username_entry.get() == "Enter username:":
#       username_entry.delete(0, tk.END)
#       username_entry.configure(show="")
#       username_entry.configure(fg="black")
#
#   def on_entry_focus_out(event):
#     if username_entry.get() == "":
#       username_entry.insert(0, "Enter username:")
#       username_entry.configure(show="*")
#       username_entry.configure(fg="gray")
#
#
#   username_entry.bind("<FocusIn>", on_entry_focus_in)
#   username_entry.bind("<FocusOut>", on_entry_focus_out)

def set_default_appearance_mode(default_value: str):
  if default_value == "Dark mode":
    ctk.set_appearance_mode("dark")
  else:
    ctk.set_appearance_mode("light")
