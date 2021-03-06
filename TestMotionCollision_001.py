# Starter code for an adventure type game.
# University of Utah, David Johnson, 2017.
# This code, or code derived from this code, may not be shared without permission.
# Authors: Ivan Lee and Celine Cavanaugh

import sys, pygame, math


# This function loads a series of sprite images stored in a folder with a
# consistent naming pattern: sprite_# or sprite_##. It returns a list of the images.
def load_piskell_sprite(sprite_folder_name, number_of_frames):
    frame_counts = []
    padding = math.ceil(math.log(number_of_frames, 2))
    for frame in range(number_of_frames):
        folder_and_file_name = sprite_folder_name + "/sprite_" + str(frame).rjust(padding, '0') + ".png"
        frame_counts.append(pygame.image.load(folder_and_file_name).convert_alpha())

    return frame_counts

def load_tiles_and_dict_and_rect():
    watertile = pygame.image.load("Water_Tile.png").convert_alpha()
    mosstile = pygame.image.load("Moss_Tile.png").convert_alpha()
    stonetile = pygame.image.load("Stone_Tile.png").convert_alpha()
    tiles_rect = stonetile.get_rect()

    tiles = {}
    tiles[(0,157,255,255)] = watertile
    tiles[(0,67,7,255)] = mosstile
    tiles[(129,129,129,255)] = stonetile

    return (tiles, tiles_rect)

# The main loop handles most of the game
def main():
    # Initialize pygame
    pygame.init()

    screen_size = height, width = (700, 500)
    screen = pygame.display.set_mode(screen_size)

    #load minimap
    world = pygame.image.load("Mini_Map.png").convert()
    world_rect = world.get_rect()
    (mapx, mapy) = (0, 0)

    #Tile different terrain types
    tiles, tiles_rect = load_tiles_and_dict_and_rect()
    #tiles that fit on the screen
    map_tile_width = (width // tiles_rect.width) + 10
    map_tile_height = (height // tiles_rect.height) + 1

    # create the hero character
    hero = load_piskell_sprite("hero", 1)
    hero_rect = hero[0].get_rect()
    hero_rect.center = (350, 250)

    # add in another character
    snake = pygame.image.load("snake.png").convert_alpha()
    snake_rect = snake.get_rect()
    snake_rect.center = 700, 800

    sword = pygame.image.load("sword.png").convert_alpha()
    sword_rect = sword.get_rect()
    sword_rect.center = 200, 200

    potion = pygame.image.load("potion.png").convert_alpha()
    potion_rect = potion.get_rect()
    potion_rect.center = 500, 300

    crown = pygame.image.load("crown.png").convert_alpha()
    crown_rect = crown.get_rect()
    crown_rect.center = 100, 200

    key = pygame.image.load("key.png").convert_alpha()
    key_rect = key.get_rect()
    key_rect.center = 100, 200

    # add in a treasure item
    treasure = pygame.image.load("treasurechest2.png").convert_alpha()
    treasure_rect = treasure.get_rect()
    treasure_rect.center = 750, 400

    # The clock helps us manage the frames per second of the animation
    clock = pygame.time.Clock()

    # Mostly used to cycle the animation of sprites
    frame_count = 0;

    # variable to show if we are still playing the game
    playing = True

    # variable for hero direction
    is_facing_left = True

    # Variable to track text on the screen. If you set the dialog string to something and set the position and the
    # counter, the text will show on the screen for dialog_counter number of frames.
    dialog_counter = 0
    dialog = ''
    dialog_position = (0, 0)

    #where the character is
    mapx = 0
    mapy = 0

    # Load font
    pygame.font.init()  # you have to call this at the start,
    # if you want to use this module.
    myfont = pygame.font.SysFont('Comic Sans MS', 30)

    # create the inventory and make it empty
    inventory = {}

    # This list should hold all the sprite rectangles that get shifted with a key press.
    rect_list = [snake_rect, treasure_rect, key_rect, crown_rect, sword_rect, potion_rect]

    # Loop while the player is still active
    while playing:
        # start the next frame
        screen.fill((170, 190, 190))

        # Check events by looping over the list of events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                playing = False

        # check for keys that are pressed
        # Note the indent makes it part of the while playing but not part of the for event loop.
        keys = pygame.key.get_pressed()
        # check for specific keys
        # movement says how the world should shift. Pressing keys changes the value in the movement variables.
        movement_x = 0
        movement_y = 0
        if keys[pygame.K_LEFT]:
            is_facing_left = True
            movement_x += 5
        if keys[pygame.K_RIGHT]:
            is_facing_left = False
            movement_x -= 5
        if keys[pygame.K_UP]:
            movement_y += 5
        if keys[pygame.K_DOWN]:
            movement_y -= 5


        #stop character from moving off the map
        if mapx < 0:
            mapx = 0
        if mapx > world.get_width()-1-(map_tile_width-1):
            mapx = world.get_width()-1-(map_tile_width-1)
        if mapy < 0:
            mapy = 0
        if mapy > world.get_height()-1-(map_tile_height-1):
            mapy = world.get_height()-1-(map_tile_height-1)

        # Move all the sprites in the scene by movement amount.
        # You can still move the rect of an individual sprite to make
        # it move around the landscape.
        for rect in rect_list:
            rect.move_ip(movement_x, movement_y)

        #drawing the map
        for y in range(0, map_tile_height):
            y_index = y + mapy
            for x in range(0, map_tile_width):
                x_index = x + mapx
                pixelColor = world.get_at((x_index, y_index))
                tiles_rect.topleft = (x * tiles_rect.width, y * tiles_rect.height)
                screen.blit(tiles[tuple(pixelColor)], tiles_rect)

        # Check for touching ghost.
        if hero_rect.colliderect(snake_rect):
            # Respond differently depending on gold status
            if "sword" and "potion" and "crown" in inventory:
                dialog = "No! You have defeated me."
            else:
                dialog = "Die puny mortal. (game end)"
            # These say where and for how long the dialog prints on the screen
            dialog_counter = 50
            dialog_position = (100, 100)


        # Check for touching the gold chest.
        if hero_rect.colliderect(treasure_rect) and "gold" not in inventory:
            inventory["gold"] = True
            dialog = "Gold added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(sword_rect) and "sword" not in inventory:
            inventory["sword"] = True
            dialog = "Sword added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(potion_rect) and "potion" not in inventory:
            inventory["potion"] = True
            dialog = "Potion added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(key_rect) and "key" not in inventory:
            inventory["key"] = True
            dialog = "Key added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        if hero_rect.colliderect(crown_rect) and "crown" not in inventory:
            inventory["crown"] = True
            dialog = "Crown added to inventory"
            dialog_counter = 30
            dialog_position = (300, 200)

        # Draw the characters
        screen.blit(snake, snake_rect)
        pygame.draw.rect(screen, (0, 255, 0), snake_rect, 3)

        # Only draw the gold if it hasn't been picked up

        if "sword" not in inventory:
            screen.blit(sword, sword_rect)
        if "potion" not in inventory:
            screen.blit(potion, potion_rect)
        if "crown" not in inventory:
            screen.blit(crown, crown_rect)
        if "gold" not in inventory and hero_rect.colliderect(snake_rect):
            screen.blit(treasure, treasure_rect)

        # Pick the sprite frame to draw
        hero_sprite = hero[frame_count % len(hero)]
        # Flip the sprite depending on direction
        if not is_facing_left:
            hero_sprite = pygame.transform.flip(hero_sprite, True, False)
        screen.blit(hero_sprite, hero_rect)
        pygame.draw.rect(screen, (0, 255, 0), hero_rect, 3)

        # draw any dialog
        if dialog:
            textsurface = myfont.render(dialog, False, (0, 0, 0))
            screen.blit(textsurface, dialog_position)
            # Track how long the dialog is on screen
            dialog_counter -= 1
            if dialog_counter == 0:
                dialog = ''

        # Bring drawn changes to the front
        pygame.display.update()

        frame_count += 1

        # 30 fps
        clock.tick(30)

        #draw the minimap
        screen.blit(world, world_rect)

    # loop is over
    pygame.quit()
    sys.exit()


# Start the program
main()