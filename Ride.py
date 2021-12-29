class Ride:
    def __init__(self, x, y, wT):
        self.x = x
        self.y = y
        self.waitingTime = wT
        self.connected = True
    def abierta(self, temperaturas):
        sector = self.x//10 + self.y//10*2
        if(20 <= temperaturas[sector][1] <= 30):
            return True
        return False
        