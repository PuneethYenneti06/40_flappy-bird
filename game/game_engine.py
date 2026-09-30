import pygame
from array import array
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

        self.pipe_interval = 90

        self.score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_over_title_font = pygame.font.SysFont("Arial", 60)
        self.game_over_score_font = pygame.font.SysFont("Arial", 40)
        self.game_over_hint_font = pygame.font.SysFont("Arial", 25)
        self.game_over = False
        self.waiting_for_input = True
        self.flap_sound = None
        self.score_sound = None
        self.death_sound = None
        self._init_sounds()

        self.reset("Medium")

    def _make_tone(self, frequency, duration, volume=0.25):
        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            return None

        sample_rate, mixer_format, channels = mixer_info

        if abs(mixer_format) != 16:
            return None

        sample_count = int(sample_rate * duration)
        samples = array("h")
        amplitude = int(32767 * volume)

        import math

        for i in range(sample_count):
            value = int(
                amplitude * math.sin(
                    2 * math.pi * frequency * i / sample_rate
                )
            )
            for _ in range(channels):
                samples.append(value)

        return pygame.mixer.Sound(buffer=samples.tobytes())

    def _init_sounds(self):
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init()

            mixer_info = pygame.mixer.get_init()
            if mixer_info is None:
                return

            sample_rate, mixer_format, channels = mixer_info

            if abs(mixer_format) != 16:
                return

            def make_sequence(notes):
                samples = array("h")
                amplitude = int(32767 * 0.25)

                import math

                for frequency, duration in notes:
                    sample_count = int(sample_rate * duration)

                    for i in range(sample_count):
                        value = int(
                            amplitude * math.sin(
                                2 * math.pi * frequency * i / sample_rate
                            )
                        )

                        for _ in range(channels):
                            samples.append(value)

                return pygame.mixer.Sound(buffer=samples.tobytes())

            self.flap_sound = make_sequence([
                (900, 0.06)
            ])

            self.score_sound = make_sequence([
                (900, 0.07),
                (1200, 0.09)
            ])

            self.death_sound = make_sequence([
                (500, 0.12),
                (250, 0.18)
            ])

        except Exception:
            self.flap_sound = None
            self.score_sound = None
            self.death_sound = None

    def _set_game_over(self):
        if self.game_over:
            return

        self.game_over = True

        if self.death_sound:
            self.death_sound.play()

    def reset(self, difficulty):
        settings = DIFFICULTIES[difficulty]

        self.difficulty = difficulty
        self.pipe_speed = settings["pipe_speed"]
        self.pipe_gap = settings["gap"]

        self.bird = Bird(self.width // 4, self.height // 2)
        self._spawn_timer = 0
        self.pipes = [
            Pipe(
                self.width + 100,
                self.height,
                speed=self.pipe_speed,
                gap=self.pipe_gap
            )
        ]

        self.score = 0
        self.game_over = False
        self.waiting_for_input = True

    def handle_event(self, event):
        # Handle replay/quit input while game is over.
        if self.game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.reset("Easy")
                elif event.key == pygame.K_2:
                    self.reset("Medium")
                elif event.key == pygame.K_3:
                    self.reset("Hard")
                elif event.key == pygame.K_ESCAPE:
                    pygame.event.post(pygame.event.Event(pygame.QUIT))
            return

        # Flap is edge-triggered (KEYDOWN / MOUSEBUTTONDOWN), not held.
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            self.bird.flap()
            if self.flap_sound:
                self.flap_sound.play()

        if event.type == pygame.MOUSEBUTTONDOWN:
            self.bird.flap()
            if self.flap_sound:
                self.flap_sound.play()

    def handle_input(self):
        # Reserved for continuously-held-key input; flapping is handled
        # in handle_event instead, so there's nothing to poll here.
        pass

    def update(self):
        if self.game_over:
            return

        self.bird.update()

        if self.bird.y - self.bird.radius <= 0 or self.bird.y + self.bird.radius >= self.height:
            self._set_game_over()
            return

        self._spawn_timer += 1
        if self._spawn_timer >= self.pipe_interval:
            self._spawn_timer = 0
            self.pipes.append(
                Pipe(
                    self.width,
                    self.height,
                    speed=self.pipe_speed,
                    gap=self.pipe_gap
                )
            )

        for pipe in self.pipes:
            pipe.move()

            bird_rect = self.bird.rect()
            if bird_rect.colliderect(pipe.top_rect()) or \
               bird_rect.colliderect(pipe.bottom_rect()):
                self._set_game_over()
                return

            if not pipe.scored and pipe.x + pipe.width < self.bird.x:
                pipe.scored = True
                self.score += 1
                if self.score_sound:
                    self.score_sound.play()

    def render(self, screen):
        for pipe in self.pipes:
            pygame.draw.rect(screen, GREEN, pipe.top_rect())
            pygame.draw.rect(screen, GREEN, pipe.bottom_rect())

        pygame.draw.circle(screen, WHITE, (int(self.bird.x), int(self.bird.y)), self.bird.radius)

        score_text = self.font.render(f"Score: {self.score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        difficulty_text = self.font.render(
            f"Difficulty: {self.difficulty}",
            True,
            WHITE
        )
        screen.blit(difficulty_text, (10, 45))

        if self.game_over:
            overlay = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 160))
            screen.blit(overlay, (0, 0))

            title = self.game_over_title_font.render("GAME OVER", True, WHITE)
            score = self.game_over_score_font.render(
                f"Final Score: {self.score}", True, WHITE
            )
            hint = self.game_over_hint_font.render(
                "1 - Easy    2 - Medium    3 - Hard    Esc - Quit",
                True,
                WHITE
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