from defaults import gfx_batch, window_height
import math
import pyglet
import random
from pyglet.window import key
from pyglet.gl import *
white_sprite = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 255))

def attr_none(b):
    return [], b

def generate_gun(level =0,coin=0,parts=0):
    return  {

    # basics
    'gun_type': random.choice(["pistol","grenade","rifle","shotgun","sniper"]),
    'x_speed':random.randint(3, 20),
    'y_speed':0,
    'size':random.randint(1, 10),
    'shot_range':random.randint(100,1000),
    'acc':random.randint(0,500)/100,
    'damage':random.randint(1,5),
    'reload':random.randint(5,100),
    'nano':random.randint(25,300),
    'pierce':0,
    'special1': attr_none,
    'special1':random.choice([proc_large_explode,proc_swirl]),
    'special1_chance':.03,

    'special2':attr_none,
    'special2_chance':random.random()-.5,

    'collide':attr_none,
    'collide_chance':1
    }

class gun(object):
    def __init__(self, basic, coins = 0, parts = 0):
        self.gun_type = basic['gun_type']
        self.x_speed = basic['x_speed']
        self.y_speed = basic['y_speed']
        self.base_x_speed = basic['x_speed']
        self.size = basic['size']
        self.shot_range = basic['shot_range']
        self.acc = basic['acc']
        self.damage = basic['damage']
        self.reload = basic['reload']
        self.nano = basic['nano']
        self.pierce = basic['pierce']
        self.special1 = basic['special1']
        self.special1_chance = basic['special1_chance']
        self.special2 = basic['special2']
        self.special2_chance = basic['special2_chance']
        self.collide = basic['collide']
        self.collide_chance = basic['collide_chance']

class bullet(object):
    def __init__(self, pos, gun, direction):
        self.gun = gun
        self.direction = direction
        bullet = pyglet.image.create(gun.size, gun.size, white_sprite)
        self.x = pos[0]
        self.y = pos[1]
        self.counter = 0
        self.sprite = pyglet.sprite.Sprite(img=bullet, x = pos[0], y = pos[1], batch=gfx_batch)
        self.x_speed = gun.x_speed*direction
        self.base_x_speed = gun.base_x_speed
        self.pierce = gun.pierce
        self.y_speed = gun.y_speed+((random.random()-.5)*gun.acc)
        self.size = gun.size
        self.range = gun.shot_range+random.random()*100
        self.damage = gun.damage
        self.distance = 0

        self.special1_chance = gun.special1_chance
        self.special1  = gun.special1
        self.special2_chance = gun.special2_chance
        self.special2  = gun.special2

        self.collide = gun.collide
        self.collide_chance = gun.collide_chance

    def proc_special1(self, b):
        if random.random() < self.special1_chance:
            return self.special1(b)
        else:
            return [], b

    def proc_special2(self, b):
        if random.random() < self.special2_chance:
            return self.special2(b)
        else:
            return [], b

    def proc_collide(self, b):
        if random.random() < self.collide_chance:
            return self.collide(b)
        else:
            return [], b


class jetpack(object):
    def __init__(self, pos, gun, fire_gen):

        bullet = pyglet.image.create(2, 5, pyglet.image.SolidColorImagePattern(color=fire_gen))
        self.x = pos[0]
        self.y = pos[1]
        self.counter = 0
        self.sprite = pyglet.sprite.Sprite(img=bullet, x = pos[0], y = pos[1], batch=gfx_batch)
        self.x_speed = gun.x_speed+((random.random()-.5)*gun.acc)
        self.base_x_speed = gun.base_x_speed
        self.y_speed = gun.y_speed
        self.size = gun.size
        self.pierce = gun.pierce
        self.range = gun.shot_range+random.random()*100
        self.damage = gun.damage
        self.distance = 0

        self.special1_chance = 0
        self.special1 = attr_none
        self.special2_chance = 0
        self.special2 = attr_none

        self.collide = attr_none
        self.collide_chance = 0

    def proc_special1(self, b):
        if random.random() < self.special1_chance:
            return self.special1(b)
        else:
            return [], b

    def proc_special2(self, b):
        if random.random() < self.special2_chance:
            return self.special2(b)
        else:
            return [], b

    def proc_collide(self, b):
        if random.random() < self.collide_chance:
            return self.collide(b)
        else:
            return [], b

class extra_bullet(object):
    def __init__(self, pos, damage, x_dir, y_dir, size = 3, special1=attr_none, special2=attr_none, special1_chance=0, special2_chance=0):
        self.direction = 1
        bullet = pyglet.image.create(size, size, white_sprite)
        self.x = pos[0]
        self.y = pos[1]
        self.sprite = pyglet.sprite.Sprite(img=bullet, x = pos[0], y = pos[1], batch=gfx_batch)
        self.x_speed = x_dir
        self.base_x_speed = 50
        self.y_speed = y_dir
        self.pierce = 0
        self.size = 1
        self.base = 0
        self.counter = 0
        self.range = 200
        self.damage = damage
        self.distance = 0
        self.special1_chance = special1_chance
        self.special1 = special1
        self.special2_chance = special2_chance
        self.special2 = special2

        self.collide = attr_none
        self.collide_chance = 0

    def proc_special1(self, b):
        if random.random() < self.special1_chance:
            return self.special1(b)
        else:
            return [], b

    def proc_special2(self, b):
        if random.random() < self.special2_chance:
            return self.special2(b)
        else:
            return [], b

    def proc_collide(self, b):
        if random.random() < self.collide_chance:
            return self.collide(b)
        else:
            return [], b

# Notes
# The best way to kill a current bullet right now is to set its distance to greater than its range. It will be garbage collected on the next tick

# Bullet TYPES. This means that a bullet given this special will move or change in this way
# For example, giving an added bullet the bees attrute will make it move around randomly at the place it spawns
# This can be useful for things that change that bullet itself instead of adding new bullets



###############################
###### Bullet attributes ######
###############################

# Bullet Movement
def attr_bullet_forward(b):
    b.x_speed +=1 * b.direction
    return [], b

def attr_bullet_backward(b):
    b.x_speed -=1 * b.direction
    return [], b

def attr_bullet_right(b):
    b.x_speed +=1
    return [], b
def attr_bullet_move_left(b):
    b.sprite.x-= .5
    return [],b

def attr_bullet_left(b):
    b.x_speed -=1
    return [], b

def attr_bullet_up(b):
    b.y_speed +=1
    return [], b

def attr_bullet_down(b):
    b.y_speed -=1
    return [], b

def attr_bees(b):
    b.x_speed = random.randint(-5,5)
    b.y_speed = random.randint(-5,5)
    return [], b

def attr_gravity(b):
    if b.y_speed>-8:
        b.y_speed-= 1
    return [], b

def attr_grow(b):
    b.size += 1
    bullet = pyglet.image.create(b.size, b.size, white_sprite)
    b.sprite = pyglet.sprite.Sprite(img=bullet, x = b.sprite.x, y = b.sprite.y, batch=gfx_batch)
    return [], b


################################
###### Random proc Events ######
################################

def proc_large_explode(b):
    bullets = []
    for i in range(15):
        bullets.append(extra_bullet((b.sprite.x,b.sprite.y), b.damage, (random.random()-.5)*20, (random.random()-.5)*20, 5))
    for bs in bullets:
        bs.special1 = proc_create_bee
        bs.special1_chance = .1
        bs.pierce = 1
        bs.range = 100
    return bullets, b
def proc_smite_explode(b):
    if b.distance > b.counter:
        b.special2 = random.choice([proc_large_explode,collide_small_explode,collide_spirit_bomb,collide_garbage_dump,collide_pulse,collide_encircle])
        b.special_chance = 1
    return [], b

def proc_swirl(b):
    b.counter += 1
    if b.counter % random.randint(1,30) == 0:
        b.y_speed -= 3 *cmp(b.y_speed,0)
        b.counter = 0

    if b.y_speed == 0:
        b.y_speed = random.choice([-1,1])

    return [], b
def proc_create_bee(b):
    bee = extra_bullet((b.sprite.x,b.sprite.y), b.damage, 0, 0, random.randint(1,3))
    bee.special1 = attr_bees
    bee.special1_chance = .5
    return [bee], b

##############################
###### Collision Events ######
##############################
def collide_smite(b):
    smite = extra_bullet((b.sprite.x,window_height), b.damage * 2, 0, -20)
    smite.pierce = 1
    smite.range = window_height - b.sprite.y + 40
    smite.special1 = attr_grow
    smite.special1_chance = .3
    smite.special2 = proc_smite_explode
    smite.counter = window_height - b.sprite.y
    smite.special2_chance = 1
    return [smite], b





def collide_spirit_bomb(b):
    smite = extra_bullet((b.sprite.x,window_height), b.damage * 2, 0, -2)
    smite.pierce = 1
    smite.range = window_height - b.sprite.y +20
    smite.special1 = attr_grow
    smite.special1_chance = 1
    smite.special2 = attr_bullet_move_left
    smite.special2_chance = 1
    return [smite], b






def collide_garbage_dump(b):
    bullets = []
    for i in range(random.randint(10,20)):
        bullets.append(extra_bullet((b.sprite.x+random.randint(-10,10),b.sprite.y+random.randint(0,100)), b.damage, (random.random()-.5)*10, random.randint(-20,-2), random.randint(1,10)))
    for i in range(random.randint(10,20)):
        bullets.append(extra_bullet((b.sprite.x+random.randint(-10,10),b.sprite.y+random.randint(-100,0)), b.damage, (random.random()-.5)*10, random.randint(-20,-2), random.randint(1,10)))
    return bullets, b

def collide_small_explode(b):
    bullets = []
    for i in range(10):
        bullets.append(extra_bullet((b.sprite.x,b.sprite.y), b.damage, (random.random()-.5)*20, (random.random()-.5)*20, 1))
    for bs in bullets:
        bs.range = 25
    return bullets, b



def collide_encircle(b):

    bee = [extra_bullet((b.sprite.x+50, b.sprite.y+50), b.damage, -3, -3, 2, special1=attr_bullet_left, special2=attr_bullet_down, special1_chance=1, special2_chance=1),
    extra_bullet((b.sprite.x+50, b.sprite.y-50), b.damage, -3, 3, 2, special1=attr_bullet_left, special2=attr_bullet_up, special1_chance=1, special2_chance=1),
    extra_bullet((b.sprite.x-50, b.sprite.y+50), b.damage, 3, -3, 2, special1=attr_bullet_right, special2=attr_bullet_down, special1_chance=1, special2_chance=1),
    extra_bullet((b.sprite.x-50, b.sprite.y-50), b.damage, 3, 3, 2, special1=attr_bullet_right, special2=attr_bullet_up, special1_chance=1, special2_chance=1),
    extra_bullet((b.sprite.x+100, b.sprite.y), b.damage, -6, 0, 2, special1=attr_bullet_left, special1_chance=1),
    extra_bullet((b.sprite.x-100, b.sprite.y), b.damage, 6, 0, 2, special1=attr_bullet_right, special1_chance=1),
    extra_bullet((b.sprite.x, b.sprite.y+100), b.damage, 0, -6, 2, special1=attr_bullet_down, special1_chance=1),
    extra_bullet((b.sprite.x, b.sprite.y-100), b.damage, 0, 6, 2, special1=attr_bullet_up, special1_chance=1),]

    # bee = [extra_bullet((b.sprite.x+50, b.sprite.y+50), b.damage, 0, 0, 2, special1=attr_bullet_left, special2=attr_bullet_down, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x+50, b.sprite.y-50), b.damage, 0, 0, 2, special1=attr_bullet_left, special2=attr_bullet_up, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x-50, b.sprite.y+50), b.damage, 0, 0, 2, special1=attr_bullet_right, special2=attr_bullet_down, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x-50, b.sprite.y-50), b.damage, 0, 0, 2, special1=attr_bullet_right, special2=attr_bullet_up, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x+100, b.sprite.y), b.damage, 0, 0, 2, special1=attr_bullet_left, special2=attr_bullet_left, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x-100, b.sprite.y), b.damage, 0, 0, 2, special1=attr_bullet_right, special2=attr_bullet_right, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x, b.sprite.y+100), b.damage, 0, 0, 2, special1=attr_bullet_down, special2=attr_bullet_down, special1_chance=1, special2_chance=1),
    # extra_bullet((b.sprite.x, b.sprite.y-100), b.damage, 0, 0, 2, special1=attr_bullet_up, special2=attr_bullet_up, special1_chance=1, special2_chance=1)]
    return bee, b


def collide_pulse(b):
    # if b.distance > 50:
    a = extra_bullet((b.sprite.x, b.sprite.y), b.damage, 3, 2, 2)
    c = extra_bullet((b.sprite.x, b.sprite.y), b.damage, 3, -2, 2)
    d = extra_bullet((b.sprite.x, b.sprite.y), b.damage, -3, 2, 2)
    e = extra_bullet((b.sprite.x, b.sprite.y), b.damage, -3, -2, 2)
    f = extra_bullet((b.sprite.x, b.sprite.y), b.damage, 5, 0, 2)
    g = extra_bullet((b.sprite.x, b.sprite.y), b.damage, -5, 0, 2)
    h = extra_bullet((b.sprite.x, b.sprite.y), b.damage, 0, 5, 2)
    i = extra_bullet((b.sprite.x, b.sprite.y), b.damage, 0, -5, 2)
    return [a,c,d,e,f,g,h,i], b


gun_j = {

# basics
'gun_type':'pistol',
'x_speed':7,
'y_speed':0,
'size':3,
'shot_range':300,
'acc':0,
'damage':1,
'reload':15,
'nano':0,
'pierce':0,
'special1':attr_none,
'special1_chance':1,
'special2':attr_none,
'special2_chance':0,

'collide':collide_smite,
'collide_chance':1,
}


gun_k = {'gun_type':'rifle',
'x_speed':10,
'y_speed':0,
'size':3,
'shot_range':500,
'acc':1,
'damage':1,
'reload':5,
'nano':0,
'pierce':0,
# proc
'special1':attr_none,
'special1_chance':0,
'special2':proc_create_bee,
'special2_chance':.1,

'collide':attr_none,
'collide_chance':0,
}

gun_l = {'gun_type':'sniper',
'x_speed':20,
'y_speed':0,
'size':30,
'shot_range':1000,
'acc':1,
'damage':10,
'reload':100,
'nano':500,
'pierce':0,
'special1':attr_none,
'special1_chance':.01,
'special2':attr_none,
'special2_chance':.01,

'collide':attr_none,
'collide_chance':0,
}

gun_i = {'gun_type':'grenade',
'x_speed':7,
'y_speed':15,
'size':10,
'shot_range':1000,
'acc':1,
'damage':10,
'reload':100,
'nano':500,
'pierce':0,
'special1':attr_gravity,
'special1_chance':.7,
'special2':attr_none,
'special2_chance':.01,

'collide':collide_garbage_dump,
'collide_chance':1,
}

gun_jump = {'gun_type':'jetpack',
'x_speed':0,
'y_speed':-2,
'size':2,
'shot_range':30,
'acc':5,
'damage':1,
'reload':0,
'nano':0,
'pierce':0,
'special1':attr_none,
'special1_chance':0,
'special2':attr_none,
'special2_chance':.01,

'collide':attr_none,
'collide_chance':0,
}
def get_gun():
    return gun_i,gun_j,gun_k
