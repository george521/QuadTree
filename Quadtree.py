from point import Point
from node import Node

class Quadtree:
    def __init__(self, center, limit):
        self.root = Node(None, center, limit)

    def insert(self, point):
        self.root.add(point)

    def query(self, top_left, top_right, bottom_right, bottom_left):
        show_points = self.root.search(top_left, top_right, bottom_right, bottom_left, None)
        for i in show_points:
            print("x:" , i.x, "y:" , i.y)
    def delete(self, point):
        self.root.remove_point(point)
