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


    def split(self):
        print("Splitting Node...")
        self.tl = Node(self, Point(self.center.x - self.limit/4, self.center.y + self.limit/4), self.limit/2)
        self.tr = Node(self, Point(self.center.x + self.limit/4, self.center.y + self.limit/4), self.limit/2)
        self.bl = Node(self, Point(self.center.x - self.limit/4, self.center.y - self.limit/4), self.limit/2)
        self.br = Node(self, Point(self.center.x + self.limit/4, self.center.y - self.limit/4), self.limit/2)
        for i in self.points:
            if (i.x < self.center.x):
                if(i.y > self.center.y):
                    self.tl.add(i)
                else:
                    self.bl.add(i)
            else:
                if(i.y > self.center.y):
                    self.tr.add(i)
                else:
                    self.br.add(i)
        del self.points[:]
        #print(len(self.points))
            

    def add(self, point):
        #print(self.center.x , self.center.y, self)
        if (not self.find_point(point)):
            raise Exception("Point outside the range of Quadtree.")
        flag = True
        if ((self.capacity > len(self.points))and (self.tl == None)):
            for i in self.points:
                if ((i.x==point.x)and (i.y==point.y)):
                    flag = False
                    print("Point already exists in QuadTree...")
                    break
                else:
                    flag = True
            if (flag == True):
                print("Inserting point(", point.x, ",", point.y, ") into QuadTree...")
                self.points.append(point)
        elif((self.capacity == len(self.points))and (self.tl == None)):
            self.split()
            if (point.x < self.center.x):
                if(point.y > self.center.y):
                    self.tl.add(point)
                else:
                    self.bl.add(point)
            else:
                if(point.y > self.center.y):
                    self.tr.add(point)
                else:
                    self.br.add(point)
        else:
            if (point.x < self.center.x):
                if(point.y > self.center.y):
                    self.tl.add(point)
                else:
                    self.bl.add(point)
            else:
                if(point.y > self.center.y):
                    self.tr.add(point)
                else:
                    self.br.add(point)

    #check if rectangle overlaps with square    
    def overlap(self, rectangle):     
        if(self.tl_limit.x > rectangle.br.x or rectangle.tl.x > self.br_limit.x): 
            return False
        if(self.tl_limit.y < rectangle.br.y or rectangle.tl.y < self.br_limit.y): 
            return False  
        return True

        
    def search(self, rec):
        print("Searching...")
        if(self.tl == None):
            for i in self.points:
                if ( i.x >= rec.bl.x and i.x <= rec.tr.x and i.y >= rec.bl.y and i.y <= rec.tr.y):
                    rec.points.append(i)
        else:
            if (self.tl.overlap(rec)):
                self.tl.search(rec)
            if (self.tr.overlap(rec)):
                self.tr.search(rec)
            if (self.br.overlap(rec)):
                self.br.search(rec)
            if (self.bl.overlap(rec)):
                self.bl.search(rec)
                
        for i in rec.points:
            print("x:" , i.x, "y:" , i.y)
        return

    def kNN_search(self, point, k, search_range, root):
        if(self.tl == None):
            for i in self.points:
                if ( i.x >= search_range.bl.x and i.x <= search_range.tr.x and i.y >= search_range.bl.y and i.y <= search_range.tr.y):
                    flag = True
                    for j in search_range.points:
                        if ((i.x==j.x)and (i.y==j.y)):
                            flag = False
                            break
                        else:
                            flag = True
                    if (flag == True):
                        search_range.points.append(i)
        else:
            if (self.tl.overlap(search_range)):
                self.tl.kNN_search(point, k, search_range, root)
            if (self.tr.overlap(search_range)):
                self.tr.kNN_search(point, k, search_range, root)
            if (self.br.overlap(search_range)):
                self.br.kNN_search(point, k, search_range, root)
            if (self.bl.overlap(search_range)):
                self.bl.kNN_search(point, k, search_range, root)

        if( len(search_range.points) == k):
            for i in search_range.points:
                print("Found point(" , i.x, "," , i.y, ")")
            return
        elif(len(search_range.points) > k):
            self.Euclidean(point, search_range.points, k)
            return
        else:
            if(root.tl_limit.x > search_range.tl.x and root.tl_limit.y < search_range.tl.y and root.br_limit.x < search_range.br.x and root.br_limit.y > search_range.br.y ):
                for i in search_range.points:
                    print("Found point(" , i.x, "," , i.y, ")")
                return 
            else:
                search_range.extend(2)
                root.kNN_search(point, k, search_range, root)
                
            
    def Euclidean(self, p1, points, k):
        neighbors = []
        s_list = [[] for i in range(len(points))]
        for i in range(len(points)):
            d = math.sqrt((points[i].x - p1.x)**2 + (points[i].y - p1.y)**2)
            s_list[i].append(points[i])
            s_list[i].append(d)
        s_list.sort(key = lambda x: x[1])
        for i in range(k):
            neighbors.append(s_list[i][0])
        for i in neighbors:
            print("Found point(" , i.x, "," , i.y, ")")

    #check if point inside square
    def find_point(self, point): 
        if (point.x > self.bl_limit.x and point.x < self.tr_limit.x and point.y > self.bl_limit.y and point.y < self.tr_limit.y) : 
            return True
        else: 
            return False

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
            


