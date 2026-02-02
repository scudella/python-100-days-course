import tkinter

window = tkinter.Tk()
window.title("My first window")
window.minsize(width=500, height=400)
# padding
window.config(padx=20, pady=20)

my_label = tkinter.Label(text="This is a label", font=("Arial", 18))
# my_label.pack()
#padding
my_label.config(padx=20, pady=20)
my_label.grid(row=0, column=0)

button2 = tkinter.Button(text="New Button")
button2.grid(row=0, column=2)

my_label["text"] = "Another label"

def button_clicked():
    my_label.config(text=input.get())

button = tkinter.Button(text="Click me", command=button_clicked)
button.grid(row=1, column=1)

input = tkinter.Entry(width=10)
input.grid(row=2, column=3)


window.mainloop()