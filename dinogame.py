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

class DinoPlayer(pygame.sprite.Sprite):
    def __init__(self) -> None:
        super().__init__()

        self.rect = pygame.Rect(50, 350, 20, 50)
        self.is_jumped = False

        self.jump_time = 10
        self.jump_time_remain = self.jump_time
        self.jump_speed = 10

    def jump(self, ground: pygame.Rect):
        if self.rect.colliderect(ground):
            self.is_jumped = True
            self.jump_time_remain = self.jump_time

    def sit(self):
        if not self.is_jumped:
            self.rect.height = 25
            self.rect.y = 375

    def stand(self, ground: pygame.Rect):
        if not self.is_jumped:
            self.rect.height = 50
            if self.rect.colliderect(ground):
                self.rect.y = 350

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
            if keys[pygame.K_DOWN]:
                self.player.sit()
            else:
                self.player.stand(self.ground)

            self.take_action()
            self.render()

def main():
    game = DinoGame()
    game.play_manual()

if __name__ == "__main__":
    main()
