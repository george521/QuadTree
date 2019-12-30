class Rectangle:
    def __init__(self, tl, tr, br, bl):
        self.tl = tl
        self.tr = tr
        self.br = br
        self.bl = bl
        self.points = []

    def extend(self, number):
        self.tl.x -= number
        self.tl.y += number
        self.tr.x += number
        self.tr.y += number
        self.br.x += number
        self.br.y -= number
        self.bl.x -= number
        self.bl.y -= number
