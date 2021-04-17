import random
import pygame

random.seed()

class Number (object):
    def __init__(self, num, x, y, width, height, image):
        self.number = num
        self.position = random.randint(1, 16)
        self.x = x
        self.y = y
        self.w = width
        self.h = height
        self.image = image
        self.hasMerged = True

    def __eq__(self, other):
        return self.number == other.number

    def draw(self, window):
        pass

    def __str__(self):
        return str(self.number)


#a = [[0] * m for i in range(n)]
