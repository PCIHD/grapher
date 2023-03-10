from dash import Dash, html
import dash_cytoscape as cyto
import pandas as pd

node_list = [('N1', 'N2'), ('N2', 'N3'), ('N2', 'N4'), ('N3', 'N5'), ('N5', 'N6'), ('N3', 'N7'),('N11','N2'),('N15','N16')
            ]
nodes_df = pd.DataFrame(node_list, columns=['source', 'target'])
print(nodes_df)

source_nodes = nodes_df[~nodes_df['source'].isin(nodes_df['target'].to_list())]['source'].to_list()
print(source_nodes)


# gets target nodes of a currently being processed node.
class node_traversal:
    def __init__(self, source_nodes: list):
        self.source_nodes = source_nodes

    def get_child(self, node_id: str):
        return nodes_df[nodes_df['source'] == node_id]['target'].to_list()

    def get_parents(self, node_id: str):
        return nodes_df[nodes_df['target'] == node_id]['source'].to_list()

    def recurse_node_fetch(self, dag: dict, node_queue: list):
        if len(node_queue) == 0:
            for id in dag:
                dag[id]['source_id'] = set(dag[id]['source_id'])
                dag[id]['target_id'] = set(dag[id]['target_id'])
            return dag
        node = node_queue.pop()
        if node not in dag.keys():
            dag[node] = {'id': node, 'source_id': [], 'target_id': []}
        node_children = self.get_child(node)
        print('Node children', node_children)
        if len(node_children) > 0:
            dag[node]['target_id'].extend(node_children)
            for child in node_children:
                parents = self.get_parents(child)
                if len(parents) <= 1:
                    dag[child] = {'source_id': [node], 'target_id': []}

                else:
                    dag[node]['source_id'].extend(parents)
                    [self.source_nodes.remove(x) for x in parents if x in self.source_nodes]
                    dag[child] = {'source_id': [node], 'target_id': []}
                    for parent in parents:
                        if parent not in dag.keys():
                            node_queue.append(parent)
                node_queue.extend(node_children)
            return self.recurse_node_fetch(dag, node_queue)
        return self.recurse_node_fetch(dag, node_queue)

    def parse_root_nodes(self):
        dags = []
        while self.source_nodes:
            node = source_nodes.pop()
            dag = {}
            dag = self.recurse_node_fetch(dag, [node])
            dags.append(dag)
        return dags


if __name__ == '__main__':
    dag_parser = node_traversal(source_nodes)
    dags = dag_parser.parse_root_nodes()
    print(dags)
    nodes = []
    edges = []
    print(f"{len(dags)}  dags found.")
    for dag in dags:
        for node in dag:
            nodes.append({'data': {'id': node, 'label': node}})

        for node in dag:
            curr_node = dag[node]
            for target in curr_node['target_id']:
                edges.append({'data': {'source': node, 'target': target}})
    elements = nodes + edges
    app = Dash(__name__)
    print(elements)
    app.layout = html.Div([
        html.P("Dash Cytoscape:"),
        cyto.Cytoscape(
            id='cytoscape',
            elements=elements,
            layout={'name': 'circle'},
            style={'width': '400px', 'height': '400px'},
            stylesheet=[{
                'selector': 'node',
                'style': {
                    'label': 'data(id)'
                }
            }, {
                'selector': 'edge',
                'style': {
                    'curve-style': 'bezier',

                    'target-arrow-shape': 'triangle',
                }}]
        )
    ])

    app.run_server(debug=True)
