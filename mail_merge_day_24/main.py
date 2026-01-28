with open("./Input/Letters/starting_letter.txt", "r") as letter:
    by_line = letter.readlines()
    with open("./Input/Names/invited_names.txt", "r") as names:
        name_list = names.readlines()
        original_header = by_line[0]
        by_line.pop(0)
        for name in name_list:
            header = original_header.replace("[name]", name.strip())
            with open(f"./Output/ReadyToSend/letter_for_{name.strip()}.docx", "w") as final_letter:
                final_letter.write(header)
                for line in by_line:
                    final_letter.write(line)
