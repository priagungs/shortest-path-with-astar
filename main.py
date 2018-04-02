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
        while(len(self.queue) != 0):
            curr = self.queue.pop(0)
            if(curr[0] == destNode):
                break
            for idx in range(len(self.adjMatrix[curr[0]])):
                if(self.adjMatrix[initNode][idx] != -999):
                    self.queue.append([idx, self.adjMatrix[initNode][idx] + self.heurMatrix[idx][destNode] + curr[1], curr[2].append(idx)])
                    self.queue.sort(key = lambda x : x[1])
        return curr[2], curr[0]                    
        