class MiError(Exception):
    """La clase de error"""
    def __init__(self, valor):
        self.valor = valor

    def __str__(self):
        return f'Error {self.valor}'

r = 120

try:
    if r > 20:
        raise MiError(33)

except MiError as e:
    print(e)
