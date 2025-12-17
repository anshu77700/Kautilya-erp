import tkinter as tk
from tkinter import messagebox, ttk

# list to store products
products = []

def only_number(value):
    return value == "" or value.replace(".","", 1).isdigit()
root =  tk.Tk()
vcmd = root.register(only_number)
root.title("Product Entry")
root.geometry("300x200")

style = ttk.Style()
style.theme_use("default")
style.configure("TEntry", foreground="black", fieldbackground="white")

# label + input for name
tk.Label(root, text="Product Name").pack()
name_entry = ttk.Entry(root)
name_entry.pack()

# label + input for price
tk.Label(root, text="Price").pack()
price_entry = ttk.Entry(
    root,
    validate="key",
    validatecommand=(vcmd, "%P")
)
price_entry.pack()

def focus_price(event):
    price_entry.focus()

name_entry.bind("<Return>", focus_price)

def add_from_enter(event):
    add_product()

price_entry.bind("<Return>", add_from_enter)

def add_product():
    name = name_entry.get()
    try:
        price = float(price_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Price must be a number")
        return

    if name == "" or price == "":
        messagebox.showerror("Error", "Please enter product name and price")
        return

    products.append({"name": name, "price": price})
    # messagebox.showinfo("Added", f"{name} added successfully")

    product_table.insert("",tk.END, values=(name, price))

    name_entry.delete(0, tk.END)
    price_entry.delete(0, tk.END)
    name_entry.focus()


tk.Button(root, text="Add Product", command=add_product).pack(pady=10)

#Product table

columns = ("name", "price")

product_table = ttk.Treeview(
    root,
    columns=columns,
    show="headings"
)

product_table.heading("name", text="Product Name")
product_table.heading("price", text="Price")

product_table.pack(pady=10, fill="x")

root.mainloop()