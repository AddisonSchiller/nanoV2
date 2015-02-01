from defaults import window_height, window_width
import math
import pyglet
import random
from pyglet.window import key
from pyglet.gl import *

#red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 255))
red_sprite = pyglet.image.load('sprites/ghost.png')

#efloat = pyglet.image.create(30, 30, red_sprite)
efloat = red_sprite


class enemy(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(red_sprite, random.randint(10, window_width-50), random.randint(10, window_height-50))
        self.max_hp = random.randint(1, 10)
        self.hp = self.max_hp
        self.pattern = pyglet.image.SolidColorImagePattern(color=(255,0,0,255))
        self.health = pyglet.sprite.Sprite(img=pyglet.image.create(self.hp*45/self.max_hp, 1, self.pattern), x = self.sprite.x, y = self.sprite.y + self.sprite.height+5)


class floater(object):
    def __init__(self):
        self.sprite = pyglet.sprite.Sprite(efloat, random.randint(10, window_width-50), random.randint(10, window_height-50))
        self.max_hp = random.randint(1, 10)
        self.hp = self.max_hp
        self.pattern = pyglet.image.SolidColorImagePattern(color=(255,0,0,255))
        self.health = pyglet.sprite.Sprite(img=pyglet.image.create(self.hp*45/self.max_hp, 1, self.pattern), x = self.sprite.x, y = self.sprite.y + self.sprite.height+5)
        self.touch_damage = 10
        self.x_speed = 0
        self.y_speed = 0
        self.base_x_speed = 4
        self.last_collision = (0,0)

    def ai(self, position):
        if math.sqrt(abs(float(position[0] - self.sprite.x)**2 + (position[1] - self.sprite.y)**2)) < 400:
            point = (position[0]+20, position[1]+40)
            speed = 10
            x1, x2, y1, y2 = position[0] -20, self.sprite.x, position[1] -20, self.sprite.y
            xdir, ydir = cmp(x1-x2,0), cmp(y1-y2,0)
            try:
                move = int(float(abs(x1-x2))/(abs(x1-x2)+abs(y1-y2))*speed)
                x_move = move*xdir
                y_move = (speed - move)*ydir
            except:
                y_move = 0
                x_move = 0

            self.sprite.x += x_move
            self.sprite.y += y_move
            self.health = pyglet.sprite.Sprite(img=pyglet.image.create(self.hp*45/self.max_hp, 1, self.pattern), x = self.sprite.x, y = self.sprite.y + self.sprite.height+5)


e = []
def make_enemies():
    return [floater(),floater(),floater(),floater(),floater(),]
