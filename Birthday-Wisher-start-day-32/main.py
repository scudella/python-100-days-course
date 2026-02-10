import smtplib
import datetime
import random

my_email = "edu@gmail.com"
password = "this is an app password"
to_email = "test@hotmail.com"

now = datetime.datetime.now()
nameOfDay = now.strftime('%A')

with open("quotes.txt", "r") as file:
    quotes = file.readlines()
    quote_of_the_day = random.choice(quotes)
    quoteList = quote_of_the_day.split(" - ")
    quote = quoteList[0]
    author = quoteList[1]

with smtplib.SMTP('smtp.gmail.com', 587) as connection:
    connection.starttls()
    connection.login(user=my_email, password=password)
    connection.sendmail(
        from_addr=my_email,
        to_addrs=to_email,
        msg=f"Subject: Quote of the Day\n\n{quote.strip()}\n\n{author.strip()}" )
