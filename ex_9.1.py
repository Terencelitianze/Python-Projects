def convert(value,unit):
    
    if unit == "F":
        value = (value*9/5)+32
        print(value)
    elif unit == "C":
        value = (value*5/9)-32
        print(value)
    else:
        print("invalid unit")
    

convert(103, "C")