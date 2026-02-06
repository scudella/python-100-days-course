import pandas

nato_df = pandas.read_csv("nato_phonetic_alphabet.csv")

nato_dict = {row.letter: row.code for (index, row) in nato_df.iterrows()}

def generate_phonetic():
    word = input("Enter a word: ").upper()

    try:
        output_list = [nato_dict[char] for char in word]
        print(output_list)
    except KeyError:
        print("Sorry, only letters in the alphabet, please")
        generate_phonetic()

generate_phonetic()