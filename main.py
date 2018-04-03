from copy import deepcopy
from random import randint
class Graph:
    def __init__(self, adjMatrix, heurMatrix, nodes):
        self.adjMatrix = adjMatrix # adjMatrix[x][y] = cost from x to y
        self.heurMatrix = heurMatrix # heurMatrix[x][y] = cost from x to y heuristically
        self.nodes = nodes # array of nodes, translation from actual name of node to number from 0..n 

        # queue[0] = current node
        # queue[1] = f(x) = total cost + heuristic cost to destination
        # queue[2] = list of nodes that are passed from initial node to current node
        self.queue = []

    def AStar(self, initNode, destNode):
        self.queue.append([initNode, 0, [initNode]])
        curr = []
        # visitedNode = []
        i = 1
        while(len(self.queue) != 0):
            curr = self.queue.pop(0)
            print(i)
            i+=1
            print(curr)
            if(curr[0] == destNode):
                break
            for idx in range(len(self.adjMatrix[curr[0]])):
                if(self.adjMatrix[curr[0]][idx] != -999):
                    # visitedNode = deepcopy(curr[2])
                    self.queue.append([idx, self.adjMatrix[curr[0]][idx] + self.heurMatrix[idx][destNode] + curr[1], curr[2].append(idx)])
                    print(self.queue[len(self.queue)-1])
                    self.queue.sort(key = lambda x : x[1])
        return curr[2], curr[0]
    
    def ConvertAdjMatrix(self):
        res = []
        for id1 in range(len(self.nodes)):
            for id2 in range(len(self.nodes)):
                if(self.adjMatrix[id1][id2] != -999):
                    res.append((self.nodes[id1],self.nodes[id2],self.adjMatrix[id1][id2]))
        return res

import networkx as nx
import matplotlib.pyplot as plt

nodes = [1,2,3,4]
adj = [
    [-999, 3, 1, -999],
    [3, -999, 5, 4],
    [1, 5, -999, 2],
    [-999, 4, 2, -999]
]

heu = [
    [0, 3, 1, 5],
    [3, 0, 5, 4],
    [1, 5, 0, 2],
    [5, 4, 2, 0]
]

myGraph = Graph(adj, heu, nodes)

visitedNodes, cost = myGraph.AStar(myGraph.nodes.index(1), myGraph.nodes.index(4))
print(visitedNodes)
print(cost)

G = nx.Graph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(myGraph.ConvertAdjMatrix())
labels = nx.get_edge_attributes(G, 'weight')
pos = {}
for node in nodes:
    temp = (randint(0,1000), randint(0,1000))
    while temp in pos.values():
        temp = (randint(0,1000), randint(0,1000))
    pos[node] = temp
nx.draw(G,pos,with_labels=True, font_weight='bold')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
plt.show()

