# CTU13 Data Analyst

This repository contains two Python scripts, `draw.py` and `calculate.py`, that analyze network traffic data from the CTU-13 dataset. The scripts create and visualize network graphs and calculate several graph attributes such as centrality measures.

## Files Overview

### `draw.py`

This script reads `.binetflow` files from the CTU-13 dataset, creates directed network graphs using the `networkx` library, and visualizes the graphs. It saves the resulting graph as PNG images.

#### Functionality:

- Reads the `.binetflow` files.
- Constructs a directed graph where nodes represent IP addresses and edges represent communication between them.
- Visualizes the graph using `matplotlib` and saves it as a PNG file.

#### How it works:

1. The script loops through directories in the specified dataset directory.
2. For each `.binetflow` file, it creates a directed graph using `networkx`.
3. The graph is then drawn using `matplotlib` and saved as a PNG image.

#### Example Usage:

```bash
python draw.py
```

### `calculate.py`

This script calculates various graph metrics, including degree, centrality measures, and page rank, from `.binetflow` data files using the `igraph` library. It saves these metrics in CSV format.

#### Functionality:
- Creates a directed graph using `igraph`.
- Calculates graph attributes such as:
  - Degree
  - In-degree
  - Out-degree
  - Closeness centrality
  - Eigenvector centrality
  - PageRank
  - Alpha centrality
- Saves the results as CSV files for further analysis.

#### How it works:
1. The script iterates through the specified dataset directory.
2. For each `.binetflow` file, it creates a graph and calculates the desired metrics.
3. The results are saved as a CSV file in the same directory.

#### Example Usage:

```bash
python calculate.py
```

## Note on Graph Visualization

Due to the enormous size of the graph generated from the dataset, it is almost impossible to draw and save it as a single image. The sheer number of nodes and edges would make the visualization process computationally expensive and result in images that are impractical to analyze.

Therefore, instead of attempting to draw the graph, we focus on calculating and extracting the necessary graph parameters (such as degree, centrality measures, etc.) and save these values in a CSV file for further analysis. This approach allows us to efficiently handle large-scale graphs and derive meaningful insights without the need for expensive and impractical visualizations.

### Wireshark and Npcap Installation

To analyze the network traffic data from the CTU-13 dataset, you can utilize Wireshark, a powerful network protocol analyzer. It allows you to capture and inspect network packets, making it easier to debug and explore network traffic.

#### Wireshark Installation

1. Download the Wireshark installer from the official website:  
   [Wireshark 4.4.3 (Windows)](https://2.na.dl.wireshark.org/win64/Wireshark-4.4.3-x64.exe)

2. During installation, you will be prompted to install **Npcap**, a packet capture library. It is highly recommended to install it, as it allows Wireshark to capture network traffic and perform real-time analysis.

3. Follow the installation steps, and once complete, you can start analyzing the `.binetflow` files and other network capture data in the CTU-13 dataset with Wireshark.

#### Npcap Installation

Npcap is an essential component for network capture and is included in the Wireshark installation process. If you decide to install Wireshark, make sure that the **Npcap** option is selected during the setup. If you prefer to install Npcap separately, you can download it here:  
[Npcap Download](https://nmap.org/npcap/)

Once installed, Npcap will allow you to capture network data using tools like Wireshark or other compatible software.

## Installation

You can install the necessary dependencies using `pip`:

```bash
pip install pandas networkx igraph matplotlib numpy
```

## Contributing

Feel free to fork the repository, submit pull requests, or open issues if you have any improvements or suggestions. Contributions are welcome!

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

Copyright 2025, Max Base
