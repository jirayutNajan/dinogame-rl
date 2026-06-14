import pygame

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

class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, color, speed) -> None:
        super().__init__()

        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.speed = speed

    def draw(self, screen: pygame.Surface):
        pygame.draw.rect(screen, self.color, self.rect)

class Bird(Obstacle):
    def __init__(self, x, y) -> None:
        self.width = 20
        self.height = 20
        self.speed = 5
        self.color = BROWN

        super().__init__(x, y, self.width, self.height, self.color, self.speed)

class Cactus(Obstacle):
    def __init__(self, x, y) -> None:
        self.width = 20
        self.height = 20
        self.speed = 5
        self.color = GREEN

        super().__init__(x, y, self.width, self.height, self.color, self.speed)

class DinoPlayer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.width = 30
        self.height = 90
        self.x = 50
        self.y = 310

        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.is_jumped = False

        self.jump_time = 10
        self.jump_time_remain = self.jump_time
        self.jump_speed = 10

        self.spawn_obstacle_rate = None

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
        pygame.draw.rect(screen, GREEN, self.rect)

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

        self.game_over = False
        self.score = 0
        return self._get_observation()

    def _get_observation(self):
        pass

    def take_action(self, action:int|None=None):
        # action is jump or sit for player, type of int
        self.update_logic()

    def update_logic(self):
        # gravity
        if not self.player.rect.colliderect(self.ground) and not self.player.is_jumped:
            self.player.rect.y += self.gravity
        self.player.update()

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
        # render ground
        pygame.draw.rect(self.screen, BROWN, self.ground)

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
            self.render()

def main():
    game = DinoGame()
    game.play_manual()

if __name__ == "__main__":
    main()
