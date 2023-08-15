import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "WVBWXNNW6M4J3VEY"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "cc81423667b94f94a497977b446dc19c"

account_sid = "ACf0f882f3fee3ea34f344d5246df4c42a"
auth_token = "917ded08892ec36a9ca93242d2eae900"


stock_parameters = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK,
    "apikey": STOCK_API_KEY,
}

response = requests.get(STOCK_ENDPOINT, params=stock_parameters)
response.raise_for_status()
data = response.json()


time_series = data["Time Series (Daily)"]
time_series_list = list(time_series.items())


price_close = [float(values['4. close']) for date, values in time_series_list[:2]]
percent_diff = ((price_close[1] - price_close[0]) / price_close[0]) * 100
rounded_percent_diff = round(percent_diff, 2)
if rounded_percent_diff > 5 or rounded_percent_diff < -5:
    if rounded_percent_diff > 0:
        symbol = f"🔺{rounded_percent_diff}%"
    else:
        symbol = f"🔻{rounded_percent_diff}%"

    news_parameters = {
        "q": COMPANY_NAME,
        "language": "en",
        "apiKey": NEWS_API_KEY,
    }
    response = requests.get(NEWS_ENDPOINT, params=news_parameters)
    response.raise_for_status()
    data = response.json()
    news = data["articles"][:3]

    title = [item["title"] for item in news]
    description = [item["description"] for item in news]
    for title, description in zip(title, description):
        client = Client(account_sid, auth_token)

        message = client.messages.create(
            from_='+18787887278',
            body=f"{STOCK}: {symbol}\nHeadline: {title}\nBrief: {description} ",
            to='+639760151450'
        )
        print(message.status)





## STEP 1: Use https://newsapi.org/docs/endpoints/everything
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
#HINT 1: Get the closing price for yesterday and the day before yesterday. Find the positive difference between the two prices. e.g. 40 - 20 = -20, but the positive difference is 20.
#HINT 2: Work out the value of 5% of yerstday's closing stock price. 



## STEP 2: Use https://newsapi.org/docs/endpoints/everything
# Instead of printing ("Get News"), actually fetch the first 3 articles for the COMPANY_NAME. 
#HINT 1: Think about using the Python Slice Operator



## STEP 3: Use twilio.com/docs/sms/quickstart/python
# Send a separate message with each article's title and description to your phone number. 
#HINT 1: Consider using a List Comprehension.



#Optional: Format the SMS message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

