import customtkinter as ctk
import csv

def open_window(parent):
    win = ctk.CTkToplevel(parent)
    win.title("Add Expense")
    win.geometry("420x380")
    win.resizable(False, False)

    def add():
        amount = amount_entry.get()
        category = category_entry.get()
        date = date_entry.get()

        if not (amount and category and date):
            msg.configure(text="Fill all details!", text_color="red")
            return

        with open("expense.csv", "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([date, category, amount])

        msg.configure(text="Expense added!", text_color="green")

    # 🔹 Title
    title = ctk.CTkLabel(win, text="Add Expense",
                         font=("Times New Roman", 24, "bold"))
    title.pack(pady=20)

    # 🔹 Input Frame (centers everything)
    frame = ctk.CTkFrame(win)
    frame.pack(pady=10)

    # Amount
    ctk.CTkLabel(frame, text="Amount").grid(row=0, column=0, padx=10, pady=10)
    amount_entry = ctk.CTkEntry(frame, width=180)
    amount_entry.grid(row=0, column=1, pady=10)

    # Category
    ctk.CTkLabel(frame, text="Category").grid(row=1, column=0, padx=10, pady=10)
    category_entry = ctk.CTkEntry(frame, width=180)
    category_entry.grid(row=1, column=1, pady=10)

    # Date
    ctk.CTkLabel(frame, text="Date").grid(row=2, column=0, padx=10, pady=10)
    date_entry = ctk.CTkEntry(frame, width=180)
    date_entry.grid(row=2, column=1, pady=10)

    # Button
    ctk.CTkButton(win,
                  text="Add Expense",
                  command=add,
                  fg_color="#27ae60",
                  hover_color="#2ecc71",
                  width=180).pack(pady=15)

    # Message
    msg = ctk.CTkLabel(win, text="")
    msg.pack()

    win.grab_set()