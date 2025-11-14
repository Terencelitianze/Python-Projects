class Bank:
    def __init__(self):
        self.__balance = 0
    def deposit(self,money):
        self.__balance = self.__balance + money 
    def withdraw(self,amount):
        if amount > self.__balance:
            print("There is not enough money in your bank.")
        else:
            self.__balance = self.__balance - amount
            print("you have",self.__balance,"remaining")
    def print(self):
        print(self.__balance)

bank = Bank()

while True:
    decision = int(input("Enter 1 to deposit, press 2 to withdraw, and press 3 to print balance: "))
    if decision == 1:
        money = int(input("How much do you want to deposit: "))
        bank.deposit(money)
    elif decision == 2:
        amount = int(input("How much do you want to withdraw: "))
        bank.withdraw(amount)
    elif decision == 3:
        bank.print()
