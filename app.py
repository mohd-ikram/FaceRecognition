from attendance_sys import *
from waitress import serve
import os
import tkinter as tk
from tkinter import messagebox
from register import *




def register_user():
    filename = filename_entry.get()
    if len(filename)==0:
        messagebox.showerror("Invalid Filename", "Please enter valid file name")
        return
    else:
        message = capture_and_save_image(filename)
        messagebox.showerror("Message", message)
        return


# Create the main window
window = tk.Tk()
window.title("Registration and Check-in/Check-out")

# Create labels and entry widget for filename
filename_label = tk.Label(window, text="File Name:")
filename_label.grid(row=0, column=0, padx=5, pady=5)
filename_entry = tk.Entry(window)
filename_entry.grid(row=0, column=1, columnspan=2, padx=5, pady=5)

# Create button for registration
register_button = tk.Button(window, text="Register",command=lambda:register_user())
register_button.grid(row=0, column=3, padx=5, pady=5)

# Create buttons for check-in and check-out in a separate row
checkin_button = tk.Button(window, text="Check In", command=lambda:read_camera_faces(True))
checkin_button.grid(row=1, column=0, padx=5, pady=5)
checkout_button = tk.Button(window, text="Check Out", command=lambda:read_camera_faces(False))
checkout_button.grid(row=1, column=1, padx=5, pady=5)

# Run the main event loop
window.mainloop()
