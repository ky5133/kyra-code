import tkinter as tk 
import random

root=tk.Tk()
root.geometry('400x400')
root.title("Rock,Paper,Scissors")

def play(user_choice):
    options = ["Rock", "Paper", "Scissors"]
    # Requirement 3: Random choice for computer
    computer_choice = random.choice(options)
    
    # Requirement 5: Display winner by checking rules
    if user_choice == computer_choice:
        result = "It's a Tie!"
    elif (user_choice == "Rock" and computer_choice == "Scissors") or \
         (user_choice == "Paper" and computer_choice == "Rock") or \
         (user_choice == "Scissors" and computer_choice == "Paper"):
        result = f"You Win! {user_choice} beats {computer_choice}"
    else:
        result = f"You Lose! {computer_choice} beats {user_choice}"
    
    result_label.config(text=f"Computer chose: {computer_choice}\n{result}")

Instructions=tk.Label(root, text="Choose Rock, Paper, or scissors:", pady=20,padx=20)
Instructions.pack()
Rock_button=tk.Button(root,text="Rock", command=lambda: play("Rock"), pady=10,padx=20)
Rock_button.pack()
Paper_button=tk.Button(root,text="Paper", command=lambda: play("Paper"), pady=10,padx=20)
Paper_button.pack()
Scissors_button=tk.Button(root,text="Scissors", command=lambda: play("Scissors"), pady=10,padx=20)
Scissors_button.pack()
result_label=tk.Label(root, text="",pady=30,font="Arial 16 bold")
result_label.pack()
root.mainloop()
                      
