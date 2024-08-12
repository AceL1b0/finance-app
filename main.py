import ttkbootstrap as tb
from ttkbootstrap import *
from ttkbootstrap.toast import ToastNotification
from tkinter import Listbox, filedialog
from datetime import date, datetime
import csv
from excel import Excel
import shutil
import sys, os


def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Month Balance App 1.0/EN")
        self.root.geometry("1000x450")

        self.columns = ["date", "amount", "category", "description"]
        self.csv_file = "finance_data.csv"
        self.today = date.today()

        # Create the notebook
        self.notebook = tb.Notebook(root, bootstyle="danger")
        self.notebook.grid(row=0, column=0, )

        # Create tabs
        self.main_tab = tb.Frame(self.notebook, bootstyle="dark")
        self.csv_file_tab = tb.Frame(self.notebook, bootstyle="dark")
        self.excel_file_tab = tb.Frame(self.notebook, bootstyle="dark")

        self.notebook.add(self.main_tab, text="Main")
        self.notebook.add(self.csv_file_tab, text="CSV Files")
        self.notebook.add(self.excel_file_tab, text="Excel Files")

        # Create a main frame
        frame_1 = tb.Frame(self.main_tab, bootstyle="dark")
        frame_1.grid(row=0, column=0, padx=20, pady=20, sticky="n")

        self.main_label = tb.Label(
            frame_1, text="Enter the transaction", font=("Helvetica", 28),
            bootstyle="info")
        self.main_label.grid(row=1, column=0, columnspan=2, padx=30, pady=30,
                             sticky="w")

        # Create data entries
        # Date
        my_date_label = tb.Label(frame_1, text="Enter the date",
                                 font=("Helvetica", 16), bootstyle="secondary")
        my_date_label.grid(row=2, column=0, padx=5, pady=5, sticky="w")

        self.my_date = tb.DateEntry(frame_1, bootstyle="secondary",
                                    firstweekday=0, width=17,
                                    dateformat="%d-%m-%Y",
                                    startdate=self.today)
        self.my_date.grid(row=2, column=1, padx=5, pady=5)

        # Amount
        amount_label = tb.Label(frame_1, text="Enter the amount ",
                                font=("Helvetica", 16), bootstyle="secondary")
        amount_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        amount_label_2 = tb.Label(
            frame_1, text="(float. point numbers with ' . ' ) ",
            font=("Helvetica", 16), bootstyle="secondary")
        amount_label_2.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.amount = tb.Entry(frame_1, bootstyle="secondary",
                               font=("Helvetica", 16))
        self.amount.grid(row=4, column=1, padx=5, pady=5)

        # Category
        categories = ["", "Income", "Expense"]
        self.category_label = tb.Label(frame_1, text="Enter category",
                                       font=("Helvetica", 16),
                                       bootstyle="secondary")
        self.category_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.category = tb.Combobox(frame_1, bootstyle="secondary",
                                    values=categories, width=18)
        self.category.grid(row=5, column=1, padx=5, pady=5)
        self.category.current(0)

        # Description
        self.description_categories = {
            "Income": ["", "Salary", "Rent Income"],
            "Expense": ["", "Children", "Car", "Drugstore", "Food",
                        "Furnishing", "Electronics", "Standing Payments",
                        "Presents", "Clothes", "Insurance", "Fun",
                        "Animals", "Other"]
        }
        self.description_label = tb.Label(frame_1, text="Enter description",
                                          font=("Helvetica", 16),
                                          bootstyle="secondary")
        self.description_label.grid(row=6, column=0, padx=5, pady=5,
                                    sticky="w")

        self.description = tb.Combobox(frame_1, bootstyle="secondary",
                                       values=[], width=18)
        self.description.grid(row=6, column=1, padx=5, pady=5)

        self.category.bind("<<ComboboxSelected>>", self.update_description)

        # Create button and label for transactions
        # Button to add payment
        add_button = tb.Button(
            frame_1, text="Add Payment", command=self.add,
            bootstyle="warning outline")
        add_button.grid(row=7, column=0, columnspan=2, pady=10)

        # Create frame for displaying payments
        frame_2 = tb.Frame(self.main_tab, bootstyle="dark")
        frame_2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Label for payments list
        payments_label = tb.Label(frame_2, text="Payments",
                                  font=("Helvetica", 28),
                                  bootstyle="info")
        payments_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Listbox to display payments
        self.payments_listbox = Listbox(frame_2, width=50, height=15)
        self.payments_listbox.grid(row=1, column=0, padx=5, pady=5,
                                   sticky="nsew")

        # Configure grid layout for frame_2
        frame_2.grid_rowconfigure(1, weight=1)
        frame_2.grid_columnconfigure(0, weight=1)

        # Create a frame for CSV file and entries
        # Frame for CSV actions
        csv_frame = tb.Frame(self.csv_file_tab, bootstyle="dark")
        csv_frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        # Clear CSV Button
        clear_csv_button = tb.Button(csv_frame, text="Clear CSV",
                                     command=self.clear_csv,
                                     bootstyle="warning outline")
        clear_csv_button.grid(row=0, column=0, padx=5, pady=5)

        # Treeview to display CSV data
        self.csv_treeview = ttk.Treeview(csv_frame, columns=self.columns,
                                         show="headings")
        self.csv_treeview.heading("date", text="Date")
        self.csv_treeview.heading("amount", text="Amount")
        self.csv_treeview.heading("category", text="Category")
        self.csv_treeview.heading("description", text="Description")
        self.csv_treeview.grid(row=1, column=0, columnspan=2, padx=5, pady=5,
                               sticky="nsew")

        # Scrollbar for the Treeview
        scrollbar = ttk.Scrollbar(csv_frame, orient=tk.VERTICAL,
                                  command=self.csv_treeview.yview)
        self.csv_treeview.configure(yscroll=scrollbar.set)
        scrollbar.grid(row=1, column=2, sticky="ns")

        # Configure grid layout for frame_3
        csv_frame.grid_rowconfigure(1, weight=1)
        csv_frame.grid_columnconfigure(1, weight=1)

        # Payments Values
        payment_date_str = self.my_date.entry.get()
        payment_date = datetime.strptime(payment_date_str,
                                         '%d-%m-%Y').date()
        self.payment_date_formated = payment_date.strftime('%d-%m-%Y')
        self.payment_amount = self.amount.get()
        self.payment_category = self.category.get()
        self.payment_description = self.description.get()

        self.load_csv()

        # Populate the Xlsx Tab
        self.frame_3 = tb.Frame(self.excel_file_tab, bootstyle="dark")
        self.frame_3.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.first_day_label = tb.Label(
            self.frame_3, text="Choose the date of the first payment",
            font=("Helvetica", 16), bootstyle="secondary")
        self.first_day_label.grid(row=1, column=0, padx=5, pady=5)

        self.first_day = tb.DateEntry(
            self.frame_3, bootstyle="secondary", firstweekday=0, width=17,
            dateformat="%d-%m-%Y", startdate=self.today)
        self.first_day.grid(row=1, column=1, padx=5, pady=5)

        self.last_day_label = tb.Label(
            self.frame_3, text="Choose the date of the last payment",
            font=("Helvetica", 16), bootstyle="secondary")
        self.last_day_label.grid(row=2, column=0, padx=5, pady=5)

        self.last_day = tb.DateEntry(
            self.frame_3, bootstyle="secondary", firstweekday=0, width=17,
            dateformat="%d-%m-%Y", startdate=self.today)
        self.last_day.grid(row=2, column=1, padx=5, pady=5)

        # Button for generating the xlsx file
        xlsx_button = tb.Button(
            self.frame_3, text="Get Excel",
            command=self.generate_xlsx,
            bootstyle="warning outline")
        xlsx_button.grid(row=3, column=0, columnspan=2, pady=10)

        self.excel_file_tab.grid_rowconfigure(0, weight=1)
        self.excel_file_tab.grid_columnconfigure(0, weight=1)

        # In Excel Tab Create frame_4 for displaying Xlsx Files
        frame_4 = tb.Frame(self.excel_file_tab, bootstyle="dark")
        frame_4.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Label for Xlsx File
        excel_label = tb.Label(frame_4, text="Right Click to Save the File",
                               font=("Helvetica", 28),
                               bootstyle="info")
        excel_label.grid(row=0, column=0, padx=5, pady=5, sticky="n")

        # Listbox to display Xlsx Files
        self.excel_listbox = Listbox(frame_4, width=50, height=15)
        self.excel_listbox.grid(row=1, column=0, padx=5, pady=5,
                                sticky="nsew")

        # Configure grid layout for frame_4
        frame_4.grid_rowconfigure(1, weight=1)
        frame_4.grid_columnconfigure(0, weight=1)

        # Developed by Label
        copyright_label = tb.Label(
            root, text="Developed with Python by AceL1b0",
            font=("Helvetica", 15), bootstyle="danger")
        copyright_label.grid(row=1, column=0, padx=5, pady=5, sticky="ew")

    def update_description(self, event):
        selected_category = self.category.get()

        if selected_category in self.description_categories:
            self.description["values"] = (
                self.description_categories)[selected_category]
            self.description.current(0)
        else:
            self.description["values"] = []
            self.description.set("")

    def clear_csv(self):
        for item in self.csv_treeview.get_children():
            self.csv_treeview.delete(item)

        with open(self.csv_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=self.columns)
            writer.writeheader()

    def load_csv(self):
        try:
            with open(self.csv_file, mode='r') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    self.csv_treeview.insert("", tk.END, values=(
                        row["date"], row["amount"], row["category"],
                        row["description"]))
        except FileNotFoundError:
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.DictWriter(file, fieldnames=self.columns)
                writer.writeheader()

    def add_entry(self, my_date, amount, category, description):
        new_entry = {
            "date": my_date,
            "amount": amount,
            "category": category,
            "description": description
        }

        with open(self.csv_file, "a", newline="") as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.columns)
            writer.writerow(new_entry)

    def add(self):
        payment_date_str = self.my_date.entry.get()
        payment_date = datetime.strptime(payment_date_str,
                                         '%d-%m-%Y').date()
        self.payment_date_formated = payment_date.strftime('%d-%m-%Y')
        self.payment_amount = self.amount.get()
        self.payment_category = self.category.get()
        self.payment_description = self.description.get()

        # Add entry to the CSV file
        self.add_entry(self.payment_date_formated, self.payment_amount,
                       self.payment_category, self.payment_description)

        # Insert payments to the Listbox
        self.payments_listbox.delete(0, tk.END)
        self.payments_listbox.insert(
            tk.END, f"Date: {self.payment_date_formated}")
        self.payments_listbox.insert(
            tk.END, f"Amount: {self.payment_amount}")
        self.payments_listbox.insert(
            tk.END, f"Category: {self.payment_category}")
        self.payments_listbox.insert(
            tk.END, f"Description: {self.payment_description}")
        self.payments_listbox.insert(tk.END, "")

        # Update the main label
        self.main_label.config(text=f"Added successfully")
        self.main_label.after(1500, lambda: self.main_label.config(
            text="Enter the transaction"))

        # Clear the entry fields
        self.amount.delete(0, tb.END)
        self.category.current(0)
        self.description.current(0)

        # Insert the new entry into the Treeview
        self.csv_treeview.insert("", tk.END, values=(
            self.payment_date_formated, self.payment_amount,
            self.payment_category, self.payment_description))

    def generate_xlsx(self):
        first_date_str = self.first_day.entry.get()
        first_date = datetime.strptime(first_date_str,
                                       '%d-%m-%Y').date()
        first_date_formated = first_date.strftime('%d-%m-%Y')

        last_date_str = self.last_day.entry.get()
        last_date = datetime.strptime(last_date_str,
                                      '%d-%m-%Y').date()
        last_date_formated = last_date.strftime('%d-%m-%Y')
        Excel.get_excel(first_date_formated, last_date_formated)

        # Toast Message after generating Xlsx File
        toast_message = ToastNotification(
            title="Months Balance App Message",
            message="Excel file has been generated!",
            duration=5000,
            alert=True
        )
        toast_message.show_toast()

        self.payments_listbox.delete(0, tk.END)
        self.excel_listbox.insert(
            tk.END,
            f"{first_date_formated}_{last_date_formated}.xlsx")

        # Create the context menu
        self.context_menu = tk.Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="Save As",
                                      command=self.save_as)

        # Bind right-click to show the context menu
        self.excel_listbox.bind("<Button-2>", self.show_context_menu)

    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)

    def save_as(self):
        selected_file = self.excel_listbox.get(tk.ACTIVE)
        if selected_file:
            file_path = filedialog.asksaveasfilename(defaultextension=".xlsx",
                                                     filetypes=[("Excel files",
                                                                 "*.xlsx")])
            if file_path:
                shutil.copy(selected_file, file_path)


if __name__ == "__main__":
    root = tb.Window(themename="solar")
    app = FinanceApp(root)
    root.mainloop()
    input()
