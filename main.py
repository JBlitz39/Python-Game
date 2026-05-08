class Fish:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def swin(self, xdist, ydist):
        self.x = xdist
        self.y = ydist

fish1 = Fish(10, 15, 45, 25)
fish1.swin(20, 20)
print(fish1.x)
print(fish1.y)
