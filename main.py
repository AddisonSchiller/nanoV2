import random
import math
import pyglet

from pyglet.gl import *
from pyglet.window import key

from character import Character
from enemy import make_enemies
from gun import bullet, generate_gun
from collision2 import sprite_collision
from terrain import terrain_frame, terrain, fill_terrain, terrain_batch,build_base
from defaults import Experience_breakpoints,window_height, window_width, background, foreground,gfx_batch,Stash_batch,Shop_batch,Gun_batch,update_shop, update_stash,update_gun
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

window = pyglet.window.Window(window_width, window_height)
global window_grid, c
# Initialize the terrain character and push its key handler
def initialize_level():
    window_grid = [[0]*(window_width/200) for i in xrange(window_height/200)]
    global c,e, terrains, start_location, end_location, end_sprite, base
    e = make_enemies()
    terrains, start_location, end_location, end_sprite = fill_terrain(window_grid)
    c = Character(start_location, terrains, e, end_sprite,c)
    c.base = False
    c.area_level += 1
    window.push_handlers(c.key_handler)

#load character from file if it exists, if not, use baselines of new char
def load_character(hp=100,nano=0,gun_parts=0,level = 1,xp = 0):
    global c,e, terrains, start_location, end_location, end_sprite
    terrains, start_location, end_location, end_sprite = build_base()
    e = []
    c = Character(start_location, terrains, e, end_sprite)
    c.hp,c.max_hp,c.nano_coins,c.gun_parts,c.level,c.experience = hp,hp,nano,gun_parts,level,xp


#load into base after death or at start of game
def start_base():
    window_grid = [[0]*(window_width/200) for i in xrange(window_height/200)]
    global c,e, terrains, start_location, end_location, end_sprite
    terrains, start_location, end_location, end_sprite = build_base()
    e = []
    try:
        c = Character(start_location, terrains, e, end_sprite,c)
    except:
        c = Character(start_location, terrains, e, end_sprite)
    c.base = True
    c.area_level = 0
    window.push_handlers(c.key_handler)

#grants experience and money, also interacts with still in developemtn xp/leveling system
#should be moved into enemy object
def drop_loot():
    global c
    drop = random.randint(0,8)

    for i in range(drop):
        c.nano_coins += random.randint(0,5)
    c.gun_parts += 1
    c.gun_base_list.append(generate_gun())
    if c.level < 100:
        c.experience += (1.1**c.area_level)/2 +1
        print c.experience," ",c.level

        if c.experience >= Experience_breakpoints[c.level]:
            c.experience = c.experience - Experience_breakpoints[c.level]
            c.level +=1
            c.max_hp += 5
            c.hp = c.max_hp


try:
    save = open('Saves/pony.save','r')
    exec save.read()
except:
    pass
start_base()

def update(ts):
    if c.hp < 0:
        c.hp = c.max_hp
        for enemy in c.e:
            enemy.sprite.delete
            enemy.health.delete
            c.e.remove(enemy)
        for n, b in enumerate(c.bullets):
            c.removeBullet(b)
        start_base()
    if c.checks > 1:
        c.checks = 0
        if c.save > 5:
            new_save = open('/Saves/pony.save','w')
            savefunc = "load_character(" + str(c.max_hp) + "," + str(c.nano_coins) + "," + str(c.gun_parts) + "," + str(c.level) + "," + str(c.experience) + ")"
            new_save.write(savefunc)
            new_save.close
            c.save = 0
        if c.reset > 1:
            c.reset = 0
            for enemy in c.e:
                enemy.sprite.delete
                enemy.health.delete
                c.e.remove(enemy)
            for n, b in enumerate(c.bullets):
                c.removeBullet(b)
            initialize_level()


    c.update(ts, bullet)
    c.update_bullets(ts)
    c.update_assets(ts)
    # for enemy in e:
    #     enemy.sprite.x += random.choice([5,-5])
    #     enemy.health = pyglet.sprite.Sprite(img=pyglet.image.create(enemy.hp*45/enemy.max_hp, 1, enemy.pattern), x = enemy.sprite.x, y = enemy.sprite.y + enemy.sprite.height+5)

    for n, b in enumerate(c.bullets):

        for enemy in c.e:
            if sprite_collision(enemy.sprite, b.sprite):
                enemy.hp -= b.damage
                added_bullets, c.bullets[n] = b.proc_collide(b)
                c.bullets += added_bullets
                c.removeBullet(b)
                if enemy.hp <= 0:
                    enemy.sprite.delete
                    enemy.health.delete
                    drop_loot()
                    c.e.remove(enemy)
                break


def update_ai(ts):
    for enemy in e:
        enemy.ai((c.sprite.x, c.sprite.y))
        if sprite_collision(c.sprite, enemy.sprite) and c.immune_ticks == 0:
            c.immune_ticks = 30
            if c.shield > 0:
                c.shield -= enemy.touch_damage *c.area_level
            else:
                c.hp -= enemy.touch_damage * c.area_level
        # try:
        #     # THIS NEEDS TO HANDLE THE FRAME
        #     for t in terrains[int(enemy.sprite.y) / 200][int(enemy.sprite.x) / 200]:
        #         if sprite_collision(t.sprite, enemy.sprite):
        #             enemy.sprite.x -= enemy.x_speed * 2
        #             enemy.sprite.y -= enemy.y_speed * 2
        #             enemy.last_collision = (enemy.sprite.x, enemy.sprite.y)
        #             break
        #
        #     for t in terrains[int(enemy.sprite.y) / 200][int(enemy.sprite.x) / 200 + 1]:
        #         if sprite_collision(t.sprite, enemy.sprite):
        #             enemy.sprite.x -= enemy.x_speed * 2
        #             enemy.sprite.y -= enemy.y_speed * 2
        #             enemy.last_collision = (enemy.sprite.x, enemy.sprite.y)
        #             break
        #
        #     for t in terrains[int(enemy.sprite.y) / 200 + 1][int(enemy.sprite.x) / 200]:
        #         if sprite_collision(t.sprite, enemy.sprite):
        #             enemy.sprite.x -= enemy.x_speed * 2
        #             enemy.sprite.y -= enemy.y_speed * 2
        #             enemy.last_collision = (enemy.sprite.x, enemy.sprite.y)
        #             break
        #
        #     for t in terrains[int(enemy.sprite.y) / 200 + 1][int(enemy.sprite.x) / 200 + 1]:
        #         if sprite_collision(t.sprite, enemy.sprite):
        #             enemy.sprite.x -= enemy.x_speed * 2
        #             enemy.sprite.y -= enemy.y_speed * 2
        #             enemy.last_collision = (enemy.sprite.x, enemy.sprite.y)
        #             break
        #
        # except IndexError:
        #     pass


pyglet.clock.schedule_interval(update,  1 / 100.0)

pyglet.clock.schedule_interval(update_ai,  1 / 100.0)

@window.event
def on_draw():
    # clear for next draw
    window.clear()
    end_sprite.draw()

    # draw gray background
    pyglet.gl.glClearColor(0.5, 0.5, 0.5, 1)

    # draw the character
    if c.base == True:
        c.merchant.draw()
        c.stash.draw()
        if c.show_stash >= 30:
            update_stash(c)
            update_gun(c)
            Stash_batch.draw()
            Gun_batch.draw()
        if c.shop >= 30:
            update_shop(c)
            Shop_batch.draw()
    c.char_gun_parts_label.text = str(c.gun_parts)
    c.coin_label.text = str(c.nano_coins)
    c.char_gun_parts_label.draw()
    c.sprite.draw()
    c.health_bar.draw()
    c.shield_bar.draw()
    c.nano_bar.draw()
    c.reload_bar.draw()
    c.coin_label.draw()
    gfx_batch.draw()
    for enemy in e:
        enemy.sprite.draw()
        enemy.health.draw()

    terrain_batch.draw()

pyglet.app.run()
