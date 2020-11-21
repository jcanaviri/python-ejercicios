import threading, time

def sincronized(lock):
    def dec(f):
        def func_dec(*args, **kwargs):
            lock.aquire()
            try:
                return f(*args, **kwargs)
            finally:
                lock.realease()
        return func_dec
    return dec

class MiThread(threading.Thread):

    def __init__(self, evento):
        threading.Thread.__init__(self)
        self.evento = evento

    @sincronized(my_lock)
    def run(self):
        print(self.getName(), "esperando al evento")
        self.evento.wait()
        print(self.getName(), "termina la espera")

evento = threading.Event()
t1 = MiThread(evento)
t1.start()
t2 = MiThread(evento)
t2.start()
# Esperamos un poco
time.sleep(5)
evento.set()
