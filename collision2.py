from defaults import  window_height, window_width, frame_width

def sprite_collision(sprite1, sprite2):
    br = (sprite1.x, sprite1.y, sprite1.x + sprite1.width, sprite1.y + sprite1.height)
    tr = (sprite2.x, sprite2.y, sprite2.x + sprite2.width, sprite2.y + sprite2.height)
    return collision(br,tr)

def collision(rect1, rect2):
    return not(rect1[0]>rect2[2] or rect2[0]>rect1[2] or rect1[1]>rect2[3] or rect2[1]>rect1[3])

def check_frame_collision(char):
    return char.x < frame_width or\
        char.y + char.height > window_height - frame_width or\
        char.x + char.width > window_width - frame_width or \
        char.y < frame_width

# Checks which grids you collide with and checks collision only for the objects in that grid
def check_grid_collision(char, terrains):
    char_grid = (char.y/200, char.x/200)
    for t in terrains[char_grid[0]][char_grid[1]]:
        if sprite_collision(char, t.sprite):
            return True

    # In theory you don't need to check down or left since the original check
    ## is done on the bottom left, lets see if this works in practice.

    # If the width of the sprite goes into the next grid right
    right = (char.x + char.width)/200 != char_grid[1]
    up = (char.y + char.height)/200 != char_grid[0]
    if right:
        for t in terrains[char_grid[0]][char_grid[1]+1]:
            if sprite_collision(char, t.sprite):
                return True

    # If the height of the sprite goes into the next grid up
    if up:
        for t in terrains[char_grid[0]+1][char_grid[1]]:
            if sprite_collision(char, t.sprite):
                return True

    # If height and width goes into upper right
    if up and right:
        for t in terrains[char_grid[0]+1][char_grid[1]+1]:
            if sprite_collision(char, t.sprite):
                return True

    return False
