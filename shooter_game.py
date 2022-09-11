#Створи власний Шутер!

from pygame import *
import pygame_menu
from random import randint

mixer.init()
font.init()
init()



WIDTH = 900
HEIGHT = 600
window = display.set_mode((WIDTH, HEIGHT))
display.set_caption("Shooter")
font1 = font.SysFont("Impact", 50)
result = font1.render("", True, (0, 255, 0))


mixer.music.load("space.ogg")
mixer.music.set_volume(0.5) #гучність фонової музики
mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")
fire_sound.set_volume(0.05)


class GameSprite(sprite.Sprite):
    def __init__(self, image_name, x, y, width, height):
        super().__init__()
        self.image = transform.scale(image.load(image_name), (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = width
        self.height = height

    def draw(self):
        window.blit(self.image, self.rect)

class Player(GameSprite):
    def __init__(self):
        super().__init__("rocket.png", 400, HEIGHT-200, 80, 120)
        self.speed = 5
        self.hp = 100
        self.bullets = sprite.Group()
        self.points = 0

    def fire(self):
        new_bullet = Bullet(self.rect.centerx-7, self.rect.y+5)
        self.bullets.add(new_bullet)
        fire_sound.play()

    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT] and self.rect.x>0:
            self.rect.x -= self.speed
        if keys[K_RIGHT] and self.rect.x<WIDTH-self.width:
            self.rect.x += self.speed

        if keys[K_SPACE]:
            self.fire()




class Ufo(GameSprite):
    def __init__(self):
        rand_x = randint(0, WIDTH-120)
        rand_y = randint(-400, -100)

        super().__init__("ufo.png", rand_x, rand_y, 120, 60)
        self.speed = randint(3, 5)
        self.hp = 100

    def update(self):
        self.rect.y += self.speed
        if self.rect.y > HEIGHT + self.height:
            self.rect.x = randint(0, WIDTH-120)
            self.rect.y = randint(-400, -100)



class Bullet(GameSprite):
    def __init__(self, x, y):
        super().__init__("bullet.png", x, y, 20, 15)
        self.speed = 5

    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0 - self.height:
            self.kill()



bg = transform.scale(image.load("galaxy.jpg"), (WIDTH, HEIGHT))
player = Player()
ufos = sprite.Group()


font2 = font.SysFont("Impact", 25)

points_text = font2.render("Points: " + str(player.points), True, (255, 255, 255))
hp_text = font2.render("Hp: " + str(player.hp), True, (255, 255, 255))



for i in range(5):
    ufo = Ufo()
    ufos.add(ufo)



run = True
finish = False
clock = time.Clock()
FPS = 60
rand_ufo = 300


while run:
    window.blit(bg, (0,0))
    for e in event.get():
        if e.type == QUIT:
            run = False

    if not finish:
        player.update()
        player.draw()

        ufos.update()
        ufos.draw(window)

        player.bullets.update()
        player.bullets.draw(window)

        window.blit(points_text, (30, 30))
        window.blit(hp_text, (WIDTH-150, 30))


        collides = sprite.groupcollide(ufos, player.bullets, True, True)
        for i in collides:
            player.points += 1
            points_text = font2.render("Points: " + str(player.points), True, (255, 255, 255))

        collide_list = sprite.spritecollide(player, ufos, True)

        rand_num = randint(0, rand_ufo)
        if rand_num == 5:
            ufo = Ufo()
            ufos.add(ufo)
            if rand_ufo >= 50:
                rand_ufo -= 20


        for kick in collide_list:
            player.hp -= 25
            hp_text = font2.render("Hp: " + str(player.hp), True, (255, 255, 255))

        if player.hp <=0:
            finish = True
            result = font1.render("You lose!", True, (255, 0, 0))

        if player.points > 10:
            finish = True
            result = font1.render("You win!", True, (0, 255, 0))


    else:
        window.blit(result, (300, 300))


    display.update()
    clock.tick(FPS)
