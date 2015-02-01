import pyglet
import random
from pyglet.gl import *
from defaults import window_width, window_height, frame_width

terrain_color = pyglet.image.SolidColorImagePattern((255, 255, 255, 255))
terrain_batch = pyglet.graphics.Batch()


class terrain(object):
    def __init__(self, x, y, xs, ys):
        self.sprite = pyglet.sprite.Sprite(
            img=pyglet.image.create(xs, ys, terrain_color),
            x=x,
            y= y,
            batch = terrain_batch,
            )

# draws the frame around the window
terrain_frame = [
    terrain(0, 0, window_width, frame_width),
    terrain(0, window_height-frame_width, window_width, frame_width),
    terrain(0, 0, frame_width, window_height),
    terrain(window_width-frame_width, 0, frame_width, window_height),
]
s_line = [0,0,200,10]


def make_terrain_options():

    random_height = random.randint(1,138)
    dual_pillar = random.randint(0,158)
    # Used to make the tunnel floor look smoother if random_height is > 130
    if (130-random_height < 0):
        special_height = 0
    else:
        special_height =130-random_height
    return [
        [[dual_pillar,0, 10, 139-random_height],[dual_pillar,200-random_height,10,random_height],s_line], # Dual pillars
        [[0, 0, 10, 140 - random_height],[158, 0, 10, 140 - random_height], #bottom
        [0,200-random_height,10,random_height],[158, 200-random_height, 10, random_height], #top
        [0,200-random_height,158,10],[0,special_height,158,10]], #tunnel floors
        [[100,0,10,100],s_line], # bottom pillar and floor
        [[0,0,50,10],[0,50,50,10],[0,0,10,50]], # C-Shape
        [s_line],



    ]
def build_start_end(new_grid, window_grid):
    start_end_index = [[0,0], [(window_width/200) -1,0], [(window_width/200) -1, (window_height/200) -1], [0, (window_height/200) -1]]
    start,end = random.sample(start_end_index,2)
    window_grid[start[1]][start[0] ] = 1
    window_grid[end[1]][end[0] ] = 1
    new_grid[start[1]][start[0] ] = [terrain(50 + 200 * start[0], 50 + 200 * start[1], 100, 10)]
    new_grid[end[1]][end[0] ] = [terrain(50 + 200 * end[0], 50 + 200 * end[1], 100, 10), terrain(75 + 200 * end[0], 100 + 200 * end[1], 50, 10)]
    start_location = (100 + 200 * start[0], 100 + 200 * start[1])
    end_location = (100 + 200 * end[0], 100 + 200 * end[1])
    return new_grid, window_grid, start_location, end_location


def build_bridges(new_grid, window_grid):

    for n_row,row in enumerate(window_grid):
        i =  random.choice(range(len(row) -2)) +1
        row[i] = 1
        if n_row -1 != window_height/200:
            row_c = ((n_row -1) *200)
            window_grid[n_row -1][i] =1
            new_grid[n_row-1][i] = [
            #    terrain(75 + 200 * i,63 + row_c ,50,10),
                terrain(0 + 200 * i,126 + row_c ,50,10),
            #    terrain(150 + 200 * i,126 + row_c ,50,10),
                terrain(75+ 200 * i,189 + row_c ,50,10)
                ]
    return new_grid, window_grid


    # start_end_index = [[0,0], [(window_width/200) -1,0], [(window_width/200) -1, (window_height/200) -1], [0, (window_height/200) -1]]
    # start,end = random.sample(start_end_index,2)
    # window_grid[start[1]][start[0] ] = 1
    # window_grid[end[1]][end[0] ] = 1
    # new_grid[start[1]][start[0] ] = [terrain(50 + 200 * start[0], 50 + 200 * start[1], 100, 10)]
    # new_grid[end[1]][end[0] ] = [terrain(50 + 200 * end[0], 50 + 200 * end[1], 100, 10), terrain(75 + 200 * end[0], 100 + 200 * end[1], 50, 10)]
    # start_location= (100 + 200 * start[0], 100 + 200 * start[1])
    # return new_grid, window_grid, start_location
def build_base():
    new_grid = [[[]]*(window_width/200) for i in xrange(window_height/200)]
    new_grid[0][0] = [terrain(50, 50, 100, 10),terrain(75 , 100, 50, 10)]
    end_location = (100, 100)
    start_location = (90,111)
    end_sprite = pyglet.sprite.Sprite(img=pyglet.image.create(50, 50, pyglet.image.SolidColorImagePattern((0, 255, 0, 255))),x=end_location[0]-25, y=end_location[1]+10)
    return new_grid,start_location,end_location,end_sprite



def fill_terrain(window_grid):

    # builds a grid and terrain options. After that it enumerates through the grid and draws
    # terrain from the list

    new_grid = [[[]]*(window_width/200) for i in xrange(window_height/200)]
    new_grid, window_grid, start_location, end_location = build_start_end(new_grid,window_grid)
    end_sprite = pyglet.sprite.Sprite(img=pyglet.image.create(50, 50, pyglet.image.SolidColorImagePattern((0, 255, 0, 255))),x=end_location[0]-25, y=end_location[1]+10)
    new_grid,window_grid = build_bridges(new_grid, window_grid)
    for n_col, col in enumerate(new_grid):
        for n_row, row in enumerate(col):
            if window_grid[n_col][n_row] == 0:
                new_grid[n_col][n_row] = [] # since they point to the same [] it needs to be reinstantiated for each
                for t in random.choice(make_terrain_options()):
                    new_grid[n_col][n_row] += [
                        terrain(t[0]+n_row*200, t[1]+n_col*200, t[2], t[3])
                    ]

    return new_grid,  start_location, end_location, end_sprite
