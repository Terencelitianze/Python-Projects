String = input("Please input four names that are seperated by comma: ")

List = String.split(",")

print("\n"*100)
value = input("please enter one new word: ")
New_List = [value] + List

Message = ["Sorry, wrong guess","Congradulations"]
Guess = input("please guess a word in the list: ")
result = Guess in New_List
print(Message[result])

