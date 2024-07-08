class Obstacle:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def off_screen(self) -> bool:
        return self.x < -300

    def collided_with_player(self, player, isBird: bool) -> bool:
        if player.x + player.width > self.x and player.x < self.x + self.width:
            if player.isDucking:
                if self.y < player.y + player.height < self.y + self.height:
                    return True
            else:
                if isBird:
                    if (self.y < player.y + 30 < self.y + self.height) or (
                            self.y + self.height > player.y + player.height - 30 > self.y):
                        return True
                else:
                    if player.y + player.height > self.y:
                        return True
        return False

    def player_passed(self, player) -> bool:
        return player.x > self.x + self.width


if __name__ == '__main__':
    import pygame
    from player import Player
    from ground import Ground
    from cactus import Cactus
    from pygame.surface import Surface
    from random import randint

    pygame.init()
    _width, _height = 1920, 1000
    FPS = 60
    gameSpeed = 20

    screen = pygame.display.set_mode((_width, _height))
    clock = pygame.time.Clock()

    ground_img = pygame.image.load('../assets/ground.png')
    dinoRun1Img = pygame.image.load('../assets/dinoRun1.png')
    dinoRun2Img = pygame.image.load('../assets/dinoRun2.png')
    dinoDuck1Img = pygame.image.load('../assets/dinoDuck1.png')
    dinoDuck2Img = pygame.image.load('../assets/dinoDuck2.png')

    def draw_image(image: Surface, x: float, y: float, width: float, height: float) -> None:
        image = pygame.transform.scale(image, (width, height))
        screen.blit(image, (x, y))

        # Draw bounding box
        pygame.draw.rect(screen, (255, 0, 0), (x, y, width, height), 2)

    _player = Player(_width, _height)
    ground = Ground(screen, _height, _width, 5, ground_img)

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
                    _player.jump(isBigJump=True)
                if event.key == pygame.K_DOWN:
                    _player.duck()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    _player.stop_ducking()

        ground.update()
        _player.update(_height)

        screen.fill((255, 255, 255))
        ground.show()
        _player.show(dinoRun1Img, dinoRun2Img, dinoDuck1Img, dinoDuck2Img, draw_image)

        # Update and show each cactus
        for cactus in cacti:
            cactus.update(gameSpeed)
            cactus.show(screen, debug=True)

        # Increment cactus spawn timer
        cactus_spawn_timer += 1

        # Generate a new cactus if the timer reaches the interval
        if cactus_spawn_timer >= cactus_spawn_interval:
            new_cactus = Cactus.init_cactus(_width, _height, _all_cacti_imgs, _last_cactus_x)
            cacti.append(new_cactus)
            _last_cactus_x = new_cactus.x + _min_distance_between_cacti + randint(50, 150)  # Randomize the spacing
            cactus_spawn_timer = 0  # Reset the spawn timer

        # Check for collisions and passing
        for cactus in cacti:
            if cactus.collided_with_player(_player, isBird=False):  # Assuming cactus is not a bird
                print("Collision detected!")
                running = False  # End the game on collision

            if cactus.player_passed(_player):
                print("Player passed a cactus!")

        # Remove cacti that are off-screen to save memory
        cacti = [cactus for cactus in cacti if not cactus.off_screen()]

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
