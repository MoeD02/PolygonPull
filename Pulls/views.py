from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
import requests
import pandas as pd
import time

API_KEY = "oAuWrjlpFZgzGC7zBlolCz8awHWN6XOm"

def index(request):
    return render(request, "Pulls/home.html")


def process_stock_query(request):
    if request.method == "POST":
        # Process the submitted data
        query = {
            "stock_ticker": request.POST.get("stock_ticker"),
            "multiplier": request.POST.get("multiplier"),
            "timespan": request.POST.get("timespan"),
            "start_date": request.POST.get("from"),
            "end_date": request.POST.get("to"),
            "adjusted": request.POST.get("adjusted") == "on",
            "sort": request.POST.get("sort"),
            "limit": request.POST.get("limit"),
        }
        print("Received query in process_stock_query:")
        for key, value in query.items():
            print(f"{key}: {value}")
        pull_data(query)
        return HttpResponse(f"Received data in process_stock_query: {query}")
    return HttpResponse("Invalid request method.")


from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from datetime import datetime
import requests
import pandas as pd
import time

API_KEY = "oAuWrjlpFZgzGC7zBlolCz8awHWN6XOm"


def index(request):
    return render(request, "Pulls/home.html")


def process_stock_query(request):
    if request.method == "POST":
        # Process the submitted data
        query = {
            "stock_ticker": request.POST.get("stock_ticker"),
            "multiplier": request.POST.get("multiplier"),
            "timespan": request.POST.get("timespan"),
            "start_date": request.POST.get("from"),
            "end_date": request.POST.get("to"),
            "adjusted": request.POST.get("adjusted") == "on",
            "sort": request.POST.get("sort"),
            "limit": request.POST.get("limit"),
        }
        print("Received query in process_stock_query:")
        for key, value in query.items():
            print(f"{key}: {value}")
        pull_data(query)
        return HttpResponse(f"Received data in process_stock_query: {query}")
    return HttpResponse("Invalid request method.")


def pull_data(query):
    stock_data = pd.DataFrame()
    URL = f"https://api.polygon.io/v2/aggs/ticker/{query['stock_ticker']}/range/{query['multiplier']}/{query['timespan']}/{query['start_date']}/{query['end_date']}"
    PARAMS = {
        "adjusted": "true",
        "sort": "asc",
        "limit": "50000",
        "apiKey": API_KEY,
    }

    try:
        response = requests.get(URL, params=PARAMS)
        if response.status_code == 200:
            data = response.json()
            if data["status"] == "OK" and "results" in data:
                # Flatten the data and store in a pandas dataframe
                df = pd.json_normalize(data["results"])
                df["datetime"] = df["t"].apply(
                    lambda x: datetime.utcfromtimestamp(x / 1000).strftime(
                        "%Y-%m-%d %H:%M:%S"
                    )
                )
                df = df.drop("t", axis=1)
                df["stock_date"] = pd.to_datetime(df["datetime"]).dt.date
                df["Stock Ticker"] = query["stock_ticker"]

                print(
                    f"Data of {query['stock_ticker']} for date {query['start_date']} is converted to dataframe"
                )

                # Append to stock_data
                stock_data = pd.concat([stock_data, df], ignore_index=True)

                print(
                    f"Data of {query['stock_ticker']} for date {query['start_date']} is appended to stock_data"
                )
            else:
                print("Failed to fetch data or no results found.")
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")

    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")

    # Save to CSV file
    if not stock_data.empty:
        stock_data.to_csv(r"C:\Users\dahbo\Downloads\stock_data.csv", index=False)
    else:
        print("No data to save.")
