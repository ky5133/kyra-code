import tkinter as tk

root=tk.Tk()
root.geometry('400x400')
root.title('Password Strenght Checker App')

def check_password():
    password=entry.get()
    lenght=len(password)

    if lenght<=5 :
        result_label.config(root,text="Weak",fg='ed')

    elif  6 <= lenght <= 8 :
        result_label.config(root,text="Medium",fg='Yellow')

    elif 8 <= lenght <= 12 :
        result_label.config(root,text="strong",fg='Green')      

    else:
        result_label.config(root,text="Very Strong",fg="Dark Green")


label=tk.Label(root,text="Enter Password:") 
label.pack(pady=10)  

entry= tk.Entry(root,show="*")
entry.pack(pady=5)

result_label=tk.Label(root,text="",font=("Arial",14,"bold"))
result_label.pack(pady=20)

check_button=tk.Label(root,text="Check password",command=check_password)
check_button.pack(pady=10)


root.mainloop()
