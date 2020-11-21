while True:
    usuario = input("\nIntroduzca el nombre de usuario: ")
    caracteres = len(usuario)
    if caracteres > 6 and caracteres < 12:
        if usuario.isalnum():
            print("True")
            break
        else:
            print("El nombre de usuario puede contener solo letras y números")
    elif caracteres < 6:
        print("El nombre de usuario debe contener al menos 6 caracteres")
    else:
        print("El nombre de usuario no puede contener más de 12 caracteres")
