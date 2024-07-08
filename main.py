import pygame
from pygame.surface import Surface
from random import randint

from modules import Player, Ground, Cactus


class DinoGame:
    def __init__(self) -> None:
        # self.canvas = None
        # self.canvasCtx = None
        # self.tRex = None
        # self.distanceMeter = None
        # self.distanceRan = 0
        # self.highestScore = 0
        # self.time = 0
        # self.runningTime = 0
        # self.msPerFrame = 1000 / FPS
        # self.currentSpeed = self.config.SPEED
        # self.obstacles = []
        # self.started = False
        # self.activated = False
        # self.crashed = False
        # self.paused = False
        # self.resizeTimerId_ = None
        # self.playCount = 0
        #
        # # Sound FX
        # self.audioBuffer = None
        # self.soundFx = {}
        # # Global web audio context for playing sounds
        # self.audioContext = None
        # # Images
        # self.images = {}
        # self.imagesLoaded = 0
        # self.loadImages()

        self.debug = False
        self.running = True

        pygame.init()

        # Set the window title
        pygame.display.set_caption('Chrome Dino')

        # Load the icon image
        icon = pygame.image.load('assets/favicon.png')
        pygame.display.set_icon(icon)

        self.width, self.height = 1920, 1000
        self.FPS = 60
        self.gameSpeed = 20

        self.screen = pygame.display.set_mode((self.width, self.height))
        self.clock = pygame.time.Clock()
        
        # Declare Images
        self.all_cacti_imgs: list = []
        self.ground_img = None
        self.dinoRun1Img = None
        self.dinoRun2Img = None
        self.dinoDuck1Img = None
        self.dinoDuck2Img = None

        self.cacti = []  # List to store multiple cacti instances
        self.last_cactus_x = self.width  # Start position for the first cactus
        self.cactus_spawn_timer = 0
        self.cactus_spawn_interval = self.FPS  # Adjust as needed (in frames)
        self.min_distance_between_cacti = 30  # Minimum distance between consecutive cacti
            
    def run(self) -> None:
        self.load_images()

        player = Player(self.width, self.height)
        ground = Ground(self.screen, self.height, self.width, 5, self.ground_img)

        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE or event.key == pygame.K_UP:
                        player.jump(isBigJump=True)
                    if event.key == pygame.K_DOWN:
                        player.duck()
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_DOWN:
                        player.stop_ducking()

            ground.update()
            player.update(self.height)

            self.screen.fill((255, 255, 255))
            ground.show()
            player.show(self.dinoRun1Img, self.dinoRun2Img, self.dinoDuck1Img, self.dinoDuck2Img, self.draw_image)

            # Update and show each cactus
            for cactus in self.cacti:
                cactus.update(self.gameSpeed)
                cactus.show(self.screen, debug=self.debug)

            # Increment cactus spawn timer
            self.cactus_spawn_timer += 1

            # Generate a new cactus if the timer reaches the interval
            if self.cactus_spawn_timer >= self.cactus_spawn_interval:
                new_cactus = Cactus.init_cactus(self.width, self.height, self.all_cacti_imgs, self.last_cactus_x)
                self.cacti.append(new_cactus)
                _last_cactus_x = new_cactus.x + self.min_distance_between_cacti + randint(50, 150)  # Randomize the spacing
                self.cactus_spawn_timer = 0  # Reset the spawn timer

            # Check for collisions and passing
            for cactus in self.cacti:
                if cactus.collided_with_player(player, isBird=False):  # Assuming cactus is not a bird
                    print("Collision detected!")
                    self.running = False  # End the game on collision

                if cactus.player_passed(player):
                    print("Player passed a cactus!")

            # Remove cacti that are off-screen to save memory
            self.cacti = [cactus for cactus in self.cacti if not cactus.off_screen()]

            pygame.display.flip()
            self.clock.tick(self.FPS)

        pygame.quit()

    def load_images(self) -> None:
        self.ground_img = pygame.image.load('assets/ground.png')
        self.dinoRun1Img = pygame.image.load('assets/dinoRun1.png')
        self.dinoRun2Img = pygame.image.load('assets/dinoRun2.png')
        self.dinoDuck1Img = pygame.image.load('assets/dinoDuck1.png')
        self.dinoDuck2Img = pygame.image.load('assets/dinoDuck2.png')

        self.all_cacti_imgs = [
            pygame.image.load('assets/cactusLargeDouble.png'),
            pygame.image.load('assets/cactusLargeSingle.png'),
            pygame.image.load('assets/cactusLargeTriple.png'),
            pygame.image.load('assets/cactusSmallDouble.png'),
            pygame.image.load('assets/cactusSmallSingle.png'),
            pygame.image.load('assets/cactusSmallTriple.png'),
        ]
        
    def draw_image(self, image: Surface, x: float, y: float, width: float, height: float) -> None:
        image = pygame.transform.scale(image, (width, height))
        self.screen.blit(image, (x, y))

        # Draw bounding box
        if self.debug:
            pygame.draw.rect(self.screen, (255, 0, 0), (x, y, width, height), 2)


if __name__ == '__main__':
    dinoGame = DinoGame()
    dinoGame.run()
