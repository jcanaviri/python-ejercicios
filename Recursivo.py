def jugar(intento = 1):
    respuesta = input("¿De que color es una naranja?: ")
    if respuesta.lower() != "naranja":
        if intento < 3:
            print("Fallaste :(")
            intento += 1
            jugar(intento)
        else:
            print("Ya perdite :(")
    else:
        print("Ganaste :)")

jugar()