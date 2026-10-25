
import json
import os

CARPETA = "BaldiMods"
os.makedirs(CARPETA, exist_ok=True)


def listar_proyectos():
    return [
        f[:-5] for f in os.listdir(CARPETA)
        if f.endswith(".json")
    ]


def elegir_proyecto():
    proyectos = listar_proyectos()

    if not proyectos:
        print("No hay proyectos guardados.")
        return None

    for i, nombre in enumerate(proyectos, 1):
        print(f"{i}. {nombre}")

    try:
        n = int(input("Selecciona un proyecto: "))
        if 1 <= n <= len(proyectos):
            return proyectos[n - 1]
    except ValueError:
        pass

    print("Selección inválida.")
    return None


def crear_proyecto():
    nombre = input("Nombre del proyecto: ").strip()

    if not nombre or nombre in (".", ".."):
        print("Nombre inválido.")
        return

    nombre = "".join(
        c for c in nombre
        if c.isalnum() or c in "_- "
    ).strip()

    if not nombre:
        print("Nombre inválido.")
        return

    ruta = os.path.join(CARPETA, nombre + ".json")

    if os.path.exists(ruta):
        print("Ese proyecto ya existe.")
        return

    mod = {
        "nombre": nombre,
        "baldi": {
            "nombre": "Baldi",
            "velocidad": 5.0
        },
        "escuela": "Here School",
        "cuadernos": 7,
        "personajes": [],
        "objetos": []
    }

    guardar_datos(ruta, mod)
    print("¡Proyecto creado!")


def guardar_datos(ruta, datos):
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def editar_proyecto():
    nombre = elegir_proyecto()
    if nombre is None:
        return

    ruta = os.path.join(CARPETA, nombre + ".json")

    with open(ruta, "r", encoding="utf-8") as archivo:
        mod = json.load(archivo)

    while True:
        print(f"\n=== EDITANDO: {nombre} ===")
        print("1. Nombre de Baldi")
        print("2. Velocidad de Baldi")
        print("3. Nombre de la escuela")
        print("4. Cantidad de cuadernos")
        print("5. Añadir personaje")
        print("6. Borrar personaje")
        print("7. Añadir objeto")
        print("8. Borrar objeto")
        print("9. Ver proyecto")
        print("10. Guardar y salir")

        op = input("Opción: ")

        if op == "1":
            mod["baldi"]["nombre"] = input("Nombre: ")

        elif op == "2":
            try:
                velocidad = float(input("Velocidad: "))
                if velocidad <= 0:
                    print("La velocidad debe ser positiva.")
                else:
                    mod["baldi"]["velocidad"] = velocidad
            except ValueError:
                print("Introduce un número válido.")

        elif op == "3":
            mod["escuela"] = input("Nombre de la escuela: ")

        elif op == "4":
            try:
                cantidad = int(input("Cuadernos: "))
                if cantidad < 1:
                    print("Debe haber al menos un cuaderno.")
                else:
                    mod["cuadernos"] = cantidad
            except ValueError:
                print("Introduce un número entero.")

        elif op == "5":
            nombre_personaje = input("Nombre del personaje: ")
            if nombre_personaje.strip():
                mod["personajes"].append(nombre_personaje)

        elif op == "6":
            for i, personaje in enumerate(mod["personajes"], 1):
                print(f"{i}. {personaje}")
            try:
                i = int(input("Número a borrar: ")) - 1
                if 0 <= i < len(mod["personajes"]):
                    mod["personajes"].pop(i)
                    print("Personaje borrado.")
            except ValueError:
                print("Número inválido.")

        elif op == "7":
            objeto = input("Nombre del objeto: ")
            if objeto.strip():
                mod["objetos"].append(objeto)

        elif op == "8":
            for i, objeto in enumerate(mod["objetos"], 1):
                print(f"{i}. {objeto}")
            try:
                i = int(input("Número a borrar: ")) - 1
                if 0 <= i < len(mod["objetos"]):
                    mod["objetos"].pop(i)
                    print("Objeto borrado.")
            except ValueError:
                print("Número inválido.")

        elif op == "9":
            print(json.dumps(mod, indent=4, ensure_ascii=False))

        elif op == "10":
            guardar_datos(ruta, mod)
            print("Proyecto guardado.")
            break

        else:
            print("Opción inválida.")


def borrar_proyecto():
    nombre = elegir_proyecto()
    if nombre is None:
        return

    confirmar = input(
        f"¿Borrar definitivamente '{nombre}'? (s/n): "
    ).lower()

    if confirmar == "s":
        ruta = os.path.join(CARPETA, nombre + ".json")
        os.remove(ruta)
        print("Proyecto eliminado.")


def menu():
    while True:
        print("""
================================
      BALDI MOD CREATOR
================================
1. Crear proyecto
2. Editar proyecto
3. Ver proyectos
4. Borrar proyecto
0. Salir
""")

        opcion = input("Selecciona: ")

        if opcion == "1":
            crear_proyecto()

        elif opcion == "2":
            editar_proyecto()

        elif opcion == "3":
            proyectos = listar_proyectos()
            if proyectos:
                for p in proyectos:
                    print("- " + p)
            else:
                print("No hay proyectos.")

        elif opcion == "4":
            borrar_proyecto()

        elif opcion == "0":
            print("¡Hasta luego!")
            break

        else:
            print("Opción inválida.")


menu()
