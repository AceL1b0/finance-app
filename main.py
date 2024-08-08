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
