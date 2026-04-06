from tkinter import *
window=Tk()
window.Title=('Event Handler')
window.geometry("100x100")

def handle_keypress(event):
    """Print the character associated to the key pressed"""
    print(event.char)

window.bind("<Key>",handle_keypress)

def handle_click(event):
    print("/nThe Button Was Clicked ")

btn=Button(text="Click me")
btn.pack()

btn.bind("<Button-1>",handle_click)

window.mainloop()