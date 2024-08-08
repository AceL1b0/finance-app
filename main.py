import ttkbootstrap as tb
from ttkbootstrap import *
from ttkbootstrap.toast import ToastNotification
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