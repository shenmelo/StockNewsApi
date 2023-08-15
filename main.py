import requests
from twilio.rest import Client


STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
STOCK_API_KEY = "YOUR KEY"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
NEWS_API_KEY = "YOUR KEY"

account_sid = "YOUR SID ACCOUNT"
auth_token = "YOUR AUTH TOKEN"


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
            from_='SENDER',
            body=f"{STOCK}: {symbol}\nHeadline: {title}\nBrief: {description} ",
            to='RECIPIENT'
        )
        print(message.status)


