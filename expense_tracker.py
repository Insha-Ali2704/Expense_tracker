from tkinter import*
import csv
root=Tk()
root.title("Expense Tracker")
root.geometry("400x280")
def add_expense():
    amount=amount_entry.get()
    category=category_entry.get()
    date=date_entry.get()
    with open("expense.csv","a",newline="") as f:
        writer=csv.write(f)
        writer.writerow([date,category,amount])
Label(root,text="Expense Tracker",fg="Black",font="Times_new_roman 15 ").pack(pady=10)

Label(root,text="Amount : ",fg="black",font="Times_new_roman 10").place(x=60,y=40)
amount_entry=Entry(root,border=2,font="arial 10",fg="dark slate grey").place(x=140,y=40)

Label(root,text="Category : ",fg="black",font="Times_new_roman 10").place(x=60,y=80)
category_entry=Entry(root,border=2,font="arial 10",fg="dark slate grey").place(x=140,y=80)

Label(root,text="Date : ",fg="black",font="Times_new_roman 10").place(x=60,y=120)
date_entry=Entry(root,border=2,font="arial 10",fg="dark slate grey").place(x=140,y=120)

Button(root,text="Add expense",font="Times_new_roman 10 bold",fg="black",bg="green",command=add_expense).place(x=160,y=170)
print("saved!")
root.mainloop()