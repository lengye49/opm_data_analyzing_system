import random


test_count = 1000000
hero_count = 0
last_hero = 0

for i in range(0, test_count):
    if last_hero >= 79:
        hero_count += 1
        last_hero = 0
        continue

    r = random.randint(0,10000)
    if r < 130:
        hero_count += 1
        last_hero = 0
    else:
        last_hero += 1

print(hero_count)
print(hero_count/test_count)
print(1/80)
