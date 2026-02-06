import pandas
from tkinter import *
import random

from pandas.core.interchange.dataframe_protocol import DataFrame

BACKGROUND_COLOR = "#B1DDC6"

flip_timer = ''

try:
    data = pandas.read_csv("words_to_learn.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/italian_words.csv")

current_list = data.to_dict(orient="records")
pick_word = random.choice(current_list)


def flip_card(side, word):
    if side == "front":
        canvas.itemconfig(canvas_image, image=card_front_image)
        canvas.itemconfig(language_text, text='Italian', fill="black")
        canvas.itemconfig(word_text, text=word["Italian"], fill="black")
    else:
        canvas.itemconfig(canvas_image, image=card_back_image)
        canvas.itemconfig(language_text, text="English", fill="white")
        canvas.itemconfig(word_text, text=word["English"], fill="white")


def next_card():
    global flip_timer
    global current_list
    global pick_word
    pick_word = random.choice(current_list)
    if flip_timer != "":
        window.after_cancel(flip_timer)
    flip_card(side="front", word=pick_word)
    flip_timer = window.after(3000, flip_card, "back", pick_word)

def delete_card():
    global current_list
    global pick_word
    current_list.remove(pick_word)
    df = pandas.DataFrame(current_list)
    df.to_csv("data/words_to_learn.csv", index=False)
    next_card()





# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Flash Cards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

card_front_image = PhotoImage(file="images/card_front.png")
card_back_image = PhotoImage(file="images/card_back.png")
button_wrong_image = PhotoImage(file="images/wrong.png")
button_right_image = PhotoImage(file="images/right.png")

canvas = Canvas(window, width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
canvas_image = canvas.create_image(400, 263, image=card_front_image)
language_text = canvas.create_text(400, 150, text="Title", fill="black", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text="Word", fill="black", font=("Arial", 60, "bold"))

canvas.grid(row=0, column=0, columnspan=2)

button_wrong = Button(window, image=button_wrong_image, highlightthickness=0, command=next_card)
button_wrong.grid(row=1, column=0)

button_right = Button(window, image=button_right_image, highlightthickness=0, command=delete_card)
button_right.grid(row=1, column=1)

next_card()



window.mainloop()