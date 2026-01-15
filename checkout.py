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

# def load_products():
#     # global products
#     if os.path.exists(PRODUCT_FILE):
#         with open (PRODUCT_FILE, "r") as f:
#             return json.load(f)
#     return[]

# products = load_products()
# product_map = {p["name"]: p for p in products}

# def save_products():
#     with open(PRODUCT_FILE, "w") as f:
#         json dump





# products = json.load(open("products.json"))


# list to store products
products = []
load_products()
product_map = {p["name"]: p for p in products}


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

current_product_name = None

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
    return f"A{len(bills)+1:04d}"

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
    serial_no = bill_no.replace("A", "")

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


# -------------------- Purchase Bill Entry --------------------

PURCHASE_FILE = "purchases.json"

def load_purchases():
    if os.path.exists(PURCHASE_FILE):
        with open(PURCHASE_FILE, "r") as f:
            return json.load(f)
    return []

def save_purchases():
    with open(PURCHASE_FILE, "w") as f:
        json.dump(purchases, f, indent=4)

purchases = load_purchases()

def generate_purchase_no():
    return f"PB{len(purchases)+1:04d}"

clear_editor = None
table_active = False

def show_purchase_screen():
    clear_content()

    # ---------- SHOP BANNER ----------
    profile = load_shop_profile()

    banner = tk.Frame(content, bg="#f0f0f0", pady=10)
    banner.pack(fill="x")

    tk.Label(banner, text=profile.get("shop_name", ""), font=("Arial", 16, "bold"), bg="#f0f0f0").pack()
    tk.Label(banner, text=profile.get("address", ""), bg="#f0f0f0").pack()
    tk.Label(
        banner,
        text=f"GST: {profile.get('gst','')} | DL: {profile.get('drug1','')} {profile.get('drug2','')}",
        bg="#f0f0f0"
    ).pack()
    tk.Label(banner, text=f"Mob: {profile.get('mob_no','')}", bg="#f0f0f0").pack()

    tk.Label(content, text="Purchase Entry", font=("Arial", 16)).pack(pady=10)

    top_row = tk.Frame(content)
    top_row.pack(fill="x", padx=10)

    # -----------------------
    # SUPPLIER SELECTION BOX
    # -----------------------

    supplier_box = tk.Frame(top_row, bd=1, relief="solid", padx=10, pady=10)
    supplier_box.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(
        supplier_box,
        text="Supplier Details",
        font=("Arial", 11, "bold")
    ).pack(anchor="w")

    # Variables
    supplier_name_var = tk.StringVar()
    supplier_mobile_var = tk.StringVar()

    # Entry
    tk.Label(supplier_box, text="Supplier Name").pack(anchor="w")
    supplier_entry = ttk.Entry(supplier_box, textvariable=supplier_name_var)
    supplier_entry.pack(fill="x", pady=2)
    supplier_entry.focus()

    # Suggestion listbox
    supplier_listbox = tk.Listbox(supplier_box, height=5)
    supplier_listbox.pack(fill="x")
    supplier_listbox.pack_forget()

    # Address label
    supplier_address_lbl = tk.Label(
        supplier_box,
        text="",
        wraplength=300,
        fg="gray"
    )
    supplier_address_lbl.pack(anchor="w", pady=3)


    # Load suppliers
    supplier_names = [p["name"] for p in parties]
    supplier_map = {p["name"]: p for p in parties}


    def update_supplier_suggestions(event=None):
        typed = supplier_name_var.get().lower()
        supplier_listbox.delete(0, tk.END)

        if not typed:
            supplier_listbox.pack_forget()
            return

        matches = [n for n in supplier_names if typed in n.lower()]

        if matches:
            supplier_listbox.pack(fill="x")
            for m in matches:
                supplier_listbox.insert(tk.END, m)
        else:
            supplier_listbox.pack_forget()


    def select_supplier(event=None):
        if not supplier_listbox.curselection():
            return

        name = supplier_listbox.get(supplier_listbox.curselection())
        data = supplier_map.get(name, {})

        supplier_name_var.set(name)
        supplier_mobile_var.set(data.get("phone", ""))
        supplier_address_lbl.config(text=data.get("address", ""))

        supplier_listbox.pack_forget()
        supplier_entry.icursor(tk.END)
        supplier_entry.focus()


    def supplier_key_down(event):
        if supplier_listbox.winfo_ismapped():
            supplier_listbox.focus()
            supplier_listbox.selection_set(0)



    # Bindings
    supplier_entry.bind("<KeyRelease>", update_supplier_suggestions)
    supplier_entry.bind("<Down>", supplier_key_down)

    supplier_listbox.bind("<Return>", select_supplier)
    supplier_listbox.bind("<Double-Button-1>", select_supplier)

    supplier_listbox.bind(
        "<Up>",
        lambda e: supplier_entry.focus()
    )

    supplier_bill_entry = None

    def supplier_enter(event):
        # If suggestion list is open, select from it
        if supplier_listbox.winfo_ismapped():
            select_supplier()
            return "break"

        # Otherwise move to Supplier Bill No
        if supplier_bill_entry:
            supplier_bill_entry.focus()
            supplier_bill_entry.select_range(0, tk.END)
        
        return "break"

    supplier_entry.bind("<Return>", supplier_enter)


    # ---------- PURCHASE META ----------

    from datetime import datetime
    now = datetime.now()

    bill_box = tk.Frame(top_row, bd=1, relief="solid", padx=10, pady=10)
    bill_box.pack(side="left", fill="both", expand=True, padx=5)

    tk.Label(bill_box, text="Purchase Info", font=("Arial", 11, "bold")).pack(anchor="w")

    purchase_no = generate_purchase_no()

    meta = [
        ("Purchase No", purchase_no),
        ("Supplier Bill No", ""),
        ("Date", datetime.now().strftime("%d-%m-%Y")),
        ("Time", datetime.now().strftime("%I:%M %p")),
        ("Supplier Mobile", supplier_mobile_var)
    ]

    for label, value in meta:
        row = tk.Frame(bill_box)
        row.pack(fill="x", pady=2)

        tk.Label(row, text=label, width=15, anchor="w").pack(side="left")

        # Supplier Mobile → auto-filled
        if isinstance(value, tk.StringVar):
            e = ttk.Entry(row, textvariable=value)
            e.config(state="readonly")

        # Supplier Bill No → editable
        elif label == "Supplier Bill No":
            supplier_bill_entry = ttk.Entry(row)
            e = supplier_bill_entry

        # Other fields → readonly
        else:
            e = ttk.Entry(row)
            e.insert(0, value)
            e.config(state="readonly")

        e.pack(side="left", fill="x", expand=True)



        # e = ttk.Entry(row, textvariable=supplier_mobile_var)

    EDITABLE_COLS = [3, 4, 9]  # Qty → Free → Discount

    def on_supplier_bill_enter(event):

        global table_active, current_row_id, current_col_index

        table_active = True

        item_table.focus_set()

        # select first row automatically
        first_row = item_table.get_children()[0]
        item_table.selection_set(first_row)
        item_table.focus_set()

        # logical cursor to PRODUCT column
        current_row_id = first_row
        current_col_index = 0

        return "break"

    supplier_bill_entry.bind("<Return>", on_supplier_bill_enter)


    # ---------- ITEMS TABLE PLACEHOLDER ----------
    # current_row_id = None
    # current_col_index = None
    global cell_editor
    cell_editor = None
    tk.Label(content, text="Purchase Items", font=("Arial", 13)).pack(pady=10)

    columns = ("Product",
               "Batch",
               "Expiry",
               "Qty",
               "Free",
               "Purchase Rate",
               "Amount",
               "Trade Rate",
               "MRP",
               "Dis%",
               "GST",
               )
    item_table = ttk.Treeview(content, columns=columns, show="headings", height=10, selectmode="browse")
    for col in columns:
        item_table.heading(col, text=col)
        item_table.column(col, width=90, anchor="center")
    item_table.pack(pady=10, fill="x")
    item_table.focus_set()
    item_table.configure(yscrollcommand=scrollbar.set)


    item_table.insert("", "end", values=("", "", "", "", "", "", "", "", "", "", ""))

    summary_frame = tk.Frame(content, bd=1, relief="solid")
    summary_frame.pack(fill="x", padx=10, pady=5)

    summary_vars = {
        "deal": tk.StringVar(value="0.00"),
        "discount": tk.StringVar(value="0.00"),
        "cgst": tk.StringVar(value="0.00"),
        "sgst": tk.StringVar(value="0.00"),
        "net": tk.StringVar(value="0.00"),
        "round": tk.StringVar(value="0.00"),
    }

    def summary_row(label, var, bold=False):
        f = ("Arial", 11, "bold") if bold else ("Arial", 11)
        row = tk.Frame(summary_frame)
        row.pack(fill="x", padx=10, pady=2)
        tk.Label(row, text=label, font=f).pack(side="left")
        tk.Label(row, textvariable=var, font=f).pack(side="right")

    summary_row("Deal Discount", summary_vars["deal"])
    summary_row("Item Discount", summary_vars["discount"])
    summary_row("CGST", summary_vars["cgst"])
    summary_row("SGST", summary_vars["sgst"])
    summary_row("Net Amount", summary_vars["net"])
    summary_row("ROUND OFF", summary_vars["round"], bold=True)



    def get_payable_qty(qty, free_text):
        free_text = free_text.strip()

        if not free_text:
            return qty

        # Case 2: slab scheme like 10+2
        if "+" in free_text:
            try:
                base, free = free_text.split("+")
                base = int(base)
                free = int(free)

                slabs = qty // base
                free_qty = slabs * free

                return qty - free_qty
            except:
                return qty

        # Case 1: simple free (adds to stock, not discount)
        return qty



    def parse_free_deal(free_text):
        free_text = free_text.strip()

        if not free_text:
            return 0, 0   # free_stock, free_discount

        # Case 2: scheme like 10+1
        if "+" in free_text:
            try:
                _, free = free_text.split("+")
                return 0, int(free)
            except:
                return 0, 0

        # Case 1: simple free like 1,2,3
        try:
            return int(free_text), 0
        except:
            return 0, 0
        


    def edit_table_cell(row_id, col_index):
        global current_row_id, current_col_index, cell_editor
        print("CELL_EDITOR INITIALIZED")


        if cell_editor:
            cell_editor.destroy()

        bbox = item_table.bbox(row_id, f"#{col_index + 1}")
        if not bbox:
            return

        x, y, w, h = bbox

        value = item_table.item(row_id, "values")[col_index]

        cell_editor = ttk.Entry(item_table)
        cell_editor.place(x=x, y=y, width=w, height=h)
        cell_editor.insert(0, value)
        cell_editor.focus()
        cell_editor.select_range(0, tk.END)

        current_row_id = row_id
        current_col_index = col_index

        cell_editor.bind("<Return>", save_cell_and_move)
        cell_editor.bind("<Escape>", lambda e: cell_editor.destroy())


    def save_cell_and_move(event=None):
        global cell_editor, current_col_index, current_row_id

        if not cell_editor:
            return

        value = cell_editor.get()
        set_table_cell(current_row_id, current_col_index, value)

        cell_editor.destroy()
        cell_editor = None

        # 🔁 CUSTOM FLOW
        if current_col_index in EDITABLE_COLS:
            idx = EDITABLE_COLS.index(current_col_index)

            if idx < len(EDITABLE_COLS) - 1:
                next_col = EDITABLE_COLS[idx + 1]
                edit_table_cell(current_row_id, next_col)
            else:
                calculate_net_amount(current_row_id)
                # focus_table_cell(current_row_id, 6)  # Net Amount
                add_new_product_row()

        return "break"

    def calculate_net_amount(row_id):
        values = list(item_table.item(row_id, "values"))

        try:
            qty = float(values[3])                 # Qty
            free_text = values[4]                  # Free
            purchase_rate = float(values[5])          # Trade Rate (NO GST)
            discount_pct = float(values[9] or 0)   # Discount %
        except:
            return

        # payable qty after scheme
        payable_qty = get_payable_qty(qty, free_text)

        gross = payable_qty * purchase_rate

        discount_value = (gross * discount_pct) / 100

        amount = round(gross - discount_value, 2)

        values[6] = amount   # ✅ Amount column (index 6)

        item_table.item(row_id, values=values)

    def update_summary():
        data = calculate_final_bill()

        summary_vars["deal"].set(f"₹ {data['deal']}")
        summary_vars["discount"].set(f"₹ {data['discount']}")
        summary_vars["cgst"].set(f"₹ {data['cgst']}")
        summary_vars["sgst"].set(f"₹ {data['sgst']}")
        summary_vars["net"].set(f"₹ {data['net']}")
        summary_vars["round"].set(f"₹ {data['round_off']}")


    def add_new_product_row():
        global current_row_id, current_col_index

        new_row = item_table.insert(
            "",
            "end",
            values=("", "", "", "", "", "", "", "", "", "", "")
        )

        current_row_id = new_row
        current_col_index = 0

        item_table.selection_set(new_row)
        item_table.focus_set()

        # 🔥 THIS LINE IS MISSING
        open_product_popup()




    def calculate_final_bill():
        total_amount = 0
        deal_discount = 0
        item_discount = 0
        gst_total = 0

        for row in item_table.get_children():
            values = item_table.item(row, "values")

            try:
                qty = float(values[3])
                free_text = values[4]
                rate = float(values[7])   # Trade Rate (NO GST)
                disc_pct = float(values[9] or 0)
                gst_pct = float(values[10] or 0)
            except:
                continue

            payable_qty = get_payable_qty(qty, free_text)

            gross = payable_qty * rate

            free_stock, free_scheme = parse_free_deal(free_text)
            deal_discount += free_scheme * rate

            disc_value = (gross * disc_pct) / 100
            item_discount += disc_value

            taxable = gross - disc_value
            gst_value = (taxable * gst_pct) / 100
            gst_total += gst_value

            total_amount += taxable

        cgst = sgst = gst_total / 2

        net = total_amount + gst_total
        rounded = (net)
        round_off = round(rounded)

        return {
            "deal": round(deal_discount, 2),
            "discount": round(item_discount, 2),
            "cgst": round(cgst, 2),
            "sgst": round(sgst, 2),
            "net": round(rounded, 2),
            "round_off": round_off
        }



    def focus_table_cell(row_id, col_index):
        global current_row_id, current_col_index

        current_row_id = row_id
        current_col_index = col_index

        item_table.selection_set(row_id)
        item_table.focus(row_id)

        print("FOCUS → row:", row_id, "col:", col_index)


    # auto-select first row & set logical cursor
    first_row = item_table.get_children()[0]
    focus_table_cell(first_row, 0)

    item_table.selection_set(first_row)
    item_table.focus_set()

    current_row_id = first_row
    current_col_index = 0



    def set_table_cell(row_id, col_index, value):
        values = list(item_table.item(row_id, "values"))
        values[col_index] = value
        item_table.item(row_id, values=values)


    def on_escape(event):
        if not table_active:
            return
        update_summary()

    root.bind("<Escape>", on_escape)





    # product_map = {p["name"]: p for p in products}
    # product_name = None
    def open_product_popup():
        # nonlocal product_name

        popup = tk.Toplevel(root)
        popup.title("Select Product")
        popup.geometry("450x350")
        popup.transient(root)
        popup.grab_set()

        tk.Label(popup, text="Select Product", font=("Arial", 12, "bold")).pack(pady=5)

        search_var = tk.StringVar()
        search_entry = ttk.Entry(popup, textvariable=search_var)
        search_entry.pack(fill="x", padx=10)
        search_entry.focus()

        listbox = tk.Listbox(popup)
        listbox.pack(fill="both", expand=True, padx=10, pady=5)

        product_names = [p["name"] for p in products]

        def update_list(*args):
            typed = search_var.get().lower()
            listbox.delete(0, tk.END)

            for name in product_names:
                if typed in name.lower():
                    listbox.insert(tk.END, name)

        def select_product(event=None):

            global current_product_name

            if not listbox.curselection():
                return

            current_product_name = listbox.get(listbox.curselection())

            # 1️⃣ Set PRODUCT column
            set_table_cell(current_row_id, 0, current_product_name)

            # 2️⃣ Get product data
            product = product_map.get(current_product_name, {})

            # 3️⃣ Get GST %
            gst_value = product.get("gst", product.get("gst_percent", ""))

            # 4️⃣ Set GST column (index 9)
            set_table_cell(current_row_id, 10, gst_value)

            popup.destroy()

            # move logical cursor to Batch column
            global current_col_index
            current_col_index = 1

            open_batch_popup()

            print("PRODUCT SELECTED →", current_product_name, "GST →", gst_value)


        def move_to_listbox(event):
            if listbox.size() > 0:
                listbox.focus_set()
                listbox.selection_clear(0, tk.END)
                listbox.selection_set(0)
            return "break"



        search_var.trace_add("write", update_list)

        listbox.bind("<Return>", select_product)
        listbox.bind("<Double-Button-1>", select_product)
        search_entry.bind("<Down>", move_to_listbox)
        listbox.bind("<Up>", lambda e: search_entry.focus())


        popup.bind("<Escape>", lambda e: popup.destroy())


    def on_item_click(event):
        global current_row_id, current_col_index


        row_id = item_table.identify_row(event.y)
        col = item_table.identify_column(event.x)

        if not row_id or not col:
            return

        current_row_id = row_id
        current_col_index = int(col[1:]) - 1

        item_table.selection_set(row_id)

        item_table.focus_set()
        print("CLICK → row:", current_row_id, "col:", current_col_index)



    item_table.bind("<Button-1>", on_item_click)


    def on_enter_key(event):
        global current_row_id, current_col_index, cell_editor, table_active

        # ❌ If table is NOT active → ignore
        if not table_active:
            return

        # If editor is open → editor handles Enter
        if cell_editor:
            return

        if current_row_id is None or current_col_index is None:
            return "break"

        # PRODUCT column
        if current_col_index == 0:
            open_product_popup()
            return "break"

        # Other editable columns
        if current_col_index in EDITABLE_COLS:
            edit_table_cell(current_row_id, current_col_index)
            return "break"

        return "break"



    root.bind("<Return>", on_enter_key)
    # item_table.bind("<Return>", on_enter_key)


    def open_batch_popup():

        global current_product_name

        if current_row_id is None:
            return

        values = item_table.item(current_row_id, "values")
        current_product_name = values[0]

        if not current_product_name:
            messagebox.showwarning("Select Product", "Select product first")
            return

        product = product_map.get(current_product_name)
        if not product:
            return

        popup = tk.Toplevel(root)
        popup.title(f"Batch – {current_product_name}")
        popup.geometry("600x350")
        popup.transient(root)
        popup.grab_set()

        tk.Label(
            popup,
            text=f"Select Batch for {current_product_name}",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        columns = ("Batch", "Expiry", "Stock")
        tree = ttk.Treeview(popup, columns=columns, show="headings", height=8)
        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, anchor="center")
        tree.pack(fill="both", expand=True, padx=10)

        # Load batches
        batches = product.get("batches", [])
        for b in batches:
            tree.insert(
                "",
                "end",
                values=(b["batch"], b["expiry"], b.get("stock", 0))
            )

        tree.focus_set()
        if tree.get_children():
            tree.selection_set(tree.get_children()[0])
        """
        def select_batch(event=None):
            sel = tree.selection()
            if not sel:
                return

            batch, expiry, stock = tree.item(sel[0], "values")

            row_values = list(item_table.item(current_row_id, "values"))
            row_values[1] = batch
            row_values[2] = expiry
            item_table.item(current_row_id, values=row_values)

            popup.destroy()

            # Move to Qty
            focus_table_cell(current_row_id, 3)
        """

        def select_batch(event=None):
            sel = tree.selection()
            if not sel:
                return

            batch_no, expiry, stock = tree.item(sel[0], "values")

            # find full batch object
            selected_batch = None
            for b in product.get("batches", []):
                if b["batch"] == batch_no:
                    selected_batch = b
                    break

            if not selected_batch:
                return

            row_values = list(item_table.item(current_row_id, "values"))

            row_values[1] = batch_no               # Batch
            row_values[2] = expiry                 # Expiry
            row_values[5] = selected_batch["purchase_rate"]
            row_values[7] = selected_batch["trade_rate"]
            row_values[8] = selected_batch["mrp"]

            item_table.item(current_row_id, values=row_values)

            popup.destroy()

            # move cursor to Qty
            # focus_table_cell(current_row_id, 3)
            edit_table_cell(current_row_id, 3)



        def open_add_batch(event=None):
            popup.destroy()
            open_add_batch_popup(product)

        tree.bind("<Return>", select_batch)
        tree.bind("<Double-Button-1>", select_batch)
        popup.bind("<Escape>", lambda e: popup.destroy())
        popup.bind("<F2>", open_add_batch)

    def open_add_batch_popup(product):

        batch_no_var = tk.StringVar()
        expiry_var = tk.StringVar()
        pr_var = tk.StringVar()
        tr_var = tk.StringVar()
        mrp_var = tk.StringVar()
        
        popup = tk.Toplevel(root)
        popup.title("Add New Batch")
        popup.geometry("350x260")
        popup.transient(root)
        popup.grab_set()

        tk.Label(popup, text=f"Add Batch – {product['name']}",
                     font=("Arial", 11, "bold")).pack(pady=5)


        entries = []

        for label, var in [
            ("Batch No", batch_no_var),
            ("Expiry (MM-YYYY)", expiry_var),
            ("Purchase Rate", pr_var),
            ("Trade Rate", tr_var),
            ("MRP", mrp_var)
        ]:
            tk.Label(popup, text=label).pack(anchor="w", padx=10)
            e = ttk.Entry(popup, textvariable=var)
            e.pack(fill="x", padx=10, pady=2)
            entries.append(e)

        entries[0].focus_set()

        for i in range(len(entries) - 1):
            entries[i].bind(
                "<Return>",
                lambda e, nxt=entries[i + 1]: (nxt.focus_set(), "break")
            )





        def save_batch():
            global current_product_name

            try:
                batch_no = batch_no_var.get().strip()
                expiry = expiry_var.get().strip()
                pr = float(pr_var.get())
                tr = float(tr_var.get())
                mrp = float(mrp_var.get())

                if not batch_no or not expiry:
                    raise ValueError

            except ValueError:
                messagebox.showerror(
                    "Invalid Input",
                    "Please fill all fields correctly"
                )
                return

            new_batch = {
                "batch": batch_no,
                "expiry": expiry,
                "purchase_rate": pr,
                "trade_rate": tr,
                "mrp": mrp,
                "stock": 0
            }

            for p in products:
                if p["name"] == current_product_name:
                    p.setdefault("batches", []).append(new_batch)
                    break

            save_products()          # ✅ save permanently
            popup.destroy()          # ✅ close popup
            open_batch_popup()       # ✅ reopen batch list

        ttk.Button(popup, text="Save Batch", command=save_batch).pack(pady=10) 
        entries[-1].bind("<Return>", lambda e: save_batch())
        popup.bind("<Return>", lambda e: save_batch()) 
        popup.bind("<Escape>", lambda e: popup.destroy())








#Side Bar Buttons

tk.Button(
    sidebar,
    text="Purchase Entry",
    command=show_purchase_screen
).pack(fill="x", pady=5)


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