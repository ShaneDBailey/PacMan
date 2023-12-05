# Main Game
import pygame
import numpy
import json
import Items
import Constants
import PacMan
class Board:

    def __init__(self):
        self.colors = numpy.array([[0, 0, 0],[100, 100, 255],[255, 255, 255]])
        self.dots = {}
        #set dots as a dictionary with maps of (x,y), instance.dot so when pacman is over .del
        with open('PacManBoard.json', 'r') as file:
            array = json.load(file)

        self.boardGrid = [list(row) for row in zip(*array)]
        self.surface = pygame.Surface((Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT))
        self.surface.fill((0,0,0))
        square = pygame.Surface((Constants.TILESIZE, Constants.TILESIZE))
        square.fill(self.colors[1])

        for x in range(len(self.boardGrid)):
            for y in range(len(self.boardGrid[0])):
                cell = self.boardGrid[x][y]
                if cell == 0:
                    self.dots[(x, y)] = Items.Dots(x, y)
                elif cell == 1:
                    self.surface.blit(square, (x*Constants.TILESIZE, y*Constants.TILESIZE))
                elif cell == 3:
                    self.dots[(x, y)] = Items.BigDots(x, y)
                elif cell == 4:
                    self.player = PacMan.Pacman(x*Constants.TILESIZE,y*Constants.TILESIZE)
                
    def drawBoard(self):
        pass
    
    def drawDots(self, screen):
        for dot_coord, dot_instance in self.dots.items():
            dot_instance.draw(screen)

    def deleteDot(self, x, y):
        dot_coord = (x, y)
        if dot_coord in self.dots:
            del self.dots[dot_coord]


def main():
    pygame.init()
    screen = pygame.display.set_mode((Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT))
    clock = pygame.time.Clock()

    gameBoard = Board()

    screen = pygame.display.set_mode((gameBoard.surface.get_width(), gameBoard.surface.get_height()))
    screen.blit(gameBoard.surface, (0, 0))

    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(gameBoard.surface, (0,0))
        gameBoard.drawDots(screen)
        gameBoard.player.update(gameBoard)
        gameBoard.player.draw(screen)

        gameBoard.deleteDot(gameBoard.player.gridx,gameBoard.player.gridy)
        
        pygame.display.flip()
        


main()
