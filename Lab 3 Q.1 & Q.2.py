import math
import tkinter as tk
from tkinter import ttk, messagebox

class DifferenceAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Difference Table Analyzer")
        self.root.geometry("1150x750")
        self.root.configure(bg="#17202A")

        self.x = []
        self.y = []
        self.table = []

        self.create_gui()

    def create_gui(self):
        tk.Label(
            self.root,
            text="LAB 3 - DIFFERENCE TABLE ANALYZER",
            font=("Arial", 22, "bold"),
            bg="#17202A",
            fg="#5DADE2"
        ).pack(pady=15)

        tk.Label(
            self.root,
            text="Automatic Error Detection & Correction",
            font=("Arial", 11),
            bg="#17202A",
            fg="#BDC3C7"
        ).pack()

        top = tk.Frame(self.root, bg="#212F3D", padx=15, pady=12)
        top.pack(fill="x", padx=20, pady=15)

        tk.Label(
            top,
            text="Number of Data Points:",
            bg="#212F3D",
            fg="white",
            font=("Arial", 11, "bold")
        ).pack(side="left")

        self.n_entry = tk.Entry(top, width=8)
        self.n_entry.pack(side="left", padx=10)

        ttk.Button(
            top,
            text="Create Input",
            command=self.create_inputs
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="Analyze Data",
            command=self.analyze
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="Clear",
            command=self.clear
        ).pack(side="left", padx=5)

        self.input_frame = tk.Frame(
            self.root,
            bg="#17202A"
        )
        self.input_frame.pack(pady=5)

        self.table_frame = tk.Frame(
            self.root,
            bg="#17202A"
        )
        self.table_frame.pack(
            fill="both",
            expand=True,
            padx=20,
            pady=10
        )

        self.result = tk.Text(
            self.root,
            height=10,
            bg="#1C2833",
            fg="#ECF0F1",
            font=("Consolas", 11)
        )
        self.result.pack(
            fill="x",
            padx=20,
            pady=10
        )

    def create_inputs(self):
        try:
            n = int(self.n_entry.get())

            if n < 3:
                raise ValueError

        except:
            messagebox.showerror(
                "Invalid Input",
                "Enter at least 3 data points."
            )
            return

        for widget in self.input_frame.winfo_children():
            widget.destroy()

        self.x_entries = []
        self.y_entries = []

        tk.Label(
            self.input_frame,
            text="Point",
            bg="#17202A",
            fg="#5DADE2",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=0, padx=15)

        tk.Label(
            self.input_frame,
            text="X",
            bg="#17202A",
            fg="#5DADE2",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=1, padx=15)

        tk.Label(
            self.input_frame,
            text="Y",
            bg="#17202A",
            fg="#5DADE2",
            font=("Arial", 11, "bold")
        ).grid(row=0, column=2, padx=15)

        for i in range(n):
            tk.Label(
                self.input_frame,
                text=i + 1,
                bg="#17202A",
                fg="white"
            ).grid(row=i + 1, column=0)

            x = tk.Entry(
                self.input_frame,
                width=12
            )
            x.grid(
                row=i + 1,
                column=1,
                padx=10,
                pady=2
            )

            y = tk.Entry(
                self.input_frame,
                width=12
            )
            y.grid(
                row=i + 1,
                column=2,
                padx=10,
                pady=2
            )

            self.x_entries.append(x)
            self.y_entries.append(y)

    def get_data(self):
        try:
            self.x = [
                float(entry.get())
                for entry in self.x_entries
            ]

            self.y = [
                float(entry.get())
                for entry in self.y_entries
            ]

            return True

        except:
            messagebox.showerror(
                "Invalid Data",
                "Please enter numbers only."
            )
            return False

    def make_table(self, y_values):
        n = len(y_values)

        table = [
            [0.0] * n
            for _ in range(n)
        ]

        for i in range(n):
            table[i][0] = y_values[i]

        for j in range(1, n):
            for i in range(n - j):
                table[i][j] = (
                    table[i + 1][j - 1]
                    - table[i][j - 1]
                )

        return table

    def show_table(self, table, title):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.table_frame,
            text=title,
            bg="#17202A",
            fg="#F7DC6F",
            font=("Arial", 14, "bold")
        ).pack(anchor="w")

        columns = ["x", "y"]

        for j in range(1, len(self.x)):
            columns.append(f"Δ^{j}y")

        tree = ttk.Treeview(
            self.table_frame,
            columns=columns,
            show="headings",
            height=8
        )

        for column in columns:
            tree.heading(
                column,
                text=column
            )
            tree.column(
                column,
                width=90,
                anchor="center"
            )

        for i in range(len(self.x)):
            row = [self.x[i]]

            for j in range(len(self.x)):
                if i < len(self.x) - j:
                    row.append(
                        round(table[i][j], 2)
                    )
                else:
                    row.append("")

            tree.insert(
                "",
                "end",
                values=row
            )

        tree.pack(
            fill="both",
            expand=True
        )

    def analyze(self):
        if not hasattr(self, "x_entries"):
            messagebox.showwarning(
                "Warning",
                "Create the input table first."
            )
            return

        if not self.get_data():
            return

        n = len(self.x)

        self.table = self.make_table(self.y)

        self.show_table(
            self.table,
            "Initial Difference Table"
        )

        target_col = 2
        err_row = 0
        max_anomaly_score = -1

        for j in range(2, n - 1):
            values = [
                self.table[i][j]
                for i in range(n - j)
            ]

            if len(values) < 3:
                continue

            mean_value = sum(values) / len(values)

            deviations = [
                abs(value - mean_value)
                for value in values
            ]

            max_deviation = max(deviations)

            mean_deviation = (
                sum(deviations) / len(deviations)
            )

            score = max_deviation / (
                mean_deviation + 0.00001
            )

            if score > max_anomaly_score:
                max_anomaly_score = score
                target_col = j
                err_row = deviations.index(
                    max_deviation
                )

        coefficient = math.comb(
            target_col,
            target_col // 2
        )

        correction = (
            self.table[err_row][target_col]
            / coefficient
        )

        target_y = (
            err_row +
            target_col // 2
        )

        old_value = self.y[target_y]

        new_value = old_value - correction

        self.result.delete(
            "1.0",
            tk.END
        )

        self.result.insert(
            tk.END,
            "ANALYSIS RESULT\n"
        )

        self.result.insert(
            tk.END,
            "=" * 55 + "\n\n"
        )

        self.result.insert(
            tk.END,
            f"Detected Difference: Δ^{target_col}y\n"
        )

        self.result.insert(
            tk.END,
            f"Error Row: {err_row}\n"
        )

        self.result.insert(
            tk.END,
            f"Suspected y value: y[{target_y}]\n\n"
        )

        self.result.insert(
            tk.END,
            f"Original value: {old_value:.2f}\n"
        )

        self.result.insert(
            tk.END,
            f"Correction value: {correction:.2f}\n"
        )

        self.result.insert(
            tk.END,
            f"Corrected value: {new_value:.2f}\n\n"
        )

        self.y[target_y] = new_value

        corrected_table = self.make_table(
            self.y
        )

        self.show_table(
            corrected_table,
            "Corrected Difference Table"
        )

        self.result.insert(
            tk.END,
            "Correction applied successfully."
        )

    def clear(self):
        for widget in self.input_frame.winfo_children():
            widget.destroy()

        for widget in self.table_frame.winfo_children():
            widget.destroy()

        self.result.delete(
            "1.0",
            tk.END
        )
        self.n_entry.delete(
            0,
            tk.END
        )
        self.x = []
        self.y = []
        self.table = []

root = tk.Tk()
app = DifferenceAnalyzer(root)
root.mainloop()