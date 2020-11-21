# ---------------------------- Métodos de Cadena ----------------------------
# Capitalize() retorna la primera letra en mayúscula y las demas a minúsculas
cadena_uno = "esta es una cadena de pyTHOn"
print(cadena_uno.capitalize())

# Lower() retorna la cadena en minúsculas
cadena_dos = "UNA CADENA EN MINUSCULA"
print(cadena_dos.lower())

# Upper() retorna la cadena en mayúscula
cadena_tres = "una cadena en mayusculas"
print(cadena_tres.upper())

# Swapcase() retorna las mayusculas en minusculas y viceversa
cadena_cuatro = "hola MUNDO xd"
print(cadena_cuatro.swapcase())

# Title() retorna la cadena en forma de titulo
cadena_cinco = "chapter 3 page 19"
print(cadena_cinco.title())

# Center(n, "") retorna la cadena al centro
cadena_seis = "Wellcome to the Jurasic World"
print(cadena_seis.center(50, "="))

# Ljust(n, "") rjust(n, "") alinea a la izquierda y a la derecha
cadena_siete = "cadena a alinear"
print(cadena_siete.ljust(25, "="))
print(cadena_siete.rjust(25, "="))

# Zfill()
numero = 1509
print(str(numero).zfill(8))

# ------------------------- Métodos de Búsqueda -------------------------
# count("") cuenta las apariciones de esa cadena
cadena = "bienvenido a mi aplicacion"
print(cadena.count("a"))

# find("") busca la subcadena dentro de una cadena 
print(cadena.find("mi"))     # Retorna la posicion en la que encuentra la subcadena
print(cadena.find("virus"))  # Retorna -1 de no encontrar la subcadena
print(cadena.find("mi", 0, 10))

# startwith("") inicia con la cadena
print(cadena.startswith("bienvenido"))
print(cadena.startswith("Wellcome"))

# endwith("") termina con la cadena
print(cadena.endswith("aplicacion"))
print(cadena.endswith("cadena"))

# ------------------------- Métodos de Sustitución -------------------------
# Formatos de cadena
print("Bienvenido a mi programa en {0}".format("Python"))
print("Importe IVA: ${0} + IVA: {1}% = Importe neto {2}".format(100, 21, 121))
print("Importe IVA: ${pesos} + IVA: {iva}% = Importe neto {total}".format(pesos = 100, iva = 21, total = 121))

# Reemplazar la cadena
cadena = "nombre apellido"
nombre_completo = "Juan Perez"

print("Muy buenos dias Sr. nombre apellido".replace(cadena, nombre_completo))

# strip() limpia la cadena al princpio y final
email = "   www.google.com   "
print(email)
print(email.strip())

# ------------------------- Métodos de Sustitucion -------------------------
# Unir una cadena de forma iterativa
formato_factura = ("N° 0000-0", "-0000 (ID: ", ")")
numero = "275"
numero_facura = numero.join(formato_factura)

print(numero_facura)

# Partir una cadena partition("") retorna una tupla
tupla = "https://www.google.com".partition("www.")
print(tupla)

protocolo, separador, dominio = tupla
print("Protocolo: {0}\nDominio: {1}".format(protocolo, dominio))

# Partir una cadena split("") retorna una lista
cadena = "python, guia, tutorial, curso".split(", ")
print(cadena)

# Partir una cadena en varias lineas
cadenas = """ linea1
linea2
linea3
linea4
"""
print(cadenas.splitlines())
