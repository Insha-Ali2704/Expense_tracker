import customtkinter as ctk
from tkinter import ttk
import csv
from datetime import datetime
import tkinter as tk

# ── Palette ────────────────────────────────────────────────────────────────────
BG_DARK      = "#0D0F14"
BG_CARD      = "#161A23"
BG_ROW_ALT   = "#1C2030"
ACCENT       = "#4F8EF7"
ACCENT2      = "#7C3AED"
SUCCESS      = "#22C55E"
WARNING      = "#F59E0B"
DANGER       = "#EF4444"
TEXT_PRIMARY  = "#F1F5F9"
TEXT_MUTED    = "#64748B"
BORDER       = "#1E2535"

CATEGORY_COLORS = {
    "food"         : "#F59E0B",
    "transport"    : "#4F8EF7",
    "health"       : "#22C55E",
    "entertainment": "#A855F7",
    "shopping"     : "#EC4899",
    "utilities"    : "#14B8A6",
    "rent"         : "#EF4444",
    "other"        : "#64748B",
}

def category_color(cat: str) -> str:
    return CATEGORY_COLORS.get(cat.lower().strip(), CATEGORY_COLORS["other"])


# ── Helper: rounded rectangle on Canvas ────────────────────────────────────────
def rounded_rect(canvas, x1, y1, x2, y2, r, **kwargs):
    pts = [
        x1+r, y1,   x2-r, y1,
        x2,   y1,   x2,   y1+r,
        x2,   y2-r, x2,   y2,
        x2-r, y2,   x1+r, y2,
        x1,   y2,   x1,   y2-r,
        x1,   y1+r, x1,   y1,
        x1+r, y1,
    ]
    return canvas.create_polygon(pts, smooth=True, **kwargs)


# ── Stat Card ──────────────────────────────────────────────────────────────────
class StatCard(ctk.CTkFrame):
    def __init__(self, parent, label, value, accent, **kw):
        super().__init__(parent,
                         fg_color=BG_CARD,
                         corner_radius=14,
                         border_width=1,
                         border_color=BORDER,
                         **kw)

        # coloured top bar
        bar = ctk.CTkFrame(self, height=4, corner_radius=2, fg_color=accent)
        bar.pack(fill="x", padx=12, pady=(10, 0))

        ctk.CTkLabel(self, text=label,
                     font=("Courier New", 10, "bold"),
                     text_color=TEXT_MUTED).pack(anchor="w", padx=16, pady=(8, 0))

        self.val_label = ctk.CTkLabel(self, text=value,
                                      font=("Georgia", 22, "bold"),
                                      text_color=TEXT_PRIMARY)
        self.val_label.pack(anchor="w", padx=16, pady=(2, 12))

    def update_value(self, v):
        self.val_label.configure(text=v)


# ── Main Window ────────────────────────────────────────────────────────────────
def open_window(parent):
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")

    app = ctk.CTkToplevel(parent)
    app.title("Expense Dashboard")
    app.geometry("820x680")
    app.resizable(True, True)
    app.configure(fg_color=BG_DARK)

    # ── Title bar area ──────────────────────────────────────────────────────────
    header = ctk.CTkFrame(app, fg_color="transparent")
    header.pack(fill="x", padx=28, pady=(24, 0))

    left_head = ctk.CTkFrame(header, fg_color="transparent")
    left_head.pack(side="left")

    ctk.CTkLabel(left_head, text="EXPENSE",
                 font=("Georgia", 28, "bold"),
                 text_color=TEXT_PRIMARY).pack(side="left")
    ctk.CTkLabel(left_head, text=" TRACKER",
                 font=("Georgia", 28, "bold"),
                 text_color=ACCENT).pack(side="left")

    ctk.CTkLabel(header,
                 text=datetime.now().strftime("%d %b %Y"),
                 font=("Courier New", 12),
                 text_color=TEXT_MUTED).pack(side="right", pady=6)

    # thin divider
    ctk.CTkFrame(app, height=1, fg_color=BORDER).pack(fill="x", padx=28, pady=(12, 0))

    # ── Stats row ───────────────────────────────────────────────────────────────
    stats_row = ctk.CTkFrame(app, fg_color="transparent")
    stats_row.pack(fill="x", padx=28, pady=18)

    card_total   = StatCard(stats_row, "TOTAL SPENT",  "₹ 0.00",  ACCENT)
    card_count   = StatCard(stats_row, "TRANSACTIONS", "0",        ACCENT2)
    card_avg     = StatCard(stats_row, "AVG / ENTRY",  "₹ 0.00",  SUCCESS)
    card_top_cat = StatCard(stats_row, "TOP CATEGORY", "—",        WARNING)

    for card in (card_total, card_count, card_avg, card_top_cat):
        card.pack(side="left", expand=True, fill="both", padx=5)

    # ── Search + filter bar ────────────────────────────────────────────────────
    toolbar = ctk.CTkFrame(app, fg_color="transparent")
    toolbar.pack(fill="x", padx=28, pady=(0, 8))

    search_var = tk.StringVar()
    search_box = ctk.CTkEntry(toolbar,
                              textvariable=search_var,
                              placeholder_text="🔍  Search by category or date…",
                              height=36,
                              corner_radius=10,
                              fg_color=BG_CARD,
                              border_color=BORDER,
                              text_color=TEXT_PRIMARY,
                              font=("Courier New", 12))
    search_box.pack(side="left", expand=True, fill="x", padx=(0, 10))

    sort_var = tk.StringVar(value="Date ↕")
    sort_menu = ctk.CTkOptionMenu(toolbar,
                                  variable=sort_var,
                                  values=["Date ↕", "Date ↓", "Amount ↑", "Amount ↓", "Category"],
                                  height=36,
                                  corner_radius=10,
                                  fg_color=BG_CARD,
                                  button_color=ACCENT,
                                  button_hover_color="#3B72D9",
                                  text_color=TEXT_PRIMARY,
                                  font=("Courier New", 12))
    sort_menu.pack(side="left")

    # ── Table area ─────────────────────────────────────────────────────────────
    table_frame = ctk.CTkFrame(app,
                               fg_color=BG_CARD,
                               corner_radius=14,
                               border_width=1,
                               border_color=BORDER)
    table_frame.pack(fill="both", expand=True, padx=28, pady=(0, 8))

    style = ttk.Style()
    style.theme_use("clam")
    style.configure("Expense.Treeview",
                    background=BG_CARD,
                    fieldbackground=BG_CARD,
                    foreground=TEXT_PRIMARY,
                    rowheight=38,
                    borderwidth=0,
                    font=("Courier New", 11))
    style.configure("Expense.Treeview.Heading",
                    background=BG_DARK,
                    foreground=TEXT_MUTED,
                    relief="flat",
                    font=("Courier New", 10, "bold"),
                    borderwidth=0)
    style.map("Expense.Treeview",
              background=[("selected", "#1E3A5F")],
              foreground=[("selected", TEXT_PRIMARY)])
    style.map("Expense.Treeview.Heading",
              background=[("active", BG_DARK)])

    # scrollbar
    sb = ttk.Scrollbar(table_frame, orient="vertical")
    sb.pack(side="right", fill="y", pady=8, padx=(0, 6))

    tree = ttk.Treeview(table_frame,
                        columns=("date", "category", "amount"),
                        show="headings",
                        style="Expense.Treeview",
                        yscrollcommand=sb.set,
                        selectmode="browse")
    sb.configure(command=tree.yview)

    tree.heading("date",     text="📅  DATE",     anchor="w")
    tree.heading("category", text="🏷  CATEGORY",  anchor="w")
    tree.heading("amount",   text="💰  AMOUNT",    anchor="e")

    tree.column("date",     width=160, anchor="w", minwidth=120)
    tree.column("category", width=240, anchor="w", minwidth=140)
    tree.column("amount",   width=140, anchor="e", minwidth=100)

    tree.tag_configure("odd",  background=BG_CARD)
    tree.tag_configure("even", background=BG_ROW_ALT)
    tree.pack(fill="both", expand=True, padx=(8, 0), pady=8)

    # ── Status bar ─────────────────────────────────────────────────────────────
    status_bar = ctk.CTkFrame(app, fg_color="transparent", height=28)
    status_bar.pack(fill="x", padx=28, pady=(0, 16))

    status_label = ctk.CTkLabel(status_bar, text="",
                                font=("Courier New", 10),
                                text_color=TEXT_MUTED)
    status_label.pack(side="left")

    # ── Data loading + filtering ───────────────────────────────────────────────
    all_rows: list[tuple] = []

    def load_csv():
        nonlocal all_rows
        all_rows.clear()
        try:
            with open("expense.csv", "r") as f:
                reader = csv.reader(f)
                for row in reader:
                    if row:           # skip blank lines
                        # normalise to 3 cols
                        date = row[0] if len(row) > 0 else ""
                        cat  = row[1] if len(row) > 1 else ""
                        amt  = row[2] if len(row) > 2 else "0"
                        all_rows.append((date, cat, amt))
        except FileNotFoundError:
            status_label.configure(text="⚠  expense.csv not found — showing sample data")
            
    def sort_key(row):
        sort = sort_var.get()
        if sort == "Amount ↑":
            try: return float(row[2].replace(",", "").replace("₹", "").strip())
            except: return 0.0
        if sort == "Amount ↓":
            try: return -float(row[2].replace(",", "").replace("₹", "").strip())
            except: return 0.0
        if sort == "Category":
            return row[1].lower()
        if sort == "Date ↓":
            return row[0]            # reverse handled below
        return row[0]                # Date ↕ ascending

    def refresh(*_):
        query = search_var.get().lower()
        filtered = [r for r in all_rows
                    if query in r[0].lower() or query in r[1].lower()]

        reverse = sort_var.get() == "Date ↓"
        filtered.sort(key=sort_key, reverse=reverse)

        tree.delete(*tree.get_children())
        total = 0.0
        cat_totals: dict[str, float] = {}

        for i, (date, cat, amt) in enumerate(filtered):
            tag = "even" if i % 2 == 0 else "odd"
            try:
                val = float(amt.replace(",", "").replace("₹", "").strip())
            except ValueError:
                val = 0.0
            total += val
            cat_totals[cat] = cat_totals.get(cat, 0.0) + val

            amount_str = f"₹ {val:,.2f}"
            tree.insert("", "end", values=(date, cat, amount_str), tags=(tag,))

        n = len(filtered)
        avg = total / n if n else 0
        top = max(cat_totals, key=cat_totals.get) if cat_totals else "—"

        card_total.update_value(f"₹ {total:,.2f}")
        card_count.update_value(str(n))
        card_avg.update_value(f"₹ {avg:,.2f}")
        card_top_cat.update_value(top)

        status_label.configure(
            text=f"Showing {n} of {len(all_rows)} transactions  •  "
                 f"Total: ₹ {total:,.2f}")

    search_var.trace_add("write", refresh)
    sort_var.trace_add("write", refresh)

    load_csv()
    refresh()

    # ── Tooltip on row hover ────────────────────────────────────────────────────
    tip = tk.Toplevel(app)
    tip.withdraw()
    tip.overrideredirect(True)
    tip.configure(bg=BG_CARD)
    tip_lbl = tk.Label(tip, bg=BG_CARD, fg=TEXT_PRIMARY,
                       font=("Courier New", 10),
                       padx=10, pady=4)
    tip_lbl.pack()

    def on_motion(event):
        row_id = tree.identify_row(event.y)
        if row_id:
            vals = tree.item(row_id, "values")
            if vals:
                tip_lbl.configure(text=f"{vals[0]}  |  {vals[1]}  |  {vals[2]}")
                tip.geometry(f"+{event.x_root+12}+{event.y_root-30}")
                tip.deiconify()
                tip.lift()
        else:
            tip.withdraw()

    tree.bind("<Motion>", on_motion)
    tree.bind("<Leave>",  lambda e: tip.withdraw())

    app.grab_set()
    app.protocol("WM_DELETE_WINDOW", lambda: (tip.destroy(), app.destroy()))


# ── Standalone test ────────────────────────────────────────────────────────────
if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    root.withdraw()
    open_window(root)
    root.mainloop()