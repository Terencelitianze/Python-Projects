import matplotlib.pyplot as plt

sales = {}

in_file = open("ex_22.2_SalesJan2009.csv","r")

in_file.readline()

for line in in_file:
    line_list = line.strip().split(',')
    if line_list[7] in sales:
        sales[line_list[7]] = sales[line_list[7]] +int(line_list[2])
    else:
        sales[line_list[7]] = int(line_list[2])

print(sales)

in_file.close()

y = list(sales.values())
x = []
y.sort(reverse = True)

def find_value_in_dict(val,x):
    for key in sales:
        if sales[key] == val and key not in x:
            return key
        return None

for value in y:
    country = find_value_in_dict(value,x)
    x.append(country)

print(y)
print(x)

plt.bar(x, y)
plt.xlabel("Countries")
plt.ylabel("Sales")
plt.title("Sales by Country in January 2009")
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better readability
plt.tight_layout()
plt.show()