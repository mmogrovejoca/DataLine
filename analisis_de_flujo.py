import pandas as pd
import networkx as nx
from pyvis.network import Network
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

def customize_network(net, df_filtered):
    """Personaliza la red con colores y opciones específicas."""
    print("Personalizando red...")
    # Asignar niveles a los nodos en la red de pyvis
    for node in net.nodes:
        node_id = node['id']
        if 'level' in net.get_node(node_id):
            node['level'] = net.get_node(node_id)['level']

        tipo_origen = df_filtered[df_filtered['OrigenDeImpactoTabla'] == node_id]['TipoOrigenDeImpactoTabla'].values
        tipo_destino = df_filtered[df_filtered['DestinoDeImpactoTabla'] == node_id]['TipoDestinoDeImpactoTabla'].values
        if 'OUTPUT' in tipo_destino:
            node['color'] = '#2ecc71'  # verde
        elif 'INPUT' in tipo_origen:
            node['color'] = "#ff8400"  # naranja
        else:
            node['color'] = '#bdc3c7'  # gris
        node['physics'] = False
        node['fixed'] = {'x': False, 'y': False}

    net.set_options('''
    {
      "layout": {
        "hierarchical": {
          "enabled": true,
          "direction": "LR",
          "sortMethod": "directed",
          "nodeSpacing": 200,
          "levelSeparation": 200
        }
      },
      "physics": {
        "hierarchicalRepulsion": {
          "nodeDistance": 200,
          "centralGravity": 0.0,
          "springLength": 200,
          "springConstant": 0.01,
          "damping": 0.09
        },
        "solver": "hierarchicalRepulsion"
      }
    }
    ''')
def insert_search_controls(output_file):
    """Inserta controles de búsqueda en el archivo HTML."""
    print(f"Insertando controles de búsqueda en {output_file}...")
    with open(output_file, 'r', encoding='utf-8') as file:
        html_content = file.read()
    search_controls = '''
    <div class="flex-container">
        <div>
            <h2>Buscar Tabla</h2>
            <input type="text" id="searchInput" placeholder="Buscar por nombre de tabla...">
            <button id="searchButton" onclick="searchTable()">Buscar</button>
            <button id="resetButton" onclick="resetGraph()">Restaurar Vista</button>
        </div>
    </div>
    <div id="consumptionTables"></div>
    '''
    html_content = html_content.replace('<div id="mynetwork"', search_controls + '<div id="mynetwork"')
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(html_content)
def add_tables_and_scripts(output_file, df_filtered):
    """Agrega tablas y scripts al archivo HTML."""
    print(f"Agregando tablas y scripts a {output_file}...")
    input_tables = df_filtered[df_filtered['TipoOrigenDeImpactoTabla'] == 'INPUT'][['OrigenDeImpactoTabla']].drop_duplicates()
    output_tables = df_filtered[df_filtered['TipoDestinoDeImpactoTabla'] == 'OUTPUT'][['DestinoDeImpactoTabla']].drop_duplicates()
    intermediate_tables = df_filtered[df_filtered['TipoOrigenDeImpactoTabla'] == 'INTERMEDIA'][['OrigenDeImpactoTabla']].drop_duplicates()
    with open(output_file, 'a', encoding='utf-8') as f:
        f.write('''
        <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            margin: 40px;
            background-color: #f9fafc;
            color: #2c3e50;
        }
        h2, h3 {
            color: #2c3e50;
            margin-bottom: 10px;
        }
        input[type="text"] {
            width: 60%;
            padding: 12px;
            margin: 10px 10px 20px 0;
            border: 1px solid #ccc;
            border-radius: 6px;
            font-size: 16px;
        }
        button {
            padding: 12px 20px;
            margin: 10px 5px 20px 0;
            border: none;
            background-color: #3498db;
            color: white;
            border-radius: 6px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s ease;
        }
        button:hover {
            background-color: #2980b9;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 30px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
            background-color: white;
            border-radius: 6px;
            overflow: hidden;
        }
        th, td {
            padding: 12px 15px;
            text-align: left;
            border-bottom: 1px solid #eee;
        }
        th {
            background-color: #3498db;
            color: white;
            font-weight: 600;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #eaf6ff;
        }
        .flex-container {
            display: flex;
            justify-content: space-between;
            gap: 20px;
            margin-top: 30px;
        }
        .flex-container > div {
            flex: 1;
        }
        </style>
        <hr>
        <h2>Tablas por Tipo</h2>
        <div class="flex-container">
            <div>
                <h3>INPUT</h3>
                ''' + input_tables.to_html(index=False) + '''
            </div>
            <div>
                <h3>OUTPUT</h3>
                ''' + output_tables.to_html(index=False) + '''
            </div>
            <div>
                <h3>INTERMEDIAS</h3>
                ''' + intermediate_tables.to_html(index=False) + '''
            </div>
        </div>
        <hr>
        <script type="text/javascript">
        function searchTable() {
            var input = document.getElementById("searchInput").value.toUpperCase();
            var tables = document.querySelectorAll("table");
            for (let table of tables) {
                let rows = table.getElementsByTagName("tr");
                for (let row of rows) {
                    let cell = row.getElementsByTagName("td")[0];
                    if (cell) {
                        let txtValue = cell.textContent || cell.innerText;
                        row.style.display = txtValue.toUpperCase().indexOf(input) > -1 ? "" : "none";
                    }
                }
            }
            highlightNode(input);
        }
        function highlightNode(nodeId) {
            if (typeof network !== 'undefined') {
                let found = false;
                for (let node in network.body.nodes) {
                    let nodeObj = network.body.nodes[node];
                    let label = nodeObj.options.label;
                    if (label && label.toUpperCase() === nodeId) {
                        found = true;
                        const originalColor = nodeObj.options.color;
                        const originalSize = nodeObj.options.size || 10;
                        // Asegúrate de que el nodo no esté oculto
                        nodeObj.hidden = false;
                        // Centra la vista en el nodo
                        network.focus(node, {
                            scale: 1.5,
                            animation: { duration: 1000, easingFunction: "easeInOutQuad" }
                        });
                        // Resalta el nodo
                        nodeObj.setOptions({
                            color: { background: '#ff0000', border: '#ff0000' },
                            size: 20
                        });
                        setTimeout(() => {
                            nodeObj.setOptions({
                                color: originalColor,
                                size: originalSize
                            });
                        }, 3000);
                        var visibleNodes = new Set([node]);
                        // Función para realizar DFS y encontrar nodos de tipo INPUT
                        function dfs(node, visited, level, levels) {
                            visited.add(node);
                            if (!levels[level]) {
                                levels[level] = new Set();
                            }
                            levels[level].add(node);
                            var connectedFrom = network.getConnectedNodes(node, 'from');
                            for (let connectedNode of connectedFrom) {
                                if (!visited.has(connectedNode)) {
                                    dfs(connectedNode, visited, level + 1, levels);
                                }
                            }
                        }
                        // Realizar DFS desde el nodo inicial
                        var levels = {};
                        dfs(node, visibleNodes, 0, levels);
                        var allNodes = network.body.data.nodes.get();
                        var updateArray = [];
                        for (let n of allNodes) {
                            updateArray.push({
                                id: n.id,
                                hidden: !visibleNodes.has(n.id)
                            });
                        }
                        network.body.data.nodes.update(updateArray);
                        // Mostrar tablas de consumo por nivel
                        var consumptionTablesHTML = "<h3>Tablas de Consumo por Nivel:</h3>";
                        for (let level in levels) {
                            consumptionTablesHTML += `<h4>Nivel ${level}:</h4><ul>`;
                            levels[level].forEach(node => {
                                consumptionTablesHTML += `<li>${network.body.nodes[node].options.label}</li>`;
                            });
                            consumptionTablesHTML += "</ul>";
                        }
                        document.getElementById("consumptionTables").innerHTML = consumptionTablesHTML;
                        break;
                    }
                }
                if (!found) {
                    alert("Tabla no encontrada en el grafo.");
                }
            }
        }
        function resetGraph() {
            if (typeof network !== 'undefined') {
                var allNodes = network.body.data.nodes.get();
                var updateArray = [];
                for (let n of allNodes) {
                    updateArray.push({
                        id: n.id,
                        hidden: false
                    });
                }
                network.body.data.nodes.update(updateArray);
                document.getElementById("consumptionTables").innerHTML = "";
            }
        }
        </script>
        ''')
def main():
    ruta_excel = Path('TRAZA.xlsx')
    hojas = pd.read_excel(ruta_excel, sheet_name=None)
    for nombre_hoja, df in hojas.items():
        df_filtered = filter_data(df)
        G = create_graph(df_filtered)
        net = Network(height='750px', width='100%', directed=True, notebook=False)
        net.from_nx(G)
        net.toggle_physics(False)
        customize_network(net, df_filtered)
        output_file = Path(f'malla_grafica_{nombre_hoja}.html')
        net.save_graph(str(output_file))
        insert_search_controls(output_file)
        add_tables_and_scripts(output_file, df_filtered)
        print(f"Archivo generado: {output_file}")
if __name__ == "__main__":
    main()
