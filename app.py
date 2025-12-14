import tkinter as tk
from tkinter import messagebox

#Create Window
root = tk.Tk()
root.title("My first app")

#Function to run on button click
def say_Hello():
    messagebox.showinfo("Hello", "Hello! This is your first GUI button.")

#Create Button
btn = tk.Button(root, text="Click Me", command=say_Hello)
btn.pack(pady=20) #place button in window

#Run the window
root.mainloop()