student_grades = [["John",'9','10','7','6'],['Mary','9','8','8'],['Smith','8','4'],['Adam','6','4','7','5','10']]
total = 0
counter = 0
for student in student_grades:
    sum = 0
    for grade in student[1:]:    
        sum = sum + int(grade)
        total = total +int(grade)
        counter = counter + 1
    print(student[0]+"'s average is",sum/len(student[1:]))
print("the class average is",total/counter)

