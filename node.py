from __future__ import division
import math
from point import Point
from rectangle import Rectangle


class Node:
    def __init__(self, parent, center, limit):
        self.parent = parent
        self.center = center
        self.limit = limit
        self.capacity = 5
        self.tl_limit = Point(self.center.x - self.limit/2, self.center.y + self.limit/2)
        self.br_limit = Point(self.center.x + self.limit/2, self.center.y - self.limit/2)
        self.tr_limit = Point(self.center.x + self.limit/2, self.center.y + self.limit/2)
        self.bl_limit = Point(self.center.x - self.limit/2, self.center.y - self.limit/2)
        self.tl = None
        self.tr = None
        self.bl = None
        self.br = None
        self.points = []
        self.depth = 0


    def split(self, root):
        #print("Splitting Node...")
        self.tl = Node(self, Point(self.center.x - self.limit/4, self.center.y + self.limit/4), self.limit/2)
        self.tr = Node(self, Point(self.center.x + self.limit/4, self.center.y + self.limit/4), self.limit/2)
        self.bl = Node(self, Point(self.center.x - self.limit/4, self.center.y - self.limit/4), self.limit/2)
        self.br = Node(self, Point(self.center.x + self.limit/4, self.center.y - self.limit/4), self.limit/2)

        if ((root.limit/(2**root.depth)) > self.limit/2):
            root.depth += 1
            
        for i in self.points:
            if (i.x < self.center.x):
                if(i.y > self.center.y):
                    self.tl.add(i, root)
                else:
                    self.bl.add(i, root)
            else:
                if(i.y > self.center.y):
                    self.tr.add(i, root)
                else:
                    self.br.add(i, root)
        del self.points[:]
            

    def add(self, point, root):
        if (not self.find_point(point)):
            raise Exception("Point outside the range of Quadtree.")
        if ((self.capacity > len(self.points))and (self.tl == None)):
            for i in self.points:
                if ((i.x==point.x)and (i.y==point.y)):
                    raise Exception("Point already exists in QuadTree...")
            self.points.append(point)
        elif((self.capacity == len(self.points))and (self.tl == None)):
            self.split(root)
            if (point.x < self.center.x):
                if(point.y > self.center.y):
                    self.tl.add(point, root)
                else:
                    self.bl.add(point, root)
            else:
                if(point.y > self.center.y):
                    self.tr.add(point, root)
                else:
                    self.br.add(point, root)
        else:
            if (point.x < self.center.x):
                if(point.y > self.center.y):
                    self.tl.add(point, root)
                else:
                    self.bl.add(point, root)
            else:
                if(point.y > self.center.y):
                    self.tr.add(point, root)
                else:
                    self.br.add(point, root)

    #check if rectangle overlaps with square    
    def overlap(self, rectangle):     
        if(self.tl_limit.x > rectangle.br.x or rectangle.tl.x > self.br_limit.x): 
            return False
        if(self.tl_limit.y < rectangle.br.y or rectangle.tl.y < self.br_limit.y): 
            return False  
        return True

        
    def r_search(self, rec):
        if(self.tl == None):
            for i in self.points:
                if i not in rec.points:
                    if ( i.x >= rec.bl.x and i.x <= rec.tr.x and i.y >= rec.bl.y and i.y <= rec.tr.y):
                        rec.points.append(i)
        else:
            if (self.tl.overlap(rec)):
                self.tl.r_search(rec)
            if (self.tr.overlap(rec)):
                self.tr.r_search(rec)
            if (self.br.overlap(rec)):
                self.br.r_search(rec)
            if (self.bl.overlap(rec)):
                self.bl.r_search(rec)
                
        return rec.points

    def kNN_search(self, point, k, search_range, root, r):
        tmp = []
        tmp = self.Euclidean(point, root.r_search(search_range), k, r)
        if (root.tl_limit.x > search_range.tl.x and root.tl_limit.y < search_range.tl.y and root.br_limit.x < search_range.br.x and root.br_limit.y > search_range.br.y ):
            return tmp
        elif len(tmp)< k:
            r += (root.limit/(2**root.depth))
            search_range.extend(root.limit/(2**root.depth))
            return root.kNN_search(point, k, search_range, root, r)
        else:
            return tmp

            
    def Euclidean(self, p1, points, k, r):
        neighbors = []
        s_list = [[] for i in range(len(points))]
        for i in range(len(points)):
            d = math.sqrt((points[i].x - p1.x)**2 + (points[i].y - p1.y)**2)
            if (points[i].x == p1.x and points[i].y == p1.y):
                s_list[i].append(points[i])
                s_list[i].append(float('Inf'))
            if r >= d:
                s_list[i].append(points[i])
                s_list[i].append(d)
            else:
                s_list[i].append(points[i])
                s_list[i].append(float('Inf'))
        s_list.sort(key = lambda x: x[1])
        if(k>len(points)):            
            for i in range(len(points)):
                if not(s_list[i][0].x == p1.x and s_list[i][0].y == p1.y):
                    neighbors.append(s_list[i][0])
        else:
            for i in range(k):
                if not(s_list[i][0].x == p1.x and s_list[i][0].y == p1.y):
                    neighbors.append(s_list[i][0])
        return neighbors

    #check if point inside square
    def find_point(self, point): 
        if (point.x > self.bl_limit.x and point.x < self.tr_limit.x and point.y > self.bl_limit.y and point.y < self.tr_limit.y) : 
            return True
        else: 
            return False

    def findNode(self, point):
        if (self.tl == None):
            return self
        else:
            if (self.tl.find_point(point)):
                return self.tl.findNode(point)
            if (self.tr.find_point(point)):
                return self.tr.findNode(point)
            if (self.br.find_point(point)):
                return self.br.findNode(point)
            if (self.bl.find_point(point)):
                return self.bl.findNode(point)

    def remove_point(self, point):
        if(self.tl == None):
            for i in self.points:
                if (i.x == point.x and i.y == point.y):
                    print("Deleting point(",point.x,",",point.y,")")
                    self.points.remove(i)
                    if (len(self.points)==0):
                        self.parent.merge()
                    break
                else:
                    raise Exception("Point doesn't exist")
            
        else:
            if (self.tl.find_point(point)):
                self.tl.remove_point(point)
            if (self.tr.find_point(point)):
                self.tr.remove_point(point)
            if (self.br.find_point(point)):
                self.br.remove_point(point)
            if (self.bl.find_point(point)):
                self.bl.remove_point(point)
            
    def merge(self):
        if(len(self.tl.points) == 0 and len(self.tr.points) == 0 and len(self.br.points) == 0 and len(self.bl.points) == 0):
            self.tl = None
            self.tr = None
            self.br = None
            self.bl = None
            if (self.parent != None):
                self.parent.merge()
            


