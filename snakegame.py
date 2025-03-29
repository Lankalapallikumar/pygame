import pygame, random


SCREEN_WIDTH, SCREEN_HEIGHT, SNAKE_SIZE, SPEED = 800, 600, 20, 15
WHITE, GREEN, RED, BLUE, BLACK = (255, 255, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (0, 0, 0)

pygame.init()
clock = pygame.time.Clock()

class SnakeGame:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Snake Game")
        self.snake_pos = [100, 50]
        self.snake_body = [[100, 50], [90, 50], [80, 50]]
        self.food_pos = self.generate_food()
        self.direction, self.change_to = 'RIGHT', 'RIGHT'
        self.score = 0

  
    def generate_food(self):
        while True:
            x = random.randrange(0, SCREEN_WIDTH // SNAKE_SIZE) * SNAKE_SIZE
            y = random.randrange(0, SCREEN_HEIGHT // SNAKE_SIZE) * SNAKE_SIZE
            if [x, y] not in self.snake_body:
                return [x, y]

   
    def display_score(self):
        score_surface = pygame.font.SysFont('Arial', 24).render(f'Score: {self.score}', True, BLUE)
        self.screen.blit(score_surface, (10, 10))

  
    def move(self):
        if self.change_to == 'UP' and self.direction != 'DOWN': self.direction = 'UP'
        if self.change_to == 'DOWN' and self.direction != 'UP': self.direction = 'DOWN'
        if self.change_to == 'LEFT' and self.direction != 'RIGHT': self.direction = 'LEFT'
        if self.change_to == 'RIGHT' and self.direction != 'LEFT': self.direction = 'RIGHT'

        if self.direction == 'UP': self.snake_pos[1] -= SNAKE_SIZE
        if self.direction == 'DOWN': self.snake_pos[1] += SNAKE_SIZE
        if self.direction == 'LEFT': self.snake_pos[0] -= SNAKE_SIZE
        if self.direction == 'RIGHT': self.snake_pos[0] += SNAKE_SIZE

        self.snake_body.insert(0, list(self.snake_pos))

       
        if abs(self.snake_pos[0] - self.food_pos[0]) < SNAKE_SIZE and abs(self.snake_pos[1] - self.food_pos[1]) < SNAKE_SIZE:
            self.score += 10
            self.food_pos = self.generate_food()
        else:
            self.snake_body.pop()

    
    def collision(self):
        if (0 <= self.snake_pos[0] < SCREEN_WIDTH and 
            0 <= self.snake_pos[1] < SCREEN_HEIGHT):
            for block in self.snake_body[1:]:
                if self.snake_pos == block:
                    return True
            return False
        return True

    
    def render(self):
        self.screen.fill(BLACK)
        for pos in self.snake_body:
            pygame.draw.rect(self.screen, GREEN, pygame.Rect(pos[0], pos[1], SNAKE_SIZE, SNAKE_SIZE))
        pygame.draw.rect(self.screen, RED, pygame.Rect(self.food_pos[0], self.food_pos[1], SNAKE_SIZE, SNAKE_SIZE))
        self.display_score()

    
    def start_screen(self):
        font = pygame.font.SysFont('Arial', 36)
        self.screen.fill(BLACK)
        text = font.render("Press SPACE to Start", True, WHITE)
        self.screen.blit(text, (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 20))
        pygame.display.flip()

        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    waiting = False

    
    def run(self):
        self.start_screen()

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP: self.change_to = 'UP'
                    if event.key == pygame.K_DOWN: self.change_to = 'DOWN'
                    if event.key == pygame.K_LEFT: self.change_to = 'LEFT'
                    if event.key == pygame.K_RIGHT: self.change_to = 'RIGHT'

            self.move()

            if self.collision():
                running = False

            self.render()
            
            pygame.display.update()
            clock.tick(SPEED)

        pygame.quit()
        print("Game Over. Final Score:", self.score)

if __name__ == "__main__":
    game = SnakeGame()
    game.run()
