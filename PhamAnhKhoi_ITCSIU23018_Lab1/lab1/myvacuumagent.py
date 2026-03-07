from lab1.vacuum import *

import heapq
from collections import deque

DEBUG_OPT_DENSEWORLDMAP = False

AGENT_STATE_UNKNOWN = 0
AGENT_STATE_WALL = 1
AGENT_STATE_CLEAR = 2
AGENT_STATE_DIRT = 3
AGENT_STATE_HOME = 4

AGENT_DIRECTION_NORTH = 0
AGENT_DIRECTION_EAST = 1
AGENT_DIRECTION_SOUTH = 2
AGENT_DIRECTION_WEST = 3

def direction_to_string(cdr):
    cdr %= 4
    return  "NORTH" if cdr == AGENT_DIRECTION_NORTH else\
            "EAST"  if cdr == AGENT_DIRECTION_EAST else\
            "SOUTH" if cdr == AGENT_DIRECTION_SOUTH else\
            "WEST" #if dir == AGENT_DIRECTION_WEST

"""
Internal state of a vacuum agent
"""
class MyAgentState:

    def __init__(self, width, height):

        # Initialize perceived world state
        self.world = [[AGENT_STATE_UNKNOWN for _ in range(height)] for _ in range(width)]
        self.world[1][1] = AGENT_STATE_HOME

        # Agent internal state
        self.last_action = ACTION_NOP
        self.direction = AGENT_DIRECTION_EAST
        self.pos_x = 1
        self.pos_y = 1

        # Metadata
        self.world_width = width
        self.world_height = height
        print(width, height)

    """
    Update perceived agent location
    """
    def update_position(self, bump):
        if not bump and self.last_action == ACTION_FORWARD:
            if self.direction == AGENT_DIRECTION_EAST:
                self.pos_x += 1
            elif self.direction == AGENT_DIRECTION_SOUTH:
                self.pos_y += 1
            elif self.direction == AGENT_DIRECTION_WEST:
                self.pos_x -= 1
            elif self.direction == AGENT_DIRECTION_NORTH:
                self.pos_y -= 1

    """
    Update perceived or inferred information about a part of the world
    """
    def update_world(self, x, y, info):
        self.world[x][y] = info

    """
    Dumps a map of the world as the agent knows it
    """
    def print_world_debug(self):
        for y in range(self.world_height):
            for x in range(self.world_width):
                if self.world[x][y] == AGENT_STATE_UNKNOWN:
                    print("?" if DEBUG_OPT_DENSEWORLDMAP else " ? ", end="")
                elif self.world[x][y] == AGENT_STATE_WALL:
                    print("#" if DEBUG_OPT_DENSEWORLDMAP else " # ", end="")
                elif self.world[x][y] == AGENT_STATE_CLEAR:
                    print("." if DEBUG_OPT_DENSEWORLDMAP else " . ", end="")
                elif self.world[x][y] == AGENT_STATE_DIRT:
                    print("D" if DEBUG_OPT_DENSEWORLDMAP else " D ", end="")
                elif self.world[x][y] == AGENT_STATE_HOME:
                    print("H" if DEBUG_OPT_DENSEWORLDMAP else " H ", end="")

            print() # Newline
        print() # Delimiter post-print

"""
Vacuum agent
"""
class MyVacuumAgent(Agent):

    def __init__(self, world_width, world_height, log):
        super().__init__(self.execute)
        self.initial_random_actions = 10
        self.iteration_counter = world_height * world_width * 2 # Task 2 requirements
        self.state = MyAgentState(world_width, world_height)
        self.log = log

    def move_to_random_start_position(self, bump):
        action = random()

        self.initial_random_actions -= 1
        self.state.update_position(bump)

        if action < 0.1666666:   # 1/6 chance
            self.state.direction = (self.state.direction + 3) % 4
            self.state.last_action = ACTION_TURN_LEFT
            return ACTION_TURN_LEFT
        elif action < 0.3333333: # 1/6 chance
            self.state.direction = (self.state.direction + 1) % 4
            self.state.last_action = ACTION_TURN_RIGHT
            return ACTION_TURN_RIGHT
        else:                    # 4/6 chance
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD

    def execute(self, percept):

        ###########################
        # DO NOT MODIFY THIS CODE #
        ###########################

        bump = percept.attributes["bump"]
        dirt = percept.attributes["dirt"]
        home = percept.attributes["home"]

        # Move agent to a randomly chosen initial position
        if self.initial_random_actions > 0:
            self.log("Moving to random start position ({} steps left)".format(self.initial_random_actions))
            return self.move_to_random_start_position(bump)

        # Finalize randomization by properly updating position (without subsequently changing it)
        elif self.initial_random_actions == 0:
            self.initial_random_actions -= 1
            self.state.update_position(bump)
            self.state.last_action = ACTION_SUCK
            self.log("Processing percepts after position randomization")
            return ACTION_SUCK


        ########################
        # START MODIFYING HERE #
        ########################

        # Max iterations for the agent
        if self.iteration_counter < 1:
            if self.iteration_counter == 0:
                self.iteration_counter -= 1
                self.log("Iteration counter is now 0. Halting!")
                self.log("Performance: {}".format(self.performance))
            return ACTION_NOP

        self.log("Position: ({}, {})\t\tDirection: {}".format(self.state.pos_x, self.state.pos_y,
                                                              direction_to_string(self.state.direction)))

        # Track position of agent
        self.state.update_position(bump)
        
        self.iteration_counter -= 1

        if bump:
            # Get an xy-offset pair based on where the agent is facing
            offset = [(0, -1), (1, 0), (0, 1), (-1, 0)][self.state.direction]

            # Mark the tile at the offset from the agent as a wall (since the agent bumped into it)
            self.state.update_world(self.state.pos_x + offset[0], self.state.pos_y + offset[1], AGENT_STATE_WALL)

        # Update perceived state of current tile
        if dirt:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_DIRT)
        else:
            self.state.update_world(self.state.pos_x, self.state.pos_y, AGENT_STATE_CLEAR)

        # Debug
        self.state.print_world_debug()

        # Decide action
        # if dirt:
        #     self.log("DIRT -> choosing SUCK action!")
        #     self.state.last_action = ACTION_SUCK
        #     return ACTION_SUCK
        # elif bump:
        #     self.state.last_action = ACTION_NOP
        #     return ACTION_NOP
        # else:
        #     self.state.last_action = ACTION_FORWARD
        #     return ACTION_FORWARD
        
        if dirt:
            self.log("DIRT -> SUCK it!")
            self.state.last_action = ACTION_SUCK
            return ACTION_SUCK
        
        frontier = self.find_frontier()
        
        if frontier:
            self.log("Frontier found at {}, {}".format(frontier[0], frontier[1]))
            path = self.a_star((self.state.pos_x, self.state.pos_y), frontier)
            if path:
                self.log("Following path to frontier: {}".format(path))
                action = self.follow_path(path)
                self.state.last_action = action
                return action
            else:
                self.log("No path to frontier found, choosing NOP")
                self.state.last_action = ACTION_NOP
                return ACTION_NOP
        elif not home:
            self.log("No frontier found, but not at home. Returning home.")
            path = self.a_star((self.state.pos_x, self.state.pos_y), (1, 1))
            if path:
                self.log("Following path to home: {}".format(path))
                action = self.follow_path(path)
                self.state.last_action = action
                return action
            else:
                self.log("No path to home found, choosing NOP")
                self.state.last_action = ACTION_NOP
                return ACTION_NOP
        else:
            self.log("No frontier found, but already at home. Choosing NOP.")
            self.state.last_action = ACTION_NOP
            return ACTION_NOP
            
        
        
    #############################
    # UTILS FUNCTIONS FOR AGENT #
    #############################
        
    def heuristic(self, current, target):
        """
        Manhattan distance heuristic for grid-based pathfinding
        """
        return abs(current[0] - target[0]) + abs(current[1] - target[1])
    
    def get_neighbors(self, position):
        """
        Get valid neighboring positions (up, down, left, right) that are not walls
        """
        x, y = position
        neighbors = []
        for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 0 <= nx < self.state.world_width and 0 <= ny < self.state.world_height:
                if self.state.world[nx][ny] != AGENT_STATE_WALL:
                    neighbors.append((nx, ny))
        return neighbors

    def a_star(self, start, goal):
        """
        Path finding algorithm
        """
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristic(start, goal), 0, start))
        came_from = {}
        g_score = {start: 0}
        
        while open_set:
            _, current_g, current = heapq.heappop(open_set)
            
            if current == goal:
                path = []
                while current in came_from:
                    path.append(current)
                    current = came_from[current]
                path.reverse()
                return path
            
            for neighbor in self.get_neighbors(current):
                tentative_g_score = g_score[current] + 1
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + self.heuristic(neighbor, goal)
                    heapq.heappush(open_set, (f_score, tentative_g_score, neighbor))
                    came_from[neighbor] = current
                    
        return None  # No path found
    
    """
    def find_frontier(self):
        frontiers = set()

        for x in range(self.state.world_width):
            for y in range(self.state.world_height):
                
                if self.state.world[x][y] == AGENT_STATE_UNKNOWN:
                    continue
                if self.state.world[x][y] == AGENT_STATE_WALL:
                    continue

                for dx, dy in [(0,-1),(1,0),(0,1),(-1,0)]:
                    nx, ny = x+dx, y+dy

                    if 0 <= nx < self.state.world_width and 0 <= ny < self.state.world_height:
                        if self.state.world[nx][ny] == AGENT_STATE_UNKNOWN:
                            frontiers.add((nx, ny))

        if not frontiers:
            return None

        # Return the closest frontier
        return min(
            frontiers,
            key=lambda f: self.heuristic((self.state.pos_x,self.state.pos_y),f)
        )
    """
        
    def find_frontier(self):
        """
        Find the nearest frontier cell (unknown cell adjacent to a known cell) using BFS
        """
        queue = deque([(self.state.pos_x, self.state.pos_y)])
        visited = set([(self.state.pos_x, self.state.pos_y)])

        while queue:
            x, y = queue.popleft()

            for dx, dy in [(0, -1), (1, 0), (0, 1), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if 0 <= nx < self.state.world_width and 0 <= ny < self.state.world_height:
                    if (nx, ny) not in visited:
                        visited.add((nx, ny))
                        
                        cell_state = self.state.world[nx][ny]
                        
                        if cell_state == AGENT_STATE_UNKNOWN:
                            return (nx, ny)

                        elif cell_state != AGENT_STATE_WALL:
                            queue.append((nx, ny))
                            
        return None
    
    
    def follow_path(self, path):
        """
        Follow the given path and return the next action
        """
        if not path:
            return ACTION_NOP
        
        next_cell = path[0]
        dx = next_cell[0] - self.state.pos_x
        dy = next_cell[1] - self.state.pos_y
        
        desired_direction = None
        if dx == 1:
            desired_direction = AGENT_DIRECTION_EAST
        elif dx == -1:
            desired_direction = AGENT_DIRECTION_WEST
        elif dy == 1:
            desired_direction = AGENT_DIRECTION_SOUTH
        elif dy == -1:
            desired_direction = AGENT_DIRECTION_NORTH
        
        if self.state.direction == desired_direction:
            self.state.last_action = ACTION_FORWARD
            return ACTION_FORWARD
        else:
            turn_direction = (desired_direction - self.state.direction) % 4
            if turn_direction == 1:  # Turn right
                self.state.direction = (self.state.direction + 1) % 4
                self.state.last_action = ACTION_TURN_RIGHT
                return ACTION_TURN_RIGHT
            else:  # Turn left
                self.state.direction = (self.state.direction + 3) % 4
                self.state.last_action = ACTION_TURN_LEFT
                return ACTION_TURN_LEFT