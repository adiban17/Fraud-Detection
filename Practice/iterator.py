'''
Iterator :-
An object that returns elements one at a time from a sequence (or data stream)
and remebers its position between calls.
A Python object is an iterator if it has:
__iter__() -> Returns the iterator object itself
__next__() -> Returns the next item in the sequence (raises stopIteration when no more items)

'''

class Dice:

    def __init__(self, rolls):
        self.rolls = rolls
        self.count = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.count < self.rolls:
            self.count += 1
            return random.randint(1, 6)
        else:
            raise StopIteration


import random

dice = Dice(3)

for die in dice:
    print(die)

dice = [die for die in Dice(4)]
print(dice)