from typing import Callable
from pygame.surface import Surface


class Player:
    def __init__(self, width: float, height: float) -> None:
        self.x: float = width / 6
        self.y: float = height - 350
        self.width: float = 132
        self.height: float = 144

        self.isGrounded: bool = True
        self.isDucking: bool = False
        self.velocityY: float = 0
        self.gravity: float = 1
        self.maxFallSpeed: int = 30

        self.animTimer: int = 0
        self.displayRun1: bool = True
        self.displayDuck1: bool = False

        self.obstacles: list = []
        self.obstacle_spawn_timer: int = 50
        self.obstacle_index: int = 0
        self.obstacles_passed: set = set()

        self.isAlive: bool = True

    def move(self, height: float) -> None:
        self.y -= self.velocityY
        if not self.isGrounded:
            self.velocityY -= self.gravity

            if self.y > height - 350:
                self.velocityY = 0
                self.y = height - 350
                self.isGrounded = True

                if self.isDucking:
                    self.width = 177

    def jump(self, isBigJump: bool) -> None:
        if self.isDucking:
            self.stop_ducking()

        if self.isGrounded:
            self.isGrounded = False

            if isBigJump:
                self.velocityY = 22
                self.gravity = 1
            else:
                self.velocityY = 18
                self.gravity = 1.2

    def duck(self) -> None:
        if self.isDucking:
            return

        self.isDucking = True
        self.gravity = 5

        if self.isGrounded:
            self.width = 177

    def stop_ducking(self) -> None:
        self.isDucking = False
        self.width = 132

    def update(self, height: float) -> None:
        self.move(height)

        self.animTimer += 1

        if self.animTimer == 5:
            self.animTimer = 0
            self.displayRun1 = not self.displayRun1

            if self.isDucking:
                self.displayDuck1 = not self.displayDuck1

    def show(
        self,
        dinoRun1Img: Surface,
        dinoRun2Img: Surface,
        dinoDuck1Img: Surface,
        dinoDuck2Img: Surface,
        image: Callable
    ) -> None:
        if not self.isGrounded:
            image(dinoRun2Img, self.x, self.y, self.width, self.height)
            return

        if not self.isDucking:
            if self.displayRun1:
                image(dinoRun1Img, self.x, self.y, self.width, self.height)
            else:
                image(dinoRun2Img, self.x, self.y, self.width, self.height)
        else:
            if self.isGrounded:
                if self.displayDuck1:
                    image(dinoDuck1Img, self.x, self.y, self.width, self.height)
                else:
                    image(dinoDuck2Img, self.x, self.y, self.width, self.height)


if __name__ == '__main__':
    import pygame

    from ground import Ground

    # Initialize Pygame and create a screen object
    pygame.init()
    _width, _height = 1920, 1000
    FPS = 60

    # Create the screen
    screen = pygame.display.set_mode((_width, _height))
    clock = pygame.time.Clock()

    # Load images
    ground_img = pygame.image.load('../assets/ground.png')
    _dinoRun1Img = pygame.image.load('../assets/dinoRun1.png')
    _dinoRun2Img = pygame.image.load('../assets/dinoRun2.png')
    _dinoDuck1Img = pygame.image.load('../assets/dinoDuck1.png')
    _dinoDuck2Img = pygame.image.load('../assets/dinoDuck2.png')


    def draw_image(image: Surface, x: float, y: float, width: float, height: float) -> None:
        image = pygame.transform.scale(image, (width, height))
        screen.blit(image, (x, y))


    # Create a player instance
    ground = Ground(screen, _height, _width, FPS, ground_img)
    player = Player(_width, _height)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                    player.jump(isBigJump=True)
                if event.key == pygame.K_DOWN:
                    player.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    player.stop_ducking()

        # Update player
        ground.update()
        player.update(_height)

        # Clear the screen
        screen.fill((255, 255, 255))

        # Draw player
        ground.show()  # Uncomment for Ground object
        player.show(_dinoRun1Img, _dinoRun2Img, _dinoDuck1Img, _dinoDuck2Img, draw_image)

        # Update the display
        pygame.display.flip()

        # Cap the frame rate
        clock.tick(FPS)

    # Quit Pygame
    pygame.quit()
