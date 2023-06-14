import pygame.mouse

from Settings import *
import random
from Player import Player
from NPC import NPC
from Crosshair import Crosshair
from Enemy import Enemy
from Camera import CameraGroup
from Button import Button
from Object import Platform, Castle


class Game:
    def __init__(self):
        pygame.mixer_music.play(-1)
        self.start = True
        self.game_over = False
        self.win = False
        self.pause = False
        self.difficulty = 0
        self.time_spawn = time_spawn

        self.number_of_enemies = 10

        self.max_score = 0

        self.camera_group = CameraGroup()

        self.player = Player(pl1, 50, player_start)
        self.ally = NPC(player_image_1, 150, ally_start)
        self.ally2 = NPC(player_image_1, 238, ally_start + HEIGHT // 7.5)
        self.enemy = Enemy(enemy_image, max_right, enemy_start)

        self.players = pygame.sprite.Group()
        self.players.add(self.player, self.ally, self.ally2)

        self.enemy_group = pygame.sprite.Group()
        self.enemy_group.add(self.enemy)
        self.enemy_list = [self.enemy]

        self.camera_group.add(self.players, self.enemy_group)
        self.camera_group.add(Platform(), Castle())

        self.players_arrows = pygame.sprite.Group()
        self.enemy_arrows = pygame.sprite.Group()

        self.crosshair = Crosshair(0.035)
        self.timer = 10

        self.max_enemies = enemy_number
        self.kills = 0
        self.total_kills = 0
        self.lives = self.player.health

        self.space = 50
        self.text_height = HEIGHT - HEIGHT / 25
        self.skull_x = 50

        self.pause_screen = pygame.Surface((0, 0))

        self.pause_button = Button(self.skull_x + 10.5 * self.space, HEIGHT // 1.04, pause_image, WIDTH / 12000)
        self.play_button = Button(WIDTH // 2, HEIGHT // 2, play_image, WIDTH / 5000)
        self.start_button = Button(WIDTH // 2, HEIGHT // 1.2, start_image, WIDTH / 20000)
        self.how_to_play_button = Button(WIDTH // 2, HEIGHT // 1.1, how_to_play, WIDTH / 20000)
        self.exit_button1 = Button(WIDTH // 1.505, HEIGHT // 3.4, exit_tutorial, WIDTH / 20000)
        self.exit_button2 = Button(self.skull_x + 13.5 * self.space, HEIGHT // 1.04, fill(exit_tutorial, (255, 0, 0)), WIDTH / 20000)
        self.home_button = Button(self.skull_x + 12 * self.space, HEIGHT // 1.04, home_image, WIDTH / 40000)
        self.show_tutorial = False

        self.shoot_time = self.enemy.shoot_time
        self.enemy_speed = self.enemy.speed
        self.miss_delta = self.enemy.miss_delta
        self.animation_time = self.enemy.animation_time

        # sounds
        self.walk_sound = False

    def update(self):
        if self.start:
            self.start_game()
        else:
            self.lives = self.player.health
            self.draw_window()

            if self.lives == 0:
                if not self.game_over:
                    pygame.mixer.music.stop()
                    lose_sound.play()
                    self.game_over = True

            if self.game_over:
                self.over()
                self.display_score()
            elif self.win:
                self.won()

            else:
                self.add_players()
                self.display_score()
                self.check_win()
                self.event_loop()
                self.key_input()
                self.handle_enemies()
                enemy_arrow.set_alpha(255)

    def draw_window(self):
        if not self.pause:
            self.camera_group.custom_draw(self.players_arrows, self.enemy_arrows)
            if self.pause_button.draw(screen):
                self.pause = True
                self.pause_screen = screen.copy()

        else:
            self.display_menu()

        if self.home_button.draw(screen):
            self.start = True
        if self.exit_button2.draw(screen):
            pygame.quit()
            exit()

        self.crosshair.draw(screen)

    def event_loop(self):
        for event in pygame.event.get():  # Event Loop
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.MOUSEBUTTONUP:
                if self.player.alive():
                    bow_draw.stop()
                    self.player.bow_draw_played = False
                    self.player.shoot()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_SPACE \
                        or event.key == pygame.K_w:
                    if self.player.height + 1 >= self.player.collision_rect.y >= self.player.height - 1\
                            and not self.player.is_on_ladder():
                        jump_sound.play()
                        self.player.y_velocity = (-12)
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

    def add_players(self):
        self.players_arrows.add(self.player.arrow_group, self.ally.arrow_group, self.ally2.arrow_group)
        for enemy in self.enemy_list:
            self.enemy_arrows.add(enemy.arrow_group)

        self.camera_group.add(self.players_arrows, self.enemy_arrows)

        if pygame.time.get_ticks() % 800 <= random.randint(self.time_spawn - 1, self.time_spawn + 1) \
                and len(self.enemy_group) < self.max_enemies:
            new_enemy = Enemy(enemy_image, max_right, enemy_start)
            self.camera_group.add(new_enemy.arrow_group)
            self.enemy_group.add(new_enemy)
            self.camera_group.add(self.enemy_group)
            self.enemy_list.append(new_enemy)

    def key_input(self):
        key_input = pygame.key.get_pressed()  # moving the player left and right

        if key_input[pygame.K_LEFT] or key_input[pygame.K_a]:
            if self.player.rect.x > 5:
                self.player.walk('left')
                if not self.walk_sound:
                    walk_sound.play(-1)
                    self.walk_sound = True
        elif key_input[pygame.K_RIGHT] or key_input[pygame.K_d]:
            if self.player.rect.x < WIDTH // 4:
                self.player.walk('right')
                if not self.walk_sound:
                    walk_sound.play(-1)
                    self.walk_sound = True

        else:
            self.walk_sound = False
            walk_sound.stop()

        if key_input[pygame.K_DOWN] or key_input[pygame.K_s]:
            if self.player.on_ladder():
                self.player.rect.y += 1

        if key_input[pygame.K_UP] or key_input[pygame.K_w]:
            if self.player.on_ladder():
                self.player.rect.y -= 1

    def handle_enemies(self):
        for enemy in self.enemy_list:
            if not enemy.alive():
                self.enemy_list.remove(enemy)
            elif enemy.dead and enemy.dead_time == 50:
                self.kills += 1

            enemy.shoot_time = self.shoot_time
            enemy.miss_delta = self.miss_delta
            enemy.speed = self.enemy_speed
            enemy.animation_time = self.animation_time

        if len(self.enemy_list) > 0:
            if self.enemy_list[0].rect.x > enemy_stop - enemy_space:
                self.enemy_list[0].last_enemy_x = enemy_stop
            for i in range(1, len(self.enemy_list)):
                self.enemy_list[i].last_enemy_x = self.enemy_list[i - 1].rect.x

    # draw_text('LEVEL COMPLETE!', font, WHITE, (200, 300))
    @staticmethod
    def draw_text(text, font, color, pos):
        img = font.render(text, True, color)
        rect = img.get_rect()
        rect.center = pos
        screen.blit(img, rect)

    def display_score(self):
        lives = str(self.lives)
        kills = str(self.total_kills + self.kills)
        max_kills = str(self.max_score)
        difficulty = self.convert_difficulty()
        enemies_left = str(self.number_of_enemies - self.kills)

        screen.blit(skull_image, (self.skull_x, self.text_height - WIDTH // 60))
        self.draw_text(kills, score_font, 'white', (self.skull_x + self.space + 10, self.text_height))
        screen.blit(heart_image, (self.skull_x + 2 * self.space, self.text_height - WIDTH // 65))
        self.draw_text(lives, score_font, 'white', (self.skull_x + 3 * self.space + 15, self.text_height))

        self.draw_text(difficulty, score_font, 'white', (self.skull_x + 5 * self.space + 30, self.text_height))
        self.draw_text('left:', little_font, 'white', (self.skull_x + 8 * self.space, self.text_height + 2))
        self.draw_text(enemies_left, little_font, 'white', (self.skull_x + 9 * self.space, self.text_height + 2))

        screen.blit(trophy_image, (WIDTH - 120, self.text_height - 20))
        self.draw_text(max_kills, score_font, 'white', (WIDTH - 110 + self.space, self.text_height))

    def difficulty_changes(self):
        if self.kills == self.number_of_enemies:
            self.difficulty += 1

            self.enemy_speed += 2
            self.animation_time = round((-3 / 4) * self.difficulty + 4)
            self.shoot_time = self.enemy_list[-1].shoot_time // 1.5
            self.miss_delta = self.enemy_list[-1].miss_delta * 2 // 3

            self.total_kills += self.kills
            self.kills = 0
            self.number_of_enemies += 5
            self.time_spawn += 2
            self.max_enemies += 4

    def check_win(self):
        self.difficulty_changes()

        if self.difficulty > 2:
            self.difficulty = 2
            pygame.mixer.music.stop()
            win_sound.play()
            self.win = True

    def convert_difficulty(self):
        if self.difficulty == 0:
            return 'easy'
        if self.difficulty == 1:
            return 'medium'
        else:
            return 'hard'

    def start_game(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()

        pygame.mouse.set_visible(True)
        screen.fill('black')
        rect = logo.get_rect()
        rect.center = (WIDTH // 2, HEIGHT // 2)
        screen.blit(logo, rect)

        if self.start_button.draw(screen):
            self.start = False
            pygame.mouse.set_visible(False)

        if self.how_to_play_button.draw(screen):
            self.show_tutorial = True

        if self.show_tutorial:
            rect = tutorial.get_rect()
            rect.center = (WIDTH // 2, HEIGHT // 1.5)
            screen.blit(tutorial, rect)
            if self.exit_button1.draw(screen):
                self.show_tutorial = False

    def display_menu(self):
        screen.blit(self.pause_screen, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
        if self.play_button.draw(screen):
            self.pause = False

    def reset(self, max_score):
        self.__init__()
        self.max_score = max_score

    def reset_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    exit()
                self.reset(max(self.max_score, self.total_kills + self.kills))

    def over(self):
        line1 = 'GAME OVER'
        line2 = 'press anywhere to start'

        self.draw_text(line1, headline_font, (255, 50, 50), (WIDTH // 2, HEIGHT // 2 - 100))
        self.draw_text(line2, score_font, 'white', (WIDTH // 2, HEIGHT // 2 - 50))

        self.reset_event()

    def won(self):
        line1 = 'YOU WON!'
        line2 = 'press anywhere to start'

        self.draw_text(line1, headline_font, (50, 255, 50), (WIDTH // 2, HEIGHT // 2 - 100))
        self.draw_text(line2, score_font, 'white', (WIDTH // 2, HEIGHT // 2 - 50))

        self.reset_event()
