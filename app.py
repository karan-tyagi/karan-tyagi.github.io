# Name: Karan Tyagi
# SJSU ID: 015908932

# imports
from flask import Flask
from flask import render_template
from flask import request
import yfinance as yf
from datetime import date, datetime

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')

    elif request.method == 'POST':
        try:
            ticker = str(request.form['tickerSymbol'])
            stock_info = yf.Ticker(ticker).info
            current_date = str(date.today().strftime("%B %d"))
            current_time = str(datetime.now().strftime("%H:%M:%S"))
            current_day = str(date.today().strftime("%A"))
            current_year = str(date.today().strftime("%Y"))
            timeZone = "PDT"
            print(current_date, current_time)
            # full name of the company
            fullName = stock_info["longName"]
            # current stock price
            curr_price = stock_info["currentPrice"]
            # previous closing price
            prevClosingPrice = stock_info["previousClose"]
            # price change, that is, current price - previous closing price
            price_change = curr_price - prevClosingPrice
            perc_change = ((price_change) / prevClosingPrice) * 100
            if price_change > 0:
                price_change = "+" + str(round(price_change, 2))
                perc_change = "+" + str(round(perc_change, 2))
            else:
                price_change = str(round(price_change, 2))
                perc_change = str(round(perc_change, 3))

            stock_data = {'currentDay': f"Date and Time: {current_day}",
                        'currentDate': current_date, 'currentTime': current_time,
                        'currentYear': current_year, 'currentTimezone': timeZone,
                        'companyName': f"Company Name: {fullName}",
                        'stockPrice': f"Current Price: {curr_price}",
                        'valueChange': f"Value Change: {price_change}",
                        'percentChange': f"Percent Change: {perc_change}%"}

        except:
            error_message = "Please enter a valid symbol!"
            stock_data = {"errorMessage": error_message}

        return render_template('index.html', **stock_data)


if __name__ == "__main__":
    app.run(debug=True)
