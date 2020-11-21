def suma(a, b):
    return a + b

def resta(a, b):
    return a - b

def multiplicacion(a, b):
    return a * b

def division(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        raise("No se puede dividir entre cero")

while True:
    try:
        a = int(input("Introduce el primer numero: "))
        b = int(input("Introduce el segundo numero: "))
        break
    except ValueError:
        print("Los datos son incorrectos, Intentalo denuevo")

opcion = input("Introduce la operacion: ")

if opcion == "suma":
    print(suma(a, b))
elif opcion == "resta":
    print(resta(a, b))
elif opcion == "multiplicacion":
    print(multiplicacion(a, b))
elif opcion == "division":
    print(division(a, b))
else:
    print("Operacion no contemplada")
