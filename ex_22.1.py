import matplotlib.pyplot as plt

x = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20]
y1 = []
y2 = []
y3 = []
for i in x:
    y1.append(i)
for i in x:
    num = i**2
    y2.append(num)
for i in x:
    num = 400 - i**2
    y3.append(num)

#plt.plot(x,y1,color = "r", label = "y1 = x")
#plt.plot(x,y2, color = "g", label = "y2 = x^2")
#plt.plot(x,y3, color = "m", label = "y3 = 400 - x^2")

plt.bar(x,y2, 1, color = "g", label = "y2 = x^2")
plt.bar(x,y3, 1, color = "m", label = "y3 = 400 - x^2")
plt.bar(x,y1, 1, color = "r", label = "y1 = x")

plt.xlabel("x")
plt.ylabel("y")
plt.legend()
plt.xlim(0,20)
plt.ylim(0.400)
plt.title("Functions")
plt.show()
