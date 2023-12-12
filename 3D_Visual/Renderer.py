__author__ = 'Yarden Frank'
from Projection import *
from Object3D import *


class Renderer:
    def __init__(self):
        self.RES = self.WIDTH, self.HEIGHT = 1600 * 0.8, 900 * 0.8  # resolution
        self.projection = Projection(self)
        self.FPS = 60
        self.screen = pg.display.set_mode(self.RES)
        self.clock = pg.time.Clock()
        self.cube = Object3D(self, 'cube')
        self.pyramid = Object3D(self, 'pyramid')
        self.pyramid.color = [254, 254, 1]

        self.run()

    def draw(self):
        #self.screen.fill(pg.Color('black'))
        self.cube.draw()
        self.pyramid.draw()

        self.cube.rotate_x(self.cube.angle)  # rotating the object
        self.cube.rotate_y(-self.cube.angle)
        self.cube.rotate_z(self.cube.angle)
        self.cube.translate((0.005, 0.005, 0))
        self.cube.scale(0.999)

        self.pyramid.rotate_y(self.pyramid.angle)  # rotating the object
        self.pyramid.rotate_z(-self.pyramid.angle)

    def run(self):
        while True:
            [exit() for i in pg.event.get() if i.type == pg.QUIT or (i.type == pg.KEYDOWN and i.key == pg.K_ESCAPE)]
            self.draw()
            pg.display.flip()
            pg.display.set_caption('FPS: ' + str(int(self.clock.get_fps())))
            self.clock.tick(self.FPS)
