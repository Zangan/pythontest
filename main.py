import pygame
import random
import button
from pygame.locals import *

pygame.init()
pygame.display.set_caption("Run Forest!")

SCREEN_WIDTH = 960
SCREEN_HEIGHT = 540
FPS = 30
GAME_SPEED = 1

clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
smallfont = pygame.font.SysFont('TimesNewRoman',35) 

bg_scroll = 0

bg_imgs = []
for bg in range (2,6):
    bg_img = pygame.transform.scale(pygame.image.load(f"layer_0{bg}_1920 x 1080.png").convert_alpha(), (960,540))
    bg_imgs.append(bg_img)
bg_width = bg_imgs[0].get_width()

ground_image = pygame.image.load("layer_01_1920 x 1080.png").convert_alpha()
ground_width = ground_image.get_width()
ground_height = ground_image.get_height()

def draw_bg():
    for x in range(5):
        speed = GAME_SPEED
        for bg in bg_imgs:
            screen.blit(bg, ((x * bg_width) - bg_scroll * speed, 0))
            speed += .2

def draw_ground():
    for x in range(15):
        screen.blit(ground_image, ((x * ground_width) - bg_scroll * 2.2, SCREEN_HEIGHT - ground_height))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = player_img
        self.surf.set_colorkey((135, 206, 250), RLEACCEL)
        self.rect = self.surf.get_rect()

    # Move the sprite based on user keypresses
    def update(self, pressed_keys):
        if any((pressed_keys[K_w], pressed_keys[K_UP])):
            self.rect.move_ip(0, -5 * GAME_SPEED)
        if pressed_keys[K_s]:
            self.rect.move_ip(0, 5 * GAME_SPEED)
        if pressed_keys[K_a]:
            self.rect.move_ip(-5 * GAME_SPEED, 0)
        if pressed_keys[K_d]:
            self.rect.move_ip(5 * GAME_SPEED, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

class Enemy(pygame.sprite.Sprite):

    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = enemy_img
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5 * GAME_SPEED, 15 * GAME_SPEED)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        self.surf = cloud_img
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        # The starting position is randomly generated
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )

    # Move the cloud based on a constant speed
    # Remove the cloud when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-20 * GAME_SPEED, 0)
        if self.rect.right < 0:
            self.kill()

# Instantiation.
player_img = pygame.transform.scale(pygame.image.load("jet.png").convert_alpha(), (100,50))
enemy_img = pygame.transform.scale(pygame.image.load("missile.png").convert_alpha(), (100,50))
cloud_img = pygame.transform.scale(pygame.image.load("cloud.png").convert_alpha(), (100,50))
resume_img = pygame.image.load("resume.png").convert_alpha()
options_img = pygame.image.load("options.png").convert_alpha()
quit_img = pygame.image.load("quit.png").convert_alpha()
play_button = button.Button(SCREEN_WIDTH/2-100, SCREEN_HEIGHT/2, resume_img, .1)
options_button = button.Button(SCREEN_WIDTH/2, SCREEN_HEIGHT/2, options_img, .4)
quit_button = button.Button(SCREEN_WIDTH/2+100, SCREEN_HEIGHT/2, quit_img, .4)

player = Player()
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)
ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True
game_start = False
menu_state = "main"

while running:
    clock.tick(FPS)
    screen.fill((135, 206, 250))
    draw_bg()
    draw_ground()

    if game_start == False:
        for event in pygame.event.get():
            mouse = pygame.mouse.get_pos()
            if menu_state == "main":
                if play_button.draw(screen):
                    game_start = True
                elif options_button.draw(screen):
                    menu_state = "options"
                elif quit_button.draw(screen):
                    running = False
            elif menu_state == "options":
                pass
            # MAKE OPTION BUTTONS
            elif event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False

        pygame.display.update()

    elif game_start == True:
        pressed_keys = pygame.key.get_pressed()
        player.update(pressed_keys)
        enemies.update()
        clouds.update()
        #screen.fill((135, 206, 250))
        
        if pressed_keys[K_a] and bg_scroll > 0:
            bg_scroll -= 5
        elif pressed_keys[K_d] and bg_scroll < 3000:
            bg_scroll += 5

        for entity in all_sprites:
            screen.blit(entity.surf, entity.rect)

        for event in pygame.event.get():
            if event.type == ADDENEMY:
                # Create the new enemy and add it to sprite groups
                new_enemy = Enemy()
                enemies.add(new_enemy)
                all_sprites.add(new_enemy)
            elif event.type == ADDCLOUD:
                # Create the new cloud and add it to sprite groups
                new_cloud = Cloud()
                clouds.add(new_cloud)
                all_sprites.add(new_cloud)

        if pygame.sprite.spritecollideany(player, enemies):
            pass
            #player.kill()
            #running = False
        elif event.type == QUIT:
                running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                #running = False
                menu_state == "main"
                game_start == False

        screen.blit(player.surf, player.rect)
        pygame.display.flip()

pygame.quit()