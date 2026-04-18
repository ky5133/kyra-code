
import tkinter as tk
from tkinter import messagebox

def calculate_interest():
    try:
        p = float(entry_p.get())
        t = float(entry_t.get())
        r = float(entry_r.get())

        si = (p * r * t) / 100
        ci = p * (pow((1 + r / 100), t)) - p

        lbl_si_res.config(text=f"Simple Interest: {si:.2f}")
        lbl_ci_res.config(text=f"Compound Interest: {ci:.2f}")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values")

root = tk.Tk()
root.title("Age Calculator App") 
root.geometry("400x400")
root.configure(bg="#f0f0f0")

tk.Label(root, text="Interest Calculator", font=("Arial", 14, "bold"), bg="#f0f0f0").pack(pady=10)

frame = tk.Frame(root, bg="#f0f0f0")
frame.pack(pady=10)

tk.Label(frame, text="Principle:", bg="#f0f0f0").grid(row=0, column=0, padx=10, pady=5, sticky="e")
entry_p = tk.Entry(frame)
entry_p.grid(row=0, column=1, padx=10, pady=5)

tk.Label(frame, text="Time (years):", bg="#f0f0f0").grid(row=1, column=0, padx=10, pady=5, sticky="e")
entry_t = tk.Entry(frame)
entry_t.grid(row=1, column=1, padx=10, pady=5)

tk.Label(frame, text="Rate of Interest (%):", bg="#f0f0f0").grid(row=2, column=0, padx=10, pady=5, sticky="e")
entry_r = tk.Entry(frame)
entry_r.grid(row=2, column=1, padx=10, pady=5)

btn_calc = tk.Button(root, text="Calculate", command=calculate_interest, bg="#4CAF50", fg="white", width=15)
btn_calc.pack(pady=20)

lbl_si_res = tk.Label(root, text="Simple Interest: 0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
lbl_si_res.pack(pady=5)

lbl_ci_res = tk.Label(root, text="Compound Interest: 0.00", font=("Arial", 10, "bold"), bg="#f0f0f0")
lbl_ci_res.pack(pady=5)

root.mainloop()