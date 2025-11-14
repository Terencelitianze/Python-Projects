import random

class Coin:
    def __init__(self):
        self.__side_up = ["head","tail"] 

    def toss(self):
        self.__side_up = self.__side_up[random.randint(0,1)]
        print(self.__side_up)

    def getter(self):
        return self.__side_up
    def setter(self, sideup):
        self.__side_up = sideup
        print(self.__side_up)

coin = Coin()
print(coin.getter())
coin.setter(["boy"])





