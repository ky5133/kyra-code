import tkinter as tk

def calculate_product():
    
        # Get numbers from entry widgets
        num1 = float(entry1.get())
        num2 = float(entry2.get())
        product = num1 * num2
        
        
        result_text.delete(1.0, tk.END)
        result_text.insert(tk.END, f"Product: {product}")
    


root = tk.Tk()
root.title("Getting Started with Widgets")
root.geometry("400x300")


desc_label = tk.Label(root, text="This app calculates the product of two numbers.", wraplength=350)
desc_label.pack(pady=10)


tk.Label(root, text="Enter first number:").pack()
entry1 = tk.Entry(root)
entry1.pack()

tk.Label(root, text="Enter second number:").pack()
entry2 = tk.Entry(root)
entry2.pack()


calc_button = tk.Button(root, text="Calculate Product", command=calculate_product, bg="lightblue")
calc_button.pack(pady=10)


result_text = tk.Text(root, height=2, width=30)
result_text.pack(pady=10)

root.mainloop()