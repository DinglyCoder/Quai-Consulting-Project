class PlayerData:
    buyPrice = 0
    sellPrice = 0
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.earnings = 0
        

    def processBuy(self, price):
        self.buyPrice = price

    def processSell(self, price):
        self.sellPrice = price
        self.earnings = self.sellPrice - self.buyPrice
