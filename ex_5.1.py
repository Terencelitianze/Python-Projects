Score = int(input("please enter your score: "))


if Score >= 90 and Score <=100:
    Grade = "A"
elif Score >=80 and Score < 90:
    Grade = "B"
elif Score >=70 and Score < 80:
    Grade = "C"
elif Score >=60 and Score < 70:
    Grade = "D"
elif Score >=0 and Score < 60:
    Grade = "F"
else:
    print("please enter a valid value")

print("you got ",Grade," for your exam!")