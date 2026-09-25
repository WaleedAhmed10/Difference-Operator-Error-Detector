import tkinter as tk
from tkinter import ttk, messagebox

x = []
y = []
table = []

def create_inputs():
    try:
        n = int(n_entry.get())
        if n < 2:
            messagebox.showerror("Error", "Enter at least 2 data points.")
            return
    except:
        messagebox.showerror("Error", "Enter a valid number.")
        return

    for widget in input_frame.winfo_children():
        widget.destroy()

    global x_entries, y_entries
    x_entries = []
    y_entries = []

    tk.Label(input_frame, text="Point", bg="#202020", fg="white").grid(row=0, column=0)
    tk.Label(input_frame, text="x", bg="#202020", fg="white").grid(row=0, column=1)
    tk.Label(input_frame, text="y", bg="#202020", fg="white").grid(row=0, column=2)

    for i in range(n):
        tk.Label(input_frame, text=i + 1, bg="#202020", fg="white").grid(row=i + 1, column=0)

        xe = tk.Entry(input_frame, width=12)
        xe.grid(row=i + 1, column=1, padx=5, pady=2)

        ye = tk.Entry(input_frame, width=12)
        ye.grid(row=i + 1, column=2, padx=5, pady=2)

        x_entries.append(xe)
        y_entries.append(ye)

    tk.Button(
        input_frame,
        text="Build Difference Table",
        command=build_table
    ).grid(row=n + 1, column=0, columnspan=3, pady=10)

def build_table():
    global x, y, table

    try:
        x = [float(e.get()) for e in x_entries]
        y = [float(e.get()) for e in y_entries]
    except:
        messagebox.showerror("Error", "Enter numbers only.")
        return

    n = len(x)
    table = [[0] * n for _ in range(n)]

    for i in range(n):
        table[i][0] = y[i]

    for j in range(1, n):
        for i in range(n - j):
            table[i][j] = table[i + 1][j - 1] - table[i][j - 1]

    show_table()
    create_origin()

def show_table():
    for widget in table_frame.winfo_children():
        widget.destroy()

    tk.Label(
        table_frame,
        text="Difference Table (Forward Differences)",
        bg="#202020",
        fg="#5DADE2",
        font=("Arial", 14, "bold")
    ).pack()

    columns = ["x", "y"]

    for i in range(1, len(x)):
        columns.append(f"Δ^{i}y")

    table_container = tk.Frame(table_frame, bg="#202020")
    table_container.pack(fill="x")

    tree = ttk.Treeview(
        table_container,
        columns=columns,
        show="headings",
        height=7
    )

    x_scroll = tk.Scrollbar(
        table_container,
        orient="horizontal",
        command=tree.xview
    )

    tree.configure(xscrollcommand=x_scroll.set)

    for column in columns:
        tree.heading(column, text=column)
        tree.column(column, width=85, anchor="center")

    for i in range(len(x)):
        row = [x[i]]

        for j in range(len(x)):
            if i < len(x) - j:
                row.append(round(table[i][j], 2))
            else:
                row.append("")

        tree.insert("", "end", values=row)

    tree.pack(fill="x")
    x_scroll.pack(fill="x")

def create_origin():
    for widget in origin_frame.winfo_children():
        widget.destroy()

    tk.Label(
        origin_frame,
        text="Select the origin point:",
        bg="#202020",
        fg="white"
    ).pack(side="left")

    global origin_box

    origin_box = ttk.Combobox(
        origin_frame,
        state="readonly",
        width=20
    )

    values = []

    for i in range(len(x)):
        values.append(f"{i}: x={x[i]}, y={y[i]}")

    origin_box["values"] = values
    origin_box.current(0)
    origin_box.pack(side="left", padx=10)

    tk.Button(
        origin_frame,
        text="Show Operators",
        command=show_operators
    ).pack(side="left")

def show_operators():
    index = origin_box.current()

    result.delete("1.0", tk.END)

    result.insert(
        tk.END,
        f"Origin : y{index} = {y[index]} at x{index} = {x[index]}\n"
    )

    result.insert(tk.END, "-" * 60 + "\n\n")

    result.insert(tk.END, "Forward differences (Δ):\n")

    for j in range(1, len(x) - index):
        result.insert(
            tk.END,
            f"    Δ^{j}y{index} = {table[index][j]}\n"
        )

    result.insert(tk.END, "\nBackward differences (∇):\n")

    if index == 0:
        result.insert(
            tk.END,
            "    No backward differences available.\n"
        )
    else:
        for j in range(1, index + 1):
            result.insert(
                tk.END,
                f"    ∇^{j}y{index} = {table[index - j][j]}\n"
            )

    result.insert(tk.END, "\nCentral differences (δ):\n")

    if index > 0 and index < len(x) - 1:
        central_1 = (table[index][1] + table[index - 1][1]) / 2

        result.insert(
            tk.END,
            f"    δ^1y{index} = {central_1}\n"
        )

    for j in range(2, len(x)):
        if j % 2 == 0:
            row = index - j // 2

            if row >= 0 and row + j < len(x):
                result.insert(
                    tk.END,
                    f"    δ^{j}y{index} = {table[row][j]}\n"
                )
        else:
            row1 = index - (j + 1) // 2
            row2 = index - (j - 1) // 2

            if row1 >= 0 and row2 >= 0:
                if row1 + j < len(x) and row2 + j < len(x):
                    central = (
                        table[row1][j] +
                        table[row2][j]
                    ) / 2

                    result.insert(
                        tk.END,
                        f"    δ^{j}y{index} = {central}\n"
                    )

def search():
    query = query_entry.get().strip().lower()

    if query == "":
        return

    query = query.replace("delta", "Δ")
    query = query.replace("nabla", "∇")
    query = query.replace("del", "δ")
    query = query.replace(" ", "")

    if "y" in query:
        find_label(query)
    else:
        find_value(query)

def find_label(query):
    found = False

    for j in range(1, len(x)):
        for i in range(len(x) - j):
            labels = [
                f"Δ^{j}y{i}",
                f"∇^{j}y{i + j}"
            ]

            if j % 2 == 0:
                labels.append(f"δ^{j}y{i + j // 2}")

            for label in labels:
                if label.lower() == query:
                    result.insert(
                        tk.END,
                        f"\n{label} = {table[i][j]}\n"
                    )
                    found = True

    if not found:
        result.insert(
            tk.END,
            f"\nNo label found for {query}\n"
        )

def find_value(query):
    try:
        value = float(query)
    except:
        result.insert(
            tk.END,
            "\nEnter a valid label or number.\n"
        )
        return

    labels = []

    for j in range(1, len(x)):
        for i in range(len(x) - j):
            if table[i][j] == value:
                labels.append(f"Δ^{j}y{i}")
                labels.append(f"∇^{j}y{i + j}")

                if j % 2 == 0:
                    labels.append(f"δ^{j}y{i + j // 2}")

    result.insert(
        tk.END,
        f"\nValue {value} appears as:\n"
    )

    if labels:
        result.insert(
            tk.END,
            "    " + ", ".join(labels) + "\n"
        )
    else:
        result.insert(
            tk.END,
            "    No labels found.\n"
        )
       
def clear():
    n_entry.delete(0, tk.END)

    for widget in input_frame.winfo_children():
        widget.destroy()

    for widget in table_frame.winfo_children():
        widget.destroy()

    for widget in origin_frame.winfo_children():
        widget.destroy()

    result.delete("1.0", tk.END)
    query_entry.delete(0, tk.END)

root = tk.Tk()
root.title("LAB 4 - Difference Operators")
root.geometry("1000x700")
root.configure(bg="#202020")

canvas = tk.Canvas(root, bg="#202020", highlightthickness=0)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
canvas.pack(side="left", fill="both", expand=True)

main_container = tk.Frame(canvas, bg="#202020")
canvas_window = canvas.create_window((0, 0), window=main_container, anchor="nw")

def update_scroll(event):
    canvas.configure(scrollregion=canvas.bbox("all"))

def resize_container(event):
    canvas.itemconfig(canvas_window, width=event.width)

main_container.bind("<Configure>", update_scroll)
canvas.bind("<Configure>", resize_container)

tk.Label(
    main_container,
    text="LAB 4 - DIFFERENCE OPERATORS",
    font=("Arial", 22, "bold"),
    bg="#202020",
    fg="#5DADE2"
).pack(pady=15)

tk.Label(
    main_container,
    text="Difference Table | Forward | Backward | Central | Value Lookup",
    bg="#202020",
    fg="white",
    font=("Arial", 11)
).pack()

main_frame = tk.Frame(main_container, bg="#202020")
main_frame.pack(pady=15)

tk.Label(
    main_frame,
    text="Enter number of data points:",
    bg="#202020",
    fg="white"
).grid(row=0, column=0)

n_entry = tk.Entry(main_frame, width=8)
n_entry.grid(row=0, column=1, padx=10)

tk.Button(
    main_frame,
    text="Create Input",
    command=create_inputs
).grid(row=0, column=2)

tk.Button(
    main_frame,
    text="Clear",
    command=clear
).grid(row=0, column=3, padx=5)

input_frame = tk.Frame(main_container, bg="#202020")
input_frame.pack()

table_frame = tk.Frame(main_container, bg="#202020")
table_frame.pack(fill="x", padx=20)

origin_frame = tk.Frame(main_container, bg="#202020")
origin_frame.pack(pady=10)

result = tk.Text(
    main_container,
    height=15,
    width=100,
    bg="#101010",
    fg="white",
    font=("Consolas", 11)
)
result.pack(padx=20, pady=10)

query_frame = tk.Frame(main_container, bg="#202020")
query_frame.pack(pady=5)

tk.Label(
    query_frame,
    text="Query:",
    bg="#202020",
    fg="white"
).pack(side="left")

query_entry = tk.Entry(query_frame, width=25)
query_entry.pack(side="left", padx=10)

tk.Button(
    query_frame,
    text="Find",
    command=search
).pack(side="left")

tk.Label(
    query_frame,
    text="  Example: Δ^2y0 or 24",
    bg="#202020",
    fg="#AAAAAA"
).pack(side="left")

root.mainloop()