import pyglet
import random
from pyglet.gl import *


# window properties and grid (in pixels)

window_height = 800
window_width = 1400
num_col = window_width/200
num_row = window_height/200
frame_width = 10


# batches
gfx_batch = pyglet.graphics.Batch()

# levels
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)


#Stash bars
Stash_batch = pyglet.graphics.Batch()
stash_label1 = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/2 +50, y=window_height/2 +40,anchor_x='left', anchor_y='center', batch=Stash_batch)
stash_label2 = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/2 + 50, y=window_height/2 +20,anchor_x='left', anchor_y='center', batch=Stash_batch)
stash_label3 = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/2 +50, y=window_height/2,anchor_x='left', anchor_y='center', batch=Stash_batch)
stash_label2.color = (0,255,0,255)

#crafting bars
Shop_batch = pyglet.graphics.Batch()
gun_parts_amount = pyglet.text.Label("0",font_name='Times New Roman',font_size=16,x= window_width/2 +50, y=window_height/2 +40,anchor_x='left', anchor_y='center',batch = Shop_batch)
gun_parts_label = pyglet.text.Label("parts",font_name='Times New Roman',font_size=16,x= window_width/2 -50 , y=window_height/2 +40,anchor_x='left', anchor_y='center',batch = Shop_batch)
gun_base_choice = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/2 + 50, y=window_height/2 +20,anchor_x='left', anchor_y='center',batch = Shop_batch)
gun_base_label = pyglet.text.Label("base",font_name='Times New Roman',font_size=16,x= window_width/2 -50, y=window_height/2 +20,anchor_x='left', anchor_y='center',batch = Shop_batch)
input_coin_label = pyglet.text.Label("coins",font_name='Times New Roman',font_size=16,x= window_width/2 -50, y=window_height/2,anchor_x='left', anchor_y='center',batch = Shop_batch)
coin_amount_label = pyglet.text.Label("0",font_name='Times New Roman',font_size=16,x= window_width/2 +50, y=window_height/2,anchor_x='left', anchor_y='center',batch = Shop_batch)
okay_label = pyglet.text.Label("ok",font_name='Times New Roman',font_size=16,x= window_width/2, y=window_height/2 -20 ,anchor_x='left', anchor_y='center',batch = Shop_batch)


#gun stats bars
Gun_batch = pyglet.graphics.Batch()
gun_type_label = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/1.5 +50, y=window_height/2 ,anchor_x='left', anchor_y='center', batch=Gun_batch)
gun_speed_label = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/1.5 +50, y=window_height/2 -20,anchor_x='left', anchor_y='center', batch=Gun_batch)
gun_damage_label = pyglet.text.Label("None",font_name='Times New Roman',font_size=16,x= window_width/1.5 +50, y=window_height/2 -40,anchor_x='left', anchor_y='center', batch=Gun_batch)

# xp breakpoints
Experience_breakpoints = {}
for i in range(0,99):
    Experience_breakpoints[i +1] = 50 * (i) + 10 * 1.06**i
def update_shop(c):
    if c.selection == 0:
        gun_parts_amount.color = (0,255,0,255)
    else:
        gun_parts_amount.color = (255,255,255,255)

    if c.selection == 1:
        gun_base_choice.color = (0,255,0,255)
    else:
        gun_base_choice.color = (255,255,255,255)

    if c.selection == 2:
        coin_amount_label.color = (0,255,0,255)
    else:
        coin_amount_label.color = (255,255,255,255)

    if c.selection == 3:
        okay_label.color = (0,255,0,255)
    else:
        okay_label.color = (255,255,255,255)
    try:
        gun_base_choice.text = str(c.gun_base_amount +1) + ' ' +c.gun_base_list[c.gun_base_amount]['gun_type']
    except:
        pass
    gun_parts_amount.text = str(c.gun_part_amount)
    coin_amount_label.text = str(c.coin_amount)

def update_stash(c):
    try:
        stash_label2.text = c.gun_list[c.selection].gun_type
    except:
        stash_label2.text = 'Empty'
    try:
        stash_label1.text = c.gun_list[c.selection -1].gun_type
    except:
        stash_label1.text = ''
    try:
        if c.selection +1 == len(c.gun_list):
            stash_label3.text = c.gun_list[0].gun_type
        else:
            stash_label3.text = c.gun_list[c.selection +1].gun_type
    except:
        stash_label3.text = ''

def update_gun(c):
    try:
        gun_type_label.text = "Gun Type: " + c.gun_list[c.selection].gun_type
    except:
        gun_type_label.text = "Gun Type: "
    try:
        gun_speed_label.text = "Speed: " + str(c.gun_list[c.selection].x_speed)
    except:
        gun_speed_label.text = "Speed: "
    try:
        gun_damage_label.text = "Damage: " + str(c.gun_list[c.selection].damage)
    except:
        gun_damage_label.text = "Damage: "
