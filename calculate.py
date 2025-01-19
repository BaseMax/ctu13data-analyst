import os
import numpy as np
import pandas as pd
import igraph as ig
from typing import Dict

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
    A = g.get_adjacency().data
    degree_matrix = np.diag(g.degree())
    I = np.identity(len(g.vs))

    # (I - alpha * A) * c = degree_vector
    M = I - alpha * np.array(A)
    degree_vector = np.array(g.degree())
    
    centrality = np.linalg.solve(M, degree_vector)
    
    return {g.vs[i]['name']: centrality[i] for i in range(len(g.vs))}


def create_graph_from_binetflow(binetflow_file: str) -> ig.Graph:
    """
    Create a directed graph from a .binetflow file.

    :param binetflow_file: str
        Path to the .binetflow file.
    :return: igraph.Graph object
        The graph created from the binetflow data.
    """
    print("Reading the .binetflow file...")
    df = pd.read_csv(binetflow_file, sep=',', header=0)

    print("Creating the graph...")
    src_ip_column = 'SrcAddr'
    dst_ip_column = 'DstAddr'
    
    g = ig.Graph(directed=True)

    ip_addresses = pd.concat([df[src_ip_column], df[dst_ip_column]]).unique()
    g.add_vertices(ip_addresses)

    for _, row in df.iterrows():
        src_ip = row[src_ip_column]
        dst_ip = row[dst_ip_column]
        g.add_edge(src_ip, dst_ip)
    
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

    attributes['degree'] = g.degree()

    attributes['in_degree'] = g.indegree()

    attributes['out_degree'] = g.outdegree()

    attributes['closeness'] = g.closeness()

    attributes['eigenvector'] = g.eigenvector_centrality()

    attributes['pagerank'] = g.pagerank()

    attributes['alpha_centrality'] = calculate_alpha_centrality(g, alpha=0.1)

    return attributes


def save_results_to_csv(file_name: str, attributes: Dict[str, any]) -> None:
    """
    Save the calculated graph attributes to a CSV file.

    :param file_name: str
        The name of the CSV file to save the results to.
    :param attributes: dict
        The graph attributes to save.
    """
    results_df = pd.DataFrame(attributes)
    
    results_df.to_csv(file_name, index=False)
    print(f"Results saved to {file_name}")


for root, dirs, files in os.walk(dataset_dir):
    print(f"Processing directory: {root}")

    if not root.endswith("\\5"):
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
