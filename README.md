# Visualizador de Grafos de Dependencia de Tablas

Este script de Python genera una visualización interactiva de un grafo de dependencias entre tablas a partir de un archivo Excel. La visualización se guarda como un archivo HTML que se puede abrir en cualquier navegador web.

## Características

-   **Visualización Jerárquica:** Muestra las dependencias de las tablas en un diseño jerárquico de izquierda a derecha, desde las tablas de origen (INPUT) hasta las tablas de destino (OUTPUT).
-   **Coloreado de Nodos:** Los nodos se colorean según su tipo:
    -   **Naranja:** Tablas de entrada (INPUT)
    -   **Verde:** Tablas de salida (OUTPUT)
    -   **Gris:** Tablas intermedias (INTERMEDIA)
-   **Búsqueda Interactiva:** Permite buscar tablas por su nombre y resalta el nodo correspondiente en el grafo.
-   **Listado de Tablas:** Muestra listas de tablas de entrada, salida e intermedias debajo del grafo.

## Instalación

1.  **Clona el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-REPOSITORIO>
    ```

2.  **Crea un entorno virtual (recomendado):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # En Windows, usa `venv\Scripts\activate`
    ```

3.  **Instala las dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
    *(Nota: Se generará un archivo `requirements.txt` en el siguiente paso).*

## Uso

1.  **Prepara tu archivo de datos:**
    -   Asegúrate de tener un archivo Excel (por ejemplo, `TRAZA.xlsx`).
    -   El archivo debe contener una o más hojas con las siguientes columnas:
        -   `OrigenDeImpactoTabla`
        -   `DestinoDeImpactoTabla`
        -   `TipoOrigenDeImpactoTabla` (con valores como 'INPUT', 'INTERMEDIA')
        -   `TipoDestinoDeImpactoTabla` (con valores como 'OUTPUT', 'INTERMEDIA')
        -   `campaña` (opcional, no se usa en la versión actual del script)

2.  **Actualiza el nombre del archivo en el script (opcional):**
    -   Si tu archivo Excel no se llama `TRAZA.xlsx`, abre el archivo `analisis_de_flujo.py` y cambia el nombre del archivo en la función `main`:
        ```python
        def main():
            ruta_excel = Path('TU_ARCHIVO.xlsx')
            # ...
        ```

3.  **Ejecuta el script:**
    ```bash
    python analisis_de_flujo.py
    ```

4.  **Abre el archivo HTML:**
    -   El script generará un archivo HTML por cada hoja en tu archivo Excel (por ejemplo, `malla_grafica_Flujo1.html`).
    -   Abre este archivo en tu navegador web para ver la visualización del grafo.
