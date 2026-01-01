import json
import os
import tkinter as tk
from tkinter import messagebox, ttk
import tkinter.simpledialog as simpledialog

# Function to check if profile exists
def is_profile_created():
    return os.path.exists(SHOP_FILE)

# Save products to JSON
def save_products():
    with open("products.json", "w") as file:
        json.dump(products, file, indent=4)

# Load Products on app start
def load_products():
    global products
    if os.path.exists("products.json"):
        with open("products.json", "r") as file:
            products = json.load(file)


# list to store products
products = []
load_products()


def only_number(value):
    return value == "" or value.replace(".","", 1).isdigit()

# Unique Product ID auto genrator
def generate_product_id():
    return f"P{len(products)+1:03d}"

# To Create GUI
root =  tk.Tk()
vcmd = root.register(only_number)
root.title("Product Entry")
root.geometry("1300x700")


content = tk.Frame(root, bg="white")
content.pack(side="right", fill="both", expand=True)


# Help in screen switch
def clear_content():
    for widget in content.winfo_children():
        widget.destroy()

style = ttk.Style()
style.theme_use("default")
style.configure("TEntry", foreground="black", fieldbackground="white")

def show_product_screen():
    clear_content()

    tk.Label(content, text="Product Master", font=("Arial", 14)).pack(pady=10)
    # label + input for name
    tk.Label(content, text="Product Name").pack()
    name_entry = ttk.Entry(content)
    name_entry.pack()

    tk.Label(content, text="Company Name (Optional)").pack()
    company_entry = ttk.Entry(content)
    company_entry.pack()


    tk.Label(content, text="HSN Code").pack()
    hsn_entry = ttk.Entry(content)
    hsn_entry.pack()


    tk.Label(content, text="Unit (e.g. Box, Strip, Bottle)").pack()
    unit_entry = ttk.Entry(content)
    unit_entry.pack()

    tk.Label(content, text="GST %").pack()
    gst_entry = ttk.Entry(
        content,
        validate="key",
        validatecommand=(vcmd, "%P")
    )
    gst_entry.pack()

    tk.Label(content, text="Opening Stock (Optional)").pack()
    stock_entry = ttk.Entry(
        content,
        validate="key",
        validatecommand=(vcmd, "%P")
    )
    stock_entry.pack()

    # label + input for price
    """
    tk.Label(content, text="Price").pack()
    price_entry = ttk.Entry(
        content,
        validate="key",
        validatecommand=(vcmd, "%P")
    )
    price_entry.pack()
    """

    # To make Keyboard Friendly
    def focus_company(event):
        company_entry.focus()

    def focus_hsn(event):
        hsn_entry.focus()

    def focus_unit(event):
        unit_entry.focus()

    def focus_gst(event):
        gst_entry.focus()

    def focus_stock(event):
        stock_entry.focus()

    name_entry.bind("<Return>", focus_company)
    company_entry.bind("<Return>", focus_hsn)
    hsn_entry.bind("<Return>", focus_unit)
    unit_entry.bind("<Return>", focus_gst)
    gst_entry.bind("<Return>", focus_stock)
    stock_entry.bind("<Return>", lambda e: add_product())

    # def add_from_enter(event):
    #     add_product()

    # stock_entry.bind("<Return>", add_from_enter)

    #error pop-up screen when add product button is clicked
    def add_product():
        product_id = generate_product_id()

        name = name_entry.get()
        company = company_entry.get()
        hsn = hsn_entry.get()
        unit = unit_entry.get()
        try:
            gst = float(gst_entry.get())
        except ValueError:
            messagebox.showerror("Error", "GST must be a number")
            return

        try:
            stock = int(stock_entry.get()) if stock_entry.get() != "" else 0
        except ValueError:
            messagebox.showerror("Error", "Stock must be a number")
            return
    
        if name == "":
            messagebox.showerror("Error", "Product name is required")
            return
    
        products.append({
            "product_id": product_id,
            "name": name,
            "company": company,
            "hsn": hsn,
            "gst": gst,
            "unit": unit,
            "stock": stock
        })
    
        save_products()
        # messagebox.showinfo("Added", f"{name} added successfully")
    
        # product_table.insert("",tk.END, values=(name, price))
    
        name_entry.delete(0, tk.END)
        company_entry.delete(0, tk.END)
        hsn_entry.delete(0, tk.END)
        gst_entry.delete(0, tk.END)
        unit_entry.delete(0, tk.END)
        stock_entry.delete(0, tk.END)
        name_entry.focus()


    tk.Button(content, text="Add Product", command=add_product).pack(pady=10)

    #Product table
    """
    columns = ("name", "price")

    product_table = ttk.Treeview(
        content,
        columns=columns,
        show="headings"
    )

    product_table.heading("name", text="Product Name")
    product_table.heading("price", text="Price")

    product_table.pack(pady=10, fill="x")
    """

# ---------------- USER PROFILE ----------------

# Saving system
SHOP_FILE = "shop_profile.json"

# Fresh User Check
def load_shop_profile():
    if os.path.exists(SHOP_FILE):
        with open(SHOP_FILE, "r") as f:
            return json.load(f)
    return {}

def save_shop_profile(data):
    with open(SHOP_FILE, "w") as f:
        json.dump(data, f, indent=4)


def show_user_profile():
    clear_content()

    tk.Label(content, text="Shop Profile", font=("Arial", 14)).pack(pady=10)

    profile = load_shop_profile()

    entries = {}

    def field(key, label, value="", readonly=True):
        tk.Label(content, text=label).pack()
        e = ttk.Entry(content)
        e.insert(0, value)
        if readonly:
            e.config(state="readonly")
        e.pack()
        entries[key] = e
        return e

    field("shop_name", "Shop Name", profile.get("shop_name", ""))
    field("address", "Address", profile.get("address", ""))
    field("gst", "GST Number", profile.get("gst", ""))
    field("drug1", "Drug License No 1", profile.get("drug1", ""))
    field("drug2", "Drug License No 2", profile.get("drug2", ""))
    field("mob_no", "Mobile Number", profile.get("mob_no", ""))

    save_btn = tk.Button(content, text="Save Profile", state="disabled")
    save_btn.pack(pady=5)

    # Edit User Profile with Master Key
    def enable_editing():
        master_key = simpledialog.askstring(
            "Master Key", "Enter Master Key:", show="*"
        )
        if master_key == "YourSecretKey":
            for e in entries.values():
                e.config(state="normal")
            save_btn.config(state="normal")
        else:
            messagebox.showerror("Error", "Incorrect Master Key")

    def save_profile_changes():
        data = {k: e.get() for k, e in entries.items()}
        save_shop_profile(data)
        messagebox.showinfo("Saved", "Profile updated successfully")
        for e in entries.values():
            e.config(state="readonly")
        save_btn.config(state="disabled")

    save_btn.config(command=save_profile_changes)

    tk.Button(content, text="Edit Profile", command=enable_editing).pack(pady=10)


# Side bar
sidebar = tk.Frame(root, width=200, bg="#2c2c2c")
sidebar.pack(side="left", fill="y")

# Parties master
PARTY_FILE = "parties.json"

def load_parties():
    if os.path.exists(PARTY_FILE):
        with open(PARTY_FILE, "r") as f:
            return json.load(f)
    return []

def save_parties():
    with open(PARTY_FILE, "w") as f:
        json.dump(parties, f, indent=4)

parties = load_parties()

# parties GUI
def show_party_master():
    clear_content()

    tk.Label(content, text="Party Master", font=("Arial", 14)).pack(pady=10)

    def field(label):
        tk.Label(content, text=label).pack()
        e = ttk.Entry(content)
        e.pack()
        return e

    name_entry = field("Party Name")
    address_entry = field("Address")
    gst_entry = field("GST Number")
    drug1_entry = field("Drug Licence 1")
    drug2_entry = field("Drug Licence 2")
    phone_entry = field("Phone (Optional)")
    balance_entry = field("Opening Balance")

    def add_party():
        if name_entry.get() == "":
            messagebox.showerror("Error", "Party Name is required")
            return

        party = {
            "name": name_entry.get(),
            "address": address_entry.get(),
            "gst": gst_entry.get(),
            "drug1": drug1_entry.get(),
            "drug2": drug2_entry.get(),
            "phone": phone_entry.get(),
            "opening_balance": balance_entry.get() or "0"
        }

        parties.append(party)
        save_parties()

        for e in [name_entry, address_entry, gst_entry, drug1_entry, drug2_entry, phone_entry, balance_entry]:
            e.delete(0, tk.END)

        name_entry.focus()

    tk.Button(content, text="Add Party", command=add_party).pack(pady=10)

# -------------------- Billing --------------------

BILL_FILE = "bills.json"

def load_bills():
    if os.path.exists(BILL_FILE):
        with open(BILL_FILE, "r") as f:
            return json.load(f)
    return []

def save_bills():
    with open(BILL_FILE, "w") as f:
        json.dump(bills, f, indent=4)

bills = load_bills()

def generate_bill_no():
    return f"B{len(bills)+1:04d}"

#  < Billing GUI >

def show_billing_screen():
    clear_content()

    current_items = []
    

    # -----------------------
    # SHOP BANNER (TOP)
    # -----------------------
    profile = load_shop_profile()  # load shop details

    banner_frame = tk.Frame(content, bg="#f0f0f0", pady=10)
    banner_frame.pack(fill="x")

    tk.Label(banner_frame, text=profile.get("shop_name", "SHOP NAME"), 
             font=("Arial", 16, "bold"), bg="#f0f0f0").pack()
    tk.Label(banner_frame, text=profile.get("address", ""), 
             font=("Arial", 10), bg="#f0f0f0").pack()
    tk.Label(banner_frame, text=f"GST: {profile.get('gst','')} | Drug License: {profile.get('drug1','')} | {profile.get('drug2', '')}", 
             font=("Arial", 10), bg="#f0f0f0").pack()
    tk.Label(banner_frame, text=f"Mob No: {profile.get('mob_no', '')}",
             font=("Arial", 10), bg="#f0f0f0").pack()


    tk.Label(content, text="Sales Bill", font=("Arial", 16)).pack(pady=10)

    # bill_no = generate_bill_no()
    # tk.Label(content, text=f"Bill No: {bill_no}").pack()

    top_row = tk.Frame(content)
    top_row.pack(fill="x", padx=10, pady=10)

    
    # LEFT RECTANGLE → PARTY DETAILS
    """
    party_box = tk.Frame(
        header_row,
        content,
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    party_box.pack(side="left", fill="both", expand=True, padx=5)
    """
    # tk.Label(
    #     party_box,
    #     text="Party Details",
    #     font=("Arial", 11, "bold")
    # ).pack(anchor="w")

    party_box = tk.Frame(top_row, bd=1, relief="solid", padx=10, pady=10)
    party_box.pack(side="left", fill="x", expand=True, padx=10)

    tk.Label(party_box, text="Party Name").pack(anchor="w")

    party_var = tk.StringVar()
    party_mobile_var = tk.StringVar()
    party_entry = ttk.Entry(party_box, textvariable=party_var)
    party_entry.pack(fill="x", pady=2)
    party_entry.focus()

    party_address_lbl = tk.Label(
        party_box,
        text="",
        wraplength=300,
        fg="gray"
    )
    party_address_lbl.pack(anchor="w", pady=3)


    party_listbox = tk.Listbox(party_box, height=5)
    party_listbox.pack(fill="x")
    party_listbox.pack_forget()

    suggestion_box = tk.Listbox(
        party_box,
        height=5
    )
    suggestion_box.pack(fill="x")
    suggestion_box.pack_forget()


    party_names = [p["name"] for p in parties]
    party_map = {p["name"]: p for p in parties}


    def update_suggestions(event=None):
        typed = party_var.get().lower()
        suggestion_box.delete(0, tk.END)

        if not typed:
            suggestion_box.pack_forget()
            return

        matches = [p for p in party_names if typed in p.lower()]

        if matches:
            suggestion_box.pack(fill="x")
            for m in matches:
                suggestion_box.insert(tk.END, m)
        else:
            suggestion_box.pack_forget()


            
    party_entry.bind("<KeyRelease>", update_suggestions)


    def move_down(event):
        if suggestion_box.size() > 0:
            suggestion_box.focus()
            suggestion_box.selection_set(0)

        party_entry.bind("<Down>", move_down)


    def move_to_list(event):
        if suggestion_box.size() > 0:
            suggestion_box.focus_set()
            suggestion_box.selection_clear(0, tk.END)
            suggestion_box.selection_set(0)


    party_entry.bind("<Down>", move_to_list)


    # def select_party(event=None):
    #     if suggestion_box.curselection():
    #         selected = suggestion_box.get(suggestion_box.curselection())
    #         party_var.set(selected)
    #         suggestion_box.pack_forget()
    #         party_entry.icursor(tk.END)

    #         # 🔥 AUTO-FILL PARTY MOBILE
    #         party_mobile_var.set(party_map[selected].get("phone", ""))

    def select_party(event=None):
        if suggestion_box.curselection():
            selected = suggestion_box.get(suggestion_box.curselection())
            party_var.set(selected)
            suggestion_box.pack_forget()
            party_entry.icursor(tk.END)

            party_data = party_map[selected]

            # ✅ SHOW ADDRESS BELOW PARTY NAME
            party_address_lbl.config(
            text=party_data.get("address", "")
            )

            # 🔥 AUTO-FILL PARTY MOBILE
            party_mobile_var.set(party_map[selected].get("phone", ""))




    suggestion_box.bind("<Return>", select_party)
    suggestion_box.bind("<Double-Button-1>", select_party)

    party_entry.bind("<Escape>", lambda e: suggestion_box.pack_forget())



    party_address_lbl = tk.Label(party_box, text="", wraplength=300)
    party_address_lbl.pack(anchor="w", pady=3)
    # =-=-=--=-=-=-=-

    # RIGHT RECTANGLE → BILL META INFO
    bill_box = tk.Frame(
        top_row,
        bd=1,
        relief="solid",
        padx=10,
        pady=10
    )
    bill_box.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        bill_box,
        text="Bill Information",
        font=("Arial", 11, "bold")
    ).pack(anchor="w")

    # ----------------------------------------

    bill_no = generate_bill_no()
    serial_no = bill_no.replace("B", "")

    from datetime import datetime
    now = datetime.now()

    bill_data = [
        ("Bill No", bill_no),
        ("Serial No", serial_no),
        ("Date", now.strftime("%d-%m-%Y")),
        ("Time", now.strftime("%I:%M %p")),
        ("Party Mobile", "")
    ]

    for label, value in bill_data:
        row = tk.Frame(bill_box)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=label, width=12, anchor="w").pack(side="left")

        if label == "Party Mobile":
            e = ttk.Entry(row, textvariable=party_mobile_var)
        else:
            e = ttk.Entry(row)
            e.insert(0, value)
            e.config(state="readonly")

        e.pack(side="left", fill="x", expand=True)




    # Product dropdown
    tk.Label(content, text="Select Product").pack()
    product_names = [p["name"] for p in products]
    product_var = tk.StringVar()
    product_combo = ttk.Combobox(content, textvariable=product_var, values=product_names)
    product_combo.pack()

    tk.Label(content, text="Quantity").pack()
    qty_entry = ttk.Entry(content)
    qty_entry.pack()

    tk.Label(content, text="Rate").pack()
    rate_entry = ttk.Entry(content)
    rate_entry.pack()

    # tree view table of product
    columns = ("Product", "Qty", "Rate", "Total")

    item_table = ttk.Treeview(content, columns=columns, show="headings", height=6)
    for col in columns:
        item_table.heading(col, text=col)
    item_table.pack(pady=10, fill="x")

    def add_item():
        try:
            qty = float(qty_entry.get())
            rate = float(rate_entry.get())
        except ValueError:
            messagebox.showerror("Error", "Qty and Rate must be numbers")
            return
        
        product = product_var.get()
        if product == "":
            messagebox.showerror("Error", "Select Product")
            return
        
        total = qty * rate

        item = {
            "product": product,
            "qty": qty,
            "rate": rate,
            "total": total
        }

        current_items.append(item)
        item_table.insert("", tk.END, values=(product, qty, rate, total))

        grand = sum(i["total"] for i in current_items)
        grand_total_var.set(f"Grand Total: {grand:.2f}")

        qty_entry.delete(0, tk.END)
        rate_entry.delete(0, tk.END)
        qty_entry.focus()


    tk.Button(content, text="Add Item", command=add_item).pack(pady=5)

    grand_total_var = tk.StringVar(value="0.00")
    tk.Label(content, textvariable=grand_total_var, font=("Arial", 12)).pack()

    """
    def calculate_total():
        try:
            qty = float(qty_entry.get())
            rate = float(rate_entry.get())
            total = qty * rate
            grand_total_var.set(f"Grand Total: {total:.2f}")
        except:
            pass

    qty_entry.bind("<KeyRelease>", lambda e: calculate_total())
    rate_entry.bind("<KeyRelease>", lambda e: calculate_total())
    """

    def save_bill():
        if party_var.get() == "" or not current_items:
            messagebox.showerror("Error", "Party and items required")
            return

        bill = {
            "bill_no": bill_no,
            "party": party_var.get(),
            "items": current_items,
            "grand_total": grand_total_var.get()
        }

        bills.append(bill)
        save_bills()
        messagebox.showinfo("Saved", "Bill saved")
        show_billing_screen()


    tk.Button(content, text="Save Bill", command=save_bill).pack(pady=10)


#Side Bar Buttons

tk.Button(
    sidebar,
    text="Billing",
    command=show_billing_screen
).pack(fill="x", pady=5)


tk.Button(
    sidebar,
    text="Party Master",
    command=show_party_master
).pack(fill="x", pady=5)

tk.Button(
    sidebar,
    text="Product Master",
    command=show_product_screen
).pack(fill="x", pady=5)
tk.Button(
    sidebar,
    text="User Profile",
    command=show_user_profile
).pack(fill="x", pady=5)

show_product_screen()

# fresh user setup
def show_first_time_profile():
    # Disable sidebar buttons
    for widget in sidebar.winfo_children():
        widget.config(state="disabled")
    
    clear_content()
    
    tk.Label(content, text="Welcome! Create Shop Profile", font=("Arial", 16)).pack(pady=20)
    
    def field(label):
        tk.Label(content, text=label).pack()
        e = ttk.Entry(content)
        e.pack()
        return e
    
    shop_name = field("Shop Name")
    address = field("Address")
    gst = field("GST Number")
    drug1 = field("Drug License No 1")
    drug2 = field("Drug License No 2")
    mob_no = field("Mobile Number")
    
    def save_profile_first_time():
        if shop_name.get() == "":
            messagebox.showerror("Error", "Shop Name is required")
            return
        data = {
            "shop_name": shop_name.get(),
            "address": address.get(),
            "gst": gst.get(),
            "drug1": drug1.get(),
            "drug2": drug2.get(),
            "mob_no": mob_no.get()
        }
        save_shop_profile(data)
        # Re-enable sidebar buttons
        for widget in sidebar.winfo_children():
            widget.config(state="normal")
        # Show normal profile screen
        show_user_profile()
    
    tk.Button(content, text="Save Profile", command=save_profile_first_time).pack(pady=20)

# checking if user is fresh or not
if not is_profile_created():
    show_first_time_profile()
else:
    show_product_screen()

root.mainloop()