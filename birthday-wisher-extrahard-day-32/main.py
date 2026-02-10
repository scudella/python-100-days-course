##################### Extra Hard Starting Project ######################
import datetime
import pandas
import smtplib
import random

my_email = "test@gmail.com"
password = ""
to_email = "test@hotmail.com"

# 1. Update the birthdays.csv

# 2. Check if today matches a birthday in the birthdays.csv

# 3. If step 2 is true, pick a random letter from letter templates and replace the [NAME] with the person's actual name from birthdays.csv

# 4. Send the letter generated in step 3 to that person's email address.

now = datetime.datetime.now()
file = pandas.read_csv("birthdays.csv")
birthday_dict = file.to_dict(orient="records")

for record in birthday_dict:
    if record["month"] == now.month and record["day"] == now.day:
        filename = f"letter_{random.randint(1,3)}.txt"
        with open(f"letter_templates/{filename}", "r") as fileLetter:
            letterList = fileLetter.readlines()
            letter = "".join(letterList)
            letter = letter.replace("[NAME]", record["name"])
        with smtplib.SMTP('smtp.gmail.com', 587) as connection:
            connection.starttls()
            connection.login(user=my_email, password=password)
            connection.sendmail(
            from_addr=my_email,
            to_addrs=record["email"],
            msg=f"Subject: Happy Birthday!!\n\n{letter}")
