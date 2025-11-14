birthday = {}

file = open("ex_11.1_birthdays2.csv","r")
for line in file:
    List = line.strip().split(",")
    birthday[List[0]] = List[1]
file.close
print(birthday)

print("1.Look up a birthday")
print("2.Add a new birthday")
print("3.Change a birthday")
print("4.Delete a birthday")
print("5.Quit the program")

def look_up():
    look = input("enter the name of the person: ")
    output = birthday.get(look,"not found")
    return output 

def add():
    value = input("please enter the name: ")
    date = input("please enter the date: ")
    birthday[value] = date
    return

def change():
    name = input("please enter the name: ")
    change_date = input("please enter the date you want to change to: ")
    birthday[name] = change_date
    return

def delete():
    name = input("please enter the name you want to delete: ")
    del birthday[name]
    return

while True: 
    User_input = input("please enter the number to the function you want to run: ")
    if User_input == "1":
        print(look_up())
    elif User_input == "2":
        add()
    elif User_input == "3":
        change()
    elif User_input == "4":
        delete()
    elif User_input == "5":
        break

file = open("ex_11.1_birthdays2.csv","a")
for key in birthday:
    record = birthday[key]
    line = (str(key)+","+str(record)+"\n")
file.write(line)
file.close    
