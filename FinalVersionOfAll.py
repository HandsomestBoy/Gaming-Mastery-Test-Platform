import pygame
from pygame.locals import *
import random
import os
import time
import random
from tkinter import *
import sqlite3

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED   = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,0)
MGREEN = (66, 245, 155)
GREY = (175,175,175)
FPS = 30

font_name = pygame.font.match_font('arial')
def draw_text(surf, text, size, x, y):
    font = pygame.font.Font(font_name, size)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.centerx = x
    text_rect.top = y
    surf.blit(text_surface, text_rect)

def draw_health(surf, hp, x, y):
    if hp < 0:
        hp = 0
    BAR_LENGTH = 100
    BAR_HEIGHT = 10
    fill = hp * BAR_LENGTH / 100
    
    outline_rect = pygame.Rect(x, y, BAR_LENGTH, BAR_HEIGHT)
    fill_rect = pygame.Rect(x, y, fill, BAR_HEIGHT)
    pygame.draw.rect(surf, GREEN, fill_rect)
    pygame.draw.rect(surf, WHITE, outline_rect, 2)

def draw_lives(surf, lives, img, x, y):
    # Draw a live pic every 30 pixels
    for i in range(lives):
        img_rect = img.get_rect()
        img_rect.x = x + 30 * i
        img_rect.y = y
        surf.blit(img, img_rect)

def init_screen():
    pygame.init()
    database.lobby.screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption("Main Lobby")
    database.lobby.screen.fill(BLACK)
    database.lobby.clock = pygame.time.Clock()

    game1 = pygame.image.load(os.path.join("img", "game1.png")).convert()
    game1_img = pygame.transform.scale(game1, (200, 200))
    database.lobby.screen.blit(game1_img, (33,140))
    game2 = pygame.image.load(os.path.join("img", "game3.png")).convert()
    game2_img = pygame.transform.scale(game2, (200, 200))
    database.lobby.screen.blit(game2_img, (299,140))
    game3 = pygame.image.load(os.path.join("img", "game2.png")).convert()
    game3_img = pygame.transform.scale(game3, (200, 200))
    database.lobby.screen.blit(game3_img, (565,140))
    database.lobby.target1 = pygame.rect.Rect(33, 140, 200, 200)
    database.lobby.target3 = pygame.rect.Rect(299, 140, 200, 200)
    database.lobby.target2 = pygame.rect.Rect(565, 140, 200, 200)

class PAR:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((500,600))
        pygame.display.set_caption("PRgame")
        self.clock = pygame.time.Clock()
        self.fps = 60
        self.best_score = 0
        self.score = 0
        self.all_sprites = pygame.sprite.Group()
        self.rocks = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.abilities = pygame.sprite.Group() 
        self.player = Player()
        self.background_img = pygame.image.load(os.path.join("img","background.png")).convert()
        self.die_sound = pygame.mixer.Sound(os.path.join("sound","rumble.ogg"))
        self.gun_sound = pygame.mixer.Sound(os.path.join("sound","pow1.wav"))
        self.shield_sound = pygame.mixer.Sound(os.path.join("sound","pow0.wav"))
        self.expl_sounds = [
        pygame.mixer.Sound(os.path.join("sound","expl0.wav")),
        pygame.mixer.Sound(os.path.join("sound","expl1.wav"))
        ]
        pygame.mixer.music.load(os.path.join("sound","background.ogg"))
        pygame.mixer.music.set_volume(0.3)
        pygame.mixer.music.play(-1)
    
    def draw_init(self):
        self.screen.blit(self.background_img, (0,0))
        draw_text(self.screen, 'Plane and Rocks', 50, 500/2, 600/4)
        draw_text(self.screen, '"<-  ->" or "A, D" keys to control plane', 22, 500/2, 600/2)
        draw_text(self.screen, '"SPACE" key to shoot', 22, 500/2, (600/2)+20)
        draw_text(self.screen, 'Your best Score is ' + str(self.best_score), 22, 500/2, (600/2)+80)
        draw_text(self.screen, 'Press any key to start', 18, 500/2, 600*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            self.clock.tick(self.fps)
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_normal_score(self):
        self.screen.blit(self.background_img, (0,0))
        draw_text(self.screen, 'Your Current Score is ' + str(self.score), 28, 500/2, 600/4)
        draw_text(self.screen, 'Press any key to return to main menu', 18, 500/2, 600*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            self.clock.tick(self.fps)
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_new_record(self):
        self.screen.blit(self.background_img, (0,0))
        draw_text(self.screen, 'Congratulations!', 28, 500/2, 600/4)
        draw_text(self.screen, 'You have reached a new record! ' + str(self.best_score), 28, 500/2, (600/4)+50)
        draw_text(self.screen, str(self.best_score), 64, 500/2, 600/2)
        draw_text(self.screen, 'Press any key to return to main menu', 18, 500/2, 600*3/4)
        pygame.display.update()
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("""UPDATE User_info SET
        par_score = :par_score
        WHERE oid = :oid""",
        {'par_score': self.best_score,
        'oid': database.account_oid
        })
        conn.commit()
        conn.close()
        waiting = True
        while waiting:
            self.clock.tick(self.fps)
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def update(self):
        show_init = True
        running = True
        show_new_record = False
        show_normal_score = False

        while running:
            if show_init:
                close = self.draw_init()
                if close:
                    lobby = Lobby()
                    lobby.update()
                    break
                show_init = False
                self.all_sprites.add(self.player)
                for i in range(8):
                    r = Rock()
                    self.all_sprites.add(r)
                    self.rocks.add(r)

            self.clock.tick(self.fps)
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    lobby = Lobby()
                    lobby.update()
                    break
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.shoot()

            # Update game
            self.all_sprites.update()
            # Colision of bullet and rock
            hits = pygame.sprite.groupcollide(self.rocks, self.bullets, True, True)
            for hit in hits:
                random.choice(self.expl_sounds).play()
                self.score += hit.radius
                r = Rock()
                self.all_sprites.add(r)
                expl = Explosion(hit.rect.center, 'lg')
                self.all_sprites.add(expl)
                if random.random() > 0.99:
                    ab = Abilities(hit.rect.center)
                    self.all_sprites.add(ab)
                    self.abilities.add(ab)
                self.rocks.add(r)
            
            # Colision of player and rock
            hits = pygame.sprite.spritecollide(self.player, self.rocks, True, pygame.sprite.collide_circle)
            for hit in hits:
                r = Rock()
                self.all_sprites.add(r)
                self.rocks.add(r)
                self.player.health -= hit.radius*2
                expl = Explosion(hit.rect.center, 'sm')
                self.all_sprites.add(expl)
                if self.player.health <= 0:
                    death_expl = Explosion(self.player.rect.center, 'player')
                    self.all_sprites.add(death_expl)
                    self.die_sound.play()
                    self.player.lives -= 1
                    self.player.health = 100
                    self.player.hide()
            
            # Colision of player and abilities
            hits = pygame.sprite.spritecollide(self.player, self.abilities, True)
            for hit in hits:
                if hit.type == 'shield':
                    self.player.health += 20
                    if self.player.health > 100:
                        self.player.health = 100
                    self.shield_sound.play()
                elif hit.type == 'gun':
                    self.player.gunup()
                    self.gun_sound.play()


            # letting the explotion animation finish then end game
            if self.player.lives == 0 and not(death_expl.alive()):
                if self.score > self.best_score:
                    self.best_score = self.score
                    show_new_record = True
                    if show_new_record:
                        close = self.draw_new_record()
                        if close:
                            lobby = Lobby()
                            lobby.update()
                            break
                        show_new_record = False
                elif self.score <= self.best_score:
                    show_normal_score = True
                    if show_normal_score:
                        close = self.draw_normal_score()
                        if close:
                            lobby = Lobby()
                            lobby.update()
                            break
                        show_normal_score = False
                self.player.kill()
                self.score = 0
                self.all_sprites = pygame.sprite.Group()
                self.rocks = pygame.sprite.Group()
                self.player = Player()
                show_init = True
                    

            # Gaming picture showin
            self.screen.blit(self.background_img, (0,0))
            self.all_sprites.draw(self.screen)
            draw_text(self.screen, str(self.score), 18, 500 / 2, 10)
            draw_text(self.screen, str(self.player.health), 12, 120, 15)
            draw_health(self.screen, self.player.health, 5, 15)
            draw_lives(self.screen, self.player.lives, self.player.player_lives_img, 500 - 100, 15)
            pygame.display.update()
        pygame.quit()

    def shoot(self):
        if not(self.player.hidden):
            if self.player.gun == 1:
                bullet = Bullet(self.player.rect.centerx, self.player.rect.top)
                self.all_sprites.add(bullet)
                self.bullets.add(bullet)
                self.player.shoot_sound.play()
            elif self.player.gun >= 2:
                bullet1 = Bullet(self.player.rect.left, self.player.rect.centery)
                bullet2 = Bullet(self.player.rect.right, self.player.rect.centery)
                self.all_sprites.add(bullet1)
                self.bullets.add(bullet1)
                self.all_sprites.add(bullet2)
                self.bullets.add(bullet2)
                self.player.shoot_sound.play()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.player_img = pygame.image.load(os.path.join("img","player.png")).convert()
        self.player_lives_img = pygame.transform.scale(self.player_img, (25,19))
        self.player_lives_img.set_colorkey(BLACK)
        pygame.display.set_icon(self.player_lives_img)
        self.image = pygame.transform.scale(self.player_img, (50, 38))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.radius = 20
        self.shoot_sound = pygame.mixer.Sound(os.path.join("sound","shoot.wav"))
        self.rect.centerx = 500 / 2
        self.rect.bottom = 600 - 10
        self.speedx = 8
        self.health = 100
        self.lives = 3
        self.hidden = False
        self.hide_time = 0
        self.gun = 1
        self.gun_time = 0
    
    def update(self):
        if self.gun > 1 and pygame.time.get_ticks() - self.gun_time > 5000:
            self.gun -= 1
            self.gun_time = pygame.time.get_ticks()
        
        if self.hidden and pygame.time.get_ticks() - self.hide_time > 1000:
            self.hidden = False
            self.rect.centerx = 500 / 2
            self.rect.bottom = 600 - 10
        
        key_pressed = pygame.key.get_pressed()
        if key_pressed[pygame.K_RIGHT]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_LEFT]:
            self.rect.x -= self.speedx
        if key_pressed[pygame.K_d]:
            self.rect.x += self.speedx
        if key_pressed[pygame.K_a]:
            self.rect.x -= self.speedx
        
        if self.rect.right > 500:
            self.rect.right = 500
        if self.rect.left < 0:
            self.rect.left = 0
    
    def hide(self):
        self.hidden = True
        self.hide_time = pygame.time.get_ticks()
        self.rect.center = (500/2, 600 + 500)

    def gunup(self):
        self.gun += 1
        self.gun_time = pygame.time.get_ticks()
        
class Rock(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.rock_imgs = []
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock0.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock1.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock2.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock3.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock4.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock5.png")).convert())
        self.rock_imgs.append(pygame.image.load(os.path.join("img", "rock6.png")).convert())
        self.image_ori = random.choice(self.rock_imgs)
        self.image_ori.set_colorkey(BLACK)
        self.image = self.image_ori.copy()
        self.rect = self.image.get_rect()
        self.radius = int(self.rect.width / 2 * 0.85)
        #pygame.draw.circle(self.image, RED, self.rect.center, self.radius)
        self.rect.x = random.randrange(0, 500 - self.rect.width)
        self.rect.y = random.randrange(-180, -100)
        self.speedy = random.randrange(2, 10)
        self.speedx = random.randrange(-3, 3)
        self.total_degree = 0
        self.rot_degree = random.randrange(-3, 3)

    def rotate(self):
        self.total_degree += self.rot_degree
        self.total_degree = self.total_degree % 360
        self.image = pygame.transform.rotate(self.image_ori, self.total_degree)
        center = self.rect.center
        self.rect = self.image.get_rect()
        self.rect.center = center
    
    def update(self):
        self.rotate()
        self.rect.y += self.speedy
        self.rect.x += self.speedx
        if self.rect.top > 600 or self.rect.left > 500 or self.rect.right < 0:
            self.rect.x = random.randrange(0, 500 - self.rect.width)
            self.rect.y = random.randrange(-100, -40)
            self.speedy = random.randrange(2, 10)
            self.speedx = random.randrange(-3, 3)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.bullet_img = pygame.image.load(os.path.join("img","bullet.png")).convert()
        self.image = self.bullet_img
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center, size):
        pygame.sprite.Sprite.__init__(self)
        self.size = size
        self.expl_anim = {}
        self.expl_anim['lg'] = []
        self.expl_anim['sm'] = []
        self.expl_anim['player'] = []
        self.expl_img0 = pygame.image.load(os.path.join("img", "expl0.png")).convert()
        self.expl_img0.set_colorkey(BLACK)
        self.expl_img1 = pygame.image.load(os.path.join("img", "expl1.png")).convert()
        self.expl_img1.set_colorkey(BLACK)
        self.expl_img2 = pygame.image.load(os.path.join("img", "expl2.png")).convert()
        self.expl_img2.set_colorkey(BLACK)
        self.expl_img3 = pygame.image.load(os.path.join("img", "expl3.png")).convert()
        self.expl_img3.set_colorkey(BLACK)
        self.expl_img4 = pygame.image.load(os.path.join("img", "expl4.png")).convert()
        self.expl_img4.set_colorkey(BLACK)
        self.expl_img5 = pygame.image.load(os.path.join("img", "expl5.png")).convert()
        self.expl_img5.set_colorkey(BLACK)
        self.expl_img6 = pygame.image.load(os.path.join("img", "expl6.png")).convert()
        self.expl_img6.set_colorkey(BLACK)
        self.expl_img7 = pygame.image.load(os.path.join("img", "expl7.png")).convert()
        self.expl_img7.set_colorkey(BLACK)
        self.expl_img8 = pygame.image.load(os.path.join("img", "expl8.png")).convert()
        self.expl_img8.set_colorkey(BLACK)
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img0, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img0, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img1, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img1, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img2, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img2, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img3, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img3, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img4, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img4, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img5, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img5, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img6, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img6, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img7, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img7, (30,30)))
        self.expl_anim['lg'].append(pygame.transform.scale(self.expl_img8, (75,75)))
        self.expl_anim['sm'].append(pygame.transform.scale(self.expl_img8, (30,30)))
        self.player_expl_img0 = pygame.image.load(os.path.join("img", "player_expl0.png")).convert()
        self.player_expl_img0.set_colorkey(BLACK)
        self.player_expl_img1 = pygame.image.load(os.path.join("img", "player_expl1.png")).convert()
        self.player_expl_img1.set_colorkey(BLACK)
        self.player_expl_img2 = pygame.image.load(os.path.join("img", "player_expl2.png")).convert()
        self.player_expl_img2.set_colorkey(BLACK)
        self.player_expl_img3 = pygame.image.load(os.path.join("img", "player_expl3.png")).convert()
        self.player_expl_img3.set_colorkey(BLACK)
        self.player_expl_img4 = pygame.image.load(os.path.join("img", "player_expl4.png")).convert()
        self.player_expl_img4.set_colorkey(BLACK)
        self.player_expl_img5 = pygame.image.load(os.path.join("img", "player_expl5.png")).convert()
        self.player_expl_img5.set_colorkey(BLACK)
        self.player_expl_img6 = pygame.image.load(os.path.join("img", "player_expl6.png")).convert()
        self.player_expl_img6.set_colorkey(BLACK)
        self.player_expl_img7 = pygame.image.load(os.path.join("img", "player_expl7.png")).convert()
        self.player_expl_img7.set_colorkey(BLACK)
        self.player_expl_img8 = pygame.image.load(os.path.join("img", "player_expl8.png")).convert()
        self.player_expl_img8.set_colorkey(BLACK)
        self.expl_anim['player'].append(self.player_expl_img0)
        self.expl_anim['player'].append(self.player_expl_img1)
        self.expl_anim['player'].append(self.player_expl_img2)
        self.expl_anim['player'].append(self.player_expl_img3)
        self.expl_anim['player'].append(self.player_expl_img4)
        self.expl_anim['player'].append(self.player_expl_img5)
        self.expl_anim['player'].append(self.player_expl_img6)
        self.expl_anim['player'].append(self.player_expl_img7)
        self.expl_anim['player'].append(self.player_expl_img8)
        self.image = self.expl_anim[self.size][0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(self.expl_anim[self.size]):
                self.kill()
            else:
                self.image = self.expl_anim[self.size][self.frame]
                center = self.rect.center
                self.rect = self.image.get_rect()
                self.rect.center = center

class Abilities(pygame.sprite.Sprite):
    def __init__(self, center):
        pygame.sprite.Sprite.__init__(self)
        self.type = random.choice(['shield', 'gun'])
        self.abilities_imgs = {}
        self.abilities_imgs['shield'] = pygame.image.load(os.path.join("img", "shield.png")).convert()
        self.abilities_imgs['gun'] = pygame.image.load(os.path.join("img", "gun.png")).convert()

        self.image = self.abilities_imgs[self.type]
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.speedy = 3

    def update(self):
        self.rect.y += self.speedy
        if self.rect.top > 600:
            self.kill()

class MMC:
    def __init__(self):
        self.width = 600
        self.height = 600
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Mouse Moving Control")
        self.reach_sound = pygame.mixer.Sound(os.path.join("sound","food.mp3"))
        self.dead_sound = pygame.mixer.Sound(os.path.join("sound","dead.mp3"))
        self.background_sound = pygame.mixer.Sound(os.path.join("sound","background.flac"))
        self.background_sound.play(-1)
        self.target = pygame.rect.Rect(295, 550, 10, 10)
        self.target_draging = False
        self.first_level = True
        self.second_level = False
        self.third_level = False
        self.running = True
        self.show_new_record = False
        self.show_normal_score = False
        self.show_init = True
        self.best_score = 0
        self.score = 0
        self.clock = pygame.time.Clock()
        
        #level1
        self.destination1 = pygame.rect.Rect(550, 50, 50, 50)
        self.border1 = pygame.rect.Rect(0, 0, 250, 600)
        self.border2 = pygame.rect.Rect(250, 0, 350, 50)
        self.border3 = pygame.rect.Rect(350, 100, 250, 500)

        #level2
        self.destination2 = pygame.rect.Rect(550, 550, 50, 25)
        self.border4 = pygame.rect.Rect(0, 0, 600, 50)
        self.border5 = pygame.rect.Rect(100, 100, 500, 50)
        self.border6 = pygame.rect.Rect(0, 200, 500, 50)
        self.border7 = pygame.rect.Rect(100, 300, 500, 50)
        self.border8 = pygame.rect.Rect(0, 400, 500, 50)
        self.border9 = pygame.rect.Rect(100, 500, 500, 50)
        self.border10 = pygame.rect.Rect(0, 0, 50, 600)
        self.border11 = pygame.rect.Rect(550, 100, 50, 400)
        self.border12 = pygame.rect.Rect(0, 575, 600, 25)

        #level3
        self.destination3 = pygame.rect.Rect(400, 0, 15, 15)
        self.border13 = pygame.rect.Rect(0, 0, 400, 65)
        self.border14 = pygame.rect.Rect(415, 0, 185, 50)
        self.border15 = pygame.rect.Rect(0, 65, 450, 65)
        self.border16 = pygame.rect.Rect(465, 50, 170, 100)
        self.border17 = pygame.rect.Rect(0, 130, 300, 100)
        self.border18 = pygame.rect.Rect(320, 150, 280, 55)
        self.border19 = pygame.rect.Rect(0, 230, 550, 25)
        self.border20 = pygame.rect.Rect(575, 205, 25, 395)
        self.border21 = pygame.rect.Rect(0, 0, 25, 600)
        self.border22 = pygame.rect.Rect(0, 575, 600, 25)
        self.border23 = pygame.rect.Rect(50, 275, 550, 25)
        self.border24 = pygame.rect.Rect(0, 325, 550, 25)
        self.border25 = pygame.rect.Rect(50, 375, 550, 25)
        self.border26 = pygame.rect.Rect(0, 425, 550, 25)
        self.border27 = pygame.rect.Rect(50, 475, 550, 25)
        self.border28 = pygame.rect.Rect(0, 525, 525, 75)

    def draw_init(self):
        self.screen.fill(BLUE)
        draw_text(self.screen, 'Mouse Moving Control', 50, self.width/2, self.height/4)
        draw_text(self.screen, 'drag green square to red square without touching border', 22, self.width/2, self.height/2)
        if self.best_score != 0:
            draw_text(self.screen, 'Your best score is ' + str(self.best_score) + 'sec', 22, self.width/2, (self.height/2)+80)
        draw_text(self.screen, 'Press any key to start', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_normal_score(self):
        self.screen.fill(BLUE)
        draw_text(self.screen, 'Your Current Score is '+ str(self.score) + 'sec', 28, self.width/2, self.height/4)
        draw_text(self.screen, 'Press any key to return to main menu', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_new_record(self):
        self.screen.fill(BLUE)
        draw_text(self.screen, 'Contradulations!', 28, self.width/2, self.height/4)
        draw_text(self.screen, 'You have reached a new record!', 28, self.width/2, (self.height/4)+50)
        draw_text(self.screen, str(self.best_score) + 'sec', 64, self.width/2, self.height/2)
        draw_text(self.screen, 'Press any key to return to main menu', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("""UPDATE User_info SET
        mmc_score = :mmc_score
        WHERE oid = :oid""",
        {'mmc_score': self.best_score,
        'oid': database.account_oid
        })
        conn.commit()
        conn.close()
        waiting = True
        while waiting:
            self.clock.tick(FPS)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def update(self):
        while self.running:
            if self.show_init:
                close = self.draw_init()
                if close:
                    lobby = Lobby()
                    lobby.update()
                    break
                self.show_init = False
                start_time = pygame.time.get_ticks()
            self.clock.tick(FPS)
            self.score = int((pygame.time.get_ticks()-start_time)/1000)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lobby = Lobby()
                    lobby.update()
                    self.running = False

                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:            
                        if self.target.collidepoint(event.pos):
                            self.target_draging = True
                            mouse_x, mouse_y = event.pos
                            offset_x = self.target.x - mouse_x
                            offset_y = self.target.y - mouse_y

                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 1:     
                        self.target_draging = False

                elif event.type == pygame.MOUSEMOTION:
                    if self.target_draging:
                        mouse_x, mouse_y = event.pos
                        self.target.x = mouse_x + offset_x
                        self.target.y = mouse_y + offset_y
                        if self.first_level:
                            if self.target.colliderect(self.destination1):
                                self.first_level = False
                                self.second_level = True
                                self.reach_sound.play()
                            if self.target.colliderect(self.border1):
                                self.target.x = 295
                                self.target.y = 550
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border2):
                                self.target.x = 295
                                self.target.y = 550
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border3):
                                self.target.x = 295
                                self.target.y = 550
                                self.target_draging = False
                                self.dead_sound.play()

                        if self.second_level:
                            if self.target.colliderect(self.destination2):
                                self.second_level = False
                                self.third_level = True
                                self.reach_sound.play()
                            if self.target.colliderect(self.border4):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border5):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border6):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border7):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border8):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border9):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border10):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border11):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border12):
                                self.target.x = 570
                                self.target.y = 70
                                self.target_draging = False
                                self.dead_sound.play()
            
                        if self.third_level:
                            if self.target.colliderect(self.destination3):
                                self.reach_sound.play()
                                self.third_level = False
                                if self.best_score == 0:
                                    self.best_score = self.score
                                    self.show_new_record = True
                                    if self.show_new_record:
                                        close = self.draw_new_record()
                                        if close:
                                            lobby = Lobby()
                                            lobby.update()
                                            break
                                        self.show_new_record = False
                                elif self.best_score > self.score:
                                    self.best_score = self.score
                                    self.show_new_record = True
                                    if self.show_new_record:
                                        close = self.draw_new_record()
                                        if close:
                                            lobby = Lobby()
                                            lobby.update()
                                            break
                                        self.show_new_record = False
                                else:
                                    self.show_normal_score = True
                                    if self.show_normal_score:
                                        close = self.draw_normal_score()
                                        if close:
                                            lobby = Lobby()
                                            lobby.update()
                                            break
                                        self.show_normal_score = False
                                self.show_init = True
                                self.target.x = 295
                                self.target.y = 550
                                self.first_level = True
                            if self.target.colliderect(self.border13):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border14):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border15):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border16):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border17):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border18):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border19):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border20):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border21):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border22):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border23):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border24):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border25):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border26):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border27):
                                self.target.x = 562
                                self.target.y = 562
                                self.target_draging = False
                                self.dead_sound.play()
                            if self.target.colliderect(self.border28):
                                self.target.x = 562
                                self.target.y = 562
                                #self.target_draging = False
                                self.dead_sound.play()

            self.screen.fill(BLUE)
            pygame.draw.rect(self.screen, GREEN, self.target)
            if self.first_level:
                pygame.draw.rect(self.screen, RED, self.destination1)
                pygame.draw.rect(self.screen, BLACK, self.border1)
                pygame.draw.rect(self.screen, BLACK, self.border2)
                pygame.draw.rect(self.screen, BLACK, self.border3)
            if self.second_level:
                pygame.draw.rect(self.screen, RED, self.destination2)
                pygame.draw.rect(self.screen, BLACK, self.border4)
                pygame.draw.rect(self.screen, BLACK, self.border5)
                pygame.draw.rect(self.screen, BLACK, self.border6)
                pygame.draw.rect(self.screen, BLACK, self.border7)
                pygame.draw.rect(self.screen, BLACK, self.border8)
                pygame.draw.rect(self.screen, BLACK, self.border9)
                pygame.draw.rect(self.screen, BLACK, self.border10)
                pygame.draw.rect(self.screen, BLACK, self.border11)
                pygame.draw.rect(self.screen, BLACK, self.border12)
            if self.third_level:
                pygame.draw.rect(self.screen, RED, self.destination3)
                pygame.draw.rect(self.screen, BLACK, self.border13)
                pygame.draw.rect(self.screen, BLACK, self.border14)
                pygame.draw.rect(self.screen, BLACK, self.border15)
                pygame.draw.rect(self.screen, BLACK, self.border16)
                pygame.draw.rect(self.screen, BLACK, self.border17)
                pygame.draw.rect(self.screen, BLACK, self.border18)
                pygame.draw.rect(self.screen, BLACK, self.border19)
                pygame.draw.rect(self.screen, BLACK, self.border20)
                pygame.draw.rect(self.screen, BLACK, self.border21)
                pygame.draw.rect(self.screen, BLACK, self.border22)
                pygame.draw.rect(self.screen, BLACK, self.border23)
                pygame.draw.rect(self.screen, BLACK, self.border24)
                pygame.draw.rect(self.screen, BLACK, self.border25)
                pygame.draw.rect(self.screen, BLACK, self.border26)
                pygame.draw.rect(self.screen, BLACK, self.border27)
                pygame.draw.rect(self.screen, BLACK, self.border28)
            draw_text(self.screen, 'Time: '+ str(self.score) + 'sec', 28, 100, 20)
            pygame.display.flip()
            self.clock.tick(FPS)

        pygame.quit()

class Game:
    def __init__(self):
        self.width = 600
        self.height = 600
        self.size = 40
        pygame.init()
        pygame.mixer.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Snake")
        self.screen.fill(GREEN)
        self.snake = Snake(self.screen, 1)
        self.snake.draw()
        self.apple = Apple(self.screen)
        self.apple.draw()
        self.eat_sound = pygame.mixer.Sound(os.path.join("sound","food.mp3"))
        self.dead_sound = pygame.mixer.Sound(os.path.join("sound","dead.mp3"))
        self.background_sound = pygame.mixer.Sound(os.path.join("sound","background.flac"))
        self.background_sound.play(-1)
        self.best_score = 0

    def is_collision(self, x1, x2, y1, y2):
        if x1 >= x2 and x1 < x2 + self.size:
            if y1 >= y2 and y1 < y2 + self.size:
                return True
        return False

    def all_drawing(self):
        self.snake.walk()
        self.apple.draw()
        draw_text(self.screen, "Your score: " + str(self.snake.length-1), 30, self.width-100, 10)
        pygame.display.update()
        # snake touches apple
        if self.is_collision(self.snake.x[0], self.apple.x, self.snake.y[0], self.apple.y):
            self.eat_sound.play()
            self.snake.increase_length()
            self.apple.move()  
        
    def update(self):
        running = True
        show_init = True
        show_new_record = False
        show_normal_score = False
        while running:
            if show_init:
                close = self.draw_init()
            if close:
                lobby = Lobby()
                lobby.update()
                break
            show_init = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    lobby = Lobby()
                    lobby.update()
                    running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                        if self.snake.direction != 'left':
                            self.snake.move_right()
                    elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                        if self.snake.direction != 'right':
                            self.snake.move_left()
                    elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                        if self.snake.direction != 'up':
                            self.snake.move_down()
                    elif event.key == pygame.K_UP or event.key == pygame.K_w:
                        if self.snake.direction != 'down':
                            self.snake.move_up()

            self.all_drawing()
            time.sleep(0.2)
            if self.is_lose():
                self.dead_sound.play()
                if self.best_score < self.snake.length-1:
                    self.best_score = self.snake.length-1
                    show_new_record = True
                    if show_new_record:
                        close = self.draw_new_record()
                        if close:
                            lobby = Lobby()
                            lobby.update()
                            break
                        show_new_record = False
                elif self.snake.length-1 <= self.best_score:
                    show_normal_score = True
                    if show_normal_score:
                        close = self.draw_normal_score()
                        if close:
                            lobby = Lobby()
                            lobby.update()
                            break
                        show_normal_score = False
                self.game_reset()
                show_init = True

    def draw_init(self):
        self.screen.fill(GREEN)
        draw_text(self.screen, 'Snake Game', 50, self.width/2, self.height/4)
        draw_text(self.screen, '"Arrow" or "A, S, D, W" keys to control snake', 22, self.width/2, self.height/2)
        draw_text(self.screen, 'Your best Score is ' + str(self.best_score), 22, self.width/2, (self.height/2)+80)
        draw_text(self.screen, 'Press any key to start', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            time.sleep(0.2)
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_normal_score(self):
        self.screen.fill(GREEN)
        draw_text(self.screen, 'Your Current Score is ' + str(self.snake.length-1), 28, self.width/2, self.height/4)
        draw_text(self.screen, 'Press any key to return to main menu', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        waiting = True
        while waiting:
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def draw_new_record(self):
        self.screen.fill(GREEN)
        draw_text(self.screen, 'Congratulations!', 28, self.width/2, self.height/4)
        draw_text(self.screen, 'You have reached a new record! ' + str(self.best_score), 28, self.width/2, (self.height/4)+50)
        draw_text(self.screen, str(self.best_score), 64, self.width/2, self.height/2)
        draw_text(self.screen, 'Press any key to return to main menu', 18, self.width/2, self.height*3/4)
        pygame.display.update()
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("""UPDATE User_info SET
        ns_score = :ns_score
        WHERE oid = :oid""",
        {'ns_score': self.best_score,
        'oid': database.account_oid
        })
        conn.commit()
        conn.close()
        waiting = True
        while waiting:
            # Getting inputs
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return True
                elif event.type == pygame.KEYUP:
                    waiting = False
                    return False

    def is_lose(self):
        if self.snake.x[0] < 0 or self.snake.x[0] >= self.width or self.snake.y[0] < 0 or self.snake.y[0] >= self.height:
            return True
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.x[i], self.snake.y[0], self.snake.y[i]):
                return True
        return False

    def game_reset(self):
        self.snake = Snake(self.screen, 1)
        self.apple = Apple(self.screen)

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load(os.path.join("img", "block.jpg")).convert()
        self.x = [40]*length
        self.y = [40]*length
        self.direction = 'none'
    
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.parent_screen.fill((GREEN))
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.update()
    
    def move_right(self):
        self.direction = 'right'
    
    def move_left(self):
        self.direction = 'left'
    
    def move_down(self):
        self.direction = 'down'
    
    def move_up(self):
        self.direction = 'up'

    def walk(self):
        
        for i in range(self.length-1,0,-1):
            self.x[i] = self.x[i-1]
            self.y[i] = self.y[i-1]
        if self.direction == 'right':
            self.x[0] += 40
        if self.direction == 'left':
            self.x[0] += -40
        if self.direction == 'down':
            self.y[0] += 40
        if self.direction == 'up':
            self.y[0] += -40
        if self.direction == 'none':
            self.x[0] += 0
            self.y[0] += 0
        self.draw()

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load(os.path.join("img", "apple.jpg")).convert()
        self.parent_screen = parent_screen
        self.x = 40 * 3
        self.y = 40 * 3
    
    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.update()
    
    def move(self):
        num = 600/40
        self.x = random.randint(0, num-1)*40
        self.y = random.randint(0, num-1)*40

class Lobby:
    def __init__(self):
        self.width = 800
        self.height = 800
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Main Lobby")
        self.screen.fill(BLACK)
        self.clock = pygame.time.Clock()
        self.game1 = pygame.image.load(os.path.join("img", "game1.png")).convert()
        game1_img = pygame.transform.scale(self.game1, (200, 200))
        self.screen.blit(game1_img, (33,140))
        game2 = pygame.image.load(os.path.join("img", "game3.png")).convert()
        game2_img = pygame.transform.scale(game2, (200, 200))
        self.screen.blit(game2_img, (299,140))
        game3 = pygame.image.load(os.path.join("img", "game2.png")).convert()
        game3_img = pygame.transform.scale(game3, (200, 200))
        self.screen.blit(game3_img, (565,140))
        self.target1 = pygame.rect.Rect(33, 140, 200, 200)
        self.target3 = pygame.rect.Rect(299, 140, 200, 200)
        self.target2 = pygame.rect.Rect(565, 140, 200, 200)

    def top3(self):
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM User_info")
        infos = c.fetchall()
        par1_score = 0
        par1_username = ''
        par1_oid = None
        for info in infos:
            if par1_score <= info[2]:
                par1_score = info[2]
                par1_username = info[0]
                par1_oid = info[5]
        par2_score = 0
        par2_username = ''
        par2_oid = None
        for info in infos:
            if info[5] != par1_oid:
                if par2_score <= info[2]:
                    par2_score = info[2]
                    par2_username = info[0]
                    par2_oid = info[5]
        par3_score = 0
        par3_username = ''
        par3_oid = None
        for info in infos:
            if info[5] != par1_oid and info[5] != par2_oid:
                if par3_score <= info[2]:
                    par3_score = info[2]
                    par3_username = info[0]
                    par3_oid = info[5]
        mmc1_score = 999999
        mmc1_username = ''
        mmc1_oid = None
        for info in infos:
            if mmc1_score >= info[3]:
                mmc1_score = info[3]
                mmc1_username = info[0]
                mmc1_oid = info[5]
        mmc2_score = 999999
        mmc2_username = ''
        mmc2_oid = None
        for info in infos:
            if info[5] != mmc1_oid:
                if mmc2_score >= info[3]:
                    mmc2_score = info[3]
                    mmc2_username = info[0]
                    mmc2_oid = info[5]
        mmc3_score = 999999
        mmc3_username = ''
        mmc3_oid = None
        for info in infos:
            if info[5] != mmc1_oid and info[5] != mmc2_oid:
                if mmc3_score >= info[3]:
                    mmc3_score = info[3]
                    mmc3_username = info[0]
                    mmc3_oid = info[5]
        snake1_score = 0
        snake1_username = ''
        snake1_oid = None
        for info in infos:
            if snake1_score <= info[4]:
                snake1_score = info[4]
                snake1_username = info[0]
                snake1_oid = info[5]
        snake2_score = 0
        snake2_username = ''
        snake2_oid = None
        for info in infos:
            if info[5] != snake1_oid:
                if snake2_score <= info[4]:
                    snake2_score = info[4]
                    snake2_username = info[0]
                    snake2_oid = info[5]
        snake3_score = 0
        snake3_username = ''
        snake3_oid = None
        for info in infos:
            if info[5] != snake1_oid and info[5] != snake2_oid:
                if snake3_score <= info[4]:
                    snake3_score = info[4]
                    snake3_username = info[0]
                    snake3_oid = info[5]
        
        draw_text(self.screen, "1. " + par1_username + "---" + str(par1_score), 20, 133, 380)
        draw_text(self.screen, "2. " + par2_username + "---" + str(par2_score), 20, 133, 420)
        draw_text(self.screen, "3. " + par3_username + "---" + str(par3_score), 20, 133, 460)
        draw_text(self.screen, "1. " + mmc1_username + "---" + str(mmc1_score) + "secs", 20, 399, 380)
        draw_text(self.screen, "2. " + mmc2_username + "---" + str(mmc2_score) + "secs", 20, 399, 420)
        draw_text(self.screen, "3. " + mmc3_username + "---" + str(mmc3_score) + "secs", 20, 399, 460)
        draw_text(self.screen, "1. " + snake1_username + "---" + str(snake1_score), 20, 665, 380)
        draw_text(self.screen, "2. " + snake2_username + "---" + str(snake2_score), 20, 665, 420)
        draw_text(self.screen, "3. " + snake3_username + "---" + str(snake3_score), 20, 665, 460)
        conn.commit()
        conn.close()

    def update(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:            
                        if self.target1.collidepoint(event.pos):
                            par = PAR()
                            par.update()
                            pygame.quit()
                        if self.target2.collidepoint(event.pos):
                            game = Game()
                            game.update()
                            pygame.quit()
                        if self.target3.collidepoint(event.pos):
                            mmc = MMC()
                            mmc.update()
                            pygame.quit() 
            init_screen()
            conn = sqlite3.connect('User_info.db')
            c = conn.cursor()
            c.execute("SELECT * FROM User_info WHERE oid = " + database.account_oid)
            infos = c.fetchall()
            for info in infos:
                draw_text(self.screen, "Your Best Score:", 20, 400, 20)
                draw_text(self.screen, "Plane and Rock:",20, 133, 60)
                draw_text(self.screen, "Mouse MovingControl:", 20, 399, 60)
                draw_text(self.screen, "Snake:", 20, 665, 60)
                draw_text(self.screen, str(info[2]),20, 133, 100)
                draw_text(self.screen, str(info[3]) + " secs", 20, 399, 100)
                draw_text(self.screen, str(info[4]), 20, 665, 100)
            conn.commit()
            conn.close()
            self.top3()              
            pygame.display.flip()
            self.clock.tick(FPS)
        pygame.quit()

class Database:
    def __init__(self):
        self.root = Tk()
        self.root.title('User login')
        self.root.geometry('300x400')
        self.account_oid = None

    def log_reg_page(self):
        global username_entry, password_entry
        Label(text = "Login/Register", bg = "grey", width = "500", height = "2", font = ("Calibri", 13)).pack()
        Label(text = "").pack()
        Label(self.root, text = "Username: ").pack()
        username_entry = Entry(self.root, width=30)
        username_entry.pack()
        Label(text = "").pack()
        Label(self.root, text = "Password: ").pack()
        password_entry = Entry(self.root, width=30)
        password_entry.pack()
        Label(self.root, text = "").pack()
        Button(self.root, text = "Login", width = 10, height = 1, command=self.login).pack()
        Label(text = "").pack()
        Button(text = "Register", width = 10, height = 1, command=self.register).pack()
        Label(text = "").pack()
        Button(text = "Show information", width = 20, height = 1, command = self.show_data).pack()
        
    def register(self):
        global username_entry2, password_entry2, root2
        root2 = Toplevel(self.root)
        root2.title("Register")
        root2.geometry("300x400")
        Label(root2, text = "Register", bg = "grey", width = "500", height = "2", font = ("Calibri", 13)).pack()
        Label(root2, text = "").pack()
        Label(root2, text = "Username: ").pack()
        username_entry2 = Entry(root2, width=30)
        username_entry2.pack()
        Label(root2, text = "").pack()
        Label(root2, text = "Password: ").pack()
        password_entry2 = Entry(root2, width=30)
        password_entry2.pack()
        Label(root2, text = "").pack()
        Button(root2, text = "Register", width = 10, height = 1, command=self.register_user).pack()
        Label(root2, text = "").pack()

    def register_user(self):
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("INSERT INTO User_info VALUES (:username, :password, :par_score, :mmc_score, :ns_score)",
            {
                'username': username_entry2.get(),
                'password': password_entry2.get(),
                'par_score': 0,
                'mmc_score': 999999,
                'ns_score': 0
            })

        conn.commit()
        conn.close()
        username_entry2.delete(0, END)
        password_entry2.delete(0, END)

    def show_data(self):
        #Create database or connect to one
        conn = sqlite3.connect('User_info.db')

        #create cursor
        c = conn.cursor()
        c.execute("SELECT *, oid FROM User_info")
        #c.fetchone()
        infos = c.fetchall()

        #loop through results
        print_infos = ''
        for info in infos:#infos[0]
            print_infos += str(info)
        
        Label(self.root, text=print_infos).pack()

        conn.commit()
        conn.close()

    def login(self):
        username_verify = username_entry.get()
        password_verify = password_entry.get()
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()
        c.execute("SELECT *, oid FROM User_info")
        infos = c.fetchall()
        login_sucess = False
        for info in infos:
            if username_verify == info[0]:
                if password_verify == info[1]:
                    self.account_oid = str(info[5])
                    login_sucess = True
                    break
        if login_sucess == True:
            self.root.destroy()
            self.lobby = Lobby()
            self.lobby.update()

        else:
            Label(self.root, text="Username or password not correct").pack()

        conn.commit()
        conn.close()

    def update(self):
        conn = sqlite3.connect('User_info.db')
        c = conn.cursor()

        #create table
        '''c.execute("""CREATE TABLE User_info (
            username text, 
            password text,
            par_score integer,
            mmc_score integer,
            ns_score integer
            )""")'''

        self.log_reg_page()

        conn.commit()
        conn.close()
        self.root.mainloop()


if __name__ == '__main__':
    database = Database()
    database.update()