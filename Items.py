#Items
# Powerup Sub class
import pygame
import Constants

class Dots:
    def __init__(self,x,y):
        self.color = [255,153,0]
        self.x = x
        self.y = y

    def draw(self, screen):
        # circle(surface, color, center, radius)
        pygame.draw.circle(
            screen,
            self.color,
            (
                (self.x*Constants.TILESIZE)+Constants.TILESIZE/2,
                (self.y*Constants.TILESIZE)+Constants.TILESIZE/2,
            ),
            Constants.TILESIZE/6
        )


class BigDots:
    def __init__(self,x,y):
        self.color = [[255,153,0],[255,224,179]]
        self.x = x
        self.y = y
        self.frame_count = 0
        self.frame_max = 90

    def draw(self, screen):
        # circle(surface, color, center, radius)
        self.frame_count += 1
        if(self.frame_count< 45):
            pygame.draw.circle(
                screen,
                self.color[0],
                (
                    (self.x*Constants.TILESIZE)+Constants.TILESIZE/2,
                    (self.y*Constants.TILESIZE)+Constants.TILESIZE/2,
                ),
                Constants.TILESIZE/3
            )
        else:
            pygame.draw.circle(
                screen,
                self.color[1],
                (
                    (self.x*Constants.TILESIZE)+Constants.TILESIZE/2,
                    (self.y*Constants.TILESIZE)+Constants.TILESIZE/2,
                ),
                Constants.TILESIZE/3
            )
        if self.frame_count > 90:
            self.frame_count = 0

