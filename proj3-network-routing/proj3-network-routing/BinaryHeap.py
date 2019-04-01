#!usr/bin/python3

class BinaryHeap:
    def __init__(self):
        self.array = []
        self.dictionary = {}

    def makequeue(self, allNodes, network):
        min = -1
        for i in allNodes:
            if i.dist == 0:
                min = i.node_id
            self.dictionary[i.node_id] = len(self.array)
            self.array.append(i.node_id)
        self.array = self.decreasekey(self.array, min, network)
        return self.array



    def deletemin(self, H, network):
        min = H[0]
        last = H[-1]
        H[-1] = min
        H[0] = last
        self.dictionary[last] = 0
        self.dictionary[min] = len(H) - 1

        return H.pop()

    def decreasekey(self, H, node_id, network):
        changedIndex = self.dictionary[node_id]
        while changedIndex > 0:
            changedNode = network.nodes[self.array[changedIndex]]
            newLocation = network.nodes[self.array[(changedIndex-1)//2]]
            if changedNode.dist < newLocation.dist:
                H = self.swap(H, changedIndex, (changedIndex -1)//2)
                changedIndex = (changedIndex - 1)//2
            else:
                break
        return H



    def swap(self, H, changedIndex, newLocation):
        first = H[changedIndex]
        newL = H[newLocation]

        H[changedIndex] = newL
        H[newLocation] = first

        self.dictionary[newL] = changedIndex
        self.dictionary[first] = newLocation


        return H

    def bubbleDown(self, network, H, node_id):
        changedIndex = 0   #self.dictionary[node_id]
        while changedIndex * 2+1 < len(H):

            opt1LocIndex = changedIndex * 2 + 1
            opt2LocIndex = changedIndex * 2 + 2
            opt1Dist = float("inf")
            opt2Dist = float("inf")
            changedNode = network.nodes[self.array[changedIndex]]
            if (changedIndex * 2 + 1) < len(H):
                newLocOpt1 = network.nodes[self.array[opt1LocIndex]]
                opt1Dist = newLocOpt1.dist
            if (changedIndex * 2 + 2) < len(H):
                newLocOpt2 = network.nodes[self.array[opt2LocIndex]]
                opt2Dist = newLocOpt2.dist
                if opt2Dist < opt1Dist:
                    opt1Dist = opt2Dist
                    opt1LocIndex = opt2LocIndex

            if changedNode.dist > opt1Dist:
                H = self.swap(H, changedIndex, opt1LocIndex)
                changedIndex = opt1LocIndex
            elif changedNode.dist > opt2Dist:
                H = self.swap(H, changedIndex, opt2LocIndex)
                changedIndex = opt2LocIndex
            else:
                break
        return H

