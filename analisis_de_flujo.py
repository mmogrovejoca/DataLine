import pandas as pd
import networkx as nx
import json
from pathlib import Path

def filter_data(group):
    """Filtra los datos según los criterios especificados."""
    print("Filtrando datos...")
    return group[
        (group['TipoOrigenDeImpactoTabla'].isin(['OUTPUT', 'INTERMEDIA', 'INPUT'])) |
        (group['TipoDestinoDeImpactoTabla'].isin(['OUTPUT', 'INTERMEDIA', 'INPUT']))
    ].drop_duplicates(subset=['OrigenDeImpactoTabla', 'DestinoDeImpactoTabla'])
def create_graph(df_filtered):
    """Crea un grafo dirigido a partir de los datos filtrados."""
    print("Creando grafo...")
    G = nx.DiGraph()
    edges = df_filtered[['OrigenDeImpactoTabla', 'DestinoDeImpactoTabla']].drop_duplicates()
    G.add_edges_from(edges.itertuples(index=False, name=None))

    # Calcular niveles usando ordenamiento topológico
    try:
        topo_sort = list(nx.topological_sort(G))
        levels = {node: 0 for node in topo_sort}
        for node in topo_sort:
            for pred in G.predecessors(node):
                levels[node] = max(levels[node], levels[pred] + 1)
        nx.set_node_attributes(G, levels, 'level')
    except nx.NetworkXUnfeasible:
        # Si hay un ciclo, no se puede hacer ordenamiento topológico
        print("El grafo contiene ciclos, no se puede usar ordenamiento topológico.")
        pass

    return nx.relabel_nodes(G, str)

def main():
    ruta_excel = Path('TRAZA.xlsx')
    hojas = pd.read_excel(ruta_excel, sheet_name=None)

    # Cargar la plantilla HTML
    with open('template.html', 'r', encoding='utf-8') as f:
        template_html = f.read()

    for nombre_hoja, df in hojas.items():
        df_filtered = filter_data(df)
        G = create_graph(df_filtered)

        # Preparar datos para Cytoscape.js
        graph_data = {
            "nodes": [],
            "edges": []
        }

        for node, attrs in G.nodes(data=True):
            node_id = str(node)
            tipo_origen = df_filtered[df_filtered['OrigenDeImpactoTabla'] == node_id]['TipoOrigenDeImpactoTabla'].values
            tipo_destino = df_filtered[df_filtered['DestinoDeImpactoTabla'] == node_id]['TipoDestinoDeImpactoTabla'].values

            color = '#bdc3c7' # gris por defecto
            if 'OUTPUT' in tipo_destino:
                color = '#2ecc71'  # verde
            elif 'INPUT' in tipo_origen:
                color = '#ff8400'  # naranja

            graph_data["nodes"].append({
                "data": {
                    "id": node_id,
                    "label": node_id,
                    "level": attrs.get('level', 0),
                    "color": color
                }
            })

        for source, target in G.edges():
            graph_data["edges"].append({
                "data": {
                    "source": str(source),
                    "target": str(target)
                }
            })

        # Inyectar los datos JSON en la plantilla
        final_html = template_html.replace('__GRAPH_DATA__', json.dumps(graph_data, ensure_ascii=False, indent=4))

        output_file = Path(f'malla_grafica_{nombre_hoja}.html')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(final_html)

        print(f"Archivo HTML generado: {output_file}")
if __name__ == "__main__":
    main()
