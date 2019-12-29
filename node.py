from __future__ import division
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
        print(len(self.points))
            

    def add(self, point):
        print(self.center.x , self.center.y, self)
        if (not self.find_point(point)):
            raise Exception("Point outside the range of Quadtree.")
        flag = True
        if ((self.capacity > len(self.points))and (self.tl == None)):
            for i in self.points:
                if ((i.x==point.x)and (i.y==point.y)):
                    flag = False
                    break
                else:
                    flag = True
            if (flag == True):
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

        
    def search(self, top_left, top_right, bottom_right, bottom_left, rec):
        if(self.parent == None):
            rec = Rectangle(top_left, top_right, bottom_right, bottom_left)
        if(self.tl == None):
            for i in self.points:
                if ( i.x >= rec.bl.x and i.x <= rec.tr.x and i.y >= rec.bl.y and i.y <= rec.tr.y):
                    rec.points.append(i)
        else:
            if (self.tl.overlap(rec)):
                self.tl.search(None, None, None, None, rec)
            if (self.tr.overlap(rec)):
                self.tr.search(None, None, None, None, rec)
            if (self.br.overlap(rec)):
                self.br.search(None, None, None, None, rec)
            if (self.bl.overlap(rec)):
                self.bl.search(None, None, None, None, rec)
        return rec.points

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
            

p = Node(None, Point(0,0), 10)

