#Pacman class
import pygame
import Constants

class Pacman:

    def __init__(self,x,y):
        self.color = [255,51,0]
        self.x = x
        self.y = y
        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE
        self.desired_direction = [0,0]
        self.current_direction = [0,0]

    def fully_inside_square(self, gridx, gridy):
        tile_left = gridx*Constants.TILESIZE
        tile_right = tile_left + Constants.TILESIZE
        tile_top = gridy*Constants.TILESIZE
        tile_bottom = tile_top + Constants.TILESIZE
        return (self.x > tile_left-2) and ((self.x + Constants.TILESIZE) < tile_right+2) and (self.y > tile_top-2) and ((self.y + Constants.TILESIZE) < tile_bottom+2)

    def update(self, board):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.desired_direction = [0, -1]
        elif keys[pygame.K_s]:
            self.desired_direction = [0, 1]
        elif keys[pygame.K_a]:
            self.desired_direction = [-1, 0]
        elif keys[pygame.K_d]:
            self.desired_direction = [1, 0]
        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE

        print(self.desired_direction, self.current_direction, self.gridx, self.gridy, board.boardGrid[self.gridx+self.desired_direction[0]][self.gridy+self.desired_direction[1]])

        if self.fully_inside_square(self.gridx, self.gridy):
            if board.boardGrid[self.gridx+self.desired_direction[0]][self.gridy+self.desired_direction[1]] in (0, 3, 4):
                #cell we want to move into is empty
                self.current_direction = self.desired_direction.copy()

        #is pacman fully inside a cell
        # TILE_LEFT = gridx*TILESIZE
        # TILE_RIGHT = (gridx*TILESIZE) + TILESIZE
        # self.x > TILE_LEFT and self.x+TILESIZE < TILE_RIGHT

        #mystery of why both
        if not self.fully_inside_square(self.gridx, self.gridy):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]
            
        elif board.boardGrid[self.gridx+self.current_direction[0]][self.gridy+self.current_direction[1]] in (0, 3, 4):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]

    def draw(self, screen):
        # circle(surface, color, center, radius)
        #updateDirection()
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.x + Constants.TILESIZE - Constants.TILESIZE/2,
                self.y + Constants.TILESIZE - Constants.TILESIZE/2,
            ),
            Constants.TILESIZE/2
        )