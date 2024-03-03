import tkinter as tk
from tkinter import messagebox
import sqlite3
from datetime import datetime
import matplotlib.pyplot as plt
import numpy as np


class BMI_Calculator:
    def __init__(self, root):
        self.root = root
        self.root.title("BMI Calculator")

        self.create_widgets()

        # Connect to SQLite database
        self.conn = sqlite3.connect('bmi_data.db')
        self.create_table()

        # BMI norms set by the government of India
        self.bmi_norms = {
            'underweight': (0, 18.4),
            'normal': (18.5, 24.9),
            'overweight': (25, 29.9),
            'obese': (30, float('inf'))
        }

    def create_widgets(self):
        # Labels and Entry Widgets
        self.label_weight = tk.Label(self.root, text="Weight (kg):")
        self.label_weight.grid(row=0, column=0, padx=10, pady=10)
        self.entry_weight = tk.Entry(self.root)
        self.entry_weight.grid(row=0, column=1, padx=10, pady=10)

        self.label_height = tk.Label(self.root, text="Height (cm):")
        self.label_height.grid(row=1, column=0, padx=10, pady=10)
        self.entry_height = tk.Entry(self.root)
        self.entry_height.grid(row=1, column=1, padx=10, pady=10)

        # Calculate BMI Button
        self.calculate_button = tk.Button(self.root, text="Calculate BMI", command=self.calculate_bmi)
        self.calculate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

        # BMI Result Label
        self.label_bmi = tk.Label(self.root, text="BMI:")
        self.label_bmi.grid(row=3, column=0, padx=10, pady=10)
        self.result_bmi = tk.Label(self.root, text="")
        self.result_bmi.grid(row=3, column=1, padx=10, pady=10)

        # BMI History Button
        self.history_button = tk.Button(self.root, text="BMI History", command=self.view_history)
        self.history_button.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Exit Button
        self.exit_button = tk.Button(self.root, text="Exit", command=self.root.quit)
        self.exit_button.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

    def calculate_bmi(self):
        try:
            weight = float(self.entry_weight.get())
            height = float(self.entry_height.get())

            if weight <= 0 or height <= 0:
                messagebox.showerror("Error", "Weight and height must be positive numbers.")
                return

            height /= 100  # Convert height from cm to meters
            bmi = weight / (height * height)
            self.result_bmi.config(text="{:.2f}".format(bmi))

            # Save data to database
            self.save_to_database(weight, height * 100, bmi)

            # Check BMI category
            self.check_bmi_category(bmi)

        except ValueError:
            messagebox.showerror("Error", "Please enter valid weight and height.")

    def save_to_database(self, weight, height, bmi):
        cursor = self.conn.cursor()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO bmi_data (weight, height, bmi, timestamp) VALUES (?, ?, ?, ?)",
                       (weight, height, bmi, timestamp))
        self.conn.commit()

    def check_bmi_category(self, bmi):
        for category, (lower, upper) in self.bmi_norms.items():
            if lower <= bmi <= upper:
                messagebox.showinfo("BMI Category", f"Your BMI falls under the {category} category.")
                return

    def view_history(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM bmi_data")
        data = cursor.fetchall()

        if not data:
            messagebox.showinfo("BMI History", "No BMI data available.")
            return

        weights = [record[1] for record in data]
        heights = [record[2] for record in data]
        bmis = [record[3] for record in data]
        timestamps = [record[4] for record in data]

        # Plot BMI over time
        plt.figure(figsize=(10, 6))
        plt.plot(timestamps, bmis, marker='o', color='blue', linestyle='-')
        plt.title('BMI Trend Analysis')
        plt.xlabel('Timestamp')
        plt.ylabel('BMI')
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

        # Calculate statistics
        average_bmi = np.mean(bmis)
        max_bmi = max(bmis)
        min_bmi = min(bmis)

        messagebox.showinfo("BMI Statistics", f"Average BMI: {average_bmi:.2f}\nMaximum BMI: {max_bmi}\nMinimum BMI: {min_bmi}")

    def create_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS bmi_data
                          (id INTEGER PRIMARY KEY AUTOINCREMENT,
                           weight REAL,
                           height REAL,
                           bmi REAL,
                           timestamp DATETIME)''')
        self.conn.commit()


if __name__ == "__main__":
    root = tk.Tk()
    app = BMI_Calculator(root)
    root.mainloop()