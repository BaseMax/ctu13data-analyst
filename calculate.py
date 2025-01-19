import os
import numpy as np
import pandas as pd
import igraph as ig
from typing import Dict
from scipy.sparse import csr_matrix

dataset_dir = r'C:\Users\MAX\Downloads\ctu-dataset'


def calculate_alpha_centrality(g: ig.Graph, alpha: float = 0.1) -> Dict[str, float]:
    """
    Calculate alpha centrality of the graph's nodes.

    Alpha centrality is a measure of node importance based on the network structure,
    modified by the parameter alpha.

    :param g: igraph.Graph object
        The graph for which to calculate the alpha centrality.
    :param alpha: float, default 0.1
        The alpha parameter, which controls the weight of the adjacency matrix. 
        Should be between 0 and 1.
    :return: Dictionary of node alpha centrality scores, where the key is the node name 
             and the value is the alpha centrality score.
    """
    A = csr_matrix(g.get_adjacency().data)

    I = csr_matrix(np.identity(len(g.vs)))

    # (I - alpha * A) * c = degree_vector
    M = I - alpha * A

    degree_vector = np.array(g.degree())

    centrality = np.linalg.solve(M.toarray(), degree_vector)
    
    return {g.vs[i]['name']: centrality[i] for i in range(len(g.vs))}

def create_graph_from_binetflow(binetflow_file: str) -> ig.Graph:
    """
    Create a directed graph from a .binetflow file efficiently.

    :param binetflow_file: str
        Path to the .binetflow file.
    :return: igraph.Graph object
        The graph created from the binetflow data.
    """
    print("Reading the .binetflow file...")
    df = pd.read_csv(binetflow_file, sep=',', header=0)

    print("Creating the graph...")
    g = ig.Graph(directed=True)

    ip_addresses = np.unique(df[['SrcAddr', 'DstAddr']].values.flatten())

    print("Adding vertices...")
    g.add_vertices(ip_addresses)

    print("Filtering edges...")
    edges = [(src, dst) for src, dst in zip(df['SrcAddr'], df['DstAddr']) if src != dst]

    print("Adding edges...")
    g.add_edges(edges)

    return g

def calculate_graph_attributes(g: ig.Graph) -> Dict[str, any]:
    """
    Calculate various graph attributes.

    This function calculates the degree, in-degree, out-degree, closeness centrality,
    eigenvector centrality, pagerank, and alpha centrality of the graph.

    :param g: igraph.Graph object
        The graph to calculate the attributes for.
    :return: Dictionary containing graph attributes.
    """
    print("Calculating graph parameters...")
    attributes = {}

    print("Calculating in-degree...")
    in_degree = g.indegree()
    max_in_degree = max(in_degree) if in_degree else 1
    attributes['in_degree'] = [d / max_in_degree for d in in_degree]

    print("Calculating out-degree...")
    out_degree = g.outdegree()
    max_out_degree = max(out_degree) if out_degree else 1
    attributes['out_degree'] = [d / max_out_degree for d in out_degree]

    print("Calculating closeness...")
    attributes['closeness'] = g.closeness()

    print("Calculating eigenvector centrality...")
    attributes['eigenvector'] = g.eigenvector_centrality()

    print("Calculating pagerank...")
    attributes['pagerank'] = g.pagerank()

    # print("Calculating alpha centrality...")
    # attributes['alpha_centrality'] = calculate_alpha_centrality(g, alpha=0.1)

    return attributes

def save_results_to_csv(file_name: str, attributes: Dict[str, any]) -> None:
    """
    Save the calculated graph attributes to a CSV file.

    :param file_name: str
        The name of the CSV file to save the results to.
    :param attributes: dict
        The graph attributes to save.
    """
    print("Saving results to CSV...")

    results_df = pd.DataFrame(attributes)
    
    results_df.to_csv(file_name, index=False)
    print(f"Results saved to {file_name}")


for root, dirs, files in os.walk(dataset_dir):
    print(f"Processing directory: {root}")

    if not root.endswith("\\11"):
        continue

    for file in files:
        if file.endswith(".binetflow"):
            binetflow_file = os.path.join(root, file)
            print(f"Processing {binetflow_file}...")

            try:
                g = create_graph_from_binetflow(binetflow_file)
                
                attributes = calculate_graph_attributes(g)

                result_file = os.path.join(root, f"{file}_attributes.csv")
                save_results_to_csv(result_file, attributes)
                
            except Exception as e:
                print(f"Error processing {binetflow_file}: {e}")
