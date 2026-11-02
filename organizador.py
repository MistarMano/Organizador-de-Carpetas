
"""
Organizador recursivo de archivos por extensión.

Solicita una carpeta de origen y otra de destino, recorre todos los
niveles de subcarpetas y mueve los archivos a subcarpetas clasificadas
por extensión. Evita sobrescribir archivos, calcula estadísticas y
muestra un informe mediante la biblioteca Rich.
"""

import os
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table


def mostrar_cabecera(consola):
    
   #Muestra el título del programa en un panel de Rich.
    
    panel = Panel(
        "[bold cyan]ORGANIZADOR DE ARCHIVOS[/bold cyan]\n"
        "[white]Clasificación automática por extensión[/white]",
        title="[bold yellow]Python[/bold yellow]",
        border_style="cyan",
        padding=(1, 3)
    )
    consola.print(panel)


def obtener_extension(nombre_archivo):

   # Obtiene la extensión de un archivo en minúsculas y sin el punto.

    nombre, extension = os.path.splitext(nombre_archivo)

    if extension:
        return extension[1:].lower()

    return "sin_extension"


def tamano_legible(tamano_bytes):
   # Convierte bytes a una unidad legible mediante divisiones sucesivas.


    unidades = ["bytes", "KB", "MB", "GB"]
    tamano = float(tamano_bytes)
    indice = 0

    while tamano >= 1024 and indice < len(unidades) - 1:
        tamano /= 1024
        indice += 1

    if indice == 0:
        return f"{int(tamano)} {unidades[indice]}"

    return f"{tamano:.2f} {unidades[indice]}"


def una_dentro_de_otra(ruta_a, ruta_b):
    
    #Comprueba si dos rutas representan la misma carpeta o si una está contenida dentro de la otra.

    ruta_a = os.path.abspath(ruta_a)
    ruta_b = os.path.abspath(ruta_b)

    # Añadir el separador evita confundir carpetas con nombres similares.
    if not ruta_a.endswith(os.sep):
        ruta_a += os.sep

    if not ruta_b.endswith(os.sep):
        ruta_b += os.sep

    return ruta_a.startswith(ruta_b) or ruta_b.startswith(ruta_a)


def nombre_disponible(ruta_destino, nombre_archivo):
   # Busca un nombre que no exista en la carpeta de destino.

    nombre, extension = os.path.splitext(nombre_archivo)
    nombre_candidato = nombre_archivo
    contador = 1

    while os.path.exists(os.path.join(ruta_destino, nombre_candidato)):
        nombre_candidato = f"{nombre}_{contador}{extension}"
        contador += 1

    return nombre_candidato


def clasificar_archivo(ruta_origen, nombre_archivo,ruta_destino, historial):
  #  Mueve un archivo a la subcarpeta correspondiente a su extensión.

    ruta_archivo = os.path.join(ruta_origen, nombre_archivo)

    # Obtener el tamaño antes de mover el archivo.
    tamano = os.path.getsize(ruta_archivo)

    extension = obtener_extension(nombre_archivo)
    carpeta_clasificada = os.path.join(ruta_destino, extension)

    # Crear la carpeta de la extensión si todavía no existe.
    os.makedirs(carpeta_clasificada, exist_ok=True)

    # Evitar sobrescribir archivos con el mismo nombre.
    nombre_final = nombre_disponible(carpeta_clasificada, nombre_archivo )

    ruta_final = os.path.join(carpeta_clasificada, nombre_final)

    # Mover el archivo y registrar el movimiento.
    shutil.move(ruta_archivo, ruta_final)

    movimiento = (
        f"{os.path.relpath(ruta_archivo, start=ruta_origen)} "
        f"→ {extension}/{nombre_final}"
    )
    historial.append(movimiento)

    return tamano


def clasificar_carpeta_recursivo(ruta_origen, ruta_destino, historial):
    
   # Clasifica todos los archivos de una carpeta y sus subcarpetas.

    tamano_total = 0

    for elemento in os.listdir(ruta_origen):
        ruta_elemento = os.path.join(ruta_origen, elemento)

        if os.path.isdir(ruta_elemento):
            tamano_total += clasificar_carpeta_recursivo(
                ruta_elemento,
                ruta_destino,
                historial
            )
            
        elif os.path.isfile(ruta_elemento):
            tamano_total += clasificar_archivo(
                ruta_origen,
                elemento,
                ruta_destino,
                historial
            )

    return tamano_total


def contar_archivos_recursivo(ruta):
    
   # Cuenta los archivos de una carpeta y todos sus subdirectorios.
    total = 0

    for elemento in os.listdir(ruta):
        ruta_elemento = os.path.join(ruta, elemento)

        if os.path.isdir(ruta_elemento):
            total += contar_archivos_recursivo(ruta_elemento)

        elif os.path.isfile(ruta_elemento):
            total += 1

    return total


def mostrar_informe(consola, movidos, tamano_total, en_origen, en_destino, historial):
    
    # Muestra las estadísticas y el historial mediante tablas de Rich.

    consola.print()

    tabla = Table(
        title="RESUMEN DE LA CLASIFICACIÓN",
        header_style="bold cyan",
        border_style="blue"
    )
    tabla.add_column("Estadística", style="white")
    tabla.add_column("Resultado", justify="right")

    tabla.add_row("Archivos movidos", f"[green]{movidos}[/green]")
    tabla.add_row("Tamaño total movido", tamano_legible(tamano_total))

    if en_origen == 0:
        origen_texto = f"[green]{en_origen}[/green]"
    else:
        origen_texto = f"[red]{en_origen}[/red]"

    tabla.add_row("Archivos restantes en origen", origen_texto)
    tabla.add_row("Archivos totales en destino", str(en_destino))

    consola.print(tabla)

    # Tabla con todos los movimientos realizados.
    tabla_historial = Table(
        title="HISTORIAL DE MOVIMIENTOS",
        header_style="bold magenta",
        border_style="magenta",
        show_lines=True
    )
    tabla_historial.add_column("N.º", justify="right", style="yellow")
    tabla_historial.add_column("Movimiento", overflow="fold")

    for numero, movimiento in enumerate(historial, start=1):
        tabla_historial.add_row(str(numero), movimiento)

    consola.print()
    consola.print(tabla_historial)


def main():
    
    consola = Console()

    mostrar_cabecera(consola)

    ruta_origen = Prompt.ask(
        "[bold cyan]Introduce la ruta de origen[/bold cyan]",
        console=consola
    ).strip().strip('"')

    ruta_destino = Prompt.ask(
        "[bold cyan]Introduce la ruta de destino[/bold cyan]",
        console=consola
    ).strip().strip('"')

    if not os.path.isdir(ruta_origen):
        consola.print(
            Panel(
                "[bold red]La carpeta de origen no existe "
                "o no es una carpeta.[/bold red]",
                border_style="red"
            )
        )
        return

    if os.path.exists(ruta_destino) and not os.path.isdir(ruta_destino):
        consola.print(
            Panel(
                "[bold red]La ruta de destino existe, "
                "pero no es una carpeta.[/bold red]",
                border_style="red"
            )
        )
        return

    if una_dentro_de_otra(ruta_origen, ruta_destino):
        consola.print(
            Panel(
                "[bold red]El origen y el destino no pueden ser "
                "la misma carpeta ni estar uno dentro del otro.[/bold red]",
                border_style="red"
            )
        )
        return

    historial = []

    try:
        with consola.status(
            "[bold cyan]Clasificando archivos...[/bold cyan]",
            spinner="dots"
        ):
            tamano_total = clasificar_carpeta_recursivo(
                ruta_origen,
                ruta_destino,
                historial
            )

        en_origen = contar_archivos_recursivo(ruta_origen)
        en_destino = contar_archivos_recursivo(ruta_destino)

        mostrar_informe(
            consola,
            len(historial),
            tamano_total,
            en_origen,
            en_destino,
            historial
        )

    except OSError as error:
        consola.print(
            Panel(
                "[bold red]Error al acceder o mover archivos:[/bold red]\n"
                f"{error}",
                border_style="red"
            )
        )


if __name__ == "__main__":
    main()
