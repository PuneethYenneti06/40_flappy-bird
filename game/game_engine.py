import pygame
from .bird import Bird
from .pipe import Pipe

# Game Engine

WHITE = (255, 255, 255)
GREEN = (0, 150, 0)

DIFFICULTIES = {
    "Easy": {"pipe_speed": 3, "gap": 200},
    "Medium": {"pipe_speed": 4, "gap": 150},
    "Hard": {"pipe_speed": 6, "gap": 120},
}

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height

        self.bird = Bird(width // 4, height // 2)
        self.pipe_speed = 4
        self.pipe_interval = 90  # frames between pipe spawns
        self._spawn_timer = 0
        self.pipes = [Pipe(width + 100, height, speed=self.pipe_speed)]

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_title_font = pygame.font.SysFont("Arial", 60)
        self.game_over_score_font = pygame.font.SysFont("Arial", 40)
        self.game_over_hint_font = pygame.font.SysFont("Arial", 25)
        self.game_over = False
        self.waiting_for_input = True

    def handle_event(self, event):
        # Flap is edge-triggered (KEYDOWN / MOUSEBUTTONDOWN), not held.
        if self.game_over:
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                self.waiting_for_input = False
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()

    def handle_input(self):
        # Reserved for continuously-held-key input; flapping is handled
        # in handle_event instead, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= self.height:
            self.game_over = True
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(Pipe(self.width, self.height, speed=self.pipe_speed))

        for pipe in self.pipes:
            pipe.move()

            bird_rect = self.bird.rect()
            if bird_rect.colliderect(pipe.top_rect()) or \
               bird_rect.colliderect(pipe.bottom_rect()):
                self.game_over = True

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title = self.game_over_title_font.render("GAME OVER", True, WHITE)
            score = self.game_over_score_font.render(
                f"Final Score: {self.score}", True, WHITE
            )
            hint = self.game_over_hint_font.render(
                "Press any key or click to continue", True, WHITE
            )

            screen.blit(
                title,
                title.get_rect(center=(self.width // 2, self.height // 2 - 80))
            )
            screen.blit(
                score,
                score.get_rect(center=(self.width // 2, self.height // 2))
            )
            screen.blit(
                hint,
                hint.get_rect(center=(self.width // 2, self.height // 2 + 60))
            )