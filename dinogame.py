import pygame
import random

# ============ CONSTANT ============
WIDTH = 700
HEIGHT = 500
FPS = 30

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BROWN = (94, 72, 43)
GRAY = (128, 128, 128)

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color) -> None:
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)

    def update(self, speed):
        self.rect.x -= speed
        if self.rect.x < -10:
            self.kill()

class Bird(Obstacle):
    def __init__(self, x, y) -> None:
        self.width = random.randint(20, 30)
        self.height = self.width
        self.color = BROWN

        super().__init__(x, y, self.width, self.height, self.color)

class Cactus(Obstacle):
    def __init__(self, x) -> None:
        self.width = random.randint(20, 25)
        self.height = random.randint(20, 55)
        self.color = GREEN

        super().__init__(x, 400-self.height, self.width, self.height, self.color)

class DinoPlayer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.width = 30
        self.height = 90
        self.x = 50
        self.y = 310

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_jumped = False

        self.jump_time = 13
        self.jump_time_remain = self.jump_time
        self.jump_speed = 10

    def jump(self, ground: pygame.Rect):
        if self.rect.colliderect(ground):
            self.is_jumped = True
            self.jump_time_remain = self.jump_time

    def sit(self, ground: pygame.Rect):
        if not self.is_jumped and self.rect.colliderect(ground):
            self.rect.height = int(self.height/2)
            self.rect.y = ground.y - int(self.height/2)

    def stand(self, ground: pygame.Rect):
        if not self.is_jumped:
            self.rect.height = self.height
            if self.rect.colliderect(ground):
                self.rect.y = self.y

    def update(self):
        if self.is_jumped:
            if self.jump_time_remain >= 0:
                self.jump_time_remain -= 1
                self.rect.y -= self.jump_speed
            else:
                self.is_jumped = False

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, GRAY, self.rect)

class DinoGame:
    def __init__(self) -> None:
        self.width = WIDTH
        self.height = HEIGHT

        # PYGAME CONFIG
        # only initialized when need to render
        self.screen = None
        self.font = None
        self.clock = None

        # GAME LOGIC
        self.gravity = 10

        # reset at start
        self.reset()

    def reset(self):
        self.player = DinoPlayer()
        self.ground = pygame.Rect(0, 400, WIDTH, 100)

        self.obtacles = pygame.sprite.Group()
        self.spawn_obstacle_rate = 5000
        self.obtacles_speed = 3

        self.game_over = False
        self.score = 0

        self.last_spawn_time = pygame.time.get_ticks()

        return self._get_observation()

    def spawn_obstacle(self):
        # pygame.time.get_ticks() is game time of the game from the game start 1000 ticks mean 1 second
        current_time = pygame.time.get_ticks()
        if current_time - self.last_spawn_time > self.spawn_obstacle_rate:
            new_obstacle = None
            if random.random() > 0.5:
                new_obstacle = Bird(self.width, 310)
            else:
                new_obstacle = Cactus(self.width)
            if self.obtacles_speed < 20:
                self.obtacles_speed += 0.2

            self.last_spawn_time = current_time
            if(self.spawn_obstacle_rate > 1400):
                self.spawn_obstacle_rate -= 2
            self.obtacles.add(new_obstacle)

    def _get_observation(self):
        pass

    def take_action(self, action:int|None=None):
        # action is jump or sit for player, type of int
        self.update_logic()
        return self._get_observation()

    def update_logic(self):
        if not self.game_over:
            # gravity
            if not self.player.rect.colliderect(self.ground) and not self.player.is_jumped:
                self.player.rect.y += self.gravity

            # update entity
            self.player.update()
            self.obtacles.update(self.obtacles_speed)
            self.score += 0.5

            self.spawn_obstacle()

            for obstacle in self.obtacles:
                if self.player.rect.colliderect(obstacle):
                    self.game_over = True
                    break

    def draw_game_over(self, screen: pygame.Surface):
        font_large = pygame.font.SysFont("Arial", 60, bold=True)
        font_small = pygame.font.SysFont("Arial", 30)

        gameover_surface = font_large.render("GAME OVER", True, RED)       # สีแดง
        retry_surface = font_small.render("Press SPACE to Play Again", True, RED) # สีขาว

        gameover_rect = gameover_surface.get_rect()
        retry_rect = retry_surface.get_rect()

        gameover_rect.center = (self.width // 2, (self.height // 2) - 40)

        retry_rect.center = (self.width // 2, (self.height // 2) + 40)

        screen.blit(gameover_surface, gameover_rect)
        screen.blit(retry_surface, retry_rect)

    def draw_score(self, screen: pygame.Surface):
        font_score = pygame.font.SysFont("Arial", 30, bold=True)

        score_surface = font_score.render(f"Score: {int(self.score)}", True, BLACK)

        score_rect = score_surface.get_rect()
        score_rect.topright = (self.width - 20, 20)

        screen.blit(score_surface, score_rect)

    def render(self):
        if self.screen is None:
            pygame.init()
            self.screen = pygame.display.set_mode((self.width, self.height))
            pygame.display.set_caption("DinoGame")
            self.clock = pygame.time.Clock()
            self.font = pygame.font

        # render screen
        self.screen.fill(WHITE)
        # render player
        self.player.draw(self.screen)
        # render obstacle
        for obstacle in self.obtacles:
            obstacle.draw(self.screen)
        # render ground
        pygame.draw.rect(self.screen, BROWN, self.ground)

        # ui
        self.draw_score(self.screen)

        if self.game_over:
            self.draw_game_over(self.screen)

        # update screen
        pygame.display.flip()

        if(self.clock):
            self.clock.tick(FPS)

    def play_manual(self):
        running = True

        # initialize video system
        if self.screen is None:
            self.render()

        # logic ตรงนี้ต้องเอาไปใส่ใน rl ด้วย อย่าลืม
        while running:
            if not self.game_over:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        # press
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_UP:
                            self.player.jump(self.ground)

                # press and hold
                keys = pygame.key.get_pressed()
                # TODO: move this logic if else to update logic
                if keys[pygame.K_DOWN]:
                    self.player.sit(self.ground)
                else:
                    self.player.stand(self.ground)

                self.take_action()
            else:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.reset()

            self.render()

def main():
    game = DinoGame()
    game.play_manual()

if __name__ == "__main__":
    main()
