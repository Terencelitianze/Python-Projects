my_string = input("please enter a string: ")

my_dict = {}

def char_frequencies(my_string):
    for i in my_string:
        if i not in my_dict:
            my_dict[i] = my_string.count(i)
    return my_dict
    
print(char_frequencies(my_string))

