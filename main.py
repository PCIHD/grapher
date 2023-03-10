from dash import Dash, html
import dash_cytoscape as cyto
import pandas as pd

node_list = [('N1','N2'),('N2','N3')]
nodes_df = pd.DataFrame(node_list,columns = ['source','target'])
print(nodes_df)

source_nodes = nodes_df[~nodes_df['source'].isin(nodes_df['target'].to_list())]['source'].to_list()
print(source_nodes)
# gets target nodes of a currently being processed node.
def get_child(node_id:str):
    return nodes_df[nodes_df['source']==node_id]['target'].to_list()

def recurse_node_fetch(dag:dict,node_queue:list):
    print('in recursion',node_queue)
    if node_queue:
        return dag
    node = node_queue.pop()
    dag[node] = {'id':node,'source_id':[], 'target_id':[]}
    node_children = get_child(node)
    print('Node children',node_children)
    if node_children:
        dag[node]['target_id'].append(node_children)
        node_queue.extend(node_children)
        return recurse_node_fetch(dag,node_queue)


def parse_root_nodes(source_nodes:list):
    dags = []
    while source_nodes:
        node = source_nodes.pop()
        dag = {}
        dags.append(recurse_node_fetch(dag,[node]))
    print(dags)

parse_root_nodes(source_nodes)
app = Dash(__name__)


# app.layout = html.Div([
#     html.P("Dash Cytoscape:"),
#     cyto.Cytoscape(
#         id='cytoscape',
#         elements=[
#             {'data': {'id': 'ca', 'label': 'Canada'}},
#             {'data': {'id': 'on', 'label': 'Ontario'}},
#             {'data': {'id': 'qc', 'label': 'Quebec'}},
#             {'data': {'source': 'ca', 'target': 'on'}},
#             {'data': {'source': 'ca', 'target': 'qc'}}
#         ],
#         layout={'name': 'breadthfirst'},
#         style={'width': '400px', 'height': '500px'}
#     )
# ])
#
#
# app.run_server(debug=True)