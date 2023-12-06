import pygame
import Constants
import heapq
import math

class Character:

    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y
        self.spacesAllowed = (0,3,4)
        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE
        self.desired_direction = [0, 0]
        self.current_direction = [0, 0]

    def fully_inside_square(self, gridx, gridy):
        tile_left = gridx * Constants.TILESIZE
        tile_right = tile_left + Constants.TILESIZE
        tile_top = gridy * Constants.TILESIZE
        tile_bottom = tile_top + Constants.TILESIZE
        return (
            (self.x > tile_left - 2)
            and ((self.x + Constants.TILESIZE) < tile_right + 2)
            and (self.y > tile_top - 2)
            and ((self.y + Constants.TILESIZE) < tile_bottom + 2)
        )

    def update_position(self, board):
        gridx = self.x // Constants.TILESIZE
        gridy = self.y // Constants.TILESIZE
        if self.fully_inside_square(gridx, gridy):
            if board.boardGrid[gridx + self.desired_direction[0]][gridy + self.desired_direction[1]] in self.spacesAllowed:
                self.current_direction = self.desired_direction.copy()

        if not self.fully_inside_square(gridx, gridy):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]

        elif board.boardGrid[gridx + self.current_direction[0]][gridy + self.current_direction[1]] in (0, 3, 4):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]

        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.x + Constants.TILESIZE - Constants.TILESIZE / 2,
                self.y + Constants.TILESIZE - Constants.TILESIZE / 2,
            ),
            Constants.TILESIZE / 2,
        )

class Pacman(Character):

    def __init__(self, x, y):
        super().__init__(x, y, (255, 51, 0))

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
        super().update_position(board)

class Ghost(Character):

    def __init__(self, x, y):
        super().__init__(x, y, (255, 0, 0))
        self.spacesAllowed = (0,3,4,6,5,7,8)
        self.made_decision = False

    def heuristic(self, current_position, target_position):
        return abs(current_position[0] - target_position[0]) + abs(current_position[1] - target_position[1])
    
    def get_neighbors(self, node, board):
        neighbors = []
        for direction in ((0, 1), (0, -1), (1, 0), (-1, 0)):
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if (
                0 <= neighbor[0] < len(board.boardGrid)
                and 0 <= neighbor[1] < len(board.boardGrid[0])
                and board.boardGrid[neighbor[0]][neighbor[1]] in self.spacesAllowed
            ):
                neighbors.append(neighbor)
        return neighbors

    def update_direction(self, board):
        player_position = (board.player.gridx, board.player.gridy)
        ghost_position = (self.gridx, self.gridy)
        self.state = 0 #Move this later 
        if self.state == 0: #Chase
            #   V check if we're at an intersection                       V Check if we already decided on a direction on this tile
            if len(self.get_neighbors(ghost_position, board)) > 2 and not self.made_decision:
                previous_tile = (ghost_position[0]-self.current_direction[0], ghost_position[1]-self.current_direction[1])
                d = -math.inf
                tile = None
                for neighbor in self.get_neighbors(ghost_position, board):
                    if neighbor == previous_tile:
                        #Ghosts won't go backwards
                        continue
                    if math.dist(neighbor, player_position) > d:
                        d = math.dist(neighbor, player_position)
                        tile = neighbor
                assert tile is not None
                
                self.current_direction = [ ghost_position[0]-neighbor[0], ghost_position[1]-neighbor[1] ]
                self.made_decision = True
            else:
                if board.boardGrid[ghost_position[0]+self.current_direction[0]][ghost_position[1]+self.current_direction[1]] in self.spacesAllowed:
                    #We're moving in a straight line, we can reset our decision making
                    self.made_decision = False
                elif not self.made_decision:
                    previous_tile = (ghost_position[0]-self.current_direction[0], ghost_position[1]-self.current_direction[1])
                    for neighbor in self.get_neighbors(ghost_position, board):
                        if neighbor != previous_tile:
                            self.current_direction = [ ghost_position[0]-neighbor[0], ghost_position[1]-neighbor[1] ]
                    self.made_decision = True
        
        elif self.state == 1: #Scatter
            pass
        else: #Frightened
            pass

        super().update_position(board)

   
