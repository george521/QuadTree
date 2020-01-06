from point import Point
from node import Node
from rectangle import Rectangle

class Quadtree:
    def __init__(self, limit):
        self.root = Node(None, Point(0,0), limit)

    def insert(self, point):
        print("Inserting point(", point.x, ",", point.y, ") into QuadTree...")
        self.root.add(point)

    def query(self, top_left, top_right, bottom_right, bottom_left):
        boundary = Rectangle(top_left, top_right, bottom_right, bottom_left)
        print("Searching...")
        show = self.root.search(boundary)
        for i in show:
            print(i.x,"|",i.y)
        
    def delete(self, point):
        self.root.remove_point(point)

    def kNN_query(self, point, k):
        print("Searching...")
        search_range = Rectangle(Point(point.x - 1, point.y + 1), Point(point.x + 1, point.y + 1), Point(point.x + 1, point.y - 1), Point(point.x - 1, point.y - 1))
        show = self.root.kNN_search(point, k, search_range, self.root, None)
        for i in show:
            print(i.x,"|",i.y)

