import random

set_count = 4
equip_count = 3


total = 0
count = 0
test_count = 1000000

for i in range(0,test_count):

    e1 = False
    count = 0

    while not e1:
        count = count + 1
        r = random.randint(0, 4000)
        if r< 1000:
            e1 = True


    # print(count)
    total += count

print(total/test_count)
print(total/test_count * 3)