import customtkinter as ctk
from tkinter import ttk
import csv
import os
import tkinter as tk
from datetime import datetime

# ── Palette (matches view_expense.py) ─────────────────────────────────────────
BG_DARK      = "#0D0F14"
BG_CARD      = "#161A23"
BG_ROW_ALT   = "#1C2030"
ACCENT       = "#4F8EF7"
ACCENT2      = "#7C3AED"
SUCCESS      = "#22C55E"
WARNING      = "#F59E0B"
DANGER       = "#EF4444"
TEXT_PRIMARY = "#F1F5F9"
TEXT_MUTED   = "#64748B"
BORDER       = "#1E2535"

CATEGORIES = ["Food", "Transport", "Health", "Entertainment",
               "Shopping", "Utilities", "Rent", "Other"]


# ── Small reusable label + entry pair ─────────────────────────────────────────
def labeled_entry(parent, label_text, row, default=""):
    ctk.CTkLabel(parent,
                 text=label_text,
                 font=("Courier New", 10, "bold"),
                 text_color=TEXT_MUTED).grid(row=row, column=0,
                                              sticky="w", padx=(0, 16), pady=8)
    var = tk.StringVar(value=default)
    entry = ctk.CTkEntry(parent,
                         textvariable=var,
                         height=36,
                         width=220,
                         corner_radius=8,
                         fg_color=BG_DARK,
                         border_color=BORDER,
                         text_color=TEXT_PRIMARY,
                         font=("Courier New", 12))
    entry.grid(row=row, column=1, pady=8, sticky="ew")
    return var, entry


# ── Edit / Delete popup ────────────────────────────────────────────────────────
def open_edit_popup(parent_win, row_index: int, row_data: tuple, on_save):
    """Opens a modal to edit or delete a single expense row."""
    pop = ctk.CTkToplevel(parent_win)
    pop.title("Edit Expense")
    pop.geometry("420x340")
    pop.resizable(False, False)
    pop.configure(fg_color=BG_DARK)
    pop.grab_set()

    # header
    hdr = ctk.CTkFrame(pop, fg_color="transparent")
    hdr.pack(fill="x", padx=24, pady=(20, 0))
    ctk.CTkLabel(hdr, text="EDIT", font=("Georgia", 20, "bold"),
                 text_color=TEXT_PRIMARY).pack(side="left")
    ctk.CTkLabel(hdr, text=" EXPENSE", font=("Georgia", 20, "bold"),
                 text_color=ACCENT).pack(side="left")

    ctk.CTkFrame(pop, height=1, fg_color=BORDER).pack(fill="x", padx=24, pady=(10, 0))

    # form
    form = ctk.CTkFrame(pop, fg_color="transparent")
    form.pack(padx=24, pady=16, fill="x")
    form.columnconfigure(1, weight=1)

    date_var,  date_entry  = labeled_entry(form, "DATE",     0, row_data[0])
    cat_var,   _           = labeled_entry(form, "CATEGORY", 1, row_data[1])
    amt_var,   amt_entry   = labeled_entry(form, "AMOUNT",   2, row_data[2])

    # replace category entry with a dropdown
    form.grid_slaves(row=1, column=1)[0].destroy()
    cat_var = tk.StringVar(value=row_data[1])
    cat_menu = ctk.CTkOptionMenu(form,
                                  variable=cat_var,
                                  values=CATEGORIES,
                                  height=36,
                                  corner_radius=8,
                                  fg_color=BG_DARK,
                                  button_color=ACCENT,
                                  button_hover_color="#3B72D9",
                                  text_color=TEXT_PRIMARY,
                                  font=("Courier New", 12))
    cat_menu.grid(row=1, column=1, pady=8, sticky="ew")

    # feedback label
    msg = ctk.CTkLabel(pop, text="", font=("Courier New", 10), text_color=DANGER)
    msg.pack()

    # buttons
    btn_row = ctk.CTkFrame(pop, fg_color="transparent")
    btn_row.pack(pady=(4, 20))

    def save():
        d = date_var.get().strip()
        c = cat_var.get().strip()
        a = amt_var.get().strip()
        if not (d and c and a):
            msg.configure(text="⚠  All fields are required.", text_color=DANGER)
            return
        try:
            float(a)
        except ValueError:
            msg.configure(text="⚠  Amount must be a number.", text_color=DANGER)
            return
        on_save(row_index, (d, c, a), action="save")
        msg.configure(text="✓  Saved!", text_color=SUCCESS)
        pop.after(700, pop.destroy)

    def delete():
        on_save(row_index, None, action="delete")
        pop.destroy()

    ctk.CTkButton(btn_row,
                  text="💾  Save Changes",
                  command=save,
                  width=160, height=36,
                  corner_radius=10,
                  fg_color=ACCENT,
                  hover_color="#3B72D9",
                  font=("Courier New", 11, "bold"),
                  text_color=TEXT_PRIMARY).pack(side="left", padx=(0, 10))

    ctk.CTkButton(btn_row,
                  text="🗑  Delete",
                  command=delete,
                  width=110, height=36,
                  corner_radius=10,
                  fg_color="#2A1A1A",
                  hover_color=DANGER,
                  border_width=1,
                  border_color=DANGER,
                  font=("Courier New", 11, "bold"),
                  text_color=DANGER).pack(side="left")


# ── Main edit window ───────────────────────────────────────────────────────────
def open_window(parent):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTkToplevel(parent)
    app.title("Edit Expenses")
    app.geometry("860x700")
    app.resizable(True, True)
    app.configure(fg_color=BG_DARK)

    # ── Header ────────────────────────────────────────────────────────────────
    header = ctk.CTkFrame(app, fg_color="transparent")
    header.pack(fill="x", padx=28, pady=(24, 0))

    left = ctk.CTkFrame(header, fg_color="transparent")
    left.pack(side="left")
    ctk.CTkLabel(left, text="EDIT",
                 font=("Georgia", 28, "bold"),
                 text_color=TEXT_PRIMARY).pack(side="left")
    ctk.CTkLabel(left, text=" EXPENSES",
                 font=("Georgia", 28, "bold"),
                 text_color=ACCENT).pack(side="left")

    ctk.CTkLabel(header,
                 text=datetime.now().strftime("%d %b %Y"),
                 font=("Courier New", 12),
                 text_color=TEXT_MUTED).pack(side="right", pady=6)

    ctk.CTkFrame(app, height=1, fg_color=BORDER).pack(fill="x", padx=28, pady=(12, 0))

    # ── Instruction banner ────────────────────────────────────────────────────
    banner = ctk.CTkFrame(app, fg_color="#151C2C", corner_radius=10,
                          border_width=1, border_color="#1E3A5F")
    banner.pack(fill="x", padx=28, pady=(14, 0))
    ctk.CTkLabel(banner,
                 text="  ✏️   Click any row to edit or delete it",
                 font=("Courier New", 11),
                 text_color="#7EB3FF").pack(anchor="w", padx=8, pady=8)

    # ── Search bar ────────────────────────────────────────────────────────────
    toolbar = ctk.CTkFrame(app, fg_color="transparent")
    toolbar.pack(fill="x", padx=28, pady=12)

    search_var = tk.StringVar()
    ctk.CTkEntry(toolbar,
                 textvariable=search_var,
                 placeholder_text="🔍  Search by category or date…",
                 height=36,
                 corner_radius=10,
                 fg_color=BG_CARD,
                 border_color=BORDER,
                 text_color=TEXT_PRIMARY,
                 font=("Courier New", 12)).pack(side="left", expand=True, fill="x", padx=(0, 10))

    # record count badge
    count_label = ctk.CTkLabel(toolbar,
                                text="0 records",
                                font=("Courier New", 10),
                                text_color=TEXT_MUTED)
    count_label.pack(side="right")

    # ── Table ─────────────────────────────────────────────────────────────────
    table_frame = ctk.CTkFrame(app, fg_color=BG_CARD,
                               corner_radius=14,
                               border_width=1,
                               border_color=BORDER)
    table_frame.pack(fill="both", expand=True, padx=28, pady=(0, 8))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Edit.Treeview",
                    background=BG_CARD,
                    fieldbackground=BG_CARD,
                    foreground=TEXT_PRIMARY,
                    rowheight=40,
                    borderwidth=0,
                    font=("Courier New", 11))
    style.configure("Edit.Treeview.Heading",
                    background=BG_DARK,
                    foreground=TEXT_MUTED,
                    relief="flat",
                    font=("Courier New", 10, "bold"))
    style.map("Edit.Treeview",
              background=[("selected", "#1E3A5F")],
              foreground=[("selected", TEXT_PRIMARY)])
    style.map("Edit.Treeview.Heading",
              background=[("active", BG_DARK)])

    sb = ttk.Scrollbar(table_frame, orient="vertical")
    sb.pack(side="right", fill="y", pady=8, padx=(0, 6))

    tree = ttk.Treeview(table_frame,
                        columns=("no", "date", "category", "amount"),
                        show="headings",
                        style="Edit.Treeview",
                        yscrollcommand=sb.set,
                        selectmode="browse")
    sb.configure(command=tree.yview)

    tree.heading("no",       text="#",            anchor="center")
    tree.heading("date",     text="📅  DATE",      anchor="w")
    tree.heading("category", text="🏷  CATEGORY",  anchor="w")
    tree.heading("amount",   text="💰  AMOUNT",    anchor="e")

    tree.column("no",       width=48,  anchor="center", minwidth=40, stretch=False)
    tree.column("date",     width=160, anchor="w",      minwidth=120)
    tree.column("category", width=240, anchor="w",      minwidth=140)
    tree.column("amount",   width=150, anchor="e",      minwidth=100)

    tree.tag_configure("odd",  background=BG_CARD)
    tree.tag_configure("even", background=BG_ROW_ALT)
    tree.pack(fill="both", expand=True, padx=(8, 0), pady=8)

    # ── Status bar ────────────────────────────────────────────────────────────
    status_bar = ctk.CTkFrame(app, fg_color="transparent", height=28)
    status_bar.pack(fill="x", padx=28, pady=(0, 16))

    status_label = ctk.CTkLabel(status_bar, text="",
                                font=("Courier New", 10),
                                text_color=TEXT_MUTED)
    status_label.pack(side="left")

    # ── Data ──────────────────────────────────────────────────────────────────
    all_rows: list[tuple] = []   # (date, category, amount)

    def load_csv():
        nonlocal all_rows
        all_rows.clear()
        try:
            with open("expense.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:
                        date = row[0] if len(row) > 0 else ""
                        cat  = row[1] if len(row) > 1 else ""
                        amt  = row[2] if len(row) > 2 else "0"
                        all_rows.append((date, cat, amt))
        except FileNotFoundError:
            status_label.configure(text="⚠  expense.csv not found")

    def save_csv():
        with open("expense.csv", "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerows(all_rows)

    def refresh(*_):
        query = search_var.get().lower()
        filtered_indices = [
            i for i, r in enumerate(all_rows)
            if query in r[0].lower() or query in r[1].lower()
        ]

        tree.delete(*tree.get_children())
        for display_num, real_idx in enumerate(filtered_indices):
            date, cat, amt = all_rows[real_idx]
            try:
                val = float(amt.replace(",", "").replace("₹", "").strip())
                amt_str = f"₹ {val:,.2f}"
            except ValueError:
                amt_str = amt
            tag = "even" if display_num % 2 == 0 else "odd"
            # store real_idx as iid so we can retrieve it on click
            tree.insert("", "end",
                        iid=str(real_idx),
                        values=(display_num + 1, date, cat, amt_str),
                        tags=(tag,))

        n = len(filtered_indices)
        count_label.configure(text=f"{n} record{'s' if n != 1 else ''}")
        status_label.configure(
            text=f"Showing {n} of {len(all_rows)} expenses  •  Click a row to edit")

    def on_row_edit(real_index: int, new_data, action: str):
        if action == "delete":
            all_rows.pop(real_index)
        elif action == "save":
            all_rows[real_index] = new_data
        save_csv()
        refresh()

    def on_row_click(event):
        row_id = tree.focus()
        if not row_id:
            return
        real_idx = int(row_id)
        row_data = all_rows[real_idx]
        open_edit_popup(app, real_idx, row_data, on_row_edit)

    tree.bind("<ButtonRelease-1>", on_row_click)
    search_var.trace_add("write", refresh)

    # ── Tooltip ───────────────────────────────────────────────────────────────
    tip = tk.Toplevel(app)
    tip.withdraw()
    tip.overrideredirect(True)
    tip.configure(bg=BG_CARD)
    tip_lbl = tk.Label(tip, bg=BG_CARD, fg="#7EB3FF",
                       font=("Courier New", 10), padx=10, pady=4,
                       text="Click to edit this row")
    tip_lbl.pack()

    def on_motion(event):
        if tree.identify_row(event.y):
            tip.geometry(f"+{event.x_root+14}+{event.y_root-32}")
            tip.deiconify()
            tip.lift()
        else:
            tip.withdraw()

    tree.bind("<Motion>", on_motion)
    tree.bind("<Leave>",  lambda e: tip.withdraw())

    load_csv()
    refresh()

    app.grab_set()
    app.protocol("WM_DELETE_WINDOW", lambda: (tip.destroy(), app.destroy(), parent.deiconify()))


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.withdraw()
    open_window(root)
    root.mainloop()