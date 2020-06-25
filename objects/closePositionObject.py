class closePosition:
    id = None
    isCall = None
    isCallInverse = None

    def __str__(self):
        print(self.id, self.isCall, self.isCallInverse)

    def __init__(self, id, isCall):
        self.id = id
        self.isCall = bool(isCall)
        self.isCallInverse = not bool(isCall)