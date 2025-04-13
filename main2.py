from random import randint

from pygame import *

WINDOW_WIDTH = 400
WINDOW_HEIGHT = 500
FPS = 60

class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height, speed):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (width, height))
        self.speed = speed
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))

class AnimatedSprite(sprite.Sprite):
    def __init__(self, sprite_sheet, x, y, width, height, speed):
        super().__init__()
        self.sprite_sheet = image.load(sprite_sheet)
        self.width = width
        self.height = height
        self.all_frames = self.loadsprites()
        self.cur_frame = 0
        self.image = self.all_frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed

    def loadsprites(self):
        frames = []
        rows = self.sprite_sheet.get_height() // self.height
        cols = self.sprite_sheet.get_width() // self.width
        for i in range(rows):
            for j in range(cols):
                frame = Surface((self.width, self.height), SRCALPHA)
                frame.blit(self.sprite_sheet, (0, 0), (j * self.width, i * self.height, self.width, self.height))
                frame = transform.scale(frame, (frame.get_width() * 4, frame.get_height() * 4))
                frames.append(frame)
                print(frame)
        return frames

    def update(self, screen):
        self.cur_frame += 0.1
        if self.cur_frame >= len(self.all_frames):
            self.cur_frame = 0
        self.image = self.all_frames[int(self.cur_frame)]

        screen.blit(self.image, (self.rect.x, self.rect.y))

class Player(AnimatedSprite):
    bullets = sprite.Group()


    def update(self, screen):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WINDOW_WIDTH - self.rect.width:
            self.rect.x += self.speed

        super().update(screen)

    def fire(self):
           bullet = Bullet("SpaceshipShooterGodot/Bullet/laser-bolts.png", self.rect.centerx, self.rect.top, 15, 20, 15)
           self.bullets.add(bullet)

    def draw_bullets(self, screen):
        self.bullets.update()
        self.bullets.draw(screen)

class Background(GameSprite):
    def __init__(self,image_name, x, y, width, height, speed):
        super().__init__(image_name, x, y, width, height, speed)

    def update(self, screen):
        self.rect.y += self.speed
        if self.rect.y >= WINDOW_HEIGHT:
            self.rect.y = 0 - self.rect.height

        super().update(screen)

class Map:
    def __init__(self):
        self.background1 = Background("background.png", 0, 0, WINDOW_WIDTH, WINDOW_HEIGHT, 5)
        self.background2 = Background("background.png",0, -WINDOW_HEIGHT, WINDOW_WIDTH, WINDOW_HEIGHT, 5)

    def update(self, screen):
        self.background1.update(screen)
        self.background2.update(screen)


class Enemy(GameSprite):

    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y >= 400:
            lost += 1
            self.rect.x = randint(0, 600)
            self.rect.y = 0
            self.speed = randint(1, 3)


class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()


lost = 0

bullets = sprite.Group()
enemies = sprite.Group()
for i in range(5):
    enemy = Enemy("SpaceshipShooterGodot/Enemies/enemy-medium.png", randint(0, 600), 0, 80, 50, randint(1, 3))
    enemies.add(enemy)



window = display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT,))
display.set_caption("Megashooter")

player = Player("SpaceshipShooterGodot/Player/ship.png", 5, 400, 16, 24, 10)
clock = time.Clock()
fps = 60
mixer.init()
mixer.music.load("spaceship shooter music/spaceship shooter .ogg")
mixer.music.play()

font.init()
font1 = font.Font(None, 70)

win = font1.render("    Win!!!", True, (210, 215, 0))
lose = font1.render("   Lose!!!", True, (210, 0, 0))

font2 = font.Font(None, 36)

map = Map()
score = 0
clock = time.Clock()

score = 0
finish = False
run = True
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False

        if e.type == KEYDOWN and e.key == K_SPACE:
            player.fire()

    if not finish:
        window.blit(window, (0, 0))

        text = font2.render(f"Рахунок: {score}", True, (255,255,255))
        text_lose = font2.render(f"Пропущено: {lost}", True, (255,255,255))
        window.blit(text, (10, 20))
        window.blit(text_lose, (510, 20))


run = True
menu = False

while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == MOUSEBUTTONDOWN:
            player.fire()

    map.update(window)

    if player.bullets:
        player.draw_bullets(window)

    enemies.update()
    enemies.draw(window)

    collides = sprite.groupcollide(enemies, player.bullets, True, True)
    for c in collides:
        score += 1
        enemy = Enemy("SpaceshipShooterGodot/Enemies/enemy-medium.png", randint(0, 600), 0, 80, 50, randint(1, 3))
        enemies.add(enemy)

        if score >= 100:
            finish = True
            window.blit(win, (200, 200))

        if lost >= 5:
            finish = True
            window.blit(lose, (200, 200))


    player.update(window)

    display.update()
    clock.tick(FPS)

    player.update(window)

    display.update()
    clock.tick(FPS)
