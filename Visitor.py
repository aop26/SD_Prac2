
class Visitor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.timer = 0
    
    def Move(self, move):
        if(0 <= self.x+move[0] < 20):
            self.x += move[0]
        if(0 <= self.y+move[1] < 20):
            self.y += move[1]
        self.timer = 0