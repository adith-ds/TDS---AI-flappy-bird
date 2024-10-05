import pygame
import random

# Initialize Pygame
pygame.init()

# Set screen dimensions dynamically
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
GROUND_HEIGHT = int(SCREEN_HEIGHT * 0.15)  # 15% of screen height
BIRD_WIDTH = int(SCREEN_WIDTH * 0.075)  # 7.5% of screen width
BIRD_HEIGHT = int(SCREEN_HEIGHT * 0.05)  # 5% of screen height
PIPE_WIDTH = int(SCREEN_WIDTH * 0.15)  # 15% of screen width
PIPE_GAP = int(SCREEN_HEIGHT * 0.25)  # 25% of screen height
BIRD_FLAP_STRENGTH = int(SCREEN_HEIGHT * 0.015)  # Reduced to 1.5% of screen height
GRAVITY = 0.5
FPS = 60

# Speed settings
INITIAL_PIPE_SPEED = 3  # Speed of pipes at the beginning
PIPE_ACCELERATION = 0.1  # Speed increase over time

# Colors
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Game classes
class Bird:
    def __init__(self):
        self.rect = pygame.Rect(50, SCREEN_HEIGHT // 2, BIRD_WIDTH, BIRD_HEIGHT)
        self.velocity = 0

    def flap(self):
        self.velocity = -BIRD_FLAP_STRENGTH

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def draw(self, screen):
        pygame.draw.rect(screen, BLUE, self.rect)

class Pipe:
    def __init__(self, x):
        # Ensure the gap does not appear in the top and bottom 20% of the screen
        min_height = int(SCREEN_HEIGHT * 0.2)
        max_height = int(SCREEN_HEIGHT * 0.8) - PIPE_GAP
        self.height = random.randint(min_height, max_height)
        self.x = x
        self.top = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)
        self.bottom = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - GROUND_HEIGHT)

    def move(self, speed):
        self.x -= speed
        self.top.x = self.x
        self.bottom.x = self.x

    def draw(self, screen):
        pygame.draw.rect(screen, GREEN, self.top)
        pygame.draw.rect(screen, GREEN, self.bottom)

def main():
    # Set up the screen with desired dimensions
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Flappy Bird Clone")
    clock = pygame.time.Clock()
    bird = Bird()
    pipes = []
    score = 0
    running = True
    game_started = False
    pipe_speed = INITIAL_PIPE_SPEED

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if not game_started:
                        game_started = True  # Start the game
                    else:
                        bird.flap()

        if game_started:
            bird.update()
            pipe_speed += PIPE_ACCELERATION * 0.01  # Gradually increase pipe speed

            if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 200:
                pipes.append(Pipe(SCREEN_WIDTH))

            for pipe in pipes:
                pipe.move(pipe_speed)
                if pipe.x + PIPE_WIDTH < 0:
                    pipes.remove(pipe)
                    score += 1

            # Check for collisions
            for pipe in pipes:
                if bird.rect.colliderect(pipe.top) or bird.rect.colliderect(pipe.bottom):
                    running = False

            # Check if the bird hits the ground or flies too high
            if bird.rect.bottom >= SCREEN_HEIGHT - GROUND_HEIGHT or bird.rect.top <= 0:
                running = False

        # Drawing
        screen.fill(WHITE)
        for pipe in pipes:
            pipe.draw(screen)
        bird.draw(screen)

        # Display score
        font = pygame.font.Font(None, 36)
        text = font.render(str(score), True, GREEN)
        screen.blit(text, (SCREEN_WIDTH // 2, 20))

        if not game_started:
            # Display "Press SPACE to Start" message
            start_text = font.render("Press SPACE to Start", True, BLUE)
            screen.blit(start_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
