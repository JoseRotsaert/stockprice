import requests
from datetime import date, timedelta
import os
from twilio.rest import Client

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
FONCTION = "TIME_SERIES_DAILY"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

ALPHAVANTAGE_API_KEY = "M576ZLP4KK7YM8BM"
ALPHAVANTAGE_ENDPOINT = "https://www.alphavantage.co/query"

NEWS_API_KEY = "7e04b56b82a8427989cd05c2e00d2be8"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

TWILIO_account_sid = "AC3527f8c0f1d47acd942a3e2eaa3b2266"
TWILIO_auth_token = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"

today = date.today()
yesterday = str(today - timedelta(days=1))
print(yesterday)   # '2017-12-26'

stock_parameters = {
    "function": FONCTION,
    "symbol": STOCK_NAME,
    "apikey": ALPHAVANTAGE_API_KEY,
}



    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]

response = requests.get(url=STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
stock_data = response.json()["Time Series (Daily)"]
stock_list = [value["4. close"] for (key, value) in stock_data.items()]
day_minus_1_stock = float(stock_list[0])
day_minus_2_stock = float(stock_list[1])

print(day_minus_1_stock)


#TODO 2. - Get the day before yesterday's closing stock price

print(day_minus_2_stock)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp

abs_stock_difference = abs(day_minus_1_stock - day_minus_2_stock)
stock_difference = day_minus_1_stock - day_minus_2_stock
print (abs_stock_difference)

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.

perc_stock_difference = round(abs_stock_difference/day_minus_1_stock*100, 2)
print(perc_stock_difference)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").

if perc_stock_difference > 1:
    news_parameters = {
        "qInTitle": COMPANY_NAME,
        "from": yesterday,
        "sortBy": "published",
        "apiKey": NEWS_API_KEY,
    }
    news_response = requests.get(url=NEWS_ENDPOINT, params=news_parameters)
    news_response.raise_for_status()
    news_data = news_response.json()["articles"][0:3]
    print(news_data)
    print(type(news_data))
    ## STEP 2: https://newsapi.org/ 
    # Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME. 

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.


# https://newsapi.org/v2/everything?q=tesla&from=2021-03-23&sortBy=publishedAt&apiKey=API_KEY

#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation



    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.

#[new_value for (key, value) in dictionary.items()]

sms_list =[]
article ={}
for num in news_data:
    article["title"]=num["title"]
    article["description"] = num["description"]
    sms_list.append(article)

print(sms_list)
#TODO 9. - Send each article as a separate message via Twilio.

if stock_difference > 0:
    symbol = "🔺"
else:
    symbol = "🔻"


for article in sms_list:
    article_title = article["title"]
    article_description = article["description"]
    body = f"{STOCK_NAME}:{symbol}{perc_stock_difference}%\nHeadline: {article_title}\nBrief: {article_description}"
    print(body)

    client = Client(TWILIO_account_sid, TWILIO_auth_token)
    message = client.messages \
        .create(
        body=f"{STOCK_NAME}:{symbol}{perc_stock_difference}%\nHeadline: {article_title}\nBrief: {article_description}",
        from_="+18602003804",
        to="+32486226706"
    )
    print(message.status)



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

