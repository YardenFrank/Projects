from Settings import *
from Enemy import Enemy
from Player import Player
from Enemy_Arrow import EnemyArrow
from Arrow import Arrow


class CameraGroup(pygame.sprite.Group):
    def __init__(self):
        super().__init__()

        # camera offset
        self.offset = pygame.math.Vector2()
        self.half_w = WIDTH // 2
        self.half_h = HEIGHT // 2

        # box setup
        self.camera_borders = {'left': 100, 'right': 100, 'top': 50, 'bottom': 0}
        left = self.camera_borders['left']
        t = self.camera_borders['top']
        w = WIDTH - (self.camera_borders['left'] + self.camera_borders['right'])
        h = HEIGHT - (self.camera_borders['top'] + self.camera_borders['bottom'])
        self.camera_rect = pygame.Rect(left, t, w, h)

        # ground
        self.ground_surf = background
        self.ground_rect = self.ground_surf.get_rect(topleft=(0, 0))

        # camera speed
        self.keyboard_speed = 5
        self.mouse_speed = 1

        # zoom
        self.zoom_scale = 1
        self.internal_surf_size = (WIDTH, HEIGHT)
        self.internal_surf = pygame.Surface(self.internal_surf_size, pygame.SRCALPHA)
        self.internal_rect = self.internal_surf.get_rect(center=(self.half_w, self.half_h))
        self.internal_surface_size_vector = pygame.math.Vector2(self.internal_surf_size)
        self.internal_offset = pygame.math.Vector2()
        self.internal_offset.x = self.internal_surf_size[0] // 2 - self.half_w
        self.internal_offset.y = self.internal_surf_size[1] // 2 - self.half_h

    def center_target_camera(self, target):
        self.offset.x = target.rect.centerx - self.half_w
        self.offset.y = target.rect.centery - self.half_h

    def box_target_camera(self, target):

        if target.rect.left < self.camera_rect.left:
            self.camera_rect.left = target.rect.left
        if target.rect.right > self.camera_rect.right:
            self.camera_rect.right = target.rect.right
        if target.rect.top < self.camera_rect.top:
            self.camera_rect.top = target.rect.top
        if target.rect.bottom > self.camera_rect.bottom:
            self.camera_rect.bottom = target.rect.bottom

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def keyboard_control(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a]:
            self.camera_rect.x -= self.keyboard_speed
        if keys[pygame.K_d]:
            self.camera_rect.x += self.keyboard_speed
        if keys[pygame.K_w]:
            self.camera_rect.y -= self.keyboard_speed
        if keys[pygame.K_s]:
            self.camera_rect.y += self.keyboard_speed

        self.offset.x = self.camera_rect.left - self.camera_borders['left']
        self.offset.y = self.camera_rect.top - self.camera_borders['top']

    def mouse_control(self):
        mouse = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset_vector = pygame.math.Vector2()

        left_border = self.camera_borders['left']
        top_border = self.camera_borders['top']
        right_border = WIDTH - self.camera_borders['right']
        bottom_border = HEIGHT - self.camera_borders['bottom']

        if top_border < mouse.y < bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector.x = mouse.x - left_border
                pygame.mouse.set_pos((left_border, mouse.y))
            if mouse.x > right_border:
                mouse_offset_vector.x = mouse.x - right_border
                pygame.mouse.set_pos((right_border, mouse.y))
        elif mouse.y < top_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, top_border)
                pygame.mouse.set_pos((left_border, top_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, top_border)
                pygame.mouse.set_pos((right_border, top_border))
        elif mouse.y > bottom_border:
            if mouse.x < left_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(left_border, bottom_border)
                pygame.mouse.set_pos((left_border, bottom_border))
            if mouse.x > right_border:
                mouse_offset_vector = mouse - pygame.math.Vector2(right_border, bottom_border)
                pygame.mouse.set_pos((right_border, bottom_border))

        if left_border < mouse.x < right_border:
            if mouse.y < top_border:
                mouse_offset_vector.y = mouse.y - top_border
                pygame.mouse.set_pos((mouse.x, top_border))
            if mouse.y > bottom_border:
                mouse_offset_vector.y = mouse.y - bottom_border
                pygame.mouse.set_pos((mouse.x, bottom_border))

        self.offset += mouse_offset_vector * self.mouse_speed

    def zoom_keyboard_control(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_z] and self.zoom_scale < 2:
            self.zoom_scale += 0.1
        if keys[pygame.K_x] and self.zoom_scale > 1:
            self.zoom_scale -= 0.1

    def custom_draw(self, player_arrows, enemy_arrows):
        self.mouse_control()

        # ground
        ground_offset = self.ground_rect.topleft - self.offset

        self.limit(ground_offset)

        self.internal_surf.blit(self.ground_surf, ground_offset)

        # active elements
        players1 = []
        enemies = []
        other = []

        for element in self.sprites():
            if isinstance(element, Enemy):
                enemies.append(element)
            elif isinstance(element, Player):
                players1.append(element)
            else:
                other.append(element)

        self.handle_other(other)
        self.handle_players(players1, enemy_arrows)
        self.handle_enemies(enemies, player_arrows)

        scaled_surf = pygame.transform.scale(self.internal_surf, self.internal_surface_size_vector * self.zoom_scale)
        scaled_rect = scaled_surf.get_rect(center=(self.half_w, self.half_h))

        screen.blit(scaled_surf, scaled_rect)

    def handle_players(self, players1, enemy_arrows):
        for player1 in players1:
            offset_pos1 = player1.rect.center - self.offset
            player1.offset = self.offset
            player1.update(self.internal_surf, enemy_arrows, offset_pos1)

    def handle_enemies(self, enemies, player_arrows):
        for enemy in enemies:
            offset_pos2 = enemy.rect.center - self.offset
            enemy.update(self.internal_surf, player_arrows, offset_pos2)

    def handle_other(self, other):
        for sprite in other:
            offset_pos3 = sprite.rect.center - self.offset
            if isinstance(sprite, Arrow):
                if isinstance(sprite, EnemyArrow):
                    sprite.offset = pygame.Vector2(0, 0)
                else:
                    sprite.offset = self.offset

            sprite.update(self.internal_surf, offset_pos3)

    def limit(self, ground_offset):
        limit_right = 300 * self.zoom_scale
        if self.offset.x >= limit_right:
            self.offset.x = limit_right
            ground_offset.x = (-limit_right)

        limit_left = (1 - self.zoom_scale) * self.half_w / 2
        if self.offset.x <= limit_left:
            self.offset.x = limit_left
            ground_offset.x = (-limit_left)

        limit_up = (1 - self.zoom_scale) * self.half_h / 2
        if self.offset.y <= limit_up:
            self.offset.y = limit_up
            ground_offset.y = (-limit_up)

        limit_down = (self.zoom_scale - 1) * self.half_h / 2
        if self.offset.y >= limit_down:
            self.offset.y = limit_down
            ground_offset.y = (-limit_down)
