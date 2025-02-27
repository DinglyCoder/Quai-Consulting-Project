import requests
from bs4 import BeautifulSoup
import random
from player import PlayerData
import time
from tqdm import tqdm
import Flask, jsonify

app = Flask(__name__)
@app.route("/calculate_earnings", methods=["GET"])
def calculate_earnings(players, coin_price, new_coin_price):
    winners = []
    losers = []
    if new_coin_price > coin_price:
        for player in players:
            if player.guess == "up":
                winners.append(player)
            elif player.guess == "down":
                losers.append(player)
    elif new_coin_price < coin_price:
        for player in players:
            if player.guess == "down":
                winners.append(player)
            elif player.guess == "up":
                losers.append(player)
    total_pool = 0
    winning_pool = 0
    for player in losers:
        total_pool += player.bet
    for player in winners:
        winning_pool += player.bet
    house_earnings = total_pool * 0.05
    total_pool -= house_earnings
    for player in winners:
        player_earnings = (player.bet / winning_pool) * total_pool
        player.earnings += player_earnings
    for player in winners:
        print(f"{player.name} earned: ${player.earnings:.2f}")
    for player in losers:
        print(f"{player.name} lost: ${player.bet:.2f}")
    return house_earnings

@app.route("/get_token_data", methods=["GET"])
def get_token_data(symbol):
    API_KEY = "089c90ae-1dbb-411d-8b08-a776beaf5220"  # Replace with your CoinMarketCap API Key
    base_url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
    headers = {"X-CMC_PRO_API_KEY": API_KEY}
    params = {"symbol": symbol.upper(), "convert": "USD"}

    response = requests.get(base_url, headers=headers, params=params)

    if response.status_code == 200:
        data = response.json()
        if symbol.upper() in data["data"]:
            coin_data = data["data"][symbol.upper()]
            return {
                "name": coin_data["name"],
                "symbol": coin_data["symbol"],
                "price": coin_data["quote"]["USD"]["price"],
                "market_cap": coin_data["quote"]["USD"]["market_cap"],
            }
        else:
            return {"error": "Coin not found in CoinMarketCap."}
    else:
        return {"error": f"API request failed with status code {response.status_code}"}

@app.route("/get_random_coin", methods=["GET"])
def get_random_coin():
    name, symbol, price, volume, market_cap, coingecko_url, page, r = "", "", "", "", "", "", "", ""
    while True:
        try:
            page = random.randint(1, 100)
            url = "https://api.coingecko.com/api/v3/coins/markets"
            params = {
                "vs_currency": "usd",
                "order": "volume_desc",
                "per_page": 10,  # Get top 10 coins
                "page": page,
                "sparkline": "false"
            }

            response = requests.get(url, params=params)
            if response.status_code == 200:
                data = response.json()
                print("Random Coin")
                r = random.randint(0,9)
                rand = data[r]
                name = rand["name"]
                symbol = rand["symbol"].upper()
                price = rand["current_price"]
                volume = rand["total_volume"]
                market_cap = rand["market_cap"]
                coingecko_url = f"https://www.coingecko.com/en/coins/{rand['id']}"

                print(f"{name} / ({symbol})")
                print(f"   💰 Price: ${price}")
                print(f"   📊 24H Volume: ${volume:,}")
                print(f"   🏦 Market Cap: ${market_cap:,}")
                print(f"   🔗 CoinGecko: {coingecko_url}\n")
            else:
                print(f"Error fetching data: {response.status_code}")
            break
        except Exception as e:
            print(e)

    return jsonify({"name": name, "symbol": symbol, "price": price, "volume": volume, "market_cap": market_cap, "coingecko_url": coingecko_url})
@app.route("/get_coin_price", methods=["GET"])
def get_coin_price(arr):
    price_changed = False
    start_time = time.time()
    while True:
        try:
            new_price = get_token_data(arr[1])["market_cap"]
            break
        except Exception as e:
            print(e)
        time.sleep(5)
    market_cap = get_token_data(arr[1])["market_cap"]
    print(f"Market Cap: ${market_cap}")
    while not price_changed:
        cur_market_cap = get_token_data(arr[1])["market_cap"]
        if cur_market_cap != market_cap:
            price_changed = True
            print(
                f"Market Cap changed from ${market_cap} to ${cur_market_cap}. Price has been updated."
            )
        time.sleep(5)
    end_time = time.time()
    print(f"Time elapsed: {end_time - start_time:.2f} seconds")

    if cur_market_cap > market_cap:
        return jsonify({"result": "up"})
    if cur_market_cap < market_cap:
        return jsonify({"result": "down"})
    
    return jsonify({"result": "error"})


def main():
    Sanika = PlayerData("Sanika", 100, "up")
    Ryan = PlayerData("Ryan", 50, "up")
    Ayush = PlayerData("Ayush", 70, "up")
    Shanti = PlayerData("Shanti", 20, "down")
    Prat = PlayerData("Prat", 50, "down")
    Ethan = PlayerData("Ethan", 30, "down")

    players = [Sanika, Ryan, Ayush, Shanti, Prat, Ethan]
    coin_info = get_random_coin()
    coin_price = coin_info[4]
    new_coin_price = get_coin_price(coin_info)
    print(new_coin_price)
    house = calculate_earnings(players, coin_price, new_coin_price)

if __name__ == "__main__":
    main()
    
