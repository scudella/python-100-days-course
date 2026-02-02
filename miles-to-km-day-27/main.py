import tkinter

window = tkinter.Tk()
window.title("Mile to Km Converter")
window.minsize(400, 300)
window.config(padx=20, pady=20)

is_equal_to_label = tkinter.Label(text="is equal to")
is_equal_to_label.grid(column=0, row=1)

input_miles = tkinter.Entry(width=10)
input_miles.grid(row=0, column=1)

miles_label = tkinter.Label(text="Miles")
miles_label.config(padx=5)
miles_label.grid(column=2, row=0)

result_label = tkinter.Label(text="0")
result_label.grid(column=1, row=1)

km_label = tkinter.Label(text="Km")
km_label.config(padx=5)
km_label.grid(column=2, row=1)

def conv_miles_to_km():
    miles = float(input_miles.get())
    km = miles * 1.60934
    result_label.config(text=str(round(km, 1)))

button = tkinter.Button(text="Calculate", command=conv_miles_to_km)
button.grid(column=1, row=2)


window.mainloop()