import math
import pyglet
import random
from defaults import gfx_batch
from pyglet.window import key
from pyglet.gl import *
from collision2 import sprite_collision, check_grid_collision, check_frame_collision
from gun import bullet, gun, gun_j, gun_k, gun_l, gun_i, gun_jump, jetpack, generate_gun
from defaults import num_row, num_col, window_height, window_width
# load character images
char_stand = pyglet.image.load('sprites/robochar.png')
char_walk = pyglet.image.load('sprites/robochar_walk.png')
char_crouch = pyglet.image.load('sprites/robochar_crouch.png')
char_crouch_walk = pyglet.image.load('sprites/robochar_crouch_walk.png')

char_stand_left = pyglet.image.load('sprites/robochar_left.png')
char_walk_left = pyglet.image.load('sprites/robochar_walk_left.png')
char_crouch_left = pyglet.image.load('sprites/robochar_crouch_left.png')
char_crouch_walk_left = pyglet.image.load('sprites/robochar_crouch_walk_left.png')

sprite_dict = {
                1:{ 1:{1:char_crouch, 0:char_crouch_walk}, 0:{1:char_walk, 0:char_stand}},
                -1:{ 1:{1:char_crouch_left, 0:char_crouch_walk_left}, 0:{1:char_walk_left, 0:char_stand_left}}
                }

white_sprite = pyglet.image.SolidColorImagePattern(color=(255, 255, 255, 150))
red_sprite = pyglet.image.SolidColorImagePattern(color=(255, 0, 0, 150))
green_sprite = pyglet.image.SolidColorImagePattern(color=(0, 255, 0, 150))
blue_sprite = pyglet.image.SolidColorImagePattern(color=(0, 0, 255, 150))

char_green = pyglet.image.create(25, 50, green_sprite)

char_green_crouch = pyglet.image.create(25, 25, green_sprite)

class Character(object):
    def __init__(self, start_location, terrains, e, end_sprite, c = "none"):
        # start_location in form (x, y) coords
        self.direction = 1
        self.sprite = pyglet.sprite.Sprite(char_stand, start_location[0], start_location[1])
        merchant_sprite = pyglet.image.load('sprites/Smith_test.png')
        stash_sprite= pyglet.image.load('sprites/Stash.png')
        self.merchant = pyglet.sprite.Sprite(merchant_sprite, window_width - 200, 10)
        self.stash = pyglet.sprite.Sprite(stash_sprite,400,10)

        # self.sprite = pyglet.sprite.Sprite(char_green, start_location[0], start_location[1])

        self.key_handler = key.KeyStateHandler()
        self.end_sprite = end_sprite
        self.bullets = []

        # movement
        self.accel = 0
        self.jump_height = 200
        self.jump_height_max = 200
        self.crouch = 0
        self.walk = 1

        # Initialize guns
        try:
            self.gun_j = c.gun_j
        except:
            self.gun_j = gun(gun_j)
        self.gun_k = gun(gun_k)
        self.gun_l = gun(gun_l)
        self.gun_i = gun(gun_i)
        self.gun_jump = gun(gun_jump)
        try:
            self.gun_list = c.gun_list
        except:
            self.gun_list = []
        try:
            self.gun_base_list = c.gun_base_list
        except:
            self.gun_base_list = []
        # character attributes

        # immunity
        self.immune_ticks = 0

        # hp

        # shield
        self.shield = 100
        self.max_shield = 100

        # nano
        self.nano = 500
        self.max_nano = 500
        try:
            self.nano_coins = c.nano_coins
        except:
            self.nano_coins = 0
        try:
            self.gun_parts = c.gun_parts
        except:
            self.gun_parts = 0
        # reload (frames between shots)

        self.reload = 100
        self.reload_time = 100
        # xp
        try:
            self.level = c.level
        except:
            self.level = 1
        try:
            self.experience = c.experience
        except:
            self.experience = 0
        try:
            self.hp = c.hp
            self.base_hp= c.base_hp
        except:
            self.hp = 100
            self.base_hp = 100
        self.max_hp = self.base_hp + 5*self.level




        self.terrains = terrains
        self.e = e
        self.run_speed = 3
        self.reload = 10
        self.reset = 0
        self.save = 0
        self.checks = 0
        self.shop = 0
        self.gun_part_amount = 0
        self.gun_base_amount = 0
        self.coin_amount = 0
        self.selection = 0
        self.selection_counter = 0
        self.okay = 0
        self.base = True
        self.show_stash = 0
        try:
            self.area_level = c.area_level
        except:
            self.area_level = 0
        # bars
        self.shield_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.shield*100/self.max_shield, 3, green_sprite), x = 50, y = window_height-40)
        try:
            self.health_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.hp*100/self.max_hp, 3, red_sprite), x = 50, y = window_height-50)
        except:
            self.health_bar = pyglet.sprite.Sprite(img=pyglet.image.create(1*100/self.max_hp, 3, red_sprite), x = 50, y = window_height-50)

        self.nano_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.nano*100/self.max_nano, 3, blue_sprite), x = 50, y = window_height-60)
        self.reload_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.reload*100/self.reload_time, 3, white_sprite), x = 50, y = window_height-70)
        self.coin_label = pyglet.text.Label(str(self.nano_coins),font_name='Times New Roman',font_size=16,x= window_width - 50, y=window_height-50,anchor_x='center', anchor_y='center')
        self.char_gun_parts_label = pyglet.text.Label(str(self.gun_parts),font_name='Times New Roman',font_size=16,x= window_width - 50, y=window_height-70,anchor_x='center', anchor_y='center')
    def set_direction(self, move):
        direction = 1
        if move < 0:
            move = abs(move)
            direction = -1
        return move, direction

    def resolve_sprite(self, move_x):
        if self.walk > 0:
            self.sprite.image = sprite_dict[self.direction][self.crouch][0]
            if self.walk>3:
                self.walk = -3
        else:
            self.sprite.image = sprite_dict[self.direction][self.crouch][1]

    def handle_movement(self, move_x, move_y):
        # This function takes the movement from key presses and translates it into
        # character movement, one pixel at a time checking collision
        # within the current grid and any other grids that the character sprite collides with
        move_x, x_direction = self.set_direction(move_x)
        move_y, y_direction = self.set_direction(move_y)

        while move_x > 0:
            self.sprite.x += 1*x_direction
            move_x -= 1

            if check_grid_collision(self.sprite, self.terrains) or check_frame_collision(self.sprite):
                self.sprite.x -= 1*x_direction
                break

        while move_y > 0:
            self.sprite.y += 1*y_direction
            move_y -= 1
            if check_grid_collision(self.sprite, self.terrains) or check_frame_collision(self.sprite):
                self.sprite.y -= 1*y_direction
                if y_direction == -1:
                    self.jump_height = self.jump_height_max
                    self.accel = 0
                break
    def update_assets(self, ts):

        if self.immune_ticks >0:
            self.immune_ticks -= 1
        if self.reload<self.reload_time:
            self.reload += 1

        if self.nano < self.max_nano:
            self.nano += 3

        if self.accel > -6:
            self.accel -= 1
        try:
            self.shield_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.shield*100/self.max_shield, 3, green_sprite), x = 50, y = window_height-40)
        except:
            pass
        try:
            self.health_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.hp*100/self.max_hp, 3, red_sprite), x = 50, y = window_height-50)
        except:
            pass
        try:
            self.nano_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.nano*100/self.max_nano, 3, blue_sprite), x = 50, y = window_height-60)
        except:
            pass
        try:
            self.reload_bar = pyglet.sprite.Sprite(img=pyglet.image.create(self.reload*100/self.reload_time, 3, white_sprite), x = 50, y = window_height-70)
        except:
            pass




    def update(self, ts, bullet):
        move_x = 0
        move_y = 0

        # Check for movement
        if self.key_handler[key.D]:
            self.direction = 1
            self.walk +=1
            move_x += self.run_speed

        if self.key_handler[key.A]:
            self.direction = -1
            self.walk +=1
            move_x -= self.run_speed

        if self.key_handler[key.W]:
            if self.jump_height > 0:
                self.bullets += [jetpack((self.sprite.x+15-9*self.direction, self.sprite.y+self.sprite.height/2), self.gun_jump, (random.randint(200,255), random.randint(0,255), random.randint(0,50), 255))]
                self.jump_height -= 1
                self.accel += 3
                if self.accel>6:
                    self.accel = 6

        move_y += self.accel
        #
        # if self.key_handler[key.R]:
        #     self.gun_k = gun(generate_gun())

        # Gun K
        if self.key_handler[key.K]:
            if len(self.bullets) < 50 and self.reload >= self.gun_k.reload and self.gun_k.nano <= self.nano:
                self.nano -= self.gun_k.nano
                self.reload = 0
                self.bullets += [bullet((self.sprite.x+15+13*self.direction, self.sprite.y+self.sprite.height-17), self.gun_k, self.direction)]

        # Gun K
        if self.key_handler[key.I]:
            if len(self.bullets) < 50 and self.reload >= self.gun_i.reload and self.gun_i.nano <= self.nano:
                self.nano -= self.gun_i.nano
                self.reload = 0
                self.bullets += [bullet((self.sprite.x+15+13*self.direction, self.sprite.y+self.sprite.height-17), self.gun_i, self.direction)]

        # Gun L
        if self.key_handler[key.L]:
            if len(self.bullets) < 50 and self.reload >= self.gun_l.reload and self.gun_l.nano <= self.nano:
                self.nano -= self.gun_l.nano
                self.reload = 0
                self.bullets += [bullet((self.sprite.x+15+13*self.direction, self.sprite.y+self.sprite.height-17), self.gun_l, self.direction)]

        # Gun J
        if self.key_handler[key.J]:
            if len(self.bullets) < 50 and self.reload >= 20:
                self.reload = 0
                self.bullets += [bullet((self.sprite.x+15+13*self.direction, self.sprite.y+self.sprite.height-17), self.gun_j, self.direction)]

        if self.key_handler[key.S]:
            self.crouch = 1
        else:
            self.crouch = 0
        if self.key_handler[key.ENTER]:
            if self.base == True and self.show_stash > 30:
                self.selection_counter += 1
                if self.selection_counter > 15:
                    self.selection_counter = 0
                    try:
                        swap = self.gun_j
                        self.gun_j = self.gun_list[self.selection]
                        self.gun_list.pop(self.selection)
                        self.gun_list.insert(self.selection,swap)
                    except:
                        pass

        if self.key_handler[key.E]:
            if sprite_collision(self.sprite, self.end_sprite):
                self.reset+= 1
                self.checks+= 1
            if sprite_collision(self.sprite, self.merchant):
                 self.shop+=1
                 self.show_stash = 0
                 if self.shop == 30:
                     self.shop += 1
                     self.selection,self.gun_part_amount,self.okay,self.gun_base_amount,self.coin_amount = 0,0,0,0,0
                 if self.shop > 60:
                     self.shop = 0
                 self.checks += 1
            if sprite_collision(self.sprite, self.stash):
                self.show_stash +=1
                self.shop = 0
                if self.show_stash == 30:
                    self.show_stash += 1
                    self.selection = 0
                if self.show_stash > 60:
                    self.show_stash = 0
                self.checks += 1


        if self.key_handler[key.P]:
            self.save +=1
            self.checks+= 1

        if self.key_handler[key.UP]:
            if self.base == True and self.show_stash >30:
               self.selection_counter += 1
               if self.selection_counter > 4:
                   self.selection_counter = 0
                   self.selection -=1
                   if self.selection < 0:
                       self.selection = len(self.gun_list) -1
            if self.base == True and self.shop > 30:
                self.selection_counter += 1
                if self.selection_counter > 4:
                    self.selection_counter = 0
                    self.selection -= 1
                    if self.selection < 0:
                        self.selection = 3

        if self.key_handler[key.DOWN]:
            if self.base == True and self.show_stash > 30:
                self.selection_counter += 1
                if self.selection_counter > 4:
                    self.selection_counter = 0
                    self.selection += 1
                    if self.selection > len(self.gun_list) -1:
                        self.selection = 0
            if self.base == True and self.shop > 30:
                self.selection_counter += 1
                if self.selection_counter > 4:
                    self.selection_counter = 0
                    self.selection += 1
                    if self.selection > 3:
                        self.selection = 0

        if self.key_handler[key.RIGHT]:
            if self.base == True and self.shop > 30:
                if self.selection == 0:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.gun_part_amount += 1
                        if self.gun_part_amount > self.gun_parts:
                            self.gun_part_amount = 0
                        self.selection_counter = 0
                if self.selection == 2:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.coin_amount += 1
                        if self.coin_amount > self.nano_coins:
                            self.coin_amount = 0
                        self.selection_counter = 0
                if self.selection == 3:
                    self.selection_counter +=1
                    if self.selection_counter > 10:
                        self.okay += 1
                        if self.okay > 10:
                            try:
                                self.gun_list.append(gun(self.gun_base_list[self.gun_base_amount],self.coin_amount,self.gun_part_amount))
                                self.gun_base_list.pop(self.gun_base_amount)
                                self.nano_coins -= self.coin_amount
                                self.gun_parts -= self.gun_part_amount
                                self.okay = 0
                                self.coin_amount = 0
                                self.gun_part_amount = 0
                            except:
                                pass
                        self.selection_counter = 0
                if self.selection == 1:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.gun_base_amount += 1
                        if self.gun_base_amount  > len(self.gun_base_list) -1:
                            self.gun_base_amount =  0
                        self.selection_counter = 0



        if self.key_handler[key.LEFT]:
            if self.base == True and self.shop > 30:
                if self.selection == 0:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.gun_part_amount -= 1
                        if self.gun_part_amount < 0:
                            self.gun_part_amount = self.gun_parts
                        self.selection_counter = 0
                if self.selection == 2:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.coin_amount -= 1
                        if self.coin_amount < 0:
                            self.coin_amount = self.nano_coins
                        self.selection_counter = 0
                if self.selection == 1:
                    self.selection_counter += 1
                    if self.selection_counter > 10:
                        self.gun_base_amount -= 1
                        if self.gun_base_amount  < 0:
                            self.gun_base_amount = len(self.gun_base_list) -1
                        self.selection_counter = 0

        self.resolve_sprite(self)
        self.handle_movement(move_x, move_y)


########
# THIS WHOLE SECTION NEEDS TO BE REFACTORED AGAIN
#######
    def update_bullets(self, ts):
        for n, b in enumerate(self.bullets):

            added_bullets, self.bullets[n] = b.proc_special1(b)
            self.bullets += added_bullets

            added_bullets, self.bullets[n] = b.proc_special2(b)
            self.bullets += added_bullets

            b.sprite.x += b.x_speed
            b.sprite.y += b.y_speed

            # check collision
            try:
                # THIS NEEDS TO HANDLE THE FRAME
                for t in self.terrains[int(b.sprite.y)/200][int(b.sprite.x)/200]:
                    if sprite_collision(t.sprite, b.sprite):
                        added_bullets, self.bullets[n] = b.proc_collide(b)
                        self.bullets += added_bullets
                        if random.random() > b.pierce:
                            try:
                                self.removeBullet(b)
                            except:
                                pass
                            break
            except IndexError:
                added_bullets, self.bullets[n] = b.proc_collide(b)
                self.bullets += added_bullets
                self.removeBullet(b)


            # calcuate total distance moved
            b.distance += abs(b.x_speed) + abs(b.y_speed)

            # if exceeded range, delete
            if b.distance > b.range:
                try:
                    self.removeBullet(b)
                except Exception as err:
                    print err
            pass

    def removeBullet(self, b):
        global gfx_bach
        self.bullets.remove(b)
        b.sprite.delete()
