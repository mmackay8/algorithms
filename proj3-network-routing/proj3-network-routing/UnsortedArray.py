#!usr/bin/python3

class UnsortedArray:
    def __init__(self):
        self.array = []

    def makequeue(self, allNodes, network):
        for i in allNodes:
            self.array.append(i.node_id)
        return self.array

    def deletemin(self, H, network):
        min_dist = float("inf")
        min_index = 0
        for i in range(len(H)):
            if network.nodes[H[i]].dist < min_dist:
                min_dist = network.nodes[H[i]].dist
                min_index = i
        return H.pop(min_index)