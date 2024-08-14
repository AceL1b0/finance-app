import pandas as pd
from datetime import datetime


class Excel:
    csv_file = "finance_data.csv"
    format = "%d-%m-%Y"

    @classmethod
    def get_excel(cls, start_date, end_date):
        df = pd.read_csv(cls.csv_file)
        df["date"] = pd.to_datetime(df["date"], format=Excel.format)

        start_date = datetime.strptime(start_date, Excel.format)
        end_date = datetime.strptime(end_date, Excel.format)

        mask = (df["date"] >= start_date) & (df["date"] <= end_date)
        cls.filtered_df = df.loc[mask]

        start_date_str = start_date.strftime("%d-%m-%Y")
        end_date_str = end_date.strftime("%d-%m-%Y")

        xlsx_file = f"{start_date_str}_{end_date_str}.xlsx"

        df = pd.DataFrame(cls.filtered_df)
        df['date'] = pd.to_datetime(df['date']).dt.strftime('%d-%m-%Y')

        total_income = df[df['category'] == 'Income']['amount'].sum()
        total_expense = df[df['category'] == 'Expense']['amount'].sum()
        savings = total_income - total_expense

        # Categories
        food = df[df['description'] == 'Food']['amount'].sum()
        furnishing = df[df['description'] == 'Furnishing']['amount'].sum()
        car = df[df['description'] == 'Car']['amount'].sum()
        drug_store = df[df['description'] == 'Drug Store']['amount'].sum()
        electronics = df[df['description'] == 'Electronics']['amount'].sum()
        baby = df[df['description'] == 'Baby']['amount'].sum()
        standing_payments = (
            df[df['description'] == 'Standing Payments']['amount'].sum())
        presents = df[df['description'] == 'Presents']['amount'].sum()
        clothes = df[df['description'] == 'Clothes']['amount'].sum()
        insurance = df[df['description'] == 'Insurance']['amount'].sum()
        fun = df[df['description'] == 'Fun']['amount'].sum()
        animals = df[df['description'] == 'Animals']['amount'].sum()
        other = df[df['description'] == 'Other']['amount'].sum()

        salary = df[df['description'] == 'Salary']['amount'].sum()
        rent_income = df[df['description'] == 'Rent Income']['amount'].sum()

        # XlsxConstructor
        writer = pd.ExcelWriter(
            xlsx_file, engine="xlsxwriter", date_format="yyyy-mm-dd")

        df.to_excel(writer, sheet_name="Sheet1", index=False)

        workbook = writer.book
        worksheet = writer.sheets["Sheet1"]
        worksheet.set_tab_color("#808080")

        header_format = workbook.add_format({
            "bold": True,
            "bg_color": "#FFC0CB",
            "font_color": "#000000",
            "border": 1

        })

        for col_num, value in enumerate(df.columns.values):
            worksheet.write(0, col_num, value, header_format)
            worksheet.set_column(col_num, col_num, 20)

        format_amount = workbook.add_format({"num_format": "#,##0.00"})

        worksheet.set_column(df.columns.get_loc('amount'),
                             df.columns.get_loc('amount'), 18, format_amount)

        # Worksheet number 2
        worksheet2 = workbook.add_worksheet("Sheet2")
        worksheet2.set_tab_color("#808080")

        expense_format = workbook.add_format({
            "bold": True,
            "bg_color": "#FF0000",
            "font_color": "#000000",
            "border": 1

        })

        income_format = workbook.add_format({
            "bold": True,
            "bg_color": "#00FFFF",
            "font_color": "#000000",
            "border": 1

        })

        savings_format = workbook.add_format({
            "bold": True,
            "bg_color": "#008000",
            "font_color": "#000000",
            "border": 1

        })

        for col_num, value in enumerate(df.columns.values):
            worksheet2.set_column(col_num, col_num, 20)

        worksheet2.write(0, 0, "Total Income", header_format)
        worksheet2.write(0, 1, total_income, income_format)

        worksheet2.write(1, 0, "Total Expense", header_format)
        worksheet2.write(1, 1, total_expense, expense_format)

        worksheet2.write(2, 0, "Savings", header_format)
        worksheet2.write(2, 1, savings, savings_format)

        worksheet2.write(4, 0, "Food", header_format)
        worksheet2.write(4, 1, food, format_amount)

        worksheet2.write(5, 0, "Furnishing", header_format)
        worksheet2.write(5, 1, furnishing, format_amount)

        worksheet2.write(6, 0, "Car", header_format)
        worksheet2.write(6, 1, car, format_amount)

        worksheet2.write(7, 0, "Drug Store", header_format)
        worksheet2.write(7, 1, drug_store, format_amount)

        worksheet2.write(8, 0, "Electronic", header_format)
        worksheet2.write(8, 1, electronics, format_amount)

        worksheet2.write(9, 0, "Baby", header_format)
        worksheet2.write(9, 1, baby, format_amount)

        worksheet2.write(10, 0, "Standing Payments", header_format)
        worksheet2.write(10, 1, standing_payments, format_amount)

        worksheet2.write(11, 0, "Presents", header_format)
        worksheet2.write(11, 1, presents, format_amount)

        worksheet2.write(12, 0, "Clothes", header_format)
        worksheet2.write(12, 1, clothes, format_amount)

        worksheet2.write(13, 0, "Insurance", header_format)
        worksheet2.write(13, 1, insurance, format_amount)

        worksheet2.write(14, 0, "Fun", header_format)
        worksheet2.write(14, 1, fun, format_amount)

        worksheet2.write(15, 0, "Animals", header_format)
        worksheet2.write(15, 1, animals, format_amount)

        worksheet2.write(16, 0, "Other", header_format)
        worksheet2.write(16, 1, other, format_amount)

        worksheet2.write(18, 0, "Salary", header_format)
        worksheet2.write(18, 1, salary, format_amount)

        worksheet2.write(19, 0, "Rent Income", header_format)
        worksheet2.write(19, 1, rent_income, format_amount)

        # Adding a chart
        chart = workbook.add_chart({'type': 'column'})
        chart.add_series({
            'name': 'Expenses',
            'categories': '=Sheet2!A5:A17',
            'values': '=Sheet2!B5:B17',
        })

        chart.set_title({'name': 'Months Balance'})
        chart.set_x_axis({'name': 'Categories'})
        chart.set_y_axis({'name': 'Amount in CZK'})

        worksheet2.insert_chart('D2', chart, {'x_scale': 1.5, 'y_scale': 1.5})

        writer.close()