import customtkinter as ctk
def expense():
    root.withdraw()
    import add_expense
    add_expense.open_window(root)
    root.after(100, lambda: root.wait_window(
    root.winfo_children()[-1]))
    root.deiconify()
def view():
    root.withdraw()
    import view_expense
    view_expense.open_window(root)
def edit():
    root.withdraw()
    import edit_expense
    edit_expense.open_window(root)
root = ctk.CTk() 
root.title("Expense Tracker")
root.geometry("400x300")
root.resizable(False, False)
ctk.set_appearance_mode("dark") 
header = ctk.CTkLabel(root, text="Expense Tracker", font=("Algerian", 25), text_color="#e0e0e0")
header.pack(pady=20)

btn1 = ctk.CTkButton(root, 
                    text="Add Expense", 
                    fg_color="#27ae60",      # Emerald Green
                    hover_color="#2ecc71",   # Light Emerald on hover
                    corner_radius=20,        # Rounded borders!
                    text_color="white",
                    font=("Times New Roman", 15, "bold"),
                    width=160,
                    height=40,command=expense)
btn1.place(x=120, y=80)
btn2 = ctk.CTkButton(root, 
                    text="View Expenses", 
                    fg_color="#27ae60",      # Emerald Green
                    hover_color="#2ecc71",   # Light Emerald on hover
                    corner_radius=20,        # Rounded borders!
                    text_color="white",
                    font=("Times New Roman", 15, "bold"),
                    width=160,
                    height=40,command=view)
btn2.place(x=120, y=140)

btn3 = ctk.CTkButton(root, 
                    text="Edit Expenses", 
                    fg_color="#27ae60",      # Emerald Green
                    hover_color="#2ecc71",   # Light Emerald on hover
                    corner_radius=20,        # Rounded borders!
                    text_color="white",
                    font=("Times New Roman", 15, "bold"),
                    width=160,
                    height=40,command=edit)
btn3.place(x=120, y=200)
root.mainloop()