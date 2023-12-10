#Shane Bailey, Nick Ford


# Main Game
import pygame
import numpy
import json
import Items
import Constants
import PacMan

#Reference guide
#https://gameinternals.com/understanding-pac-man-ghost-behavior

# board will parse the json file for the board, and spawn the corresponding walls, item, ghosts and pacman

class Board:

    def __init__(self):
        self.font = pygame.font.Font(None, 42)
        self.colors = numpy.array([[0, 0, 0],[100, 100, 255],[255, 255, 255]])
        self.dots = {}
        self.ghosts = {}
        self.mood = "scatter"
        self.timer = 0
        self.rounds = 0
        self.frightTimer = 0
        self.pacman_start = None
        self.lives = 3
        self.score = 0
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

                if cell == Constants.DOTS:
                    self.dots[(x, y)] = Items.Dots(x, y)
                elif cell == Constants.BIGDOTS:
                    self.dots[(x, y)] = Items.BigDots(x, y)
                elif cell == Constants.WALLS:
                    self.surface.blit(square, (x*Constants.TILESIZE, y*Constants.TILESIZE))
                elif cell == Constants.PACMAN:
                    self.pacman_start = (x, y)
                    self.player = PacMan.Pacman(x*Constants.TILESIZE,y*Constants.TILESIZE)
                elif cell == Constants.RED:
                    self.ghosts[Constants.RED] = PacMan.Ghost(x*Constants.TILESIZE, y*Constants.TILESIZE,(255,0,0), 3, Constants.RED)
                elif cell == Constants.PINK:
                    self.ghosts[Constants.PINK] = PacMan.Ghost(x*Constants.TILESIZE, y*Constants.TILESIZE,(255,153,204), 9, Constants.PINK)
                elif cell == Constants.BLUE:
                    self.ghosts[Constants.BLUE] = PacMan.Ghost(x*Constants.TILESIZE, y*Constants.TILESIZE,(0,255,255), 15, Constants.BLUE)
                elif cell == Constants.YELLOW:
                    self.ghosts[Constants.YELLOW] = PacMan.Ghost(x*Constants.TILESIZE, y*Constants.TILESIZE,(255,255,0), 21, Constants.YELLOW)

        assert self.pacman_start is not None

    def drawBoard(self):
        pass
    
    def drawDots(self, screen):
        for dot_instance in self.dots.values():
            dot_instance.draw(screen)

    def deleteDot(self):
        dot_coord = (self.player.gridx, self.player.gridy)
        if dot_coord in self.dots:
            self.score += 10
            if isinstance(self.dots[dot_coord], Items.BigDots):
                self.score += 40
                self.mood = "fright"
            del self.dots[dot_coord]

    def pacman_ghost_collison(self):
        collided = False
        for ghost in self.ghosts.values():
            if ghost.gridx == self.player.gridx and ghost.gridy == self.player.gridy:
                collided = True
                break
            
        if collided:
            self.player.x = self.pacman_start[0] * Constants.TILESIZE
            self.player.y = self.pacman_start[1] * Constants.TILESIZE
            self.player.current_direction = (0,1)
            self.player.desired_direction = (0,1)
            self.lives -= 1
            for ghost in self.ghosts.values():
                ghost.state = "ghost_house"
                ghost.state_info = {"timer":3*Constants.FRAME_RATE}
                
        

    def update(self):
        if self.mood == "fright" and self.frightTimer < 10 * Constants.FRAME_RATE:
            self.frightTimer += 1
            
        else:
            self.mood = " "
            self.timer += 1
            self.frightTimer = 0
            
        if(self.mood != "fright" and self.rounds < 5):
            if self.timer < 7 * Constants.FRAME_RATE:
                self.mood = "chase"
            elif self.timer < 27 * Constants.FRAME_RATE:
                self.mood = "scatter"
            else:
                self.timer = 0
                self.rounds += 1

    def draw_score_and_life(self, screen):
        score = self.font.render("Score: " + str(self.score), False, (255,255,255))
        lives = self.font.render("Lives: " + str(self.lives), False, (255,255,255))
        lives_rect = lives.get_rect()
        lives_rect.right = Constants.BOARD_WIDTH
        lives_rect.top = 0
        screen.blit(score, (0,0))
        screen.blit(lives, lives_rect.topleft)



 

def main():
    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((Constants.BOARD_WIDTH, Constants.BOARD_HEIGHT))
    clock = pygame.time.Clock()

    gameBoard = Board()

    screen = pygame.display.set_mode((gameBoard.surface.get_width(), gameBoard.surface.get_height()))
    screen.blit(gameBoard.surface, (0, 0))

    while gameBoard.lives > 0:
        clock.tick(Constants.FRAME_RATE)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(gameBoard.surface, (0,0))
        gameBoard.drawDots(screen)
        gameBoard.player.update(gameBoard)

        gameBoard.player.draw(screen)

        for color in gameBoard.ghosts:
            gameBoard.ghosts[color].update_direction(gameBoard)
            gameBoard.ghosts[color].draw(screen,gameBoard)
        

        gameBoard.deleteDot()
        if gameBoard.mood != "fright":
            gameBoard.pacman_ghost_collison()
        gameBoard.update()

        gameBoard.draw_score_and_life(screen)
        
        pygame.display.flip()

main()
