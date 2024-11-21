# Primer Parcial Grupo 13 Jueves turno mañana
# Baranczuk Thiago 1191201
# Lucas Damian Maturano 1184850
# Santiago diego otta mendez 1151647
# Valentino perez lingua 1190848

import random, datetime

def generarId(usuarios):
    continuar = True
    while continuar:
        usuarioId = random.randint(100, 999)
        idUnico = True
        for usuario in usuarios:
            if usuario['ID'] == usuarioId:
                idUnico = False
                continuar=False
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
                print(f"❌ Error: El libro con SKU '{sku}' ya existe.")
                return
        if datos[3] not in generos.values():
            print(f"❌ Error: El género '{datos[3]}' no existe.")
            return
        libro = [sku, datos[1], datos[2], datos[3], datos[4]]
        lista.append(libro)
        print(f"Libro '{datos[1]}' añadido con SKU {sku}.")
    elif elemento == "usuario":   
        valido_nombre = datos[0].isalpha() and datos[1].isalpha()  
        if valido_nombre:
            usuarioId = generarId(lista)
            usuario = {'ID': usuarioId, 'Nombre': datos[0], 'Apellido': datos[1], 'DNI': datos[2]}
            lista.append(usuario)
            print(f"Usuario '{datos[0]} {datos[1]}' registrado con ID '{usuarioId}'.")            
            try:
                arch=open("usuarios.txt", "a")
                arch.write(f"{usuarioId};{datos[0]} {datos[1]};{datos[2]}\n")
            except FileNotFoundError as mensaje:
                print("Error al abrir el archivo:", mensaje)
            except OSError as mensaje:
                print("Otro error al manejar el archivo:", mensaje)
        else:
            print("❌ Error: El nombre y apellido deben ser una cadena de caracteres.")


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
    if not lista:
        print(f"No hay {elemento}s registrados.")
        return
    
    print(f"\n{'═'*10} Lista de {elemento}s {'═'*10}")
    if elemento == "género":
        print("─" * 50)
        for idGenero, nombre in lista.items():
            print(f"ID: {idGenero} | Nombre: {nombre}")
            print("─" * 50)
    elif elemento == "libro":
        print("─" * 110)
        for libro in lista:
            print(f"SKU: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Stock: {libro[4]}")
            print("─" * 110)
    elif elemento == "usuario":
        filtro = input("Ingresa el DNI para buscar: ").strip()  
        print("─" * 50)
        encontrado = False
        for usuario in lista:
            if filtro in str(usuario['DNI']):
                print(f"ID: {usuario['ID']} | Nombre: {usuario['Nombre']} | Apellido: {usuario['Apellido']} | DNI: {usuario['DNI']}")
                print("─" * 50)
                encontrado = True
        if not encontrado:
            print("❌ No se encontró ningún usuario con ese DNI.")
    elif elemento == "prestamos":
        print("─" * 80)
        encontrado = False
        for prestamo in lista:
            print(f"ID Préstamo: {prestamo['ID']} | Libro: {prestamo['Libro']} | Usuario: {prestamo['Usuario']} | Fecha de Préstamo: {prestamo['Fecha']} | Fecha de Devolución: {prestamo['FechaDevolucion']}")
            print("─" * 80)
            encontrado = True
        if not encontrado:
            print("❌ No se encontraron préstamos.")

def cargarUsuarios():
    usuarios = []
    try:
        arch = open("usuarios.txt", "rt")
        linea = arch.readline()
        while linea:
            usuarioId, nombre_apellido, dni = linea.split(';')
            nombre, apellido = nombre_apellido.split()
            usuarios.append({'ID': int(usuarioId), 'Nombre': nombre, 'Apellido': apellido, 'DNI': int(dni)})
            linea = arch.readline()
    except FileNotFoundError as mensaje:
        print("No se encontró el archivo de usuarios.", mensaje)
    except OSError as mensaje:
        print("Error al abrir el archivo de usuarios:", mensaje)
    finally:
        try:
            arch.close()
        except NameError:
            pass
    return usuarios

def prestarLibro(usuarios, libros, prestamos):
    ver("usuario", usuarios)
    usuarioId = int(input("Ingresá el ID del usuario o -1 para volver: "))
    if usuarioId == -1:
        return
    else:
        resultados = buscarLibro(libros)
        if resultados != []:
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
                if libro[4] <= 0:  # Verifica disponibilidad
                    print(f"El libro con SKU '{skuLibro}' no está disponible para préstamo.")
                    return

                fechaPrestamo = datetime.datetime.now()
                # Calcula la fecha de devolución: 14 días después de la fecha de préstamo
                fechaDevolucion = fechaPrestamo + datetime.timedelta(days=14)

                prestamos.append({
                    'ID': len(prestamos) + 1,
                    'Libro': libro[1],  # Nombre del libro
                    'Usuario': usuario['Nombre'] + ' ' + usuario['Apellido'],  # Nombre completo del usuario
                    'Fecha': fechaPrestamo.strftime('%d/%m/%Y'),  # Fecha de préstamo
                    'FechaDevolucion': fechaDevolucion.strftime('%d/%m/%Y')  # Fecha límite de devolución
                })
                libro[4] -= 1  # Decrementa el stock del libro
                print(f"Libro con SKU '{skuLibro}' prestado al usuario '{usuario['Nombre']} {usuario['Apellido']}' hasta {fechaDevolucion.strftime('%d/%m/%Y')}.")

                
def devolverLibro(usuarios, libros, prestamos):
    ver("usuario", usuarios)
    usuarioId = int(input("Ingresá el ID del usuario o -1 para volver: "))
    if usuarioId == -1:
        return
    else:
        ver("libro", libros)
        skuLibro = int(input("Ingresá el SKU del libro a devolver o -1 para volver: "))
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
                libro[4] += 1 

            fechaDevolucionReal = datetime.datetime.now()
            if fechaDevolucionReal > prestamo['FechaDevolucion']:
                diasRetraso = (fechaDevolucionReal - prestamo['FechaDevolucion']).days
                print(f"❌ El libro se devolvió con {diasRetraso} días de retraso. Penalización aplicada.")
            prestamos.remove(prestamo)
            print(f"Libro con SKU '{skuLibro}' devuelto por el usuario '{usuario['Nombre']} {usuario['Apellido']}'.")



def menuAñadir(generos, libros, usuarios):
    continuar = True
    while continuar:
        print()
        print("═"*40)
        print("Menú Añadir".center(40))
        print("═"*40)
        print("1. 📂 Añadir género")
        print("2. 📚 Añadir libro")
        print("3. 👤 Añadir usuario")
        print("4. 🔙 Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            genero = input("Ingresá el nombre del género a añadir o enter para salir: ")
            if genero == '':
                continuar = False
            else:
                añadir("género", generos, genero)
        elif opcion == '2':
            sku = input("Ingresá el SKU del libro o enter para salir: ")
            if sku == '':
                continuar = False
            else:
                titulo = input("Ingresá el título del libro o enter para salir: ")
                if titulo == '':
                    continuar = False
                else:
                    autor = input("Ingresá el autor del libro o enter para salir: ")
                    if autor == '':
                        continuar = False
                    else:
                        genero = input("Ingresá el género del libro o enter para salir: ")
                        if genero == '':
                            continuar = False
                        else:
                            stock = int(input("Ingresá la cantidad en stock o enter para salir: "))
                            if stock == '':
                                continuar = False
                            else:
                                añadir("libro", libros, (sku, titulo, autor, genero, stock, generos))
        elif opcion == '3':
            nombre = input("Ingresá su nombre o enter para salir: ")
            if nombre == '':
                continuar = False
            else:
                apellido = input("Ingresá su apellido o enter para salir: ")
                if apellido == '':
                    continuar = False
                else:
                    while True:
                        try:
                            dni = input("Ingresá su DNI: ").strip()
                            if dni == '': 
                                continuar = False
                                break 
                            if not dni.isdigit():
                                print("❌ El DNI debe ser numérico.")
                                continue  
                            if len(dni) < 7 or len(dni) > 9:
                                print("❌ El DNI debe tener entre 7 y 9 dígitos.")
                                continue 
                            dni = int(dni)  
                            añadir("usuario", usuarios, (nombre, apellido, dni))
                            break  
                        except ValueError:
                            print("❌ Error: El DNI debe ser un número entero válido.")

        elif opcion == '4':
            continuar = False
        else:
            print("❌ Opción no válida, intentá de nuevo.")


def menuVer(generos, libros, usuarios, prestamos):
    continuar = True
    while continuar:
        print()
        print("═"*40)
        print("Menú Ver".center(40))
        print("═"*40)
        print("1. 🔍 Ver géneros")
        print("2. 🔍 Ver todos los libros")
        print("3. 🔍 Buscar libro específico")
        print("4. 🔍 Ver usuarios")
        print("5. 🔍 Ver préstamos")  # Nueva opción para ver préstamos
        print("6. 🔙 Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            ver("género", generos)
        elif opcion == '2':
            ver("libro", libros) 
        elif opcion == '3':
            buscarLibro(libros)
        elif opcion == '4':
            ver("usuario", usuarios)
        elif opcion == '5':
            ver("prestamos", prestamos) 
        elif opcion == '6':
            continuar = False
        else:
            print("Opción no válida, intentá de nuevo.")


def menuEliminar(generos, libros, usuarios):
    continuar = True
    while continuar:
        print()
        print("═"*40)
        print("Menú Eliminar".center(40))
        print("═"*40)
        print("1. 🗑️  Eliminar género")
        print("2. 🗑️  Eliminar libro")
        print("3. 🗑️  Eliminar usuario")
        print("4. 🔙 Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            ver("género", generos)
            idGenero = input("Ingresá el ID del género a eliminar o enter para volver: ")
            if idGenero:
                eliminar("género", generos, idGenero)
        elif opcion == '2':
            resultados = buscarLibro(libros) 
            if resultados:
                sku = input("Ingresá el SKU del libro a eliminar o enter para volver: ")
                if sku:
                    eliminar("libro", libros, sku)
        elif opcion == '3':
            ver("usuario", usuarios)
            idUsuario = input("Ingresá el ID del usuario a eliminar o enter para volver: ")
            if idUsuario:
                eliminar("usuario", usuarios, idUsuario)
        elif opcion == '4':
            continuar = False
        else:
            print("Opción no válida, intentá de nuevo.")

def menuPrestamos(usuarios, libros, prestamos):
    continuar = True
    while continuar:
        print()
        print("═"*40)
        print("Gestión de Préstamos".center(40))
        print("═"*40)
        print("1. 📖 Prestar libro")
        print("2. 🔄 Devolver libro")
        print("3. 🔙 Volver al menú principal")
        
        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            prestarLibro(usuarios, libros, prestamos)
        elif opcion == '2':
            devolverLibro(usuarios, libros, prestamos)
        elif opcion == '3':
            continuar = False
        else:
            print("Opción no válida, intentá de nuevo.")

def buscarLibro(libros):
    print("\nBúsqueda de Libros")
    print("Podés buscar por parte del título, autor o género.")
    
    criterio = input("Ingresá el criterio de búsqueda: ").lower()
    resultados = [libro for libro in libros if criterio in libro[1].lower() or  criterio in libro[2].lower() or  criterio in libro[3].lower()]   
    if resultados:
        print(f"\n{'═'*10} Resultados de la búsqueda {'═'*10}")
        print("─" * 110)
        for libro in resultados:
            print(f"SKU: {libro[0]} | Título: {libro[1]} | Autor: {libro[2]} | Género: {libro[3]} | Stock: {libro[4]}")
            print("─" * 110)
        return resultados
    else:
        print("No se encontraron libros que coincidan con el criterio de búsqueda.")
        return []
    
def main():
    usuarios = cargarUsuarios()
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
# MEJORAR MENU Y EL INTERFACE hecho
#AGREGAR UNA TECLA PARA VOLVER AL MENU hecho
#FILTRAR hecho
#MANEJAR UN STOCK listo
#manejo de archivos hecho
##HACER RESERVAS DE UN LIBRO
###PERIODO DE PRESTAMO/SANCION O PENALIDAD
#### TITULOS VENCIDOS Y NO DEVUELTOS
#USAR MODULO DATE TIME
#recursion


    continuar = True
    while continuar:
        print()
        print("═"*40)
        print("Sistema de Biblioteca".center(40))
        print("Menú Principal".center(40))
        print("═"*40)
        print("1. ➕ Añadir")
        print("2. 🗑️  Eliminar")
        print("3. 🔍 Ver")
        print("4. 📚 Préstamos")
        print("5. 🚪 Salir")

        opcion = input("Seleccioná una opción: ")

        if opcion == '1':
            menuAñadir(generos, libros, usuarios)
        elif opcion == '2':
            menuEliminar(generos, libros, usuarios)
        elif opcion == '3':
            menuVer(generos, libros, usuarios,prestamos)
        elif opcion == '4':
            menuPrestamos(usuarios, libros, prestamos)
        elif opcion == '5':
            print("👋 Saliste del programa. ¡Hasta la próxima!")
            continuar=False
        else:
            print("❌ Opción no válida, intentá de nuevo.")

if __name__ == "__main__":
    main()