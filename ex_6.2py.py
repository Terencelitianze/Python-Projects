alphabet = []
rot13 = []

for n in range(97,123):
    character = chr(n)
    m = n+13
    if m > 122:
        m = m - 26
    character2 = chr(m)
    alphabet.append(character)
    rot13.append(character2)

print(alphabet)
print(rot13)

message = "lbh zhfg unir fbzr jvyq vzntvangvba. gvzr geniry? frevbhfyl!!! arire zvaq, yrgf gnxr n oernx abj. ohg ubyq ba, bar zber guvat. lbhe svefg ubzrjbex nffvtazrag jvyy or eryrnfrq gbqnl ba oevtugfcnpr. vg vf rapelcgrq jvgu ebg13. :)"

new_message = ""

for n in message:
    Answer = ord(n) +13
    if Answer == 32+13:
        Answer = 32
    elif Answer >=122:
        Answer = Answer - 26
    elif Answer >=48+13 and Answer <= 57+13:
        Answer = Answer - 13
    new_message += chr(Answer)
[]
print(new_message)

