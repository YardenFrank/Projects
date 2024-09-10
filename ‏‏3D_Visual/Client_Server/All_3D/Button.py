import pygame as pg


def colorize(image, newColor):
    if not image:
        return None
    image = image.copy()
    image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
    image.fill(newColor[0:3] + (0,), None, pg.BLEND_RGBA_ADD)

    return image


# button class
class Button:
    def __init__(self, screen, pos, size=None, image=None, scale=None, drag=False, leave_on=True, buttontype=None, color=((231, 231, 231), (237, 175, 2))):
        self.button_type = buttontype
        self.screen = screen
        self.color = color  # deactivated, activated
        self.image_path = image
        self.pos_0 = None
        self.image, self.rect = None, None
        self.adjust_size(size=size, scale=scale, image=image)
        self.rect.center = pos
        self.leave_on = leave_on
        self.time_on = 0
        self.on = 0
        self.drag = drag  # if the purpose of pressing the button is to drag it
        self.clicked = False
        self.let_go = False

    def update(self, allowed):
        self.draw(allowed)

    def draw(self, allowed):
        # draw button on screen
        if self.image:
            self.screen.blit(self.image, (self.rect.x, self.rect.y))
        mouse_state = pg.mouse.get_pressed()[0]
        if self.drag:
            self.drag_button(mouse_state, allowed)
        else:
            self.one_click_button(mouse_state, allowed)

    def drag_button(self, mouse_state, allowed):
        if mouse_state == 1 and not self.on and allowed:
            pos = pg.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.turn_on()
        elif mouse_state == 0 and self.on:
            self.let_go = True
            self.turn_off()

    def one_click_button(self, mouse_state, allowed):
        if mouse_state == 1 and allowed and not self.clicked:
            pos = pg.mouse.get_pos()
            if self.rect.collidepoint(pos):
                self.click()
                self.clicked = True
        elif mouse_state == 0:
            self.clicked = False
        if self.on and not self.leave_on:
            self.time_on += 1
            if self.time_on > 7:
                self.time_on = 0
                self.click()

    def turn_on(self):
        self.on = 1
        self.image = colorize(self.image, self.color[1])

    def turn_off(self):
        self.on = 0
        self.image = colorize(self.image, self.color[0])

    def click(self):
        self.on = 1 - self.on
        self.image = colorize(self.image, self.color[self.on])

    def update_pos(self, pos):
        self.rect.center = pos

    def rel_update_pos(self, rel):
        current_pos = self.get_pos()
        self.rect.center = (current_pos[0] + rel[0], current_pos[1] + rel[1])

    def get_pos(self):
        return self.rect.center

    def adjust_size(self, size=None, scale=None, image=None):  # either size or scale
        if image:
            image = pg.image.load(image)
            if scale:
                size = image.get_width() * scale, image.get_height() * scale
            image = pg.transform.smoothscale(image, size)
            image = colorize(image, self.color[0])
            self.image = image
        self.rect = pg.Rect((0, 0), size)
