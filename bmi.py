import tkinter as tk
from tkinter import messagebox
import sqlite3
import matplotlib.pyplot as plt
from datetime import datetime

# Create the main window
root = tk.Tk()
root.title("BMI Calculator")

# Database setup
conn = sqlite3.connect('bmi_data.db')
c = conn.cursor()

# Create table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS bmi_data
             (id INTEGER PRIMARY KEY, user TEXT, weight REAL, height REAL, bmi REAL, date TEXT)''')
conn.commit()

# Functions
def calculate_bmi():
    try:
        weight = float(entry_weight.get())
        height = float(entry_height.get()) / 100  # Convert height to meters
        bmi = weight / (height ** 2)
        entry_bmi.delete(0, tk.END)
        entry_bmi.insert(0, f"{bmi:.2f}")
        save_bmi(weight, height, bmi)
    except ValueError:
        messagebox.showerror("Invalid input", "Please enter valid weight and height values.")

def save_bmi(weight, height, bmi):
    user = entry_user.get()
    if user:
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        c.execute("INSERT INTO bmi_data (user, weight, height, bmi, date) VALUES (?, ?, ?, ?, ?)",
                  (user, weight, height, bmi, date))
        conn.commit()
        messagebox.showinfo("Success", "BMI data saved successfully.")
    else:
        messagebox.showerror("Invalid input", "Please enter a user name.")

def view_history():
    user = entry_user.get()
    if user:
        c.execute("SELECT * FROM bmi_data WHERE user=? ORDER BY date DESC", (user,))
        records = c.fetchall()
        if records:
            history_window = tk.Toplevel(root)
            history_window.title("BMI History")
            for index, (id, user, weight, height, bmi, date) in enumerate(records):
                tk.Label(history_window, text=f"{date}: Weight: {weight}kg, Height: {height * 100}cm, BMI: {bmi:.2f}").grid(row=index, column=0)
        else:
            messagebox.showinfo("No Data", "No historical data found for this user.")
    else:
        messagebox.showerror("Invalid input", "Please enter a user name.")

def show_trend():
    user = entry_user.get()
    if user:
        c.execute("SELECT date, bmi FROM bmi_data WHERE user=? ORDER BY date ASC", (user,))
        records = c.fetchall()
        if records:
            dates, bmis = zip(*records)
            plt.figure(figsize=(10, 5))
            plt.plot(dates, bmis, marker='o')
            plt.title(f"BMI Trend for {user}")
            plt.xlabel("Date")
            plt.ylabel("BMI")
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()
        else:
            messagebox.showinfo("No Data", "No trend data found for this user.")
    else:
        messagebox.showerror("Invalid input", "Please enter a user name.")

# Widgets
tk.Label(root, text="User Name:").grid(row=0, column=0)
entry_user = tk.Entry(root)
entry_user.grid(row=0, column=1)

tk.Label(root, text="Weight (kg):").grid(row=1, column=0)
entry_weight = tk.Entry(root)
entry_weight.grid(row=1, column=1)

tk.Label(root, text="Height (cm):").grid(row=2, column=0)
entry_height = tk.Entry(root)
entry_height.grid(row=2, column=1)

tk.Label(root, text="BMI:").grid(row=3, column=0)
entry_bmi = tk.Entry(root, state='readonly')
entry_bmi.grid(row=3, column=1)

tk.Button(root, text="Calculate BMI", command=calculate_bmi).grid(row=4, column=0, columnspan=2)
tk.Button(root, text="View History", command=view_history).grid(row=5, column=0, columnspan=2)
tk.Button(root, text="Show Trend", command=show_trend).grid(row=6, column=0, columnspan=2)

# Run the application
root.mainloop()

# Close the database connection
conn.close()
