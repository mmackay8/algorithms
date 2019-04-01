

from PyQt5.QtCore import QLineF, QPointF, QThread, pyqtSignal



import time



class ConvexHullSolverThread(QThread):
    def __init__( self, unsorted_points,demo): 
        self.points = unsorted_points
        self.pause = demo
        QThread.__init__(self)

    def __del__(self):
        self.wait()

    # These two signals are used for interacting with the GUI.
    show_hull    = pyqtSignal(list,tuple)
    display_text = pyqtSignal(str)

    # Some additional thread signals you can implement and use for debugging,
    # if you like
    show_tangent = pyqtSignal(list,tuple)
    erase_hull = pyqtSignal(list)
    erase_tangent = pyqtSignal(list)


    def set_points( self, unsorted_points, demo):
        self.points = unsorted_points
        self.demo   = demo


    def run(self):
        assert( type(self.points) == list and type(self.points[0]) == QPointF )

        n = len(self.points)
        print( 'Computing Hull for set of {} points'.format(n) )

        t1 = time.time()
        #SORT THE POINTS BY INCREASING X-VALUE
        sorted_points = self.sort(self.points)
        t2 = time.time()
        print('Time Elapsed (Sorting): {:3.3f} sec'.format(t2-t1))

        t3 = time.time()
        #COMPUTE THE CONVEX HULL USING DIVIDE AND CONQUER
        full_hull = self.compute_hull(sorted_points)
        t4 = time.time()

        self.drawShape(full_hull)

        USE_DUMMY = False
        if USE_DUMMY:
            # This is a dummy polygon of the first 3 unsorted points
            polygon = [QLineF(self.points[i],self.points[(i+1)%3]) for i in range(3)]

            # When passing lines to the display, pass a list of QLineF objects.
            # Each QLineF object can be created with two QPointF objects
            # corresponding to the endpoints
            assert( type(polygon) == list and type(polygon[0]) == QLineF )

            # Send a signal to the GUI thread with the hull and its color
            self.show_hull.emit(polygon,(0,255,0))

        else:
            # TODO: PASS THE CONVEX HULL LINES BACK TO THE GUI FOR DISPLAY

            pass


        # Send a signal to the GUI thread with the time used to compute the
        # hull
        self.display_text.emit('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))
        print('Time Elapsed (Convex Hull): {:3.3f} sec'.format(t4-t3))

    def compute_hull(self, points):
        n = len(points)
        if n == 2:
            #self.drawShape(points)
            return points
        elif n == 3:
            #organize the points to return in a clockwise fashion
            slope1 = self.slope(points[0], points[1])
            slope2 = self.slope(points[0], points[2])
            if slope1 > slope2:
                #self.drawShape(points)

                return points

            else:
                myPoints = []
                myPoints.append(points[0])
                myPoints.append(points[2])
                myPoints.append(points[1])
                #self.drawShape(myPoints)
                return myPoints
        else:
            left = points[:len(points)//2]
            right = points[len(points)//2:]

            left_hull = self.compute_hull(left)
            right_hull = self.compute_hull(right)

            full_hull = self.merge(left_hull, right_hull, left[-1], right[0])

        return full_hull
           # self.drawShape(full_hull)

    def merge(self, left_hull, right_hull, rightmost, leftmost):
        #Find the upper Tangent
        topLeftPoint, topRightPoint = self.upperTangent(left_hull, right_hull, rightmost, leftmost)


        #Find the lower tangent
        bottomRightPoint, bottomLeftPoint = self.lowerTangent(left_hull, right_hull, rightmost, leftmost)

        right_hull_piece = []
        left_hull_piece = []


        if topRightPoint > bottomRightPoint:
            right_hull_piece = right_hull[topRightPoint:] + right_hull[:bottomRightPoint+1]
        elif topRightPoint == bottomRightPoint:
            right_hull_piece = [right_hull[topRightPoint]]
        else:
            right_hull_piece = right_hull[topRightPoint:bottomRightPoint+1]

        if bottomLeftPoint > topLeftPoint:
            left_hull_piece = left_hull[bottomLeftPoint:]+left_hull[:topLeftPoint+1]
        elif bottomLeftPoint == topLeftPoint:
            left_hull_piece = [left_hull[bottomLeftPoint]]
        else:
            left_hull_piece = left_hull[bottomLeftPoint:topLeftPoint+1]

        full_hull = left_hull_piece + right_hull_piece
        return full_hull


    def upperTangent(self, left_hull, right_hull, rightmost, leftmost):
        # Finding the upper tangent
        # Start with rightmost point on the left hull
        base_slope = self.slope(rightmost, leftmost)
        #self.drawShape([rightmost, leftmost])
        # find next clockwise point in the right hull
        comeOnGetHigher = 0
        increasing = True
        currentSlope = base_slope
        currentLeftIndex = left_hull.index(rightmost)
        currentLeftPoint = rightmost
        currentRightIndex = right_hull.index(leftmost)
        currentRightPoint = leftmost
        while comeOnGetHigher < 2:
            if increasing:  # moving clockwise on right hull

                nextSlope = self.slope(currentLeftPoint, right_hull[(currentRightIndex + 1) % len(right_hull)])
                if nextSlope > currentSlope:
                    currentSlope = nextSlope
                    currentRightIndex += 1
                    currentRightPoint = right_hull[currentRightIndex]
                    comeOnGetHigher = 0
                else:
                    increasing = False
                    comeOnGetHigher += 1
            else:  # move counter clock wise on left hull
                nextSlope = self.slope(left_hull[(currentLeftIndex - 1)%len(left_hull)], currentRightPoint)
                if nextSlope < currentSlope:
                    currentSlope = nextSlope
                    currentLeftIndex -= 1
                    currentLeftIndex  = currentLeftIndex % len(left_hull)
                    currentLeftPoint = left_hull[currentLeftIndex]
                    comeOnGetHigher = 0
                else:
                    increasing = True
                    comeOnGetHigher += 1

        upperTangent = []
        upperTangent.append(currentRightPoint)
        upperTangent.append(currentLeftPoint)
        #0self.drawShape(upperTangent)
        return currentLeftIndex, currentRightIndex

    def lowerTangent(self, left_hull, right_hull, rightmost, leftmost):
        # Finding the lower tangent
        # Start with leftmost point on the right hull
        base_slope = self.slope(rightmost, leftmost)
        comeOnGetHigher = 0
        increasing = True
        currentSlope = base_slope
        currentLeftIndex = left_hull.index(rightmost)
        currentLeftPoint = rightmost
        currentRightIndex = right_hull.index(leftmost)
        currentRightPoint = leftmost
        while comeOnGetHigher < 2:
            if increasing:  # keeping right point stationary and moving clockwise on left hull
                #index = (currentLeftIndex + 1) % len(left_hull)
                # %len(left_hull)
                newSlope = self.slope(left_hull[(currentLeftIndex + 1) % len(left_hull)], currentRightPoint)
                if newSlope > currentSlope: # keeping moving clockwise looking for biggest slopes
                    currentSlope = newSlope
                    currentLeftIndex += 1
                    currentLeftIndex = currentLeftIndex % len(left_hull)
                    currentLeftPoint = left_hull[currentLeftIndex]
                    comeOnGetHigher = 0
                else:
                    increasing = False
                    comeOnGetHigher += 1


            else:  # move counter clock wise on left hull
                newSlope = self.slope(currentLeftPoint, right_hull[currentRightIndex - 1])
                if newSlope < currentSlope:
                    currentSlope = newSlope
                    currentRightIndex -= 1
                    currentRightIndex = currentRightIndex % len(right_hull)
                    currentRightPoint = right_hull[currentRightIndex]
                    comeOnGetHigher = 0
                else:
                    increasing = True
                    comeOnGetHigher += 1


        lowerTangent = []
        lowerTangent.append(currentRightPoint)
        lowerTangent.append(currentLeftPoint)
        #self.drawShape(lowerTangent)
        return currentRightIndex, currentLeftIndex

    def slope(self, point1, point2):
        return ((point2.y()-point1.y())/(point2.x()-point1.x()))

    def drawShape(self, points):
        n = len(points)
        polygon = [QLineF(points[i], points[(i + 1) % n]) for i in range(n)]

        # When passing lines to the display, pass a list of QLineF objects.
        # Each QLineF object can be created with two QPointF objects
        # corresponding to the endpoints
        assert (type(polygon) == list and type(polygon[0]) == QLineF)

        # Send a signal to the GUI thread with the hull and its color
        self.show_hull.emit(polygon, (0, 255, 0))

    def sort(self, points):
        return sorted(points, key=lambda point: point.x())


