import pygame
import random

# Initialize Pygame and set up the display window
pygame.init()
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Shooting 2D Game")

# Constants
GRAVITY = 0.5
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Load images
player_img = pygame.image.load('player.png').convert_alpha()
enemy_img = pygame.image.load('enemy.png').convert_alpha()
collectible_img = pygame.image.load('health.png').convert_alpha()

# Classes
class Tank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect()
        self.rect.center = (100, SCREEN_HEIGHT - 100)
        self.vel_x = 0
        self.vel_y = 0
        self.health = 100
        self.lives = 3

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.vel_x = -5
        elif keys[pygame.K_RIGHT]:
            self.vel_x = 5
        else:
            self.vel_x = 0

        if keys[pygame.K_UP]:
            self.vel_y = -5
        elif keys[pygame.K_DOWN]:
            self.vel_y = 5
        else:
            self.vel_y = 0

        self.rect.x += self.vel_x
        self.rect.y += self.vel_y

        # Boundaries
        if self.rect.left < 0:
            self.rect.left = 0
        elif self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

        if self.rect.top < 0:
            self.rect.top = 0
        elif self.rect.bottom > SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class EnemyTank(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100), random.randint(50, SCREEN_HEIGHT - 50))
        self.vel_x = -3

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH + 20

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 5))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.vel_x = 10

    def update(self):
        self.rect.x += self.vel_x
        if self.rect.left > SCREEN_WIDTH:
            self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = collectible_img
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(50, SCREEN_WIDTH - 50), random.randint(50, SCREEN_HEIGHT - 50))

# Create sprites
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
projectiles = pygame.sprite.Group()
collectibles = pygame.sprite.Group()

player = Tank()
all_sprites.add(player)

# Game variables
score = 0
level = 1
player_health = player.health
player_lives = player.lives

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                projectile = Projectile(player.rect.right, player.rect.centery)
                all_sprites.add(projectile)
                projectiles.add(projectile)

    # Update
    all_sprites.update()

    # Spawn enemies
    if random.randint(1, 100) < 2 * level:
        enemy_tank = EnemyTank()
        all_sprites.add(enemy_tank)
        enemies.add(enemy_tank)

    # Spawn collectibles
    if random.randint(1, 1000) < 2:
        collectible = Collectible()
        all_sprites.add(collectible)
        collectibles.add(collectible)

    # Check collisions
    hits = pygame.sprite.spritecollide(player, enemies, True)
    if hits:
        player.health -= 10
        if player.health <= 0:
            player.lives -= 1
            player.health = 100
            if player.lives <= 0:
                running = False

    hits = pygame.sprite.groupcollide(enemies, projectiles, True, True)
    for hit in hits:
        score += 10

    hits = pygame.sprite.spritecollide(player, collectibles, True)
    if hits:
        player.health += 20
        if player.health > 100:
            player.health = 100

    # Draw
    screen.fill(BLACK)
    all_sprites.draw(screen)

    # Draw UI
    font = pygame.font.Font(None, 36)
    score_text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(score_text, (10, 10))

    player_health = player.health
    player_lives = player.lives

    health_text = font.render("Health: " + str(player_health), True, WHITE)
    screen.blit(health_text, (10, 50))

    lives_text = font.render("Lives: " + str(player_lives), True, WHITE)
    screen.blit(lives_text, (10, 90))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()

#duck image is a player
#target image is enemy
#circle image is health