import numpy as np

class Board():
    def __init__(self, n_rooms=2, room_size=(10,10)):
        self.n_rooms = n_rooms
        self.room_size = room_size
        self.board_size = tuple(s*n_rooms+1 for s in room_size)
    
    def reset(self):
        """Initialize the game board"""
        self.state = np.zeros(self.board_size)
        
        # Draw edges 
        self.state[self.n_rooms*self.room_size[0],:] = 1
        self.state[:,self.n_rooms*self.room_size[1]] = 1
        self.state[0,:] = 1
        self.state[:,0] = 1
        
        # Draw walls
        for wall_room_idx in range(1,self.n_rooms):
            wallposition = wall_room_idx*self.room_size[0]
            self.state[wallposition,:] = 1
            # Draw doors
            for door_room_idx in range(self.n_rooms):
                doorposition = door_room_idx*self.room_size[1] + np.random.randint(1, self.room_size[1])
                self.state[wallposition,doorposition] = 0
            
            wallposition = wall_room_idx*self.room_size[1]
            self.state[:,wallposition] = 1
            # Draw doors
            for door_room_idx in range(self.n_rooms):
                doorposition = door_room_idx*self.room_size[0] + np.random.randint(1, self.room_size[0])
                self.state[doorposition,wallposition] = 0   
        
    def is_wall(self, position):
        return self.state[position] == 1
    
    def get_random_empty(self):
        position = tuple(np.random.randint(0, bound) for bound in self.board_size)
        while self.is_wall(position):
            position = tuple(np.random.randint(0, bound) for bound in self.board_size)
        return position
    
    
class SnakeEnv():
    def __init__(self, n_rooms=2, room_size=(10,10)):
        self.board = Board(n_rooms, room_size)
        self.reset()
    
    def reset(self):
        """Initialize the game board and snake position"""
        self.board.reset()
        self.spawn_snake()
        self.spawn_food()
        
    def spawn_snake(self):
        self.snake_position = [self.board.get_random_empty()]
        
    def spawn_food(self):
        self.food_position = self.board.get_random_empty()
        while self.food_position in self.snake_position: 
            self.food_position = self.board.get_random_empty()
        
    def move_snake(self, move):
        """Move the snake"""        
        # Get the current snake position
        head_x, head_y = self.snake_position[0]
        
        # Update the snake position based on the current direction
        if move == "right": head_y += 1
        elif move == "left": head_y -= 1
        elif move == "up": head_x -= 1
        elif move == "down": head_x += 1
            
        self.snake_position.insert(0, (head_x, head_y))
    
    def is_food_eaten(self):
        return self.snake_position[0] == self.food_position  
    
    def is_game_over(self):
        head_position = self.snake_position[0]
        
        # Check if the snake has collided with walls
        if self.board.is_wall(head_position):
            return True
        
        # Check if the snake has collided with itself
        if head_position in self.snake_position[1:]: 
            return True
        return False
    
    def get_state(self):
        # add base board
        board_state = self.board.state.copy()
        
        # add snake 
        board_state[self.snake_position[0]] = 2
        for x,y in self.snake_position: 
            board_state[x,y] = 3
            
        # add food
        board_state[self.food_position[0],self.food_position[1]] = 4  
        return board_state
    
    def step(self, move):
        self.move_snake(move)
        state = self.get_state()
        if self.is_food_eaten():
            reward = 1
            self.spawn_food()
        else:
            reward = 0
            self.snake_position.pop()
        done = self.is_game_over()
        return state, reward, done