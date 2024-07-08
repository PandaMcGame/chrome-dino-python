from pygame.surface import Surface


class Ground:
    def __init__(self, screen: Surface, height: float, width: float, gameSpeed: float, groundImg: Surface) -> None:
        self.screen = screen
        self.y = height - 335
        self.height = 144
        self.width = width
        self.xOffset = 0
        self.gameSpeed = gameSpeed
        self.ground_img = groundImg

    def move(self) -> None:
        self.xOffset -= self.gameSpeed

        if self.xOffset <= -self.width:
            self.xOffset += self.width

    def update(self) -> None:
        self.move()

    def show(self) -> None:
        for i in range(int(self.width / self.width) + 2):
            x = i * self.width + self.xOffset

            self.screen.blit(self.ground_img, (x, self.y, self.width, self.height))


if __name__ == '__main__':
    import pygame

    # Initialize Pygame and create a screen object
    pygame.init()
    _width, _height = 1920, 1000
    _screen = pygame.display.set_mode((_width, _height))

    # Load the ground image
    _ground_img = pygame.image.load('../assets/ground.png')

    # Create a Ground object
    _game_speed = 5
    ground = Ground(_screen, _height, _width, _game_speed, _ground_img)

    WHITE = (255, 255, 255)

    # Main game loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        ground.update()

        _screen.fill(WHITE)
        ground.show()

        pygame.display.flip()

    pygame.quit()

