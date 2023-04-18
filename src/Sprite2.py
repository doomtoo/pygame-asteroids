import pygame as pg

# https://stackoverflow.com/questions/15526858/how-to-extend-a-class-in-python



class Sprite2(pg.sprite.Sprite):

    def __init__(self):
        pg.sprite.Sprite.__init__(self, self.containers)