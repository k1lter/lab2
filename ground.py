import pygame
import random
import math
import shelve

class Ground():
    def __init__(self, screen):
        self.screen = screen
        self.ground = pygame.image.load('Images/Ground.png')
        self.ground = pygame.transform.scale(self.ground, (1200, 50))
        self.fuel_image = pygame.image.load('Images/fuel.png')
        self.fuel_image = pygame.transform.scale(self.fuel_image, (75,75))
        self.fuel_rect = self.fuel_image.get_rect()
        self.comets_image = pygame.image.load('Images/comets.png')
        self.comets_image = pygame.transform.scale(self.comets_image, (200,75))
        self.comets_rect = self.comets_image.get_rect()
        self.ground_rect = self.ground.get_rect()
        self.screen_rect = screen.get_rect()
        self.ground_rect.centerx = self.screen_rect.centerx
        self.ground_rect.bottom = self.screen_rect.bottom
        self.comets = []
        self.fuels = []
        self.dead = False
        self.falling = False
        self.just_off = False
        self.score = 0
        self.font_name = pygame.font.match_font('arial')
        self.x = 0

        pygame.mixer.music.load('Sounds/Engine.mp3')
        pygame.mixer.music.set_volume(1)
    
    def create_fuel(self, fuels, screen):
        if len(self.fuels) == 0 or fuels[len(fuels) - 1].centery > 500:
            self.fuels.append(pygame.Rect(random.randint(0,1000), -100, 50, 50))
        for fuel in fuels:
            self.screen.blit(self.fuel_image, fuel)

    def change_pos_fuel(self, fuels, rocket):
        for fuel in fuels:
            fuel.centery += rocket.v_speed * 0.5

    def check_touch_fuel(self, fuels, rocket):
        for fuel in fuels:
            if rocket.rotated_rect.centery - 50 < fuel.centery + 15 and rocket.rotated_rect.centery - 50 > fuel.centery - 15 and (rocket.rotated_rect.centerx > fuel.centerx - 25 and rocket.rotated_rect.centerx < fuel.centerx + 25):
                fuels.remove(fuel)
                return True

    def create_comets(self, comets, screen):
        if len(comets) == 0 or comets[len(comets) - 1].centery > 500:
            comets.append(pygame.Rect(random.randint(0,1000),-100, 200, 30))
        for comet in comets:
            self.screen.blit(self.comets_image, comet)
    def change_pos_comets(self, comets, rocket):
        for comet in comets:
            comet.centery += rocket.v_speed * 0.5
    def check_touch(self, comets, rocket):
        for comet in comets:
            if rocket.rotated_rect.centery - 50 < comet.centery + 15 and rocket.rotated_rect.centery - 50 > comet.centery - 15 and (rocket.rotated_rect.centerx > comet.centerx - 100 and rocket.rotated_rect.centerx < comet.centerx + 100):
                print("--------------")
                print("Death")
                print("Your score: ", self.score)
                return True

    def update_ground(self, rocket, bg):
        self.screen.blit(bg, (0, 0), ( 0, self.x % 800, 1200, 800))
        self.x+= -rocket.v_speed/20
        #Изменение состояния объекта Ground. Положение, скорость и т.д. 
  
        #Стартовый переход ближе к центру экрана
        if rocket.hight > 1000:
            self.score += 1
            self.create_comets(self.comets, self.screen)
            self.create_fuel(self.fuels, self.screen)
            self.change_pos_comets(self.comets, rocket)
            self.change_pos_fuel(self.fuels, rocket)
            if self.check_touch(self.comets, rocket):
                self.dead = True
                pygame.mixer.music.stop()
            if self.check_touch_fuel(self.fuels, rocket):
                if rocket.fuelMass < 2000:
                    rocket.fuelMass += 200
        
        font = pygame.font.Font(self.font_name, 50)
        text_surface = font.render('Score:' + str(self.score), True, (255,255,255))
        text_rect = text_surface.get_rect()
        self.screen.blit(text_surface, (900,20))
        ####### Проверка на нахождение в рамках экрана
        if rocket.rotated_rect.centerx > 50 and rocket.rotated_rect.centerx < 1200:
            if rocket.v_speed > 0:
                rocket.rotated_rect.centerx += rocket.h_speed
        elif rocket.rotated_rect.centerx <= 50:
            rocket.rotated_rect.centerx = 51
        elif rocket.rotated_rect.centerx >= 1200:
            rocket.rotated_rect.centerx = 1199
        #######

        #В случае работы двигателя
        if rocket.trust:
            if rocket.alreadyStart == False:
                pygame.mixer.music.play(-1)
            rocket.alreadyStart = True
            if rocket.speed < rocket.TWR + rocket.a: #Рассчет нарастания скорости
                if rocket.rotated_rect.centery > self.screen_rect.bottom - 200:
                    rocket.rotated_rect.centery -= 0.5
                rocket.speed += rocket.a/4
                rocket.v_speed = rocket.speed * math.cos(rocket.angle*math.pi/180)
                rocket.h_speed = rocket.speed * math.sin(-rocket.angle*math.pi/180)
            else:
                #Рассчет скорости с учетом ускорения и изменения TWR
                rocket.speed = rocket.TWR + rocket.a
                rocket.v_speed = rocket.speed * math.cos(rocket.angle*math.pi/180)
                rocket.h_speed = rocket.speed * math.sin(-rocket.angle*math.pi/180)
            self.ground_rect.centery += rocket.speed * 5

            rocket.hight += rocket.v_speed * 5
            if rocket.fuelMass > 0:
                rocket.fuelMass -= 0.5
            else:
                rocket.trust = False

        #В случае если двигатель отключен
        elif rocket.trust == False and rocket.alreadyStart == True and self.falling == False:
            if self.just_off == False:
                rocket.image = pygame.image.load('Images/rocket_engoff.png')
                rocket.image = pygame.transform.scale(rocket.image, (200,200))
                rocket.rotated_image = rocket.image
            self.just_off = True
            rocket.speed -= rocket.g * 0.005
            rocket.v_speed = rocket.speed * math.cos(rocket.angle*math.pi/180)
            rocket.h_speed = rocket.speed * math.sin(-rocket.angle*math.pi/180)
            self.ground_rect.centery += rocket.speed
            rocket.hight += rocket.v_speed
            pygame.mixer.music.stop()
            self.alreadyStart = False
            if rocket.v_speed < 0:
                self.falling = True

        #В случае если ракета начала падать
        elif self.falling == True:
            if rocket.rotated_rect.centery < 800:
                rocket.rotated_rect.centery -= rocket.v_speed
                rocket.speed -= rocket.g * 0.005
                rocket.v_speed = rocket.speed * math.cos(rocket.angle*math.pi/180)
                rocket.h_speed = rocket.speed * math.sin(-rocket.angle*math.pi/180)
            else:
                print("--------------")
                print("Death")
                print("Your score: ", self.score)
                db = shelve.open('db')
                db['score'] = self.score
                db.close()
                self.dead = True

    def output(self):
        #Вывод объекта на экран
        self.screen.blit(self.ground, self.ground_rect)