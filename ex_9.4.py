def unique_list(my_list):
    Unique_list = []
    for item in my_list:
        if item not in Unique_list:
            Unique_list.append(item)
    return Unique_list

my_list = [1,2,2,2,2,3,3,3,3,4,4,4,4,4]
print(unique_list(my_list))