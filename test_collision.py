import math
import random

import pyglet
from pyglet.gl import *

import pytest
import numpy as np
from ground import ground
from collision import spriteCollision

from experimental import Sprite

def make_fix(x, y, xs, ys):
    pattern = pyglet.image.SolidColorImagePattern((random.randrange(254, 255), random.randrange(254, 255), random.randrange(254, 255),255))
    return pyglet.sprite.Sprite(
        img=pyglet.image.create(xs, ys, pattern),x = x, y = y)

def test_sprites_collide():
    a = make_fix(10, 10, 10, 10)
    b = make_fix(10, 10, 10, 10)
    assert spriteCollision(a, b)

def test_sprites_do_not_collide():
    a = make_fix(10, 10, 10, 10)
    b = make_fix(100, 100, 10, 10)
    assert not spriteCollision(a, b)
