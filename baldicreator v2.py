
import os
import json
import time

CARPETA = "BaldiMods"
os.makedirs(CARPETA, exist_ok=True)


def limpiar():
    os.system("cls" if os.name == "nt" else "clear")


def esperar():
    input("\nPresiona ENTER para continuar...")


def listar():
    return [
        f[:-5] for f in os.listdir(CARPETA)
        if f.endswith(".json")
    ]


def ruta(nombre):
    return os.path.join(CARPETA, nombre + ".json")


def crear():
    limpiar()
    print("=== NUEVO PROYECTO ===")
    nombre = input("Nombre del mod: ").strip()

    if not nombre or nombre in (".", ".."):
        print("Nombre inválido.")
        esperar()
        return

    nombre = "".join(
        c for c in nombre if c.isalnum() or c in " _-"
    ).strip()

    if not nombre:
        print("Nombre inválido.")
        esperar()
        return

    if os.path.exists(ruta(nombre)):
        print("Ya existe un proyecto con ese nombre.")
        esperar()
        return

    mod = {
        "nombre": nombre,
        "baldi": {"nombre": "Baldi", "velocidad": 5.0},
        "escuela": "Here School",
        "cuadernos": 7,
        "personajes": [],
        "objetos": []
    }

    guardar(nombre, mod)
    print("¡Proyecto creado!")
    esperar()
    editar(nombre)


def guardar(nombre, mod):
    with open(ruta(nombre), "w", encoding="utf-8") as f:
        json.dump(mod, f, indent=4, ensure_ascii=False)


def seleccionar():
    limpiar()
    proyectos = listar()

    print("=== SELECCIONAR PROYECTO ===")

    if not proyectos:
        print("No hay proyectos guardados.")
        esperar()
        return None

    for i, nombre in enumerate(proyectos, 1):
        print(f"{i}. {nombre}")

    print("0. Volver")

    try:
        n = int(input("\nSelecciona: "))
        if n == 0:
            return None
        if 1 <= n <= len(proyectos):
            return proyectos[n - 1]
    except ValueError:
        pass

    print("Selección inválida.")
    esperar()
    return None


def editar(nombre):
    try:
        with open(ruta(nombre), "r", encoding="utf-8") as f:
            mod = json.load(f)
    except (OSError, ValueError):
        print("No se pudo abrir el proyecto.")
        esperar()
        return

    while True:
        limpiar()
        print(f"=== EDITOR: {nombre} ===")
        print("1. Nombre de Baldi")
        print("2. Velocidad de Baldi")
        print("3. Nombre de la escuela")
        print("4. Cantidad de cuadernos")
        print("5. Añadir personaje")
        print("6. Borrar personaje")
        print("7. Añadir objeto")
        print("8. Borrar objeto")
        print("9. Ver configuración")
        print("10. Guardar")
        print("0. Volver")

        op = input("\nOpción: ")

        if op == "1":
            limpiar()
            mod["baldi"]["nombre"] = input("Nuevo nombre: ")

        elif op == "2":
            limpiar()
            try:
                v = float(input("Nueva velocidad: "))
                if v > 0:
                    mod["baldi"]["velocidad"] = v
                else:
                    print("La velocidad debe ser positiva.")
            except ValueError:
                print("Número inválido.")
            esperar()

        elif op == "3":
            limpiar()
            mod["escuela"] = input("Nombre de la escuela: ")

        elif op == "4":
            limpiar()
            try:
                n = int(input("Cantidad de cuadernos: "))
                if n >= 1:
                    mod["cuadernos"] = n
                else:
                    print("Debe haber al menos un cuaderno.")
            except ValueError:
                print("Número inválido.")
            esperar()

        elif op == "5":
            limpiar()
            p = input("Nombre del personaje: ").strip()
            if p:
                mod["personajes"].append(p)
                print("Personaje añadido.")
            esperar()

        elif op == "6":
            limpiar()
            borrar_lista(mod["personajes"], "personaje")

        elif op == "7":
            limpiar()
            objeto = input("Nombre del objeto: ").strip()
            if objeto:
                mod["objetos"].append(objeto)
                print("Objeto añadido.")
            esperar()

        elif op == "8":
            limpiar()
            borrar_lista(mod["objetos"], "objeto")

        elif op == "9":
            limpiar()
            print(json.dumps(mod, indent=4, ensure_ascii=False))
            esperar()

        elif op == "10":
            guardar(nombre, mod)
            limpiar()
            print("¡Proyecto guardado!")
            esperar()

        elif op == "0":
            guardar(nombre, mod)
            break


def borrar_lista(lista, tipo):
    if not lista:
        print(f"No hay {tipo}s.")
        esperar()
        return

    for i, item in enumerate(lista, 1):
        print(f"{i}. {item}")

    try:
        n = int(input("\nNúmero a borrar (0 cancela): "))
        if 1 <= n <= len(lista):
            eliminado = lista.pop(n - 1)
            print(f"Eliminado: {eliminado}")
        elif n != 0:
            print("Número inválido.")
    except ValueError:
        print("Número inválido.")

    esperar()


def borrar():
    nombre = seleccionar()
    if nombre is None:
        return

    limpiar()
    print(f"=== BORRAR: {nombre} ===")
    confirmar = input("¿Eliminar definitivamente? (s/n): ").lower()

    if confirmar == "s":
        os.remove(ruta(nombre))
        print("Proyecto eliminado.")

    esperar()


def menu():
    while True:
        limpiar()
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

        op = input("Selecciona una opción: ")

        if op == "1":
            crear()

        elif op == "2":
            nombre = seleccionar()
            if nombre:
                editar(nombre)

        elif op == "3":
            limpiar()
            print("=== MIS PROYECTOS ===")
            proyectos = listar()
            for p in proyectos:
                print("- " + p)
            if not proyectos:
                print("No hay proyectos.")
            esperar()

        elif op == "4":
            borrar()

        elif op == "0":
            limpiar()
            print("¡Hasta luego!")
            break


menu()
