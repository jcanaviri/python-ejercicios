def mi_decorador(funcion):
    def nueva_funcion(*args):
        print(f'Llamada a la funcion {funcion.__name__}')
        retorno = funcion(*args)
        return retorno

    return nueva_funcion

@mi_decorador
def imp(cadena):
    print(cadena)

imp("Hola Mundo")
