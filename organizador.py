import os
import shutil

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

def mostrar_cabecera(consola):
    panel = Panel(
        "[bold cyan]ORGANIZADOR DE ARCHIVOS[/bold cyan]\n"
        "[white]Clasificación automática por extensión[/white]",
        title="[bold yellow]Python[/bold yellow]",
        border_style="cyan"
        )
    consola.print(panel)
 
    
def obtener_extension(nombre_archivo):
    nombre, extension = os.path.splitext(nombre_archivo)
    if extension:
        return extension[1:].lower()
    
    return "sin_extension"


def tamano_legible(tamano_bytes):
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
    ruta_a = os.path.abspath(ruta_a)
    ruta_b = os.path.abspath(ruta_b)

    if not ruta_a.endswith(os.sep):
        ruta_a += os.sep

    if not ruta_b.endswith(os.sep):
        ruta_b += os.sep

    return ruta_a.startswith(ruta_b) or ruta_b.startswith(ruta_a)

