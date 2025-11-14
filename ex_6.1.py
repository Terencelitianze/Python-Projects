for n in range(1,101):
    if n%3 == 0 and n%5 == 0:
        print("FIZZ BUZZ")
    elif n%3 == 0 :
        print("FIZZ")
    elif n%5 == 0 :
        print("BUZZ")
    else:
        print(n)
