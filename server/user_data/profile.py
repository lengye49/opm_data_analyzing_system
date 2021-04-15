class Unit:

    def __init__(self, name='nobody', gen='male', strength=0, atk=100):
        print('init user')
        self.name = name
        self.gender = gen
        self.strength = strength
        self.atk = atk

    def fight(self, cost):
        self.strength -= cost
        if self.strength <= 0:
            print(self.name + ' is dead');
            self.strength = 0
            return 0
        return 1

a = Unit('a','male',10000,100)
b = Unit('b','male',8000,125)

round = 1
while True:
    print('Round ' + str(round))
    r = b.fight(a.atk)
    if r == 0:
        print('a win!')
        break

    r = a.fight(b.atk)
    if r == 0:
        print('b win!')
        break

    round += 1
