# Configuración del archivo para persistencia de datos
import os

ARCHIVO_DATOS = "catalogo.txt"

def cargar_catalogo(archivo, codigos, descripciones, stocks, precios):
    """Lee el archivo de texto y puebla los arreglos paralelos de forma síncrona."""
    if not os.path.exists(archivo):
        # Se crea un archivo con datos iniciales si no existe
        with open(archivo, "w", encoding="utf-8") as f:
            f.write("P001;Arroz Extra Costeño 1kg;500;4.50\n")
            f.write("P002;Aceite Vegetal Primor 1L;300;11.20\n")
            f.write("P003;Leche Evaporada Gloria 400g;400;4.20\n")

    try:
        with open(archivo, "r", encoding="utf-8") as f:
            for linea in f:
                linea = linea.strip()
                if not linea:
                    continue
                partes = linea.split(";")
                if len(partes) == 4:
                    codigos.append(partes[0].strip())
                    descripciones.append(partes[1].strip())
                    stocks.append(int(partes[2].strip()))
                    precios.append(float(partes[3].strip()))
    except ValueError:
        print(
            "Error: El archivo contiene datos corruptos o formatos incorrectos."
        )
    except Exception as e:
        print(f"Error inesperado al cargar el archivo: {e}")

def guardar_catalogo(archivo, codigos, descripciones, stocks, precios):
    """Volcar la información de los arreglos paralelos en el archivo de texto plano."""
    try:
        with open(archivo, "w", encoding="utf-8") as f:
            for i in range(len(codigos)):
                linea = f"{codigos[i]};{descripciones[i]};{stocks[i]};{precios[i]:.2f}\n"
                f.write(linea)
        print("Catálogo guardado en el almacenamiento local de forma exitosa.")
    except Exception as e:
        print(f"Error crítico al guardar los datos en disco: {e}")

def mostrar_catalogo(codigos, descripciones, stocks, precios):
    """Muestra en pantalla el catálogo completo formateado de forma tabular."""
    total_productos = len(codigos)
    print("\n" + "=" * 80)
    print(
        f"{'CATÁLOGO DE PRODUCTOS - PLAZA VEA':^80}"
    )  # Centrado del título
    print(f" Total referencias activas: {total_productos} / 1 200")
    print("=" * 80)
    print(
        f"{'N°':<5}{'CÓDIGO':<12}{'DESCRIPCIÓN':<35}{'STOCK':<12}{'PRECIO (S/.)':<15}"
    )
    print("-" * 80)

    for i in range(total_productos):
        print(
            f"{i+1:<5}{codigos[i]:<12}{descripciones[i]:<35}{stocks[i]:<12}{precios[i]:<15.2f}"
        )

    print("=" * 80 + "\n")

def registrar_producto(codigos, descripciones, stocks, precios):
    """Inserta un nuevo producto validando la no duplicidad del código."""
    print("\n--- REGISTRO DE NUEVO PRODUCTO ---")

    while True:
        codigo = input("Ingrese el código único del producto: ").strip().upper()

        if codigo == "":
            print("Error: El código no puede estar vacío.")
        elif codigo in codigos:
            print(
                f"Error: El código '{codigo}' ya se encuentra asignado a un producto."
            )
        else:
            break

    while True:
        descripcion = input("Ingrese la descripción del producto: ").strip()
        if descripcion == "":
            print("Error: La descripción no puede estar vacía.")
        else:
            break

    # Validaciones de entrada numérica contra caídas del sistema
    while True:
        try:
            stock = int(input("Ingrese la cantidad disponible (Stock >= 0): "))
            if stock < 0:
                print("Error: El stock inicial no puede ser un número negativo.")
                continue
            break
        except ValueError:
            print(
                "Error de formato: Ingrese exclusivamente caracteres numéricos válidos."
            )

    while True:
        try:
            precio = float(input("Ingrese el precio de venta al público (> 0): "))
            if precio <= 0:
                print("Error: El precio de venta debe ser estrictamente mayor a 0.")
                continue
            break
        except ValueError:
            print(
                "Error de formato: Ingrese exclusivamente caracteres numéricos válidos."
            )

    # Inserción sincronizada en los arreglos paralelos
    codigos.append(codigo)
    descripciones.append(descripcion)
    stocks.append(stock)
    precios.append(precio)
    print(f"Éxito: Producto '{codigo}' añadido satisfactoriamente al búfer.")

def actualizar_producto(codigos, descripciones, stocks, precios):
    """Busca un producto por código y permite actualizar de manera integral sus datos."""
    print("\n--- ACTUALIZACIÓN DE REGISTROS DE PRODUCTO ---")
    codigo_buscar = (
        input("Ingrese el código del producto a modificar: ").strip().upper()
    )

    # Búsqueda secuencial manual de la posición del índice
    indice_encontrado = -1
    for i in range(len(codigos)):
        if codigos[i] == codigo_buscar:
            indice_encontrado = i
            break

    if indice_encontrado == -1:
        print(
            f"Error: El código '{codigo_buscar}' no existe en el catálogo actual."
        )
        return

    print(f"\nProducto localizado en el índice del sistema: {indice_encontrado}")
    print(f"  Descripción actual : {descripciones[indice_encontrado]}")
    print(f"  Stock actual       : {stocks[indice_encontrado]}")
    print(f"  Precio actual      : S/. {precios[indice_encontrado]:.2f}")
    print("-" * 50)

    while True:
        nueva_desc = input(
            "Ingrese nueva descripción (Presione ENTER para mantener la actual): "
        ).strip()
        if nueva_desc:
            descripciones[indice_encontrado] = nueva_desc
        break

    while True:
        nuevo_stock_str = input(
            "Ingrese nuevo stock (Presione ENTER para mantener el actual): "
        ).strip()
        if not nuevo_stock_str:
            break
        try:
            nuevo_stock = int(nuevo_stock_str)
            if nuevo_stock < 0:
                print("Error: El stock no puede ser negativo. No se modificó.")
                continue
            stocks[indice_encontrado] = nuevo_stock
            break
        except ValueError:
            print(
                "Error de formato: Ingrese exclusivamente caracteres numéricos válidos."
            )

    while True:
        nuevo_precio_str = input(
            "Ingrese nuevo precio (Presione ENTER para mantener el actual): "
        ).strip()
        if not nuevo_precio_str:
            break
        try:
            nuevo_precio = float(nuevo_precio_str)
            if nuevo_precio <= 0:
                print("Error: El precio debe ser mayor a 0. No se modificó.")
                continue
            precios[indice_encontrado] = nuevo_precio
            print(
                f"Éxito: El registro '{codigo_buscar}' ha sido actualizado de forma temporal."
            )
            break
        except ValueError:
            print(
                "Error de formato numérico: Los valores numéricos no fueron alterados."
            )

def main():
    # Inicialización de las estructuras de datos lineales (Arreglos Paralelos)
    lista_codigos = []
    lista_descripciones = []
    lista_stocks = []
    lista_precios = []

    # Carga automática de la base de datos persistente al arrancar la sesión
    cargar_catalogo(
        ARCHIVO_DATOS,
        lista_codigos,
        lista_descripciones,
        lista_stocks,
        lista_precios,
    )

    while True:
        print("\n" + "=" * 45)
        print(f"{'SISTEMA DE CONTROL DE CATÁLOGO (V1.0)':^45}")
        print("=" * 45)
        print(" 1. Visualizar catálogo completo")
        print(" 2. Registrar nueva referencia de producto")
        print(" 3. Actualizar datos de producto existente")
        print(" 4. Guardar cambios en base de datos local")
        print(" 5. Guardar cambios y salir de la aplicación")
        print("=" * 45)

        opcion = input("Seleccione una opción operativa (1-5): ").strip()

        if opcion == "1":
            mostrar_catalogo(
                lista_codigos,
                lista_descripciones,
                lista_stocks,
                lista_precios,
            )
        elif opcion == "2":
            registrar_producto(
                lista_codigos,
                lista_descripciones,
                lista_stocks,
                lista_precios,
            )
        elif opcion == "3":
            actualizar_producto(
                lista_codigos,
                lista_descripciones,
                lista_stocks,
                lista_precios,
            )
        elif opcion == "4":
            guardar_catalogo(
                ARCHIVO_DATOS,
                lista_codigos,
                lista_descripciones,
                lista_stocks,
                lista_precios,
            )
        elif opcion == "5":
            print(
                "\nConsolidando y asegurando la persistencia de datos en el archivo..."
            )
            guardar_catalogo(
                ARCHIVO_DATOS,
                lista_codigos,
                lista_descripciones,
                lista_stocks,
                lista_precios,
            )
            print(
                "Sesión de operaciones finalizada con éxito de manera segura. ¡Buen día!"
            )
            break
        else:
            print(
                "Opción no válida. Por favor, introduzca un dígito dentro del rango del menú (1-5)."
            )

if __name__ == "__main__":
    main()
