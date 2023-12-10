#Shane Bailey, Nick Ford

import pygame
import Constants
import math

class Character:

    def __init__(self, x, y, color):
        self.color = color
        self.x = x
        self.y = y
        self.spacesAllowed = Constants.CHARACTER_SPACES
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

    def would_collide(self, board):
        gridx = self.x // Constants.TILESIZE
        gridy = self.y // Constants.TILESIZE
        if self.fully_inside_square(gridx, gridy):
            if board.boardGrid[gridx + self.current_direction[0]][gridy + self.current_direction[1]] not in Constants.CHARACTER_SPACES:
                return True
        return False

    def update_position(self, board):
        gridx = self.x // Constants.TILESIZE
        gridy = self.y // Constants.TILESIZE
        if self.fully_inside_square(gridx, gridy):
            if board.boardGrid[gridx + self.desired_direction[0]][gridy + self.desired_direction[1]] in self.spacesAllowed:
                self.current_direction = self.desired_direction.copy()

            elif board.boardGrid[gridx + self.current_direction[0]][gridy + self.current_direction[1]] == Constants.LEFT_PORTAL:
                self.x = (Constants.RIGHT_PORTAL_POSITION[0] - 1) * Constants.TILESIZE
                gridx = self.x // Constants.TILESIZE

            elif board.boardGrid[gridx + self.current_direction[0]][gridy + self.current_direction[1]] == Constants.RIGHT_PORTAL:
                self.x = (Constants.LEFT_PORTAL_POSITION[0] + 1) * Constants.TILESIZE
                gridx = self.x // Constants.TILESIZE

        if not self.fully_inside_square(gridx, gridy):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]

        if board.boardGrid[gridx + self.current_direction[0]][gridy + self.current_direction[1]] in Constants.CHARACTER_SPACES:
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
        super().__init__(x, y, (255, 255, 0))

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

    def __init__(self, x, y,color, timer, ghost_number):
        super().__init__(x, y, color)
        self.spacesAllowed = Constants.GHOST_SPACES
        self.state = "ghost_house"
        self.mood = "chase"
        self.ghost_number = ghost_number
        self.state_info = {"timer":timer*Constants.FRAME_RATE}# for when sending them to ghost house
        self.startx = x
        self.starty = y

    def modeChanger(self):
        self.mood = "scatter"
    
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
        mood = board.mood
        if(player_position == ghost_position) and mood == "fright" and self.state != "ghost_house":
            board.score += 200
            self.state = "ghost_house"
            self.state_info = {"timer":5*Constants.FRAME_RATE}
        #if self.state != "move":
            #print(self.state, self.state_info, self.current_direction, ghost_position)
        if self.state == "intersection":
            #pick a direction
            #print("Targetting", player_position)
            #print("Options", self.get_neighbors(ghost_position, board))
            previous_tile = (ghost_position[0]-self.current_direction[0], ghost_position[1]-self.current_direction[1])
            #print("Previous Tile", previous_tile)
            d = math.inf
            tile = None
            #decision of where to go based on state
            targetSpot = 0

            if mood == "chase":
                if(self.ghost_number == Constants.RED):
                    #Red guns straight for the player
                    targetSpot = (board.player.gridx,board.player.gridy)
                elif (self.ghost_number == Constants.PINK):
                    #Pink targets four spaces ahead of the player
                    targetSpot = (board.player.gridx + (board.player.current_direction[0]*4), board.player.gridy + (board.player.current_direction[1]*4))
                elif (self.ghost_number == Constants.BLUE):
                    """
                    https://gameinternals.com/understanding-pac-man-ghost-behavior
                    Inky actually uses both Pac-Man's 
                    position/facing as well as Blinky's (the red ghost's) position in his calculation. 
                    To locate Inky's target, we first start by selecting the position two tiles in front 
                    of Pac-Man in his current direction of travel, similar to Pinky's targeting method. 
                    """
                    positionA = targetSpot = (board.player.gridx + (board.player.current_direction[0]*2), board.player.gridy + (board.player.current_direction[1]*2))
                    """
                    From there, imagine drawing a vector from Blinky's position to this tile, and then doubling 
                    the length of the vector. The tile that this new, extended vector ends on will be 
                    Inky's actual target.
                    """
                    blinky_position = (board.ghosts[Constants.RED].gridx, board.ghosts[Constants.RED].gridy)
                    targetSpot = ((positionA[0] - blinky_position[0])*2, (positionA[1]-blinky_position[1])*2)
                    
                elif (self.ghost_number == Constants.YELLOW):
                    """
                    Whenever Clyde needs to determine his target tile, he first calculates his distance from Pac-Man.
                    If he is farther than eight tiles away, his targeting is identical to Blinky's, using Pac-Man's
                    current tile as his target. However, as soon as his distance to Pac-Man becomes less than eight tiles,
                    Clyde's target is set to the same tile as his fixed one in Scatter mode, just outside the
                    bottom-left corner of the maze.
                    """
                    if math.dist(ghost_position, player_position) > 8:
                        #blinky mode
                        targetSpot = player_position
                    else:
                        targetSpot = Constants.YELLOW_TARGET

            elif mood == "scatter":
                if(self.ghost_number == Constants.RED):
                    targetSpot = Constants.RED_TARGET
                elif(self.ghost_number == Constants.PINK):
                    targetSpot = Constants.PINK_TARGET
                elif(self.ghost_number == Constants.BLUE):
                    targetSpot = Constants.BLUE_TARGET
                elif(self.ghost_number == Constants.YELLOW):
                    targetSpot = Constants.YELLOW_TARGET
                    
            elif mood == "fright":
                targetSpot = player_position
                d = -math.inf

            for neighbor in self.get_neighbors(ghost_position, board):
                if mood == "fright":
                    #Choose the farthest tile
                    if math.dist(neighbor, targetSpot) > d:
                        d = math.dist(neighbor, targetSpot)
                        tile = neighbor
                else:
                    if neighbor == previous_tile:
                        #print("Skipping", neighbor)
                        continue
                    #Choose the closest tile chase logic for red
                    if math.dist(neighbor, targetSpot) < d:
                        d = math.dist(neighbor, targetSpot)
                        tile = neighbor

            assert tile is not None
            
            #print("moving towards", tile)
            self.current_direction = [tile[0] - ghost_position[0], tile[1] - ghost_position[1]]
            self.state = "move"
            self.state_info = {"started":ghost_position}
            
        elif self.state == "ghost_house":
            self.x = self.startx
            self.y = self.starty
            if self.state_info["timer"] <= 0:
                self.state = "intersection"
                self.state_info = {}
            else:
                self.state_info["timer"] -= 1

        elif self.state == "move":
            if self.fully_inside_square(self.gridx, self.gridy) and len(self.get_neighbors(ghost_position, board)) > 2 and ghost_position != self.state_info["started"]:
                self.state = "intersection"
                self.state_info = {}
            elif not self.would_collide(board):
                if board.boardGrid[self.gridx + self.current_direction[0]][self.gridy + self.current_direction[1]] == Constants.LEFT_PORTAL:
                    self.x = (Constants.RIGHT_PORTAL_POSITION[0] - 1) * Constants.TILESIZE
                    self.gridx = self.x // Constants.TILESIZE

                elif board.boardGrid[self.gridx + self.current_direction[0]][self.gridy + self.current_direction[1]] == Constants.RIGHT_PORTAL:
                    self.x = (Constants.LEFT_PORTAL_POSITION[0] + 1) * Constants.TILESIZE
                    self.gridx = self.x // Constants.TILESIZE
                else:
                    #print("free to move")
                    self.x += self.current_direction[0]
                    self.y += self.current_direction[1]
                    self.gridx = self.x // Constants.TILESIZE
                    self.gridy = self.y // Constants.TILESIZE
            else:
                
                previous_tile = (ghost_position[0]-self.current_direction[0], ghost_position[1]-self.current_direction[1])
                #print("need to turn but not to", previous_tile)
                for neighbor in self.get_neighbors(ghost_position, board):
                    if neighbor != previous_tile:
                        print("turning to", neighbor)
                        self.current_direction = [neighbor[0] - ghost_position[0], neighbor[1] - ghost_position[1]]
                        self.x += self.current_direction[0]
                        self.y += self.current_direction[1]
                        self.gridx = self.x // Constants.TILESIZE
                        self.gridy = self.y // Constants.TILESIZE
                        break



    def draw(self, screen, board):
        if(board.mood == "fright"):
            pygame.draw.circle(
                screen,
                (25,25,255),
                (
                    self.x + Constants.TILESIZE - Constants.TILESIZE / 2,
                    self.y + Constants.TILESIZE - Constants.TILESIZE / 2,
                ),
                Constants.TILESIZE / 2,
            )
        else:
            pygame.draw.circle(
                screen,
                self.color,
                (
                    self.x + Constants.TILESIZE - Constants.TILESIZE / 2,
                    self.y + Constants.TILESIZE - Constants.TILESIZE / 2,
                ),
                Constants.TILESIZE / 2,
            )
   
