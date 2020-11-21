from turtle import *

def cuadrado(lado):
    for i in range(3):
        forward(lado)
        right(120)

def triangulo(lado):
    for i in range(3):
        forward(lado)
        right(120)

def poligono(lado, n):
    for i in range(n):
        forward(lado)
        right(360 / n)

def poligonos():
    for i in range(3, 11):
        poligono(100, i)

def espiral():
    for i in range(10, 200, 5):
        poligono(i, 3)
        right(10)

espiral()

"""import turtle

window = turtle.Screen()
jimmy = turtle.Turtle()

def triangle(steps):
    grades = [60, 120, 120]

    for grade in grades:
        jimmy.right(grade)
        jimmy.forward(steps)

triangle(210)
"""