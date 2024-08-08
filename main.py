import ttkbootstrap as tb
from ttkbootstrap import *
from ttkbootstrap.toast import ToastNotification
from tkinter import Listbox, filedialog
from datetime import date, datetime
import csv


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
        amount_label = tb.Label(frame_1, text="Enter the amount",
                                font=("Helvetica", 16), bootstyle="secondary")
        amount_label.grid(row=3, column=0, padx=5, pady=5, sticky="w")

        self.amount = tb.Entry(frame_1, bootstyle="secondary",
                               font=("Helvetica", 16))
        self.amount.grid(row=3, column=1, padx=5, pady=5)

        # Category
        categories = ["", "Income", "Expense"]
        category_label = tb.Label(frame_1, text="Enter the category",
                                  font=("Helvetica", 16),
                                  bootstyle="secondary")
        category_label.grid(row=4, column=0, padx=5, pady=5, sticky="w")

        self.category = tb.Combobox(frame_1, bootstyle="secondary",
                                    values=categories, width=18)
        self.category.grid(row=4, column=1, padx=5, pady=5)
        self.category.current(0)

        # Description
        description_categories = ["", "Baby", "Car", "Drugstore", "Food",
                                  "Furnishing", "Other", "Standing Payments",
                                  "Salary", "Rent"]
        description_label = tb.Label(frame_1, text="Enter the description",
                                     font=("Helvetica", 16),
                                     bootstyle="secondary")
        description_label.grid(row=5, column=0, padx=5, pady=5, sticky="w")

        self.description = tb.Combobox(frame_1, bootstyle="secondary",
                                       values=description_categories, width=18)
        self.description.grid(row=5, column=1, padx=5, pady=5)
        self.description.current(0)

        # Create button and label for transactions
        # Button to add payment
        add_button = tb.Button(
            frame_1, text="Add Payment", command=self.add,
            bootstyle="warning outline")
        add_button.grid(row=6, column=0, columnspan=2, pady=10)

        # Create frame for displaying payments
        frame_2 = tb.Frame(self.main_tab, bootstyle="dark")
        frame_2.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # Label for payments list
        payments_label = tb.Label(frame_2, text="Payments",
                                  font=("Helvetica", 16),
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

