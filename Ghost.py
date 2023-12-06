# Ghost class
import pygame
import heapq
import Constants

class Ghost:

    def __init__(self, x, y):
        self.color = (255,0,0)
        self.x = x
        self.y = y
        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE
        self.desired_direction = [0, 0]
        self.current_direction = [0, 0]

    def fully_inside_square(self, gridx, gridy):
        tile_left = gridx*Constants.TILESIZE
        tile_right = tile_left + Constants.TILESIZE
        tile_top = gridy*Constants.TILESIZE
        tile_bottom = tile_top + Constants.TILESIZE
        return (self.x > tile_left-2) and ((self.x + Constants.TILESIZE) < tile_right+2) and (self.y > tile_top-2) and ((self.y + Constants.TILESIZE) < tile_bottom+2)

    def heuristic(self, a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def a_star(self, start, goal, board):
        open_set = []
        heapq.heappush(open_set, (0, start))
        came_from = {}
        cost_so_far = {start: 0}

        while open_set:
            current_cost, current_node = heapq.heappop(open_set)

            if current_node == goal:
                path = []
                while current_node in came_from:
                    path.append(current_node)
                    current_node = came_from[current_node]
                return path[::-1]

            for next_node in self.get_neighbors(current_node, board):
                new_cost = cost_so_far[current_node] + 1
                if next_node not in cost_so_far or new_cost < cost_so_far[next_node]:
                    cost_so_far[next_node] = new_cost
                    priority = new_cost + self.heuristic(goal, next_node)
                    heapq.heappush(open_set, (priority, next_node))
                    came_from[next_node] = current_node

        return None

    def get_neighbors(self, node, board):
        neighbors = []
        for direction in [[0, 1], [0, -1], [1, 0], [-1, 0]]:
            neighbor = (node[0] + direction[0], node[1] + direction[1])
            if (
                0 <= neighbor[0] < len(board.boardGrid)
                and 0 <= neighbor[1] < len(board.boardGrid[0])
                and board.boardGrid[neighbor[0]][neighbor[1]] not in (1,5,6,7,8)
            ):
                neighbors.append(neighbor)
        return neighbors

    def update(self, board):
        player_position = (board.player.gridx, board.player.gridy)
        ghost_position = (self.gridx, self.gridy)
        path = self.a_star(ghost_position, player_position, board)

        if path and len(path) > 1:
            next_step = path[1]
            self.desired_direction = [next_step[0] - ghost_position[0], next_step[1] - ghost_position[1]]
        else:
            self.desired_direction = [0, 0]



        self.gridx = self.x // Constants.TILESIZE
        self.gridy = self.y // Constants.TILESIZE
        print(self.desired_direction, self.current_direction, self.gridx, self.gridy, board.boardGrid[self.gridx+self.desired_direction[0]][self.gridy+self.desired_direction[1]])
        if self.fully_inside_square(self.gridx, self.gridy):
            if board.boardGrid[self.gridx+self.desired_direction[0]][self.gridy+self.desired_direction[1]] in (0, 3, 4):
                self.current_direction = self.desired_direction.copy()

        if not self.fully_inside_square(self.gridx, self.gridy):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]
            
        elif board.boardGrid[self.gridx+self.current_direction[0]][self.gridy+self.current_direction[1]] in (0, 3, 4):
            self.x += self.current_direction[0]
            self.y += self.current_direction[1]

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (
                self.x + Constants.TILESIZE - Constants.TILESIZE/2,
                self.y + Constants.TILESIZE - Constants.TILESIZE/2,
            ),
            Constants.TILESIZE/2
        )
