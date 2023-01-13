import numpy as np
import pygame

class SnakeGame():
    def __init__(self, board_size=(10,10)):
        self.board_size = board_size
        self.board = np.zeros(self.board_size)
        self.snake_position = [np.array([int(board_size[0]/2),int(board_size[1]/2)])]
        self.food_position = [np.random.randint(0, self.board_size[0]), np.random.randint(0, self.board_size[1])]
        self.direction = "right"
        self.game_over = False
        self.score = 0
    
    def initialize_game(self):
        """Initialize the game board and snake position"""
        self.board = np.zeros(self.board_size)
        self.snake_position = [np.array([int(self.board_size[0]/2),int(self.board_size[1]/2)])]
        self.food_position = [np.random.randint(0, self.board_size[0]), np.random.randint(0, self.board_size[1])]
        self.direction = "right"
        self.game_over = False
        self.score = 0
        
    def move_snake(self):
        """Move the snake in the current direction"""
        # Get the current snake position
        current_position = self.snake_position[0]
        ate_fruit = False
        # Update the snake position based on the current direction
        if self.direction == "right":
            new_position = current_position + np.array([0, 1])
        elif self.direction == "left":
            new_position = current_position + np.array([0, -1])
        elif self.direction == "up":
            new_position = current_position + np.array([-1, 0])
        elif self.direction == "down":
            new_position = current_position + np.array([1, 0])
        # Check if the new position is out of bounds or if the snake has collided with itself
        if (new_position[0] < 0 or new_position[0] >= self.board_size[0] or
            new_position[1] < 0 or new_position[1] >= self.board_size[1] or 
            tuple(new_position) in [tuple(position) for position in self.snake_position]):
            self.game_over = True
            return ate_fruit
        # Update the snake position and check if it has found food
        self.snake_position.insert(0, new_position)
        if tuple(new_position) == tuple(self.food_position):
            self.food_position = [np.random.randint(0, self.board_size[0]), np.random.randint(0, self.board_size[1])]
            ate_fruit = True
        else:
            self.snake_position.pop()
        return ate_fruit
        
    def render(self):
        """Render the current state of the game"""
        self.board = np.zeros(self.board_size)
        for pos in self.snake_position:
            self.board[pos[0]][pos[1]] = 1
        self.board[self.food_position[0]][self.food_position[1]] = 2
        print(self.board)
        
        # Create the window
        screen = pygame.display.set_mode((self.board_size[1]*10, self.board_size[0]*10))
        # Fill the background with white
        screen.fill((255, 255, 255))
        # Draw the snake and food on the screen
        for pos in self.snake_position:
            pygame.draw.rect(screen, (0, 0, 0), (pos[1]*10, pos[0]*10, 10, 10))
        pygame.draw.rect(screen, (255, 0, 0), (self.food_position[1]*10, self.food_position[0]*10, 10, 10))
        # Update the display
        pygame.display.flip()
        
    def handle_game_over(self):
        """Handle the game over condition"""
        print("Game over! Your score is: ", self.score)
        self.initialize_game()
        
    def handle_inputs(self):
        """Handle user inputs to control snake movement"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != "right":
                    self.direction = "left"
                elif event.key == pygame.K_RIGHT and self.direction != "left":
                    self.direction = "right"
                elif event.key == pygame.K_UP and self.direction != "down":
                    self.direction = "up"
                elif event.key == pygame.K_DOWN and self.direction != "up":
                    self.direction = "down"
    
    def run(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()
        self.initialize_game()
        while not self.game_over:
            self.handle_inputs()
            ate_fruit = self.move_snake()
            if ate_fruit:
                self.score += 1
            self.render()
            clock.tick(10)
            pygame.display.update()
        self.handle_game_over()
        pygame.quit()
        
if __name__ == "__main__":
    game = SnakeGame()
    game.run()       
