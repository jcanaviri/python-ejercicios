"""Documentacion del modulo
Esta es una antacion la cual debe de encontrarse
en la parte superior de nuestro script
Esta anotacion tiene como objetivo describir el modulo"""

__author__ = "Yo"
__copyright__ = "Copyright 2020"
__credits__ = ["Me", "You", "he"]
__license__ = "GPL"
__version__ = "0.0.1"
__maintainer__ = "Team Capitan America"
__email__ = "vengadoresUnidos@gmail.com"
__status__ = "Production"


CONSTANT = "I'm a constant"

full_name = "Josue Canaviri"

print(CONSTANT)

lista = [1, 2, 3, 4, 5]
resultado = list(map(lambda n : n * n, lista))

print(resultado)

# Decoradores
def decorador(funcion):
    def nueva_funcion():
        print("Esto pasa antes")
        funcion()
        print("Esto pasa despues")
    
    return nueva_funcion

@decorador
def funcion_a_decorar():
    print("Esta funcion se decorara")

funcion_a_decorar()

print(__name__)

# Si este archivo es el principal
if __name__ == '__main__':
    pass