# Primer Parcial Grupo 13 Jueves turno mañana
# Baranczuk Thiago 1191201
# Lucas Damian Maturano 1184850
# Santiago diego otta mendez 1151647
# Valentino perez lingua 1190848

import random

def generarId(usuarios):
    while True:
        usuarioId = random.randint(100, 999)
        idUnico = True
        for usuario in usuarios:
            if usuario['ID'] == usuarioId:
                idUnico = False
                break
        if idUnico:
            return usuarioId

def añadir(elemento, lista, datos, generos=None):
    if elemento == "género":
        nuevoId = max(lista.keys()) + 1 if lista else 1
        lista[nuevoId] = datos
        print(f"Género '{datos}' añadido con ID {nuevoId}.")
    elif elemento == "libro":
        sku = int(datos[0])
        for libro in lista:
            if libro[0] == sku:
                print(f"Error: El libro con SKU '{sku}' ya existe.")
                return
        if datos[3] not in generos.values():
            print(f"Error: El género '{datos[3]}' no existe.")
            return
        libro = [sku, datos[1], datos[2], datos[3], datos[4]]
        lista.append(libro)
        print(f"Libro '{datos[1]}' añadido con SKU {sku}.")
    elif elemento == "usuario":
        if not datos[0].isalpha() or not datos[1].isalpha():
            print("Error: El nombre y apellido deben ser una cadena de caracteres.")
            return
        usuarioId = generarId(lista)
        usuario = {'ID': usuarioId, 'Nombre': datos[0], 'Apellido': datos[1]}
        lista.append(usuario)
        print(f"Usuario '{datos[0]} {datos[1]}' registrado con ID '{usuarioId}'.")

def eliminar(elemento, lista, id):
    if elemento == "género":
        id = int(id)
        if id in lista:
            eliminado = lista.pop(id)
            print(f"Género '{eliminado}' eliminado.")
        else:
            print(f"El género con ID '{id}' no existe.")
    elif elemento == "libro":
        sku = int(id)
        libroEncontrado = False
        for libro in lista[:]:
            if libro[0] == sku:
                lista.remove(libro)
                print(f"Libro con SKU '{sku}' eliminado.")
                libroEncontrado = True
                break
        if libroEncontrado == False:
            print(f"El libro con SKU '{sku}' no existe.")
    elif elemento == "usuario":
        id = int(id)
        usuarioEncontrado = False
        for usuario in lista[:]:
            if usuario['ID'] == id:
                lista.remove(usuario)
                print(f"Usuario con ID '{id}' eliminado.")
                usuarioEncontrado = True
                break
        if usuarioEncontrado == False:
            print(f"El ID '{id}' no existe.")

def ver(elemento, lista):
    if lista == "":
        print(f"No hay {elemento}s registrados.")
        return
    print(f"Lista de {elemento}s:")
    if elemento == "género":
        for idGenero, nombre in lista.items():
            print(f"- ID: {idGenero}, Nombre: {nombre}")
    elif elemento == "libro":
        for libro in lista:
            print(f"- SKU: {libro[0]}, Título: {libro[1]}, Autor: {libro[2]}, Género: {libro[3]}, Stock: {libro[4]}")
    elif elemento == "usuario":
        for usuario in lista:
            print(f"- ID: {usuario['ID']}, Nombre: {usuario['Nombre']}, Apellido: {usuario['Apellido']}")

def prestarLibro(usuarios, libros, prestamos):
    ver("usuario", usuarios)
    usuarioId = int(input("Ingresá el ID del usuario o -1 para volver: "))
    if usuarioId == -1:
        return
    else:
        ver("libro", libros)
        skuLibro = int(input("Ingresá el SKU del libro a prestar o -1 para volver: "))
        if skuLibro == -1:
            return
        else:
            usuario = None
            for u in usuarios:
                if u['ID'] == usuarioId:
                    usuario = u
                    break
            if usuario == None:
                print(f"Usuario con ID '{usuarioId}' no existe.")
                return
            libro = None
            for l in libros:
                if l[0] == skuLibro:
                    libro = l
                    break
            if libro == None:
                print(f"El libro con SKU '{skuLibro}' no existe.")
                return
            if libro[4] <= 0:  # Comprobar stock
                print(f"El libro con SKU '{skuLibro}' no está disponible para préstamo.")
                return

            prestamos.append({'IdUsuario': usuarioId, 'SKULibro': skuLibro})
            libro[4] -= 1  # Reducir stock
            print(f"Libro con SKU '{skuLibro}' prestado al usuario '{usuario['Nombre']} {usuario['Apellido']}'.")

def devolverLibro(usuarios, libros, prestamos):
    ver("usuario", usuarios)
    usuarioId = int(input("Ingresá el ID del usuario o -1 para volver: "))
    if usuarioId == -1:
        return
    else:
        ver("libro", libros)
        skuLibro = int(input("Ingresá el SKU del libro a prestar o -1 para volver: "))
        if skuLibro == -1:
            return
        else:
            usuario = None
            for u in usuarios:
                if u['ID'] == usuarioId:
                    usuario = u
                    break
            if usuario == None:
                print(f"Usuario con ID '{usuarioId}' no existe.")
                return

            prestamo = None
            for p in prestamos:
                if p['IdUsuario'] == usuarioId and p['SKULibro'] == skuLibro:
                    prestamo = p
                    break
            if prestamo == None:
                print(f"No se encontró registro de que el usuario '{usuarioId}' sacó un préstamo del libro '{skuLibro}'.")
                return

            libro = None
            for l in libros:
                if l[0] == skuLibro:
                    libro = l
                    break
            if libro != None:
                libro[4] += 1  # Incrementar stock al devolver

            prestamos.remove(prestamo)
            print(f"Libro con SKU '{skuLibro}' devuelto por el usuario '{usuario['Nombre']} {usuario['Apellido']}'.")

def menuAñadir(generos, libros, usuarios):
    while True:
        print("\nAñadir:")
        print("1. Añadir género")
        print("2. Añadir libro")
        print("3. Añadir usuario")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            genero = input("Ingresá el nombre del género a añadir o enter para salir: ")
            if genero == '':
                break
            else:
                añadir("género", generos, genero)
        elif opcion == '2':
            sku = input("Ingresá el SKU del libro o enter para salir: ")
            if sku == '':
                break
            else:
                titulo = input("Ingresá el título del libro o enter para salir: ")
                if titulo == '':
                    break
                else:
                    autor = input("Ingresá el autor del libro o enter para salir: ")
                    if autor == '':
                        break
                    else:
                        genero = input("Ingresá el género del libro o enter para salir: ")
                        if genero == '':
                            break
                        else:
                            stock = int(input("Ingresá la cantidad en stock o enter para salir: "))
                            if stock == '':
                                break
                            else:
                                añadir("libro", libros, (sku, titulo, autor, genero, stock), generos)
        elif opcion == '3':
            nombre = input("Ingresá su nombre o enter para salir: ")
            if nombre == '':
                break
            else:
                apellido = input("Ingresá su apellido o enter para salir: ")
                if apellido == '':
                    break
                else:
                    añadir("usuario", usuarios, (nombre, apellido))
        elif opcion == '4':
            break
        else:
            print("Opción no válida, intentá de nuevo.")

def menuEliminar(generos, libros, usuarios):
    while True:
        print("\nEliminar:")
        print("1. Eliminar género")
        print("2. Eliminar libro")
        print("3. Eliminar usuario")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            ver("género", generos)  # Mostrar lista de géneros
            idGenero = input("Ingresá el ID del género a eliminar o enter para voler atras: ")
            if idGenero == '':
                break
            else:
                eliminar("género", generos, idGenero)
        elif opcion == '2':
            ver("libro", libros)  # Mostrar lista de libros
            sku = input("Ingresá el SKU del libro a eliminar o enter para volver atras: ")
            if sku == '':
                break
            else:
                eliminar("libro", libros, sku)
        elif opcion == '3':
            ver("usuario", usuarios)  # Mostrar lista de usuarios
            idUsuario = input("Ingresá el ID del usuario a eliminar o enter para volver atras: ")
            if idUsuario == '':
                break
            else:
                eliminar("usuario", usuarios, idUsuario)
        elif opcion == '4':
            break
        else:
            print("Opción no válida, intentá de nuevo.")

def menuVer(generos, libros, usuarios):
    while True:
        print("\nVer:")
        print("1. Ver géneros")
        print("2. Ver libros")
        print("3. Ver usuarios")
        print("4. Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            ver("género", generos)
        elif opcion == '2':
            ver("libro", libros)
        elif opcion == '3':
            ver("usuario", usuarios)
        elif opcion == '4':
            break
        else:
            print("Opción no válida, intentá de nuevo.")

def menuPrestamos(usuarios, libros, prestamos):
    while True:
        print("\nPréstamos:")
        print("1. Prestar libro")
        print("2. Devolver libro")
        print("3. Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            prestarLibro(usuarios, libros, prestamos)
        elif opcion == '2':
            devolverLibro(usuarios, libros, prestamos)
        elif opcion == '3':
            break
        else:
            print("Opción no válida, intentá de nuevo.")

def main():
    usuarios = []
    libros = [
        [1,'Duna','Frank Herbert','Ciencia Ficción',3],
        [2,'Neuromante','William Gibson','Ciencia Ficción',2],
        [3,'La comunidad del anillo','J.R.R. Tolkien','Fantasía',4],
        [4,'El nombre del viento','Patrick Rothfuss','Fantasía',6],
        [5,'La chica del tren','Paula Hawkins','Misterio',6],
        [6,'El asesinato de Roger Ackroyd','Agatha Christie','Misterio',1]
    ]
    generos = {1: 'Ciencia Ficción', 2: 'Fantasía', 3: 'Misterio'}
    prestamos = []
# MEJORAR MENU reducido el menu Y EL INTERFACE
#AGREGAR UNA TECLA PARA VOLVER AL MENU hecho
#FILTRAR POR GENERO/AUTOR/PARTE DEL TITULO
#MANEJAR UN STOCK creo q listo
##HACER RESERVAS DE UN LIBRO
###PERIODO DE PRESTAMO/SANCION O PENALIDAD
#### TITULOS VENCIDOS Y NO DEVUELTOS
#USAR MODULO DATE TIME
#
    while True:
        print("\nOpciones:")
        print("1. Añadir")
        print("2. Eliminar")
        print("3. Ver")
        print("4. Préstamos")
        print("5. Salir")

        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            menuAñadir(generos, libros, usuarios)
        elif opcion == '2':
            menuEliminar(generos, libros, usuarios)
        elif opcion == '3':
            menuVer(generos, libros, usuarios)
        elif opcion == '4':
            menuPrestamos(usuarios, libros, prestamos)
        elif opcion == '5':
            print("Saliste del programa!")
            break
        else:
            print("Opción no válida, intentá de nuevo.")

if __name__ == "__main__":
    main()