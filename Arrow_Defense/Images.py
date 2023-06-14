import pygame
from os import environ

environ['SDL_VIDEO_CENTERED'] = '1'

pygame.init()

info = pygame.display.Info()
WIDTH, HEIGHT = 1200, 675

screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.font.init()
score_font = pygame.font.Font('assets/font.ttf', 30)
headline_font = pygame.font.Font('assets/font.ttf', 60)
little_font = pygame.font.Font('assets/font.ttf', 20)


logo = pygame.image.load('assets/logo.png').convert_alpha()
logo = pygame.transform.scale(logo, (int(logo.get_width() * WIDTH // 400), int(logo.get_height() * WIDTH // 400)))

start_image = pygame.image.load('assets/icons/start.png').convert_alpha()
start_image = pygame.transform.scale(start_image, (int(start_image.get_width() * WIDTH // 400), int(start_image.get_height() * WIDTH // 400)))

how_to_play = pygame.image.load('assets/icons/how_to_play.png').convert_alpha()
how_to_play = pygame.transform.scale(how_to_play, (int(how_to_play.get_width() * WIDTH // 400), int(how_to_play.get_height() * WIDTH // 400)))

tutorial = pygame.image.load('assets/tutorial.png').convert_alpha()
tutorial = pygame.transform.scale(tutorial, (int(tutorial.get_width() * WIDTH // 1000), int(tutorial.get_height() * WIDTH // 1000)))

exit_tutorial = pygame.image.load('assets/icons/exit.png').convert_alpha()

arrow_image = pygame.transform.scale(pygame.image.load('assets/arrow.png'), (WIDTH // 30, WIDTH // 30)).convert_alpha()
background = pygame.image.load('assets/background.jpg').convert_alpha()
background = pygame.transform.scale(background, (WIDTH * 2, HEIGHT))

platform = pygame.image.load('assets/platform.png').convert_alpha()
platform = pygame.transform.scale(platform, pygame.Vector2(platform.get_size()) / 1.5)

pause_image = pygame.image.load('assets/icons/pause.png').convert_alpha()
play_image = pygame.image.load('assets/icons/play.png').convert_alpha()
home_image = pygame.image.load('assets/icons/home.png').convert_alpha()

# bow
bow1 = pygame.image.load('assets/bows/bow1.png').convert_alpha()
bow2 = pygame.image.load('assets/bows/bow2.png').convert_alpha()
bow3 = pygame.image.load('assets/bows/bow3.png').convert_alpha()
bow4 = pygame.image.load('assets/bows/bow4.png').convert_alpha()
bow5 = pygame.image.load('assets/bows/bow5.png').convert_alpha()
bow6 = pygame.image.load('assets/bows/bow6.png').convert_alpha()
bows = [bow1, bow2, bow3, bow4, bow5, bow6]

# NPC
player_image_1 = pygame.image.load('assets/player_animation/1.png').convert_alpha()
player_image_2 = pygame.image.load('assets/player_animation/2.png').convert_alpha()
player_image_3 = pygame.image.load('assets/player_animation/3.png').convert_alpha()
player_image_4 = pygame.image.load('assets/player_animation/4.png').convert_alpha()
player_image_5 = pygame.image.load('assets/player_animation/5.png').convert_alpha()
player_image_6 = pygame.image.load('assets/player_animation/6.png').convert_alpha()
player_image_7 = pygame.image.load('assets/player_animation/7.png').convert_alpha()
player_image_8 = pygame.image.load('assets/player_animation/8.png').convert_alpha()
player_image_9 = pygame.image.load('assets/player_animation/9.png').convert_alpha()
enemy_image = pygame.transform.flip(player_image_1, True, False)

players = [player_image_1, player_image_2, player_image_3, player_image_4, player_image_5, player_image_6,
           player_image_7, player_image_8, player_image_9]

# player
pl1 = pygame.image.load('assets/pl_animation/p1.png').convert_alpha()
pl2 = pygame.image.load('assets/pl_animation/p2.png').convert_alpha()
pl3 = pygame.image.load('assets/pl_animation/p3.png').convert_alpha()
pl4 = pygame.image.load('assets/pl_animation/p4.png').convert_alpha()
pl5 = pygame.image.load('assets/pl_animation/p5.png').convert_alpha()
pl6 = pygame.image.load('assets/pl_animation/p6.png').convert_alpha()

pls = [pl1, pl2, pl3, pl4, pl5, pl6]

castle_image = pygame.image.load('assets/castle.png').convert_alpha()
castle_image = pygame.transform.scale(castle_image, pygame.Vector2(castle_image.get_size()) * 0.25)

trophy_image = pygame.image.load('assets/trophy.png').convert_alpha()
skull_image = pygame.image.load('assets/skull.png').convert_alpha()
skull_image = pygame.transform.scale(skull_image, (34, 40))
heart_image = pygame.image.load('assets/heart.png').convert_alpha()
heart_image = pygame.transform.scale(heart_image, (38, 36))


def fill(surface, color):
    """Fill all pixels of the surface with color, preserve transparency."""
    image = pygame.Surface.copy(surface)
    w, h = image.get_size()
    r, g, b = color
    for x in range(w):
        for y in range(h):
            a = image.get_at((x, y))[3]
            image.set_at((x, y), pygame.Color(r, g, b, a))

    return image


def resize(sprite_list, size):
    new_list = []
    for sprite in sprite_list:
        sprite = pygame.transform.scale(sprite, pygame.Vector2(sprite.get_size()) * size)
        new_list.append(sprite)

    return new_list


pl_size = WIDTH / 5200
pl1, pl2, pl3, pl4, pl5, pl6 = resize(pls, pl_size)

arrow_image = pygame.transform.scale(arrow_image, pygame.Vector2(arrow_image.get_size()) * 0.7)
enemy_arrow = fill(arrow_image, (255, 25, 25))

bows = resize(bows, 0.6)
assets = [castle_image, platform, arrow_image, trophy_image, skull_image, heart_image]
for bow in bows:
    assets.append(bow)
for player in players:
    assets.append(player)

new_assets = resize(assets, WIDTH / 1200)
castle_image, platform, arrow_image, trophy_image, skull_image, heart_image, bow1, bow2, bow3, bow4, bow5, bow6, player_image_1, player_image_2, \
    player_image_3, player_image_4, player_image_5, player_image_6, player_image_7, player_image_8, player_image_9 = new_assets

# sounds
pygame.mixer.init()
click_sound = pygame.mixer.Sound('assets/sounds/click_sound.wav')
bow_draw = pygame.mixer.Sound('assets/sounds/bow_draw.wav')
shot_sound = pygame.mixer.Sound('assets/sounds/shot_sound.wav')
shot_sound.set_volume(0.2)
walk_sound = pygame.mixer.Sound('assets/sounds/walk_sound.wav')
walk_sound.set_volume(0.5)
jump_sound = pygame.mixer.Sound('assets/sounds/jump_sound.wav')
jump_sound.set_volume(0.3)
hit_sound = pygame.mixer.Sound('assets/sounds/hit_sound.wav')
hit_sound.set_volume(0.5)
hurt_sound = pygame.mixer.Sound('assets/sounds/hurt_sound.wav')
hurt_sound.set_volume(0.2)

lose_sound = pygame.mixer.Sound('assets/sounds/lose_sound.wav')
lose_sound.set_volume(0.1)
win_sound = pygame.mixer.Sound('assets/sounds/win_sound.wav')
win_sound.set_volume(0.5)

# music
pygame.mixer.music.load('assets/sounds/music.mp3')
pygame.mixer.music.set_volume(0.3)
