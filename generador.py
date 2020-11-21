def return_cities(*args):
    for i in args:
        yield i

cities = return_cities("Madrid", "Barcelona", "La Paz", "Santa Cruz")

print(next(cities))
