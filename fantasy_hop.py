import pygame
import sys

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fantasy Hop")
clock = pygame.time.Clock()

PLAYER_W, PLAYER_H = 40, 56
TILE = 70

# --- Procedurally drawn sprites (no external files) ---

def make_player():
    surf = pygame.Surface((PLAYER_W, PLAYER_H), pygame.SRCALPHA)
    # cloak / body
    pygame.draw.rect(surf, (70, 90, 160), (8, 22, 24, 30), border_radius=6)
    # tunic trim
    pygame.draw.rect(surf, (110, 130, 200), (8, 22, 24, 8), border_radius=4)
    # head
    pygame.draw.circle(surf, (240, 210, 180), (PLAYER_W // 2, 16), 10)
    # little pointed hat (fantasy)
    pygame.draw.polygon(surf, (120, 60, 150), [(10, 12), (30, 12), (20, -6)])
    pygame.draw.circle(surf, (250, 230, 120), (20, -4), 3)  # hat tip gem
    # eyes
    pygame.draw.circle(surf, (40, 40, 40), (16, 16), 2)
    pygame.draw.circle(surf, (40, 40, 40), (24, 16), 2)
    # boots
    pygame.draw.rect(surf, (60, 45, 40), (10, 50, 8, 6), border_radius=2)
    pygame.draw.rect(surf, (60, 45, 40), (22, 50, 8, 6), border_radius=2)
    return surf

def make_tile():
    surf = pygame.Surface((TILE, TILE), pygame.SRCALPHA)
    # dirt base
    pygame.draw.rect(surf, (120, 85, 55), (0, 0, TILE, TILE))
    # darker dirt speckles
    for pos in [(12, 30), (40, 45), (55, 25), (25, 55), (48, 60)]:
        pygame.draw.circle(surf, (95, 65, 42), pos, 4)
    # grass cap
    pygame.draw.rect(surf, (90, 160, 70), (0, 0, TILE, 16))
    pygame.draw.rect(surf, (110, 190, 85), (0, 0, TILE, 8))
    # grass blades hanging down
    for x in range(4, TILE, 10):
        pygame.draw.polygon(surf, (90, 160, 70), [(x, 16), (x + 6, 16), (x + 3, 26)])
    return surf

def make_background():
    surf = pygame.Surface((WIDTH, HEIGHT))
    # vertical sky gradient
    top = (110, 175, 220)
    bottom = (200, 225, 235)
    for y in range(HEIGHT):
        t = y / HEIGHT
        col = (int(top[0] + (bottom[0] - top[0]) * t),
               int(top[1] + (bottom[1] - top[1]) * t),
               int(top[2] + (bottom[2] - top[2]) * t))
        pygame.draw.line(surf, col, (0, y), (WIDTH, y))
    # soft clouds
    for cx, cy in [(150, 90), (500, 140), (680, 70)]:
        for dx, dy, r in [(0, 0, 26), (26, 6, 22), (-24, 6, 20), (10, -10, 18)]:
            pygame.draw.circle(surf, (245, 248, 250), (cx + dx, cy + dy), r)
    # distant hills
    pygame.draw.ellipse(surf, (150, 190, 150), (-100, 430, 500, 300))
    pygame.draw.ellipse(surf, (135, 175, 140), (300, 460, 600, 300))
    return surf

player_img = make_player()
player_img_flipped = pygame.transform.flip(player_img, True, False)
tile_img = make_tile()
bg_img = make_background()

GRAVITY = 0.8
JUMP_STRENGTH = -15
MOVE_SPEED = 5

player = pygame.Rect(100, 400, PLAYER_W, PLAYER_H)
player_vel_y = 0
on_ground = False
facing_right = True

def make_row(start_x, y, count):
    return [pygame.Rect(start_x + i * TILE, y, TILE, TILE) for i in range(count)]

platforms = []
platforms += make_row(0, 530, 24)        # long ground
platforms += make_row(200, 430, 2)
platforms += make_row(420, 350, 2)
platforms += make_row(650, 280, 2)
platforms += make_row(900, 400, 3)
platforms += make_row(1200, 320, 2)

LEVEL_WIDTH = 24 * TILE
camera_x = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # --- Horizontal movement ---
    dx = 0
    if keys[pygame.K_LEFT] or keys[pygame.K_a]:
        dx = -MOVE_SPEED
        facing_right = False
    if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
        dx = MOVE_SPEED
        facing_right = True
    player.x += dx
    for plat in platforms:
        if player.colliderect(plat):
            if dx > 0:
                player.right = plat.left
            elif dx < 0:
                player.left = plat.right

    if player.left < 0:
        player.left = 0
    if player.right > LEVEL_WIDTH:
        player.right = LEVEL_WIDTH

    # --- Jump ---
    if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and on_ground:
        player_vel_y = JUMP_STRENGTH
        on_ground = False

    # --- Gravity / vertical ---
    player_vel_y += GRAVITY
    player.y += player_vel_y
    on_ground = False
    for plat in platforms:
        if player.colliderect(plat):
            if player_vel_y > 0:
                player.bottom = plat.top
                on_ground = True
            elif player_vel_y < 0:
                player.top = plat.bottom
            player_vel_y = 0

    if player.top > HEIGHT + 200:
        player.x, player.y = 100, 400
        player_vel_y = 0

    # --- Camera ---
    camera_x = player.centerx - WIDTH // 2
    if camera_x < 0:
        camera_x = 0
    if camera_x > LEVEL_WIDTH - WIDTH:
        camera_x = LEVEL_WIDTH - WIDTH

    # --- Draw ---
    screen.blit(bg_img, (0, 0))
    for plat in platforms:
        screen.blit(tile_img, (plat.x - camera_x, plat.y))
    img = player_img if facing_right else player_img_flipped
    screen.blit(img, (player.x - camera_x, player.y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()