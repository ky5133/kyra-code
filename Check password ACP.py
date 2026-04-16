import tkinter as tk

root = tk.Tk()
root.title("Length Converter App")
root.geometry("400x400")

def check_strength():
    password = entry.get()
    length = len(password)
    
    if length <= 5:
        result_label.config(text="Weak", fg="red")
    elif 6 <= length <= 8:
        result_label.config(text="Medium", fg="yellow")
    elif 8 < length <= 12:
        result_label.config(text="Strong", fg="lightgreen")
    else:
        result_label.config(text="Very Strong", fg="darkgreen")


label = tk.Label(root, text="Enter Password:")
label.pack(pady=10)

entry = tk.Entry(root, show="*")
entry.pack(pady=5)

check_button = tk.Button(root, text="Check Strength", command=check_strength)
check_button.pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 14, "bold"))
result_label.pack(pady=20)

root.mainloop()