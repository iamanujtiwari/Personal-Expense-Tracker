import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
import os
from datetime import datetime

# File name
FILE_NAME = "expenses.csv"

# Default categories
CATEGORIES = ["Food", "Travel", "Bills", "Shopping", "Others"]

# Load or create file
if os.path.exists(FILE_NAME):
    df = pd.read_csv(FILE_NAME)
else:
    df = pd.DataFrame(columns=["DateTime", "Category", "Amount"])
    df.to_csv(FILE_NAME, index=False)

# Function to add expense
def add_expense():
    category = category_var.get()
    amount = amount_entry.get()
    
    if not amount.isdigit():
        messagebox.showerror("Error", "Please enter a valid number!")
        return

    # Current Date & Time in 12-hour format
    now = datetime.now().strftime("%Y-%m-%d %I:%M:%S %p")

    new_data = pd.DataFrame([[now, category, int(amount)]], columns=["DateTime", "Category", "Amount"])
    df_updated = pd.concat([pd.read_csv(FILE_NAME), new_data], ignore_index=True)
    df_updated.to_csv(FILE_NAME, index=False)
    
    messagebox.showinfo("Success", f"Added {amount} in {category} on {now}!")
    amount_entry.delete(0, tk.END)

# Function to show graph
def show_graph():
    if not os.path.exists(FILE_NAME):
        messagebox.showwarning("No Data", "Expense file not found!")
        return

    df_local = pd.read_csv(FILE_NAME)
    if df_local.empty:
        messagebox.showwarning("No Data", "No expenses recorded yet!")
        return

    grouped = df_local.groupby("Category")["Amount"].sum()
    total = grouped.sum()

    # Create bar chart
    ax = grouped.plot(kind="bar", color="skyblue")
    plt.title("Expense Distribution (Numbers)")
    plt.xlabel("Category")
    plt.ylabel("Amount")

    # Display values above bars
    for i, val in enumerate(grouped):
        ax.text(i, val + 5, str(val), ha="center", fontsize=10, color="black")

    # Display total clearly at the bottom
    plt.figtext(0.5, 0.01, f"💰 Total Expenses = {total}", ha="center", fontsize=12, color="red", weight="bold")

    plt.tight_layout()
    plt.show()

# UI Setup
root = tk.Tk()
root.title("Personal Expense Tracker")
root.geometry("300x250")

# Category dropdown
tk.Label(root, text="Select Category:").pack(pady=5)
category_var = tk.StringVar(value=CATEGORIES[0])
category_menu = tk.OptionMenu(root, category_var, *CATEGORIES)
category_menu.pack()

# Amount entry
tk.Label(root, text="Enter Amount:").pack(pady=5)
amount_entry = tk.Entry(root)
amount_entry.pack()

# Buttons
tk.Button(root, text="Add Expense", command=add_expense).pack(pady=10)
tk.Button(root, text="Show Graph", command=show_graph).pack(pady=5)

root.mainloop()
