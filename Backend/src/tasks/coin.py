import requests

class Coin_data:
    def __init__(self, name, currency, ask, bid):
        self.name = name
        self.currency = currency
        self.ask = float(ask)
        self.bid = float(bid)
        

    def __init__(self, data):
        self.name = data["pair"]
        self.currency = data["currency"] 
        self.ask = float(data["ask"])
        self.bid = float(data["bid"])
        

    def get_avg_price(self):
        return (self.ask + self.bid) / 2

    def __str__(self):
        return f"{self.name} ({self.currency}) - Ask: {self.ask}, Bid: {self.bid}"
    
    def get_price_specific(self,coin):
        url = f"https://api.uphold.com/v0/ticker/{self.name}-{coin}"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            
            return (float(data['bid']) + float(data['ask'])) / 2

        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {e}")

    def update_parameters(self, data):
        self.name = data["pair"] 
        self.currency = data["currency"]
        self.ask = float(data["ask"])
        self.bid = float(data["bid"])
            
def get_coins_prices(cryptos, base_currency="EUR"):
    url = f"https://api.uphold.com/v0/ticker/{base_currency}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        var = False

        for entry in data:
            for crypto in cryptos:
                if crypto.name in entry["pair"]:
                    var = True
                    crypto.update_parameters(entry)
                    break
            if var == False:
                cryptos.append(Coin_data(entry))
            var = False

        return cryptos
    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a API: {e}")
        return None

