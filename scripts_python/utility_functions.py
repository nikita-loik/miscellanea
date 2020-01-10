import numpy as np
import networkx as nx
import matplotlib
from matplotlib import pyplot as plt
plt.style.use('fivethirtyeight')



# SET LOGGER ==================================================================
import logging
logging.basicConfig(
    level=logging.INFO,
    format='%(levelname)s: %(asctime)s: %(filename)s: %(lineno)s:\n%(message)s')
logger = logging.getLogger(__name__)

# =============================================================================
population_size = 50
g_ratio = 0.5
max_partners = 5

def simulate_population(
        population_size: int = 50,
        b_ratio: float = .5,
        max_partners: int = 5,
        ):
    # Simulate population of boys and girls.
    boys = []
    girls = []
    for i in range(population_size):
        gender = np.random.choice(
            ['b', 'g'],
            p=[b_ratio, 1 - b_ratio],
            replace=True)

        if gender == 'b':
            boys.append(len(boys))
        else:
            girls.append(len(girls))
    print(
        f"boys # {len(boys)}\n"
        f"girls # {len(girls)}")


    # Convert population into a bipartite graph.
    g = nx.Graph()
    g.add_nodes_from(
        [f'b_{i}' for i in boys],
        bipartite=0)
    g.add_nodes_from(
        [f'g_{j}' for j in girls],
        bipartite=1)

    # Add random connections between boys and girls.
    boys = [i for i, d in g.nodes(data=True) if d['bipartite']==0]
    girls = [j for j, d in g.nodes(data=True) if d['bipartite']==1]
    for i in boys:
        partners_n = np.random.randint(max_partners)
        partners = np.random.choice(
            girls,
            partners_n,
            replace=False)
        for j in partners:
            g.add_edge(i, j)

    average_n_partners_boys =  g.number_of_edges() / len(boys)
    average_n_partners_girls = g.number_of_edges() / len(girls)

    print(
        f"average # partners per boy: {average_n_partners_boys:.2f}\n"
        f"average # partners per girl: {average_n_partners_girls:.2f}")
    return g


def plot_population_graph(
        g: nx.classes.graph.Graph
        ):

    boys = [i for i, d in g.nodes(data=True) if d['bipartite']==0]
    girls = [j for j, d in g.nodes(data=True) if d['bipartite']==1]

    plt.figure(figsize=(12,8))
    for i in boys:
        plt.scatter(0, int(i[2:]), c='b', s=100, alpha=0.5)
    for j in girls:
        plt.scatter(1, int(j[2:]), c='r', s=100, alpha=0.5)
        
    for partnership in g.edges():
        coordinates = [
            (0, int(partnership[0][2:])),
            (1, int(partnership[1][2:]))
            ]
        plt.plot(coordinates, c='gray',lw=1)
    text_y = round(max(len(boys), len(girls)) * 1.05)
    plt.text(x=0, y=text_y, s='boys', ha='center')
    plt.text(x=1, y=text_y, s='girls', ha='center')
    plt.axis('off')
    plt.xlim([-1, 2])

    plt.show()