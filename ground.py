import pyglet
import random
from pyglet.gl import *

Groundbatch = pyglet.graphics.Batch()

# WinWidth = 1400
# WinHeight = 800
WinWidth = 1400
WinHeight = 800

num_x = WinWidth/200
num_y = WinHeight/200
FrameWidth = 10

class the_exit(object):
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        pattern = pyglet.image.SolidColorImagePattern((0, 255, 0, 255))
        self.sprite = pyglet.sprite.Sprite(img=pyglet.image.create(xs, ys, pattern),x = x, y = y, batch=Groundbatch)


class ground(object):
    def __init__(self, x, y, xs, ys):
        self.x = x
        self.y = y
        self.xs = xs
        self.ys = ys
        pattern = pyglet.image.SolidColorImagePattern((255, 255, 255, 255))
        self.sprite = pyglet.sprite.Sprite(img=pyglet.image.create(xs, ys, pattern),x = x, y = y, batch=Groundbatch)

grounds = [
            ground(x=0, y=0, xs=WinWidth, ys=FrameWidth),
            ground(x=0, y=WinHeight-FrameWidth, xs=WinWidth, ys=FrameWidth),
            ground(x=0, y=0, xs=FrameWidth, ys=WinHeight),
            ground(x=WinWidth-FrameWidth, y=0, xs=FrameWidth, ys=WinHeight),
            the_exit(WinWidth*.2, 10, 50, 50),
        ]
n_line = [0, 200, 200, 10]
s_line = [0, 0, 200, 10]
w_line = [0, 0, 10, 200]

def make_ground_choices():
    return [
    # [[50, 50, 100, 10], [0, 100, random.randint(20,150), 10]],
    # [],
    # [s_line],
    [s_line],
    # [s_line, [0, 100, 50, 50]],
    # [s_line, [0, 0, 10, 50], [0, 50, 50, 10]],
    # [s_line, [0, 0, 10, 50], [0, 50, 100, 10]]
    # [n_line],
]





# def make_ground(w, h, grounds):
#     wed = range(0, w, 100)
#     hed = range(0, h, 100)
#     pos = range(0, 50, 1)
#     size = range(30, 200, 10)
#     for w in wed:
#         for h in hed:
#             if random.random()>.7:
#                 grounds += [ground(x=random.choice(pos)+w, y=random.choice(pos)+h,xs=random.choice(size), ys=10)]
#             if random.random()>.7:
#                 grounds += [ground(x=random.choice(pos)+w, y=random.choice(pos)+h,xs=10, ys=random.choice(size)/2)]
#     return grounds
#
def generate_level(grounds, GroundBatch):
    start_end = [0, num_y-1]
    random.shuffle(start_end)
    grid = [[0]*num_x for i in xrange(num_y) ]

    start = (random.choice(range(num_x)), start_end.pop())
    end = (random.choice(range(num_x)), start_end.pop())
    grid[start[1]][start[0]] = 1
    grid[end[1]][end[0]] = 1
    start_loc = (100+start[0]*200, 100+start[1]*200)
    grounds += [
        #start loc
        ground(100+start[0]*200, 100+start[1]*200, 50, 10),
        #end loc
        the_exit(100+end[0]*200, 110+end[1]*200, 50, 50),
        ground(100+end[0]*200, 100+end[1]*200, 50, 10),
        ground(50+end[0]*200, 50+end[1]*200, 150, 10)
    ]

    for yn in range(num_y):
        if yn != 0:
            xn = random.choice(range(num_x))
            grid[yn][xn] = 1
            grid[yn-1][xn] = 1
            grounds += [
                # N
                ground(50+xn*200, 100+yn*200, 50, 10),
                ground(100+xn*200, 50+yn*200, 50, 10),
                ground(150+xn*200, yn*200, 50, 10),
                # ground(50+xn*200, 100+yn*200, 50, 10),
                # ground(100+xn*200, 50+yn*200, 50, 10),


                # S
                # ground(100+xn*200, 210+(yn-1)*200, 50, 10),
                ground(50+xn*200, 140+(yn-1)*200, 50, 10),
                ground(100+xn*200, 70+(yn-1)*200, 50, 10),

                # ground(100+xn*200, 100+(yn-1)*200, 50, 10)
            ]

    for yn, yplot in enumerate(grid):
        for xn, xplot in enumerate(yplot):
            if grid[yn][xn] == 0:
                ground_choices = make_ground_choices()
                for x in random.choice(ground_choices):
                    grounds += [
                        ground(x[0]+xn*200, x[1]+yn*200, x[2], x[3])
                    ]
    return grounds, start_loc
