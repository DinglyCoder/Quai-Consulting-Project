import requests
from bs4 import BeautifulSoup
import random
from player import Player

def get_dexscreener_price(blockchain: str, pair_address: str):
    url = f"https://api.dexscreener.com/latest/dex/pairs/{blockchain}/{pair_address}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        price = data["pairs"][0]["priceUsd"]  # Price in USD
        return price
    else:
        raise Exception(f"Error fetching data: {response.status_code}")

# Example usage: Provide a Dex Screener pair URL
pair_address = "46rt2qdb2a6lgrk2q8fw2qptbsh6yzt1mg9ba86wrgbi"
blockchain = "solana"

def get_dex_trending_pairs():
    url = "https://api.dexscreener.com/latest/dex/trending"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        top_pairs = data.get("pairs", [])
        
        # Sort pairs by 24h volume in descending order
        sorted_pairs = sorted(top_pairs, key=lambda x: float(x.get("txns", {}).get("h24", 0)), reverse=True)

        # Print top 10 pairs
        for i, pair in enumerate(sorted_pairs[:10]):
            name = f"{pair['baseToken']['symbol']}/{pair['quoteToken']['symbol']}"
            volume = pair.get("volume", {}).get("h24", "N/A")
            price = pair.get("priceUsd", "N/A")
            chain = pair.get("chainId", "N/A")
            url = pair.get("url", "")

            print(f"{i+1}. {name} - ${price} - 24H Volume: ${volume} - Chain: {chain}")
            print(f"   Dex Screener Link: {url}\n")

    else:
        print(f"Error fetching data: {response.status_code}")
    
# get_dex_trending_pairs()

def ronaldo_coin_price():
    try:
        price = get_dexscreener_price(blockchain, pair_address)
        print(f"Price: {price}")    
    except Exception as e:
        print(e)

# ronaldo_coin_price()

def calculate_earning(winning_pool, losing_pool):
    total_pool = winning_pool + losing_pool
    house_earnings = total_pool * 0.05
    total_pool -= house_earnings

    

def get_random_coin():
    page = random.randint(1, 172)
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
        r = random.randint(1,10)
        rand = data[r]
        name = rand["name"]
        symbol = rand["symbol"].upper()
        price = rand["current_price"]
        volume = rand["total_volume"]
        market_cap = rand["market_cap"]
        coingecko_url = f"https://www.coingecko.com/en/coins/{rand['id']}"

        print(f"1. {name} ({symbol})")
        print(f"   💰 Price: ${price}")
        print(f"   📊 24H Volume: ${volume:,}")
        print(f"   🏦 Market Cap: ${market_cap:,}")
        print(f"   🔗 CoinGecko: {coingecko_url}\n")
    else:
        print(f"Error fetching data: {response.status_code}")
    return [name, symbol, price, volume, market_cap, coingecko_url]

def main():
    coin_info = get_random_coin()
    coin_name = coin_info[0]
    coin_price = coin_info[2]

if __name__ == "__main__":
    main()
    
