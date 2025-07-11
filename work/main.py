# HELLO, THE REASON WHY I ADD THE FUNCTIONS AND CHANGED COMMANDS IN MAIN.PY WITHOUT CONTRIBUTION OF PHASES IS THAT, IT DID'T SUCCESFULLY RUNNED AFTER DOWNLOADING IT.
# IT WAS WITH BUGS FROM DEVELOPERS SIDE, SO I CHANGED THE GAME STYLE AND ADDED SOME MORE THINGS, THANKS FOR ATTENTION!

import sys
import random
import pygame

pygame.init()
clock = pygame.time.Clock()

screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("PyGame Arkanoid")

muted = True

# pygame.mixer.music.load("background.mp3")
# pygame.mixer.music.play(-1)

def draw_title_screen():
    font = pygame.font.Font(None, 74)
    title = font.render("Arkanoid Game", True, (255, 255, 255))
    screen.blit(title, (screen_width // 2 - title.get_width() // 2, 200))

    font_small = pygame.font.Font(None, 36)
    prompt = font_small.render("Press SPACE to Start", True, (255, 255, 255))
    screen.blit(prompt, (screen_width // 2 - prompt.get_width() // 2, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                waiting = False

def show_game_over():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    message = font.render("Game Over", True, (255, 0, 0))
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

def show_win_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    message = font.render("You Win!", True, (0, 255, 0))
    screen.blit(message, (screen_width // 2 - message.get_width() // 2, 250))
    pygame.display.flip()
    pygame.time.wait(3000)
    pygame.quit()
    sys.exit()

class PowerUp:
    def __init__(self, x, y, type_):
        self.rect = pygame.Rect(x, y, 30, 30)
        self.type = type_
        self.speed = 3

    def move(self):
        self.rect.y += self.speed

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 0), self.rect)
        font = pygame.font.Font(None, 24)
        label = font.render(self.type, True, (0, 0, 0))
        surface.blit(label, (self.rect.x + 8, self.rect.y + 5))

draw_title_screen()

paddle_width = 100
paddle_height = 15
paddle = pygame.Rect(screen_width // 2 - paddle_width // 2,
                     screen_height - 50,
                     paddle_width,
                     paddle_height)
paddle_speed = 7

ball_radius = 10
ball = pygame.Rect(screen_width // 2 - ball_radius,
                   screen_height // 2 - ball_radius,
                   ball_radius * 2, ball_radius * 2)
ball_speed_x = 4
ball_speed_y = -4

lives = 3
brick_rows = 5
brick_cols = 10
brick_width = screen_width // brick_cols
brick_height = 30
bricks = []

for row in range(brick_rows):
    for col in range(brick_cols):
        brick = pygame.Rect(col * brick_width,
                            row * brick_height + 50,
                            brick_width - 5, brick_height - 5)
        bricks.append(brick)

powerups = []

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                muted = not muted
                pygame.mixer.music.set_volume(0 if muted else 1)
                print("Muted" if muted else "Unmuted")

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and paddle.left > 0:
        paddle.x -= paddle_speed
    if keys[pygame.K_RIGHT] and paddle.right < screen_width:
        paddle.x += paddle_speed

    ball.x += ball_speed_x
    ball.y += ball_speed_y

    if ball.left <= 0 or ball.right >= screen_width:
        ball_speed_x *= -1
    if ball.top <= 0:
        ball_speed_y *= -1

    if ball.colliderect(paddle):
        ball_speed_y *= -1

    if ball.bottom >= screen_height:
        lives -= 1
        if lives <= 0:
            show_game_over()
        else:
            ball.x = screen_width // 2 - ball_radius
            ball.y = screen_height // 2 - ball_radius
            ball_speed_x = 4
            ball_speed_y = -4

    hit_index = ball.collidelist(bricks)
    if hit_index != -1:
        hit_brick = bricks.pop(hit_index)
        ball_speed_y *= -1

        if random.random() < 0.3:
            power_type = random.choice(['E', 'S', 'L']) # E is expanding board, S is slow, L is life
            powerups.append(PowerUp(hit_brick.x + hit_brick.width // 2,
                                    hit_brick.y + hit_brick.height // 2,
                                    power_type))

    if len(bricks) == 0:
        show_win_screen()

    for powerup in powerups[:]:
        powerup.move()
        if powerup.rect.colliderect(paddle):
            if powerup.type == 'E':
                paddle.width = min(paddle.width + 30, 200)
            elif powerup.type == 'S':
                ball_speed_x = int(ball_speed_x * 0.75) or 1
                ball_speed_y = int(ball_speed_y * 0.75) or -1
            elif powerup.type == 'L':
                lives += 1
            powerups.remove(powerup)
        elif powerup.rect.top > screen_height:
            powerups.remove(powerup)

    screen.fill((0, 0, 0))

    for brick in bricks:
        pygame.draw.rect(screen, (0, 200, 255), brick)

    pygame.draw.rect(screen, (255, 255, 255), paddle)
    pygame.draw.ellipse(screen, (255, 0, 0), ball)

    for powerup in powerups:
        powerup.draw(screen)

    font = pygame.font.Font(None, 36)
    lives_text = font.render(f"Lives: {lives}", True, (255, 255, 255))
    screen.blit(lives_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)
