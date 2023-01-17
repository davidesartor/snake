import pygame
 
from utils.environment import SnakeEnv
 
class SnakeGame(SnakeEnv):
    def render(self, magnify = 20):
        """Render the current state of the game"""
        board = self.get_state()
        # Create the window
        screen = pygame.display.set_mode((self.board.board_size[1]*magnify, self.board.board_size[0]*magnify))
        # Fill the background with white
        screen.fill((255, 255, 255))
        # Draw board
        for x, row in enumerate(board):
            for y, value in enumerate(row):
                if value == 1:
                    pygame.draw.rect(screen, (0, 0, 0), (y*magnify, x*magnify, magnify, magnify))
        # Draw the snake
        for x,y in self.snake_position:
            pygame.draw.rect(screen, (0, 255, 0), (y*magnify, x*magnify, magnify, magnify))
        # Draw the food
        pygame.draw.rect(screen, (255, 0, 0), (self.food_position[1]*magnify, self.food_position[0]*magnify, magnify, magnify))
        # Update the display
        pygame.display.flip()
        
    def handle_game_over(self):
        """Handle the game over condition"""
        print("Game over! Your score is: ", self.score)
        self.reset()
        
    def get_move(self):
        """Handle user inputs to control snake movement"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_over = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    return "left"
                elif event.key == pygame.K_RIGHT:
                    return "right"
                elif event.key == pygame.K_UP:
                    return "up"
                elif event.key == pygame.K_DOWN:
                    return "down"
        return None
                    
    def run(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        clock = pygame.time.Clock()
        self.reset()
        self.score = 0
        done = False
        while not done:
            self.render()
            move = self.get_move()
            if move: 
                state, reward, done = self.step(move)
                self.score += reward
            
            clock.tick(10)
            pygame.display.update()
        self.handle_game_over()
        pygame.quit()