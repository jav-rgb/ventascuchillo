import os
import pyfiglet
from datetime import datetime

productos = []
ventas = []

def leer_datos_archivo(archivo):
    lista_datos = []
    try:
        with open(archivo, 'r') as file:
            for linea in file:
                linea = linea.strip()
                datos = linea.split(',')
                lista_datos.append(datos)
    except FileNotFoundError:
        print(f"Error: El archivo {archivo} no se encontró.")
    except Exception as e:
        print(f"Error al leer el archivo {archivo}: {e}")
    return lista_datos

def cargar_datos():
    global productos, ventas
    productos = leer_datos_archivo('productos.txt')
    ventas = leer_datos_archivo('ventas.txt')

def respaldar_datos():
    try:
        with open("productos.txt", "w") as file:
            for producto in productos:
                file.write(",".join(map(str, producto)) + '\n')
        with open("ventas.txt", "w") as file:
            for venta in ventas:
                file.write(",".join(map(str, venta)) + '\n')
        print("Datos respaldados exitosamente.")
    except Exception as e:
        print(f"Error al respaldar datos: {e}")

def registrar_venta_archivo(venta):
    try:
        with open("ventas.txt", "a") as file:
            file.write(",".join(map(str, venta)) + '\n')
    except Exception as e:
        print(f"Error al registrar la venta en el archivo: {e}")

def obtener_siguiente_folio():
    if ventas:
        ultimo_folio = int(ventas[-1][0])
        return ultimo_folio + 1
    else:
        return 1

print(pyfiglet.figlet_format("Sistema de ventas Cuchillos"))
print("""                                                    Kevin Gallardo
                                                    Javier Alegria
                                                              006D
""")
input("Presione Enter para continuar...")

cargar_datos()

opcion = 0
while opcion <= 5:
    os.system("cls")
    fecha_actual = datetime.now().strftime("%d %m %Y")
    print(f"""
                                        Fecha:   {fecha_actual}
                                        Version: v002
                SISTEMA DE VENTAS
        ................................
            1. Vender productos
            2. Reportes
            3. Mantenedores
            4. Administrador
            5. Salir
        ................................
    """)

    try:
        opcion = int(input("Ingrese una opcion entre 1-5: "))
    except ValueError:
        print("Opción inválida. Por favor, ingrese un número entre 1 y 5.")
        continue

    if opcion >= 1 and opcion <= 6:
        match opcion:
            case 1:
                os.system("cls")
                print("\n Vender productos\n")
                id_producto = input("Ingrese ID del producto a vender: ")
                encontrado = False
                for producto in productos:
                    if producto[0] == id_producto:
                        encontrado = True
                        try:
                            cantidad = int(input("Ingrese la cantidad a vender: "))
                        except ValueError:
                            print("Cantidad inválida. Debe ser un número.")
                            break
                        if cantidad <= int(producto[4]):
                            producto[4] = str(int(producto[4]) - cantidad)
                            fecha_actual = datetime.now()
                            fecha = fecha_actual.strftime("%d %m %Y")
                            folio = obtener_siguiente_folio()
                            total = cantidad * int(producto[5])
                            print(f"El total a pagar es: ${total}")
                            confirmacion = input("¿Desea realizar la compra? (s/n): ")
                            if confirmacion.lower() == 's':
                                venta = [str(folio), fecha, id_producto, str(cantidad), str(total)]
                                ventas.append(venta)
                                registrar_venta_archivo(venta)
                                respaldar_datos()
                                print("Venta realizada exitosamente.")
                            else:
                                print("Venta cancelada.")
                        elif cantidad > int(producto[4]):
                            print("No hay suficiente stock para realizar la venta.")
                            print("")
                            input("Presiona enter para reintentar...")
                if not encontrado:
                    print("Producto no encontrado.")

            case 2:
                os.system("cls")
                op = 0
                while op <= 4:
                    print("""    
                                REPORTES
                    ...................................
                        1. General de ventas
                        2. Ventas por fecha especifica
                        3. Ventas por rango de fecha
                        4. Salir al menu principal
                    ....................................
                    """)

                    try:
                        op = int(input("Ingrese una opcion entre 1-4: "))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese un número entre 1 y 4.")
                        continue

                    if op == 1:
                        try:
                            total_ventas = sum(int(venta[4].replace(']', '')) for venta in ventas)
                            print(f"Total de ventas: ${total_ventas}")
                            print("")
                            print("Listado de ventas:")
                            for venta in ventas:
                                print(f"Folio: {venta[0]}, Fecha: {venta[1]}, Producto ID: {venta[2]}, Cantidad: {venta[3]}, Total: ${venta[4]}")
                        except ValueError as e:
                            print(f"Error al calcular el total de ventas: {e}")
                            print("Verifique el archivo de ventas para corregir los datos.")

                        
                    elif op == 2:
                        os.system("cls")
                        fecha = input("Ingrese la fecha (dd mm yyyy): ")
                        total_ventas_fecha = sum(int(venta[4]) for venta in ventas if venta[1] == fecha)
                        print(f"Ventas totales en la fecha {fecha}: ${total_ventas_fecha}")
                        print(f"Listado de ventas del día {fecha}:")
                        for venta in ventas:
                            if venta[1] == fecha:
                                print(f"Folio: {venta[0]}, Producto ID: {venta[2]}, Cantidad: {venta[3]}, Total: ${venta[4]}")
                        
                    elif op == 3:
                        os.system("cls")
                        print("Ventas por rango de fecha")
                        fecha_inicio = input("Ingrese la fecha de inicio (dd mm yyyy): ")
                        fecha_fin = input("Ingrese la fecha de fin (dd mm yyyy): ")

                        try:
                            fecha_inicio = datetime.strptime(fecha_inicio, "%d %m %Y")
                            fecha_fin = datetime.strptime(fecha_fin, "%d %m %Y")
                        except ValueError:
                            print("Formato de fecha inválido. Use dd mm yyyy.")
                            continue

                        total_ventas_rango = sum(int(venta[4]) for venta in ventas if fecha_inicio <= datetime.strptime(venta[1], "%d %m %Y") <= fecha_fin)
                        print(f"Ventas totales en el rango de fecha {fecha_inicio.strftime('%d %m %Y')} a {fecha_fin.strftime('%d %m %Y')}: ${total_ventas_rango}")
                        print(f"Listado de ventas del rango {fecha_inicio.strftime('%d %m %Y')} a {fecha_fin.strftime('%d %m %Y')}:")
                        for venta in ventas:
                            fecha_venta = datetime.strptime(venta[1], "%d %m %Y")
                            if fecha_inicio <= fecha_venta <= fecha_fin:
                                print(f"Folio: {venta[0]}, Fecha: {venta[1]}, Producto ID: {venta[2]}, Cantidad: {venta[3]}, Total: ${venta[4]}")
                        
                    elif op == 4:
                        break
                    else:
                        print("Opcion invalida. Intente nuevamente.")

            case 3:
                while True:
                    print("""
                    mantenedor de productos
                ...............................
                    1. Agregar
                    2. Buscar
                    3. Eliminar
                    4. Modificar
                    5. Listar
                    6. Salir al menu principal
                ...............................
                """)
                    try:
                        op = int(input("Ingrese una opcion 1-6: "))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese un número entre 1 y 6.")
                        continue

                    match op:
                        case 1:
                            print("\n Agregar productos\n")
                            id_producto = input("Ingrese id producto: ")
                            nombre = input("Ingrese nombre de producto: ")
                            origen = input("Ingrese el origen: ")
                            talla = input("Ingrese la medida: ")
                            try:
                                stock = int(input("Ingrese el stock: "))
                                precio = int(input("Ingrese el precio: "))
                            except ValueError:
                                print("Stock y precio deben ser números.")
                                continue
                           
                            productos.append([id_producto, nombre, origen, talla, str(stock), str(precio)])
                            respaldar_datos()
                            print("Producto agregado exitosamente.")
                       
                        case 2:
                            id_producto = input("Ingrese id producto a buscar: ")
                            encontrado = False
                            for producto in productos:
                                if producto[0] == id_producto:
                                    encontrado = True
                                    print(f"Producto encontrado: {producto}")
                                    break
                            if not encontrado:
                                print("Producto no encontrado.")
                       
                        case 3:
                            id_producto = input("Ingrese id producto a eliminar: ")
                            encontrado = False
                            for i, producto in enumerate(productos):
                                if producto[0] == id_producto:
                                    encontrado = True
                                    productos.pop(i)
                                    respaldar_datos()
                                    print("Producto eliminado exitosamente.")
                                    break
                            if not encontrado:
                                print("Producto no encontrado.")
                       
                        case 4:
                            id_producto = input("Ingrese id producto a modificar: ")
                            encontrado = False
                            for i, producto in enumerate(productos):
                                if producto[0] == id_producto:
                                    encontrado = True
                                    print(f"Producto encontrado: {producto}")
                                    print("Ingrese los nuevos datos del producto (deje en blanco para no modificar):")
                                    nombre = input(f"Nombre ({producto[1]}): ") or producto[1]
                                    origen = input(f"Origen ({producto[2]}): ") or producto[2]
                                    talla = input(f"Talla ({producto[3]}): ") or producto[3]
                                    try:
                                        stock = input(f"Stock ({producto[4]}): ") or producto[4]
                                        precio = input(f"Precio ({producto[5]}): ") or producto[5]
                                        producto[1] = nombre
                                        producto[2] = origen
                                        producto[3] = talla
                                        producto[4] = str(int(stock))  # Convertimos a entero para validar
                                        producto[5] = str(int(precio))  # Convertimos a entero para validar
                                        respaldar_datos()
                                        print("Producto modificado exitosamente.")
                                    except ValueError:
                                        print("Stock y precio deben ser números.")
                                    break
                            if not encontrado:
                                print("Producto no encontrado.")
                       
                        case 5:
                            print("Listado de productos:")
                            for producto in productos:
                                print(f"ID: {producto[0]}, Nombre: {producto[1]}, Origen: {producto[2]}, Talla: {producto[3]}, Stock: {producto[4]}, Precio: {producto[5]}")
                       
                        case 6:
                            break  # sale del while y vuelve al menu principal
                        
                        case _:
                            print("Opción inválida. Intente nuevamente.")
            
            case 4:
                while True:
                    print("""
                    Administracion
                ...............................
                1. Cargar datos
                2. Respaldar datos (Grabar, actualizar)
                3. Salir al menu principal
                ...............................
                """)
                    try:
                        admin_opcion = int(input("Ingrese una opción: "))
                    except ValueError:
                        print("Opción inválida. Por favor, ingrese un número.")
                        continue

                    match admin_opcion:
                        case 1:
                            cargar_datos()
                            print("Datos cargados exitosamente.")
                        case 2:
                            respaldar_datos()
                        case 3:
                            break
                        case _:
                            print("Opción inválida. Intente nuevamente.")
            
            case 5:
                respaldar_datos()
                print("Saliendo del programa...")
                break

            case _:
                print("Opción inválida. Intente nuevamente.")

print("Fin del menu")
