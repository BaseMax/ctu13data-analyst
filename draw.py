import os
import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

dataset_dir = r'C:\Users\MAX\Downloads\ctu-dataset'

def create_graph_from_binetflow(binetflow_file):
    print("Reading the .binetflow file...")
    df = pd.read_csv(binetflow_file, sep=',', header=0)

    print("Creating the graph...")
    src_ip_column = 'SrcAddr'
    dst_ip_column = 'DstAddr'
    
    G = nx.DiGraph()

    for _, row in df.iterrows():
        src_ip = row[src_ip_column]
        dst_ip = row[dst_ip_column]
        G.add_edge(src_ip, dst_ip)
    
    return G

def draw_and_save_graph(G, output_path):
    plt.figure(figsize=(12, 12))
    pos = nx.spring_layout(G, k=0.15, iterations=20)
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color="skyblue")
    nx.draw_networkx_edges(G, pos, alpha=0.7, edge_color="gray")
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold", font_color="black")
    
    plt.axis('off')
    plt.savefig(output_path, format="PNG")
    plt.close()

for root, dirs, files in os.walk(dataset_dir):
    for file in files:
        if file.endswith(".binetflow"):
            binetflow_file = os.path.join(root, file)
            print(f"Processing {binetflow_file}...")

            try:
                G = create_graph_from_binetflow(binetflow_file)
                
                output_path = os.path.join(root, f"{file}_graph.png")
                draw_and_save_graph(G, output_path)
                print(f"Saved graph to {output_path}")
            except Exception as e:
                print(f"Error processing {binetflow_file}: {e}")
