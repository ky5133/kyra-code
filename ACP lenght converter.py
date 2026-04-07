import tkinter as tk
root = tk.Tk()
root.geometry=('400x400')
root.title('Lenght Converter')

def convert():
    inches=float(entry_inches.get())
    centimetres=inches*2.54
    label_result.config(text=f"lenght in centimetres{centimetres}")

label_instruction=tk.Label(root,text="Enter lenght in inches", fg="white",bg="blue")
label_instruction.pack(pady=20)

entry_inches=tk.Entry(root)
entry_inches.pack(pady=10) 

button_convert=tk.Button(root,text="Convert",command=convert,fg="white",bg="blue")
button_convert.pack(pady=20)

label_result=tk.Label(root,text="Lenght in cm:")
label_result.pack(pady=20)

root.mainloop()