# Visualizador de Grafos de Dependencia de Tablas

Este proyecto genera visualizaciones interactivas y dinámicas de grafos de dependencias a partir de datos en un archivo Excel. La principal característica es su capacidad para crear layouts jerárquicos y claros, donde las líneas de conexión se curvan para evitar cruces, facilitando la comprensión de flujos de datos complejos.

## Características Principales

-   **Visualización Dinámica y Clara:** Utiliza `Cytoscape.js` para renderizar el grafo, permitiendo interacciones fluidas como hacer zoom y mover los nodos.
-   **Layout Jerárquico Automático:** Emplea el algoritmo `dagre` para organizar los nodos en niveles de izquierda a derecha, representando el flujo desde el origen (`INPUT`) hasta el destino (`OUTPUT`).
-   **Enrutamiento Inteligente de Aristas:** Las líneas que conectan los nodos (`aristas`) se curvan (`unbundled-bezier`) para evitar superposiciones y cruces, lo que resulta en una visualización mucho más limpia y legible.
-   **Coloreado Semántico de Nodos:** Los nodos se colorean según su tipo para una identificación rápida:
    -   **Naranja:** Tablas de entrada (`INPUT`)
    -   **Verde:** Tablas de salida (`OUTPUT`)
    -   **Gris:** Tablas intermedias (`INTERMEDIA`)
-   **Generación Autónoma:** El script de Python procesa el archivo Excel y genera un único archivo HTML autocontenido, sin necesidad de servidores o configuraciones adicionales.

## Historial de Mejoras

Este proyecto ha evolucionado a través de varias versiones para mejorar la calidad de la visualización:

-   **v1.0: Visualización Básica (Pyvis)**
    -   Implementación inicial usando `pyvis` y `networkx`.
    -   Layout jerárquico con ordenación por `hubsize`, lo que causaba que las tablas se mezclaran.

-   **v2.0: Separación por Niveles**
    -   Se implementó un ordenamiento topológico para asignar un "nivel" a cada nodo.
    -   Se cambió el método de ordenación a `directed` en `pyvis` para respetar la jerarquía del flujo de datos.

-   **v2.1: Aristas Curvas**
    -   Se habilitó la opción `smooth` en `pyvis` para que las aristas fueran curvas, mejorando ligeramente la legibilidad. Sin embargo, las aristas todavía se cruzaban.

-   **v3.0: Migración a Cytoscape.js**
    -   Se reemplazó `pyvis` por `Cytoscape.js`, una librería de visualización de grafos mucho más potente.
    -   Se implementó el layout `dagre` para una jerarquía estricta y configurable.
    -   Se adoptó el estilo de aristas `unbundled-bezier`, que permite que las líneas se curven dinámicamente para evitar colisiones, resolviendo el problema del "enredo" de manera efectiva.

## Instalación

1.  **Clonar el repositorio:**
    ```bash
    git clone <URL-DEL-REPOSITORIO>
    cd <NOMBRE-DEL-REPOSITORIO>
    ```

2.  **Crear un entorno virtual (Recomendado):**
    ```bash
    # Para macOS/Linux
    python3 -m venv venv
    source venv/bin/activate

    # Para Windows
    python -m venv venv
    venv\Scripts\activate
    ```

3.  **Instalar las dependencias:**
    El proyecto requiere `pandas`, `networkx`, y `openpyxl`. Puedes instalarlos usando el archivo `requirements.txt`.
    ```bash
    pip install -r requirements.txt
    ```

## Uso

1.  **Prepara tu archivo de datos:**
    -   Asegúrate de tener un archivo Excel en la misma carpeta que el script. El nombre por defecto es `TRAZA.xlsx`.
    -   El archivo debe contener una o más hojas, cada una representando un grafo.
    -   Cada hoja debe tener las siguientes columnas:
        -   `OrigenDeImpactoTabla`
        -   `DestinoDeImpactoTabla`
        -   `TipoOrigenDeImpactoTabla` (con valores como 'INPUT', 'INTERMEDIA')
        -   `TipoDestinoDeImpactoTabla` (con valores como 'OUTPUT', 'INTERMEDIA')

2.  **Configura el script (Opcional):**
    -   Si tu archivo Excel tiene un nombre diferente, abre `analisis_de_flujo.py` y cambia el nombre en la función `main`:
        ```python
        def main():
            ruta_excel = Path('TU_OTRO_ARCHIVO.xlsx')
            # ...
        ```

3.  **Ejecuta el script:**
    ```bash
    python analisis_de_flujo.py
    ```

4.  **Abre el resultado:**
    -   El script generará un archivo HTML por cada hoja de tu Excel (ej. `malla_grafica_Flujo1.html`).
    -   Abre este archivo en tu navegador web para ver e interactuar con tu grafo.
