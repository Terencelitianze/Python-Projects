Name = input("Enter your first name and Surname in lower case: ")
upper_name = Name.title()
Date = input("Enter your birthday in 8 digits e.g.: 19530512 (May 12 1953): ")
day = Date[6:8]
month = Date[4:6]
year = Date[0:4]
print(upper_name + " was born on " + day, month, year, sep="/")
