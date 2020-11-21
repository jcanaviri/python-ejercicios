from collections import namedtuple
import itertools
import random
from tqdm import tqdm
import numpy as np

def _generic_arg(iterable, funcion, mejor_funcion):
    valores = [funcion(x) for x in iterable]
    mejor_valor = mejor_funcion(valores)
    candidatos = [x for x, value in zip(iterable, valores) if value == mejor_valor]
    return random.choice(candidatos)

def argmin(iterable, funcion):
    return _generic_arg(iterable, funcion, min)

def argmax(iterable, funcion):
    return _generic_arg(iterable, funcion, max)

infinito = float('inf')
EstadoJuego = namedtuple('EstadoJuego', 'mover_a, utilidad, tablero, movimientos')

# ______________________________________________________________________________
# Búsqueda MiniMax

def minimax_decision(estado, juego):
    """Dado un estado en el juego, calcule el mejor movimiento buscando 
    hacia adelante hasta los estados terminales."""

    jugador = juego.mover_a(estado)

    def max_valor(estado):
        if juego.prueba_finalizacion(estado):
            return juego.utilidad(estado, jugador)
        v = -infinito
        for a in juego.acciones(estado):
            v = max(v, min_valor(juego.resultado(estado, a)))
        return v

    def min_valor(estado):
        if juego.prueba_finalizacion(estado):
            return juego.utilidad(estado, jugador)
        v = infinito
        for a in juego.acciones(estado):
            v = min(v, max_valor(juego.resultado(estado, a)))
        return v


    # Cuerpo de decision de MiniMax:
    return argmax(juego.acciones(estado), lambda a: min_valor(juego.resultado(estado, a)))

# ______________________________________________________________________________
# Búsqueda AlfaBeta

def busqueda_alfabeta(estado, juego):
    """Busca el juego para determinar la mejor acción; use poda alfa-beta.
    Esta versión busca en todo el camino hasta las hojas."""

    jugador = juego.mover_a(estado)

    # Funciones utilizadas por AlfaBeta
    def max_valor(estado, alfa, beta):
        if juego.prueba_finalizacion(estado):
            return juego.utilidad(estado, jugador)
        v = -infinito
        for a in juego.acciones(estado):
            v = max(v, min_valor(juego.resultado(estado, a), alfa, beta))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v

    def min_valor(estado, alfa, beta):
        if juego.prueba_finalizacion(estado):
            return juego.utilidad(estado, jugador)
        v = infinito
        for a in juego.acciones(estado):
            v = min(v, max_valor(juego.resultado(estado, a), alfa, beta))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return v

    # Cuerpo de busqueda poda alfabeta:
    mejor_puntuacion = -infinito
    beta = infinito
    mejor_accion = None
    for a in juego.acciones(estado):
        v = min_valor(juego.resultado(estado, a), mejor_puntuacion, beta)
        if v > mejor_puntuacion:
            mejor_puntuacion = v
            mejor_accion = a
    return mejor_accion

# ______________________________________________________________________________
# Búsqueda Poda AlfaBeta

def busqueda_poda_alfabeta(estado, juego, d=4, prueba_poda=None, eval_fn=None):
    """Búsqueda de juego para determinar la mejor acción; usa poda alfa-beta.
    Esta versión corta la búsqueda y usa una función de evaluación."""

    jugador = juego.mover_a(estado)

    # Funciones utilizadas por AlfaBeta
    def max_valor(estado, alfa, beta, depth):
        if prueba_poda(estado, depth):
            return eval_fn(estado)
        v = -infinito
        for a in juego.acciones(estado):
            v = max(v, min_valor(juego.resultado(estado, a),
                                 alfa, beta, depth + 1))
            if v >= beta:
                return v
            alfa = max(alfa, v)
        return v

    def min_valor(estado, alfa, beta, depth):
        if prueba_poda(estado, depth):
            return eval_fn(estado)
        v = infinito
        for a in juego.acciones(estado):
            v = min(v, max_valor(juego.resultado(estado, a),
                                 alfa, beta, depth + 1))
            if v <= alfa:
                return v
            beta = min(beta, v)
        return v

    # El cuerpo de búsqueda poda AlfaBeta empieza aqui:
    # La prueba predeterminada poda a una profundidad d o a un estado terminal a
    prueba_poda = (prueba_poda or
                   (lambda estado, depth: depth > d or
                    juego.prueba_finalizacion(estado)))
    eval_fn = eval_fn or (lambda estado: juego.utilidad(estado, jugador))
    mejor_puntuacion = -infinito
    beta = infinito
    mejor_accion = None
    for a in juego.acciones(estado):
        v = min_valor(juego.resultado(estado, a), mejor_puntuacion, beta, 1)
        if v > mejor_puntuacion:
            mejor_puntuacion = v
            mejor_accion = a
    return mejor_accion

# ______________________________________________________________________________
# Clase Juego

class Juego():
    """La clase Juego es similar a la clase problema, pero esta tiene una utilidad para cada
    estay una verificacion de finalizacion en lugar de un costo de camino o alcanzar el objetivo.
    Para crear un juego, se debe crear una clase hija e implementar los metodos acciones,
    resultado, utilidad, and prueba_finalizacion. Puede sobrecarcar la visualización y los sucesores 
    o puede heredar los métodos predeterminados. Es necesario tambien establecer 
    los atributos a su estado inicial en el constructor .inicial."""

    def __init__(self, *args, **kwargs):
        self.numero_jugadores = 2

    def reiniciar(self):
        pass

    def acciones(self, estado):
        """Devuelva una lista de los movimientos permitidos en este punto."""
        raise NotImplementedError

    def resultado(self, estado, jugador_actual_jugada_ejecutada):
        """Devuelve el estado que resulta de hacer un movimiento aplicado a un estado."""
        raise NotImplementedError

    def utilidad(self, estado, jugador):
        """Devuelve el valor del estado final actual al jugador."""
        raise NotImplementedError

    def prueba_finalizacion(self, estado):
        """Devuelve True si el estado actual finaliza el juego."""
        return not self.acciones(estado)

    def mover_a(self, estado):
        """Devuelve el jugado cuyo jugador_actual_jugada_ejecutada se encuentra en este estado."""
        return estado.mover_a

    def mostrar(self, estado):
        """Imprime o muestra el estado."""
        print(estado)

    def __repr__(self):
        return '<{}>'.format(self.__class__.__name__)

    def jugar_torneo(self, partidos, *jugadores, modo="random", verbose=1,
                        barra=None, **kwargs):
        """
        modo -
          "random" - se elige aleatoriamente que empieza primero
          "ordered" - se juega en un orden determinado
          "one-each" - juega cada pareja dos veces, cambiando quién va primero
        verbose -
          0 - sin salidas
          1 - solo barra de estado
          2 - muestra un resumen
          3 - muestra un detalle
        """
        resultados = {"EMPATE": 0}
        for jugador in jugadores:
            resultados[jugador.nombre] = 0
        emparejamientos = [(a[1],b[1]) for (a,b) in
                    itertools.product(enumerate(jugadores), enumerate(jugadores))
                    if a[0] != b[0]]
        necesita_cerrar_barra = True
        if modo == "uno a uno":
            total = len(emparejamientos) * partidos * 2
        else:
            total = len(emparejamientos) * partidos
        if verbose >= 2:
            print("Torneo inicia con %s partidos..." % total)
        elif verbose == 1:
            if barra is None:
                necesita_cerrar_barra = True
                barra = tqdm(total=total)
        for (p1, p2) in emparejamientos:
            if modo == "uno a uno":
                resultado = self.jugar_partidos(partidos, p1, p2, lanzar_moneda=False, verbose=verbose, barra=barra, **kwargs)
                for jugador_nombre in resultado:
                    resultados[jugador_nombre] += resultado[jugador_nombre]
                resultado = self.jugar_partidos(partidos, p2, p1, lanzar_moneda=False, verbose=verbose, barra=barra, **kwargs)
                for jugador_nombre in resultado:
                    resultados[jugador_nombre] += resultado[jugador_nombre]
            else:
                resultado = self.jugar_partidos(partidos, p1, p2, lanzar_moneda=(modo=="random"), verbose=verbose, barra=barra, **kwargs)
                for jugador_nombre in resultado:
                    resultados[jugador_nombre] += resultado[jugador_nombre]
        if necesita_cerrar_barra:
            barra.close()
        return resultados

    def jugar_partidos(self, partidos, *jugadores, lanzar_moneda=True, verbose=1,
                     barra=None, **kwargs):
        if len(jugadores) != self.numero_jugadores:
            raise Exception("Este juego esta limitado a %d jugadores" % self.numero_jugadores)
        resultados = {"EMPATE": 0}
        for jugador in jugadores:
            resultados[jugador.nombre] = 0
        necesita_cerrar_barra = False
        if verbose == 1:
            if barra is None:
                necesita_cerrar_barra = True
                #barra = tqdm(total=partidos)
        for i in range(partidos):
            if verbose == 1:
                barra.update()
            resultado = self.jugar_juego(*jugadores, lanzar_moneda=lanzar_moneda, verbose=verbose, **kwargs)
            for jugador_nombre in resultado:
                resultados[jugador_nombre] += 1
        if necesita_cerrar_barra:
            barra.close()
        return resultados

    def obtener_accion(self, jugador, estado, turno=1, verbose=0, **kwargs):
        """
        Nivel de indirección para anular este método.
        """
        jugador_actual_jugada_ejecutada = jugador.obtener_accion(estado, turno=1, verbose=0, **kwargs)
        return jugador_actual_jugada_ejecutada

    def jugar_juego(self, *jugadores, lanzar_moneda=True, verbose=2, **kwargs):
        """Juega una n-persona, jugador_actual_jugada_ejecutada-alternado el juego."""
        if len(jugadores) == 0:
            raise Exception("Se necesita al menos un jugador")
        self.reiniciar()
        estado = self.inicial
        if lanzar_moneda:
            jugadores = list(jugadores)
            random.shuffle(jugadores)
        for jugador in jugadores:
            jugador_actual_jugada_ejecutada = jugador.establecer_juego(self) ## ejecutar inicializacion, aqui se reinicia
        turno = 1
        while True:
            for jugador in jugadores:
                if verbose >= 2:
                    print("%s esta pensando..." % jugador.nombre)
                jugador_actual_jugada_ejecutada = self.obtener_accion(jugador, estado, turno, verbose, **kwargs)
                estado = self.resultado(estado, jugador_actual_jugada_ejecutada)
                if verbose >= 2:
                    print("%s ejecuta la acción %s:" % (jugador.nombre, jugador_actual_jugada_ejecutada))
                    self.mostrar(estado)
                if self.prueba_finalizacion(estado):
                    resultado = self.utilidad(estado, self.mover_a(self.inicial))
                    self.utilidad_final = resultado
                    self.estado_final = estado
                    if resultado == 1:
                        retval = [jugadores[0].nombre]
                    elif resultado == -1:
                        retval = [p.nombre for p in jugadores[1:]]
                    elif resultado == 0:
                        retval = ["EMPATE"]
                    else:
                        retval = ["Resultado %s" % resultado]
                    if verbose >= 2:
                        print("***** %s Gana!" % ",".join(retval))
                    return retval
            turno += 1

# ______________________________________________________________________________
# Clase para el juego 3 en raya(TicTacToe)

class TicTacToe(Juego):
    """
    Juega a TicTacToe en un tablero h x v, con Max (primer jugador) jugando con 'X'.
    Un estado tiene un jugador para mover, una utilidad en caché, una lista de movimientos 
    en forma de una lista de posiciones (x, y) y un tablero, 
    en forma de un dict de {(x, y): Jugador} entradas, donde Jugador es 'X' o 'O'.
    """
    #se modifico H=5, v= 5,  k= 2 que corresponden al ejercicio 5x5 y k = al valor que se tiene que conseguir para ganar
    def __init__(self, h=5, v=5, k=3, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.h = h
        self.v = v
        self.k = k
        movimientos = [(x, y) for x in range(1, self.h + 1) for y in range(1, self.v + 1)]
        self.inicial = EstadoJuego(mover_a='S', utilidad=0, tablero={}, movimientos=movimientos)

    def acciones(self, estado):
        """los movimientos legales son aquellos que se puedan tomar 
        de los cuadrados que aun no han sido tomados."""
        return estado.movimientos

    def resultado(self, estado, jugador_actual_jugada_ejecutada):
        if jugador_actual_jugada_ejecutada not in estado.movimientos:
            return estado  # Movimientos ilegales no tienen efecto
        tablero = estado.tablero.copy()
        tablero[jugador_actual_jugada_ejecutada] = estado.mover_a
        movimientos = list(estado.movimientos)
        movimientos.remove(jugador_actual_jugada_ejecutada)
        return EstadoJuego(mover_a=('O' if estado.mover_a == 'S' else 'S'),
                         utilidad=self.calcular_utilidad(tablero, jugador_actual_jugada_ejecutada, estado.mover_a),
                         tablero=tablero, movimientos=movimientos)

    def utilidad(self, estado, jugador):
        """Devuelve para el jugador actual; 1 si gana, -1 si pierde, 0 en cualquier otra situacion."""
        return estado.utilidad if jugador == 'X' else -estado.utilidad

    def prueba_finalizacion(self, estado):
        """A estado is terminal if it is won or there are no empty squares."""
        return estado.utilidad != 0 or len(estado.movimientos) == 0

    def mostrar(self, estado):
        tablero = estado.tablero
        for y in range(self.v, 0, -1):
            for x in range(1, self.h + 1):
                print(tablero.get((x, y), '.'), end=' ')
            print()

    def calcular_utilidad(self, tablero, jugador_actual_jugada_ejecutada, jugador):
        """Si 'X' gana con este movimiento, devuelve 1; si 'O' gana, devuelve -1; de lo contrario, devuelve 0."""
        if (self.k_en_fila(tablero, jugador_actual_jugada_ejecutada, jugador, (0, 1)) or
                self.k_en_fila(tablero, jugador_actual_jugada_ejecutada, jugador, (1, 0)) or
                self.k_en_fila(tablero, jugador_actual_jugada_ejecutada, jugador, (1, -1)) or
                self.k_en_fila(tablero, jugador_actual_jugada_ejecutada, jugador, (1, 1))):
            return +1 if jugador == 'X' else -1
        else:
            return 0

    def k_en_fila(self, tablero, jugador_actual_jugada_ejecutada, jugador, delta_x_y):
        """Devuelve verdadero si hay una línea gracias al movimiento en el tablero para el jugador.."""
        (delta_x, delta_y) = delta_x_y
        x, y = jugador_actual_jugada_ejecutada
        n = 0  # n es el numero de movimientos en la fila
        while tablero.get((x, y)) == jugador:
            n += 1
            x, y = x + delta_x, y + delta_y
        x, y = jugador_actual_jugada_ejecutada
        while tablero.get((x, y)) == jugador:
            n += 1
            x, y = x - delta_x, y - delta_y
        n -= 1  # Porque contamos jugador_actual_jugada_ejecutada dos veces
        return n >= self.k

    def string_a_estado(self, string, mover_a):
        string = string.strip()
        tablero = {}
        y = self.v
        x = 1
        for s in range(len(string)):
            if string[s] in [" ", "\n", "\t"]: continue
            char = string[s]
            pos = (x,y)
            if char == ".":
                pass
            else:
                tablero[pos] = char
            x += 1
            if (x - 1) % self.h == 0:
                x = 1
                y -= 1
        movimientos = self.inicial.movimientos[:]
        for key in tablero:
            movimientos.remove(key)
        return EstadoJuego(tablero=tablero, mover_a=mover_a, utilidad=0, movimientos=movimientos)

class ConectaCuatro(TicTacToe):
    """Juego parecido a TicTacToe. 
    Tradicionalmente se los juega sobre un tablero de 7x6 y requiere marcar 4 elementos en una fila."""

    def __init__(self, h=5, v=5, k=3, *args, **kwargs):
        TicTacToe.__init__(self, h, v, k, *args, **kwargs)

    def acciones(self, estado):
        return [(x, y) for (x, y) in estado.movimientos
                if y == 1 or (x, y - 1) in estado.tablero]

# ______________________________________________________________________________
# Clase Jugadores para los juegos

class Jugador():
    """
    """
    CONTAR = 0
    def __init__(self, nombre=None):
        if nombre is None:
            nombre = "%s-%s" % (self.__class__.__name__, self.__class__.CONTAR)
            self.__class__.CONTAR += 1
        self.nombre = nombre

    def establecer_juego(self, juego):
        ## iniciar o restablecer negocios aquí en sobrecarga
        self.juego = juego

    def obtener_accion(self, estado, turno=1, verbose=0):
        raise NotImplementedError()

class JugadorHumano(Jugador):
    """
    """
    CONTAR = 0
    def obtener_accion(self, estado, turno=1, verbose=0):
        """Realizar un movimiento consultando la entrada estándar.."""
        print("Estado actual:")
        self.juego.mostrar(estado)
        print("Movimientos disponibles: {}".format(self.juego.acciones(estado)))
        print("")
        move_string = input('El jugador que mueve? ')
        try:
            jugador_actual_jugada_ejecutada = eval(move_string)
        except NameError:
            jugador_actual_jugada_ejecutada = move_string
        return jugador_actual_jugada_ejecutada

class JugadorAleatorio(Jugador):
    CONTAR = 0
    def obtener_accion(self, estado, turno=1, verbose=0):
        """Un jugador que elige un movimiento permitido aleatoriamente."""
        print("Turno Aleatorio")
        ramdo = random.choice(self.juego.acciones(estado))
        print(ramdo)
        return ramdo

class JugadorAlfaBeta(Jugador):
    CONTAR = 0
    def obtener_accion(self, estado, turno=1, verbose=0):
        return busqueda_alfabeta(estado, self.juego)

class JugadorMiniMax(Jugador):
    CONTAR = 0
    def obtener_accion(self, estado, turno=1, verbose=0):
        print("Turno de Minimax")
        mini = minimax_decision(estado, self.juego)
        print(mini)
        return mini

class JugadorPodaAlfaBeta(Jugador):
    CONTAR = 0
    def obtener_accion(self, estado, turno=1, verbose=0):
        return busqueda_poda_alfabeta(estado, self.juego, d=4,
                                       prueba_poda=None, eval_fn=None)

jugadores = [
    JugadorHumano(),
    #JugadorAleatorio(),
    #JugadorAlfaBeta(),
    #JugadorMiniMax()]
    JugadorPodaAlfaBeta()]
    #]

juego = TicTacToe()
juego.jugar_torneo(1, *jugadores, verbose=0)

