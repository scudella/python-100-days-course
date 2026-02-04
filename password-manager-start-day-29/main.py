from tkinter import *
from tkinter import messagebox
import random
import pyperclip

window = Tk()
window.title("Password Manager")
window.config(padx=50, pady=50, bg="white")


# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols = ['!', '#', '$', '%', '&', '(', ')', '*', '+']

    nr_letters = random.randint(8, 10)
    nr_symbols = random.randint(2, 4)
    nr_numbers = random.randint(2, 4)

    password_letters = [random.choice(letters) for _ in range(nr_letters)]
    password_symbols = [random.choice(symbols) for _ in range(nr_symbols)]
    password_numbers = [random.choice(numbers) for _ in range(nr_numbers)]

    password_list = password_letters + password_symbols + password_numbers
    random.shuffle(password_list)

    password = "".join(password_list)

    password_entry.insert(0, password)
    pyperclip.copy(password)


# ---------------------------- SAVE PASSWORD ------------------------------- #

def save():
    email = email_entry.get()
    website = website_entry.get()
    password = password_entry.get()

    if len(email) == 0 or len(website) == 0 or len(password) == 0:
        messagebox.showerror("Error", "Please enter all fields")
        return

    is_ok = messagebox.askokcancel(title=website, message=f"These are the details "
                                                                f"entered: \n {email} \n "
                                                                f"{password} \n"
                                                                f"Is it ok to save?")
    if is_ok:
        with open("data.txt", "a") as file:
            file.write(f"\n{website} | {email} | {password}")
        website_entry.delete(0, END)
        password_entry.delete(0, END)

# ---------------------------- UI SETUP ------------------------------- #

canvas = Canvas(window, width=200, height=200, bg="white", highlightthickness=0)
locker_image = PhotoImage(file="logo.png")
canvas.create_image(100, 100, image=locker_image)
canvas.grid(column=1, row=0)

website_label = Label(window, text="Website:", bg="white")
website_label.grid(column=0, row=1)

website_entry = Entry(window, width=41, bg="white")
website_entry.grid(column=1, row=1, columnspan=2)
website_entry.focus()

email_label = Label(window, text="Email/Username:", bg="white")
email_label.grid(column=0, row=2)

email_entry = Entry(window, width=41, bg="white")
email_entry.grid(column=1, row=2, columnspan=2, pady=4)
email_entry.insert(0, "@gmail.com")

password_label = Label(window, text="Password:", bg="white")
password_label.grid(column=0, row=3)

password_entry = Entry(window, width=24, bg="white")
password_entry.grid(column=1, row=3, padx=0)

generate_button = Button(text='Generate Password', bg="white", fg="black", highlightthickness=0, width=13, command=generate_password)
generate_button.grid(column=2, row=3)

add_button = Button(text='Add', bg="white", width=38, fg="black", highlightthickness=0, command=save)
add_button.grid(column=1, row=4, columnspan=2, pady=4)

window.mainloop()