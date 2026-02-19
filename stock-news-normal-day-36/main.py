import requests
import twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
STOCK_API_KEY = ""
NEWS_API_KEY = ""
TWILIO_SID = ""
TWILIO_AUTH_TOKEN = ""

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}

try:
    data = requests.get(url=STOCK_ENDPOINT, params=parameters)
    data.raise_for_status(),

except requests.exceptions.HTTPError as err:
    print(err)
else:
    time_series = data.json()["Time Series (Daily)"]
    last_month =  [value["4. close"] for (key, value) in time_series.items()]
    closing_price_yesterday = last_month[0]
    print(closing_price_yesterday)

    closing_price_day_before_yesterday = last_month[1]
    print(closing_price_day_before_yesterday)

    positive_diff = abs(float(closing_price_day_before_yesterday) - float(closing_price_yesterday))
    print(positive_diff)

    percentage_diff = positive_diff / float(closing_price_yesterday) * 100
    print(percentage_diff)

    ## STEP 2: https://newsapi.org/
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

    if percentage_diff > 5:
        news_parameters = {
            "apiKey": NEWS_API_KEY,
            "qInTitle": COMPANY_NAME,
        }
        try:
            news_response = requests.get(NEWS_ENDPOINT, params=news_parameters)
            news_response.raise_for_status(),
        except requests.exceptions.HTTPError as err:
            print(err)
        else:
            articles = news_response.json()["articles"]

            three_articles = articles[:3]



    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

            formatted_articles = [f"Headline: {article['title']}.\nBrief: {article['description']}." for article in three_articles]

            client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

            for article in formatted_articles:
                message = client.messages.create(
                    body = article,
                    from_ = "+5519",
                    to = "your number here",
                )




#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

