from functools import reduce

items = [1, 2, 3, 4, 5, 6, 7, 8, 9]

five_mult = map(lambda x: x * 5, items)
five_mult = list(five_mult)
print(five_mult)

evens = filter(lambda x: x % 2 == 0, items)
evens = list(evens)
print(evens)

total = reduce(lambda a, b: a + b, items)
print(total)
