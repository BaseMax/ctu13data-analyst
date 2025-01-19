import os
import pandas as pd
import igraph as ig

dataset_dir = r'C:\Users\MAX\Downloads\ctu-dataset'

def create_graph_from_binetflow(binetflow_file):
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

def calculate_graph_attributes(g):
    print("Calculating graph parameters...")
    attributes = {}

    attributes['degree'] = g.degree()
    attributes['in_degree'] = g.indegree()
    attributes['out_degree'] = g.outdegree()

    attributes['closeness'] = g.closeness()

    attributes['eigenvector'] = g.eigenvector_centrality()

    attributes['pagerank'] = g.pagerank()

    attributes['alpha_centrality'] = g.alpha_centrality(alpha=0.1)

    return attributes

def save_results_to_csv(file_name, attributes):
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
