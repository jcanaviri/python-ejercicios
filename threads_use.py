import threading

def imprime(num):
    print("Soy el hilo", num)
print("Soy el hilo principal")

for i in range(0, 10):
    t = threading.Thread(target=imprime, args=(i, ))
    t.start()
