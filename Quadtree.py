from point import Point
from node import Node
from rectangle import Rectangle

class Quadtree:
    def __init__(self, center, limit):
        self.root = Node(None, center, limit)

    def insert(self, point):
        self.root.add(point)

    def query(self, top_left, top_right, bottom_right, bottom_left):
        boundary = Rectangle(top_left, top_right, bottom_right, bottom_left)
        show_points = self.root.search(boundary)
        for i in show_points:
            print("x:" , i.x, "y:" , i.y)

    def delete(self, point):
        self.root.remove_point(point)

    def kNN_query(self, point, k):
        search_range = Rectangle(Point(point.x - 5, point.y + 5), Point(point.x + 5, point.y + 5), Point(point.x + 5, point.y - 5), Point(point.x - 5, point.y - 5))
        neighbors = self.root.kNN_search(point, k, search_range, self.root)
        for i in neighbors:
            print("x:" , i.x, "y:" , i.y)
