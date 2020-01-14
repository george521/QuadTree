from __future__ import division
from point import Point
from node import Node
from rectangle import Rectangle


class Quadtree:
    def __init__(self, limit):
        self.root = Node(None, Point(0,0), limit)
        self.m_limit = limit

    def insert(self, point):
        print("Inserting point(", point.x, ",", point.y, ") into QuadTree...")
        self.root.add(point, self.root)

    def query(self, top_left, top_right, bottom_right, bottom_left):
        boundary = Rectangle(top_left, top_right, bottom_right, bottom_left)
        print("Searching...")
        show = self.root.search(boundary)
        for i in show:
            print(i.x,"|",i.y)
        
    def delete(self, point):
        self.root.remove_point(point)

    def kNN_query(self, point, k):
        if k < 0:
            raise Exception("Number k can't be negative")
        self.kNN_range(self.root.findNode(point))
        print("Searching...")
        search_range = Rectangle(Point(point.x - self.m_limit, point.y + self.m_limit), Point(point.x + self.m_limit, point.y + self.m_limit), Point(point.x + self.m_limit, point.y - self.m_limit), Point(point.x - self.m_limit, point.y - self.m_limit))
        show = self.root.kNN_search(point, k, search_range, self.root, self.m_limit)
        for i in show:
            print(i.x,"|",i.y)

    def kNN_range(self, node):
        self.m_limit = ((self.root.limit/(2**self.root.depth)) + node.limit)



