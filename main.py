from copy import deepcopy
from random import randint
import networkx as nx
import matplotlib.pyplot as plt
from math import *
from copy import deepcopy
import sys

AVG_EARTH_RADIUS = 6371

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
            if(curr[0] == destNode):
                break
            for idx in range(len(self.adjMatrix[curr[0]])):
                if(self.adjMatrix[curr[0]][idx] != -999):
                    visitedNode = deepcopy(curr[2])
                    visitedNode.append(idx)
                    self.queue.append([idx, self.adjMatrix[curr[0]][idx] + self.heurMatrix[idx][destNode] + curr[1], visitedNode])
                    self.queue.sort(key = lambda x : x[1])
        return curr[2]
    
    def hitungCost(self, visitedNodes):
        cost = 0
        for idx in range(len(visitedNodes)-1):
            cost += self.adjMatrix[visitedNodes[idx]][visitedNodes[idx+1]]
        return cost

    def ConvertAdjMatrix(self):
        res = []
        for id1 in range(len(self.nodes)):
            for id2 in range(len(self.nodes)):
                if(self.adjMatrix[id1][id2] != -999):
                    res.append((self.nodes[id1],self.nodes[id2], round(self.adjMatrix[id1][id2], 3)))
        return res

def haversineDistance(P, Q):
    # Menghitung jarak antar 2 titik koordinat di permukaan bumi
    # Referensi kode dari https://pypi.python.org/pypi/haversine
    # convert titik dari desimal ke radian
    P1 = deepcopy(P)
    P2 = deepcopy(Q)
    P1[0], P1[1], P2[0], P2[1] = map(radians, (P1[0], P1[1], P2[0], P2[1]))
    # haversine process
    y = P2[0] - P1[0]
    x = P2[1] - P1[1]
    a = sin(y * 0.5) ** 2 + cos(P1[0]) * cos(P2[0]) * sin(x * 0.5) ** 2
    result = 2 * AVG_EARTH_RADIUS * asin(sqrt(a))
    return result

def readFile(filename):
    # Membaca sekaligus parsing dari file input untuk membaca koordinat setiap titik dan hubungan antar titik
    fin = open(filename,'r')
    n = int(fin.readline())
    Points = []
    PointName = []
    for i in range (0,n):
        line = fin.readline().split()
        PointName.append(line[0])
        Point = [float(line[1]), float(line[2])]
        Points.append(Point)
    Adjs = []
    for i in range (0,n):
        line = fin.readline().split()
        Adjs.append(line[1:len(line)])
    return Points, PointName, Adjs

def makeAdjMatrix(Points,PointName,Adjs):
    # Membuat Matriks ketetanggan dengan bobotnya adalah jarak
    AdjMat = []
    N = len(Points)
    for i in range(0,N):
        AdjArr = []
        for j in range(0,N):
            if (PointName[j] in Adjs[i]):
                AdjArr.append(haversineDistance(Points[i],Points[j]))
            else:
                AdjArr.append(-999)
        AdjMat.append(AdjArr)
    return AdjMat

def makeHeurMatrix(Points):
    # Membuat Matriks heuristik
    HeurMat = []
    N = len(Points)
    for i in range(0,N):
        HeurArr = []
        for j in range(0,N):
            if (i != j):
                HeurArr.append(haversineDistance(Points[i],Points[j]))
            else:
                HeurArr.append(-999)
        HeurMat.append(HeurArr)
    return HeurMat

#main
print("Pilih area (1/2)")
print("1. Sekitar ITB")
print("2. Sekitar Alun-Alun")
Z = int(input("Masukan pilihan: "))
if (Z==1):
    Points, PointName, Adjs = readFile("itb.txt")
elif (Z==2):
    Points, PointName, Adjs = readFile("alun.txt")
else:
    print("Pilihan tidak dikenali")
    sys.exit()
AdjMat = makeAdjMatrix(Points,PointName,Adjs)
HeurMat = makeHeurMatrix(Points)

#nodes = [1,2,3,4]
#adj = [
#    [-999, 3, 1, -999],
#    [3, -999, 5, 4],
#    [1, 5, -999, 2],
#    [-999, 4, 2, -999]
#]

#heu = [
#    [0, 3, 1, 5],
#    [3, 0, 5, 4],
#    [1, 5, 0, 2],
#    [5, 4, 2, 0]
#]

nodes = PointName
myGraph = Graph(AdjMat, HeurMat, PointName)

visitedNodes = myGraph.AStar(0, 4)
cost = myGraph.hitungCost(visitedNodes)

print(visitedNodes)
print(cost)

G = nx.Graph()
nodelistVisited = []
nodelist = []
for node in nodes:
    if(nodes.index(node) in visitedNodes):
        nodelistVisited.append(node)
    else:
        nodelist.append(node)
convertedAdjMatrix = myGraph.ConvertAdjMatrix()
edgesForVisited = []
edgesForNonVisited = []
for el in convertedAdjMatrix:
    if(nodes.index(el[0]) in visitedNodes and nodes.index(el[1]) in visitedNodes):
        edgesForVisited.append(el)
    else:
        edgesForNonVisited.append(el)
G.add_weighted_edges_from(convertedAdjMatrix)
labels = nx.get_edge_attributes(G, 'weight')
pos = {}
for idx in range(len(nodes)):
    pos[nodes[idx]] = (Points[idx][1]*10000, Points[idx][0]*10000)
nx.draw(G,pos,nodelist=nodelistVisited, with_labels=True, font_weight='bold', node_color='b')
nx.draw(G,pos,nodelist=nodelist, with_labels=True, font_weight='bold', node_color='r')
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
nx.draw_networkx_edges(G, pos, edgelist=edgesForVisited, width=8,alpha=0.5,edge_color='b')
nx.draw_networkx_edges(G, pos, edgelist=edgesForNonVisited, width=8,alpha=0.5,edge_color='r')
plt.show()

