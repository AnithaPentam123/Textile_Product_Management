import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os
from datetime import datetime

CSV_FILE = "products.csv"

# ----------------- CSV Init -------------------
def init_csv():
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["ID", "Name", "Type", "Quantity", "Date"])

def get_next_id():
    try:
        with open(CSV_FILE, mode='r') as file:
            rows = list(csv.reader(file))[1:]
            return len(rows) + 1
    except:
        return 1

# ----------------- Main Class -----------------
class TextileInventory:
    def __init__(self, root):
        self.root = root
        self.root.title("Textile Inventory Management (CSV Version)")
        self.root.geometry("800x500")
        init_csv()
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Textile Industry Inventory", font=("Helvetica", 20, "bold"))
        title.pack(pady=10)

        tab_control = ttk.Notebook(self.root)
        
        self.receive_tab = ttk.Frame(tab_control)
        self.sale_tab = ttk.Frame(tab_control)
        self.view_tab = ttk.Frame(tab_control)
        self.count_tab = ttk.Frame(tab_control)

        tab_control.add(self.receive_tab, text="Receive Product")
        tab_control.add(self.sale_tab, text="Sell Product")
        tab_control.add(self.view_tab, text="View All")
        tab_control.add(self.count_tab, text="Stats")

        tab_control.pack(expand=1, fill='both')

        self.create_receive_tab()
        self.create_sale_tab()
        self.create_view_tab()
        self.create_stats_tab()

    # ----------- Receive Tab -------------
    def create_receive_tab(self):
        tk.Label(self.receive_tab, text="Product Name:").pack(pady=5)
        self.r_name = tk.Entry(self.receive_tab)
        self.r_name.pack()

        tk.Label(self.receive_tab, text="Quantity:").pack(pady=5)
        self.r_qty = tk.Entry(self.receive_tab)
        self.r_qty.pack()

        tk.Button(self.receive_tab, text="Add Received Product", command=self.add_received).pack(pady=10)

    def add_received(self):
        name = self.r_name.get()
        qty = self.r_qty.get()

        if name == "" or not qty.isdigit():
            messagebox.showerror("Error", "Please enter valid data")
            return

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id(), name, "Received", qty, datetime.now().strftime("%Y-%m-%d")])

        messagebox.showinfo("Success", "Received product added!")
        self.r_name.delete(0, tk.END)
        self.r_qty.delete(0, tk.END)

    # ----------- Sale Tab ----------------
    def create_sale_tab(self):
        tk.Label(self.sale_tab, text="Product Name:").pack(pady=5)
        self.s_name = tk.Entry(self.sale_tab)
        self.s_name.pack()

        tk.Label(self.sale_tab, text="Quantity:").pack(pady=5)
        self.s_qty = tk.Entry(self.sale_tab)
        self.s_qty.pack()

        tk.Button(self.sale_tab, text="Add Sold Product", command=self.add_sold).pack(pady=10)

    def add_sold(self):
        name = self.s_name.get()
        qty = self.s_qty.get()

        if name == "" or not qty.isdigit():
            messagebox.showerror("Error", "Please enter valid data")
            return

        with open(CSV_FILE, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([get_next_id(), name, "Sold", qty, datetime.now().strftime("%Y-%m-%d")])

        messagebox.showinfo("Success", "Sold product added!")
        self.s_name.delete(0, tk.END)
        self.s_qty.delete(0, tk.END)

    # ----------- View Tab ----------------
    def create_view_tab(self):
        self.tree = ttk.Treeview(self.view_tab, columns=("ID", "Name", "Type", "Quantity", "Date"), show="headings")
        for col in ["ID", "Name", "Type", "Quantity", "Date"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill='both', expand=True)

        tk.Button(self.view_tab, text="Refresh", command=self.load_csv_data).pack(pady=5)
        self.load_csv_data()

    def load_csv_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)

        try:
            with open(CSV_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.tree.insert("", tk.END, values=(row["ID"], row["Name"], row["Type"], row["Quantity"], row["Date"]))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ----------- Stats Tab ---------------
    def create_stats_tab(self):
        self.stats_label = tk.Label(self.count_tab, font=("Arial", 14))
        self.stats_label.pack(pady=20)
        tk.Button(self.count_tab, text="Show Stats", command=self.calculate_stats).pack()

    def calculate_stats(self):
        received = 0
        sold = 0

        try:
            with open(CSV_FILE, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    qty = int(row["Quantity"])
                    if row["Type"] == "Received":
                        received += qty
                    elif row["Type"] == "Sold":
                        sold += qty
        except Exception as e:
            messagebox.showerror("Error", str(e))
            return

        stock = received - sold
        self.stats_label.config(text=f"Total Received: {received} | Total Sold: {sold} | In Stock: {stock}")

# ----------------- Run -----------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TextileInventory(root)
    root.mainloop()

