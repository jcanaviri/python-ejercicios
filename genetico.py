import random
import datetime
geneSet = 'abcdefghijklmnñopqrstuvwxyzABCDEFGHIJKLMNÑOPQRSTUVWXYZ '
target = 'Hola Mundo'

random.seed(2)
startTime = datetime.datetime.now()

# Funcion para generar de manera aleatoria una muestra de genes
def generate_parent(length):
    genes = []  # Lista donde se almacenan las secuencia aleatoria
    while len(genes) < length:
        sampleSize = min(length - len(genes), len(geneSet))
        # Obtención de la muestra aleatoria
        genes.extend(random.sample(geneSet, sampleSize))
    return ''.join(genes)  # Regresamos una cadena

# Funcion de optimización, si el nuestra muestra aleatoria tiene un caracter igual a nuestro target
def get_fitness(guess):
    return sum(1 for expected, actual in zip(target, guess) if expected == actual)

# Funcion para mutar a nuestra cadena original o padre
def mutate(parent):
    index = random.randrange(0, len(parent))
    childGenes = list(parent)
    newGene, alternate = random.sample(geneSet, 2)
    childGenes[index] = alternate if newGene == childGenes[index] else newGene
    return ''.join(childGenes)
    
# Funcion para imprimir en pantalla los resultados
def display(guess):
    timeDiff = datetime.datetime.now() - startTime
    fitness = get_fitness(guess)
    print('{}\t{}\t{}'.format(guess, fitness, timeDiff))

# Inicializamos nuestros parametros
bestParent = generate_parent(len(target))
bestFitness = get_fitness(bestParent)
display(bestParent)

# Creamos un ciclo para iterar nuestras funciones
# Hasta obtener nuestro target
while True:
    child = mutate(bestParent)
    childFitness = get_fitness(child)
    if bestFitness >= childFitness:
        continue
    display(child)
    if childFitness >= len(bestParent):
        break
    bestFitness = childFitness
    bestParent = child
