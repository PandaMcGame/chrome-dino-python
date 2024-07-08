from random import randint
from pygame.surface import Surface
from .obstacle import Obstacle


class Cactus(Obstacle):
    def __init__(self, x: float, y: float, width: float, height: float, cactus_img: Surface) -> None:
        super().__init__(x, y, width, height)
        self.cactus_img = cactus_img

    @staticmethod
    def init_cactus(width: float, height: float, all_cacti_imgs: list, last_cactus_x: float) -> 'Cactus':
        random_cactus_index = randint(0, len(all_cacti_imgs) - 1)
        cactus_img = all_cacti_imgs[random_cactus_index]
        cactus_width, cactus_height = cactus_img.get_size()

        # Calculate position based on the last cactus' x position
        min_distance_between_cacti = 25  # Adjust this value as needed
        x = last_cactus_x + min_distance_between_cacti + randint(50, 150)  # Randomize the spacing
        y = height - 206 - cactus_height  # Assuming height is predefined

        return Cactus(x, y, cactus_width, cactus_height, cactus_img)

    def move(self, game_speed: float) -> None:
        self.x -= game_speed

    def update(self, game_speed: float) -> None:
        self.move(game_speed)

    def show(self, screen: Surface, debug: bool = False) -> None:
        screen.blit(self.cactus_img, (self.x, self.y))

        # Draw bounding box
        if debug:
            pygame.draw.rect(screen, (255, 0, 0), (self.x, self.y, self.width, self.height), 2)


if __name__ == '__main__':
    import pygame
    from player import Player
    from ground import Ground
    from pygame.surface import Surface

    pygame.init()
    _width, _height = 1920, 1000
    FPS = 60
    gameSpeed = 20

    _screen = pygame.display.set_mode((_width, _height))
    clock = pygame.time.Clock()

    ground_img = pygame.image.load('../assets/ground.png')
    dinoRun1Img = pygame.image.load('../assets/dinoRun1.png')
    dinoRun2Img = pygame.image.load('../assets/dinoRun2.png')
    dinoDuck1Img = pygame.image.load('../assets/dinoDuck1.png')
    dinoDuck2Img = pygame.image.load('../assets/dinoDuck2.png')

    def draw_image(image: Surface, x: float, y: float, width: float, height: float) -> None:
        image = pygame.transform.scale(image, (width, height))
        _screen.blit(image, (x, y))


    player = Player(_width, _height)
    ground = Ground(_screen, _height, _width, gameSpeed, ground_img)

    _all_cacti_imgs = [
        pygame.image.load('../assets/cactusLargeDouble.png'),
        pygame.image.load('../assets/cactusLargeSingle.png'),
        pygame.image.load('../assets/cactusLargeTriple.png'),
        pygame.image.load('../assets/cactusSmallDouble.png'),
        pygame.image.load('../assets/cactusSmallSingle.png'),
        pygame.image.load('../assets/cactusSmallTriple.png'),
    ]

    cacti = []  # List to store multiple cacti instances
    _last_cactus_x = _width  # Start position for the first cactus
    cactus_spawn_timer = 0
    cactus_spawn_interval = FPS  # Adjust as needed (in frames)
    _min_distance_between_cacti = 30  # Minimum distance between consecutive cacti

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

        # Update game objects
        ground.update()
        player.update(_height)

        # Clear the screen
        _screen.fill((255, 255, 255))

        # Draw game objects
        ground.show()
        player.show(dinoRun1Img, dinoRun2Img, dinoDuck1Img, dinoDuck2Img, draw_image)

        # Update and show each cactus
        for cactus in cacti:
            cactus.update(gameSpeed)
            cactus.show(_screen)

        # Increment cactus spawn timer
        cactus_spawn_timer += 1

        # Generate a new cactus if the timer reaches the interval
        if cactus_spawn_timer >= cactus_spawn_interval:
            new_cactus = Cactus.init_cactus(_width, _height, _all_cacti_imgs, _last_cactus_x)
            cacti.append(new_cactus)
            _last_cactus_x = new_cactus.x + _min_distance_between_cacti + randint(50, 150)  # Randomize the spacing
            cactus_spawn_timer = 0  # Reset the spawn timer

        # Remove cacti that are off-screen to save memory
        cacti = [cactus for cactus in cacti if not cactus.off_screen()]

        # Update the display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
