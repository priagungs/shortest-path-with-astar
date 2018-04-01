class Graph:
    def __init__(self, adjMatrix, heurMatrix, nodes):
        self.adjMatrix = adjMatrix
        self.heurMatrix = heurMatrix
        self.nodes = nodes
        self.queue = []
    
    def AStar(self, initNode, destNode):
        self.queue.append([initNode, 0, [initNode]])
        curr = []
        while(len(self.queue) != 0):
            curr = self.queue.pop(0)
            if(curr[0] == destNode):
                break
            for idx in range(len(self.adjMatrix[curr[0]])):
                if(self.adjMatrix[initNode][idx] != -999):
                    queue.append([idx, self.adjMatrix[initNode][idx] + self.heurMatrix[idx][destNode] + curr[1], curr[2].append(idx)])
                    queue.sort(key = lambda x : x[1])
        return curr[2], curr[0]                    
        