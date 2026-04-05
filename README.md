# 💸 Expense Tracker

So I got tired of not knowing where my money goes every month, so I built this little desktop app in Python. It lets you log expenses, see them in a nice dashboard, and edit or delete them whenever you want. Nothing fancy, just a clean UI and a CSV file doing all the heavy lifting.

---

## 📁 What's in the project

```
expense-tracker/
│
├── main.py            # Start here — the home screen
├── add_expense.py     # Add a new expense
├── view_expense.py    # See everything in a dashboard with stats
├── edit_expense.py    # Click any expense to edit or delete it
├── expense.csv        # Your data lives here (auto-created)
└── README.md          # You're reading this
```

---

## ✨ What it can do

**Adding an expense** is just filling in three fields — date, category, amount — and hitting the button. It saves straight to a CSV file, no database needed.

**The view screen** is probably the nicest part. You get four stat cards at the top showing your total spent, number of transactions, average per entry, and your top spending category. Below that is a searchable, sortable table of everything you've logged. You can search by category or date and it filters in real time as you type.

**The edit screen** works the same way — same table, same search. Except now you can click any row and a popup opens with the fields pre-filled. Change what you want, hit save, done. Or delete it entirely if it was a mistake.

---

## 🛠️ Setup

You only need one install:

```bash
pip install customtkinter
```

Everything else (`tkinter`, `csv`, `datetime`) already comes with Python. No databases, no APIs, no complicated setup.

---

## 🚀 Running it

```bash
python main.py
```

That's it.

---

## 📄 How the data is stored

Everything goes into a plain `expense.csv` file that gets created the first time you add an expense. It looks like this:

```
2024-06-01, Food, 450.00
2024-06-02, Transport, 120.00
2024-06-07, Rent, 12000.00
```

You can open it in Excel or Google Sheets too if you want to do something with it outside the app.

---

## 🏷️ Categories

Food, Transport, Health, Entertainment, Shopping, Utilities, Rent, Other.

You pick from a dropdown when editing so the names stay consistent. Adding more categories is easy — just update the list in the code.

---

## 🔮 What I want to add next

- A pie chart breaking down spending by category
- Budget limits per category that turn red when you're close
- A month filter so you can see just this month's expenses
- Export whatever's on screen to a new CSV

---

## 👤 About

Just a personal side project I built to learn Python GUI stuff. Ended up being more fun than expected.
