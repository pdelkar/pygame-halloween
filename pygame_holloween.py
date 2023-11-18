import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

BORDER = pygame.Rect(WIDTH // 2 - 5, 0, 10, HEIGHT)

GHOST_WIDTH, GHOST_HEIGHT = 160, 130
FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

GHOST1_HIT = pygame.USEREVENT + 1
GHOST2_HIT = pygame.USEREVENT + 2

# Load images
GHOST1_IMAGE = pygame.image.load(os.path.join("hp1.png"))
GHOST1 = pygame.transform.rotate(pygame.transform.scale(GHOST1_IMAGE, (GHOST_WIDTH, GHOST_HEIGHT)), 360)
GHOST2_IMAGE = pygame.image.load(os.path.join("hp2.png"))
GHOST2 = pygame.transform.rotate(pygame.transform.scale(GHOST2_IMAGE, (GHOST_WIDTH, GHOST_HEIGHT)), 360)

SPACE = pygame.transform.scale(pygame.image.load(os.path.join("bb.jpg")), (WIDTH, HEIGHT))

# Set font type and size
HEALTH_FONT = pygame.font.SysFont("comicsans", 30)
WINNER_FONT = pygame.font.SysFont("comicsans", 50)

sound = pygame.mixer.Sound(f'sound.mp3')
sound.set_volume(0.5)

def draw_window(red, yellow, red_bullets, yellow_bullets, ghost2_health, ghost1_health):
    WIN.blit(SPACE, (0, 0))
    pygame.draw.rect(WIN, BLACK, BORDER)

    ghost2_health_text = HEALTH_FONT.render("Health: " + str(ghost2_health), 1, WHITE)
    ghost1_health_text = HEALTH_FONT.render("Health: " + str(ghost1_health), 1, WHITE)
    WIN.blit(ghost2_health_text, (WIDTH - ghost2_health_text.get_width() - 10, 10))
    WIN.blit(ghost1_health_text, (10, 10))

    WIN.blit(GHOST1, (yellow.x, yellow.y))
    WIN.blit(GHOST2, (red.x, red.y))

    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(WIN, YELLOW, bullet)

    pygame.display.update()

def yellow_handle_movement(keys_pressed, yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > 0:  # left
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x:  # right
        yellow.x += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > 0:  # up
        yellow.y -= VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT:  # down
        yellow.y += VEL

def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # left
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # right
        red.x += VEL
    if keys_pressed[pygame.K_UP] and red.y - VEL > 0:  # up
        red.y -= VEL
    if keys_pressed[pygame.K_DOWN] and red.y + VEL + red.height < HEIGHT:  # down
        red.y += VEL

def handle_bullets(yellow_bullets, red_bullets, yellow, red, ghost1_health, ghost2_health):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GHOST2_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(GHOST1_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH / 2 - draw_text.get_width() / 2, HEIGHT / 2))

    pygame.display.update()
    pygame.time.delay(5000)

def main():
    red = pygame.Rect(700, 300, GHOST_WIDTH, GHOST_HEIGHT)
    yellow = pygame.Rect(100, 300, GHOST_WIDTH, GHOST_HEIGHT)

    red_bullets = []
    yellow_bullets = []

    ghost1_health = 10
    ghost2_health = 10

    clock = pygame.time.Clock()

    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height // 2 - 2, 10, 5)
                    yellow_bullets.append(bullet)

                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 - 2, 10, 5)
                    red_bullets.append(bullet)

            if event.type == GHOST2_HIT:
                ghost2_health -= 1

            if event.type == GHOST1_HIT:
                ghost1_health -= 1

        winner_text = ""
        if ghost1_health <= 0:
            winner_text = "Yepee! Yellow Ghost Wins!"
        if ghost2_health <= 0:
            winner_text = "Haha! Red Ghost Wins!"
        if winner_text != "":
            draw_winner(winner_text)
            break

        keys_pressed = pygame.key.get_pressed()
        yellow_handle_movement(keys_pressed, yellow)
        red_handle_movement(keys_pressed, red)

        handle_bullets(yellow_bullets, red_bullets, yellow, red, ghost1_health, ghost2_health)

        draw_window(red, yellow, red_bullets, yellow_bullets, ghost2_health, ghost1_health)
        sound.play()

if __name__ == "__main__":
    main()
