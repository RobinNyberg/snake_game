import pygame
import random
import json
import os
from enum import Enum

# Initialize Pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
GRID_SIZE = 20
GRID_WIDTH = WINDOW_WIDTH // GRID_SIZE
GRID_HEIGHT = WINDOW_HEIGHT // GRID_SIZE

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game states
class GameState(Enum):
    MENU = 1
    PLAYING = 2
    GAME_OVER = 3

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.high_score = self.load_high_score()
        self.reset_game()

    def reset_game(self):
        self.snake = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = (1, 0)
        self.food = self.generate_food()
        self.score = 0
        self.game_state = GameState.MENU
        self.speed = 10

    def generate_food(self):
        while True:
            food = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
            if food not in self.snake:
                return food

    def load_high_score(self):
        try:
            with open('high_score.json', 'r') as f:
                return json.load(f)['high_score']
        except:
            return 0

    def save_high_score(self):
        with open('high_score.json', 'w') as f:
            json.dump({'high_score': self.high_score}, f)

    def draw_menu(self):
        self.screen.fill(BLACK)
        title = self.font.render("Snake Game", True, WHITE)
        start = self.font.render("Press SPACE to Start", True, WHITE)
        high_score_text = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        
        self.screen.blit(title, (WINDOW_WIDTH // 2 - title.get_width() // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(start, (WINDOW_WIDTH // 2 - start.get_width() // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(high_score_text, (WINDOW_WIDTH // 2 - high_score_text.get_width() // 2, WINDOW_HEIGHT * 2 // 3))

    def draw_game_over(self):
        self.screen.fill(BLACK)
        game_over = self.font.render("Game Over!", True, WHITE)
        score = self.font.render(f"Score: {self.score}", True, WHITE)
        high_score = self.font.render(f"High Score: {self.high_score}", True, WHITE)
        restart = self.font.render("Press SPACE to Restart", True, WHITE)
        
        self.screen.blit(game_over, (WINDOW_WIDTH // 2 - game_over.get_width() // 2, WINDOW_HEIGHT // 3))
        self.screen.blit(score, (WINDOW_WIDTH // 2 - score.get_width() // 2, WINDOW_HEIGHT // 2))
        self.screen.blit(high_score, (WINDOW_WIDTH // 2 - high_score.get_width() // 2, WINDOW_HEIGHT * 2 // 3))
        self.screen.blit(restart, (WINDOW_WIDTH // 2 - restart.get_width() // 2, WINDOW_HEIGHT * 3 // 4))

    def draw_game(self):
        self.screen.fill(BLACK)
        
        # Draw snake
        for segment in self.snake:
            pygame.draw.rect(self.screen, GREEN, 
                           (segment[0] * GRID_SIZE, segment[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))
        
        # Draw food
        pygame.draw.rect(self.screen, RED,
                        (self.food[0] * GRID_SIZE, self.food[1] * GRID_SIZE, GRID_SIZE - 2, GRID_SIZE - 2))
        
        # Draw score
        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))

    def update(self):
        if self.game_state == GameState.PLAYING:
            # Move snake
            new_head = (self.snake[0][0] + self.direction[0], self.snake[0][1] + self.direction[1])
            
            # Check for collisions with walls or self
            if (new_head[0] < 0 or new_head[0] >= GRID_WIDTH or
                new_head[1] < 0 or new_head[1] >= GRID_HEIGHT or
                new_head in self.snake):
                self.game_state = GameState.GAME_OVER
                if self.score > self.high_score:
                    self.high_score = self.score
                    self.save_high_score()
                return
            
            self.snake.insert(0, new_head)
            
            # Check for food collision
            if new_head == self.food:
                self.score += 1
                self.food = self.generate_food()
                self.speed = min(20, 10 + self.score // 5)  # Increase speed with score
            else:
                self.snake.pop()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.game_state in [GameState.MENU, GameState.GAME_OVER]:
                            self.reset_game()
                            self.game_state = GameState.PLAYING
                    elif self.game_state == GameState.PLAYING:
                        if event.key == pygame.K_UP and self.direction != (0, 1):
                            self.direction = (0, -1)
                        elif event.key == pygame.K_DOWN and self.direction != (0, -1):
                            self.direction = (0, 1)
                        elif event.key == pygame.K_LEFT and self.direction != (1, 0):
                            self.direction = (-1, 0)
                        elif event.key == pygame.K_RIGHT and self.direction != (-1, 0):
                            self.direction = (1, 0)

            self.update()

            if self.game_state == GameState.MENU:
                self.draw_menu()
            elif self.game_state == GameState.PLAYING:
                self.draw_game()
            elif self.game_state == GameState.GAME_OVER:
                self.draw_game_over()

            pygame.display.flip()
            self.clock.tick(self.speed)

        pygame.quit()

if __name__ == "__main__":
    game = SnakeGame()
    game.run() 