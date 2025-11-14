class TallyCounter:

    def __init__(self):
        self.counter = 0
        self.max_value = 9
        self.color = "red"

    def click(self):
        if self.counter < self.max_value:
            self.counter = self.counter + 1
            print(self.counter)
        else:
            print("Max value for the tally counter is reached")

    def reset(self):
        self.counter = 0
        print("The tally counter has been reset")

tally = TallyCounter()
while True:
    decision = int(input("Enter 1 to add 1 to tally, and press 2 to reset tally counter."))
    if decision == 1:
        tally.click()
    elif decision == 2:
        tally.reset()
    else:
        print("Error value")
