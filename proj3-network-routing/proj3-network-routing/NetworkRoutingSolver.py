#!/usr/bin/python3


from CS312Graph import *
import time
from UnsortedArray import *
from BinaryHeap import *


class NetworkRoutingSolver:
    def __init__( self ):
        pass

    def initializeNetwork( self, network ):
        assert( type(network) == CS312Graph )
        self.network = network

    def getShortestPath(self, destIndex):
        self.dest = destIndex

        # TODO: RETURN THE SHORTEST PATH FOR destIndex
        #       INSTEAD OF THE DUMMY SET OF EDGES BELOW
        #       IT'S JUST AN EXAMPLE OF THE FORMAT YOU'LL 
        #       NEED TO USE

        path_edges = []
        total_length = 0
        currNode = self.network.nodes[destIndex]

        while currNode.node_id != self.source:
            if currNode.prev == None:
                path_edges = []
                return {'cost': float("inf"), 'path': path_edges}
            previous_node = self.network.nodes[currNode.prev]
            for edge in previous_node.neighbors:
                if edge.dest.node_id == currNode.node_id:
                    #YAY!!!!
                    path_edges.append((edge.src.loc, edge.dest.loc, '{:.0f}'.format(edge.length)))
                    total_length += edge.length
            currNode = previous_node


        return {'cost': total_length, 'path': path_edges}







    def computeShortestPaths( self, srcIndex, use_heap=False ):
        myQ = None
        for node in self.network.nodes:
            node.dist = float("inf")
            node.prev = None
        if use_heap == False:
            myQ = UnsortedArray()
        else:
            myQ = BinaryHeap()
        self.source = srcIndex
        t1 = time.time()
        self.network.nodes[srcIndex].dist = 0
        H = myQ.makequeue(self.network.nodes, self.network)
        while len(H) != 0:
            x = myQ.deletemin(H, self.network)
            if(use_heap):
                H = myQ.bubbleDown(self.network, H, x)
            u = self.network.nodes[x]
            for edge in u.neighbors:
                if edge.dest.dist > u.dist + edge.length:
                    self.network.nodes[edge.dest.node_id].dist = u.dist + edge.length
                    self.network.nodes[edge.dest.node_id].prev = u.node_id
                    if(use_heap):
                        H = myQ.decreasekey(H, edge.dest.node_id, self.network)

        t2 = time.time()
        return (t2-t1)




