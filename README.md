# Months Financial Balance GUI Application v 1.0/EN

## Introduction

The Finance Manager GUI Application is a Python-based desktop application designed to help users manage their financial transactions with ease. The app allows users to input daily transactions, store them in a CSV file, and generate monthly summaries in Excel format. The application provides a user-friendly interface built using ttkbootstrap, an extension of the Tkinter library, and includes multiple tabs for managing transactions, viewing stored data, and exporting files.

## Features

Transaction Entry: Users can enter daily financial transactions, including date, amount, category, and description.
CSV Management: The app stores transactions in a CSV file, allowing for easy retrieval and editing.
Excel Export: Generate monthly summaries in Excel format, specifying the date range for transactions.
Regular Payments: Predefine regular monthly payments that can be automatically added to transactions.
Contextual Menus: Right-click context menus for saving files from the app to the local machine.
Interactive UI: The app includes interactive elements such as buttons, labels, list boxes, and date pickers.
Customizable Layout: Users can interact with different tabs and sections within the app to view and manage their financial data.
Installation. The GUI was made with pyinstaller and Platypus for bundle.

## Prerequisites
    Python 3.x installed on your machine.
## Required Python packages:
    ttkbootstrap
    pandas
    tkinter
    datetime
    csv
    xlsxwriter

## Main Window Layout
## Tabs:
### Transactions: 
Input daily transactions with fields for date, amount, category, and description.
### CSV Files: 
View and manage stored transactions.
### Excel Files: 
Manage and export data as Excel files, specifying the date range.
## Buttons:
### Add Payment: 
Saves the current transaction to the CSV file.
### Clear: 
Clears fields in CSV file. Otherwise, transactions stored in CSV files will load up when starting the app again.
### Get Excel: 
Generates an Excel summary of transactions within a specified date range.

## Generating Excel Reports:
    /Go to the Excel Files tab.
    /Select the start and end dates for the report.
    /Click Get Excel button to generate .xlsx file, then right click to save the file.
    /Generated .xlsx files will be deleted when reload the app.

### Developed by: AceL1b0
### GitHub Repository: 
https://github.com/AceL1b0/finance-app.git
### License

This project is licensed under the MIT License - see the LICENSE file for details.
