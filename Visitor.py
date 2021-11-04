
class Visitor:
    def __init__(self, id):
        self.id = id
        self.x = 1
        self.y = 1
        self.timer = 0
        self.wait = 0
    
    def Move(self, move):
        if(0 <= self.x+move[0] < 20):
            self.x += move[0]
        if(0 <= self.y+move[1] < 20):
            self.y += move[1]
        self.timer = 0

    
    def IsIn(self, atraccion):
        dX = abs(self.x-atraccion.x)
        dY = abs(self.y-atraccion.y)
        return dX+dY <= 2