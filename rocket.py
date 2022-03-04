import pygame

class Rocket():
    def __init__(self, screen):
        #Инициализация объекта Rocket
        self.screen = screen
        self.image = pygame.image.load('Images/rocket.png')
        self.image = pygame.transform.scale(self.image, (200,200))
        self.bg = pygame.image.load('Images/BackGround.png')
        self.bg = pygame.transform.scale(self.bg, (1200,3200))
        self.bg_rect = self.bg.get_rect()
        self.bg_pos = 0
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.rect.centerx = self.screen_rect.centerx
        self.rect.centery = self.screen_rect.bottom - 100
        self.tleft = False
        self.tright = False
        self.trust = False
        self.pause = False
        self.alreadyStart = False
        self.rotated_image = self.image
        self.rotated_rect = self.rect
        self.angle = 0

        #Ускорение свободного падения в условиях Земли
        self.g = 9.86

        #Ускорение аппарата
        self.a = 0.1

        #Скорость ракеты
        self.speed = 0
        self.v_speed = 0
        self.h_speed = 0

        #Высота полета в Метрах
        self.hight = 0

        #Сухая масса ракеты в Кг
        self.dryMass = 500

        #Масса топлива в Кг
        self.fuelMass = 200

        #Тяга двигателя в кН
        self.enginePower = 250

        #Тяговооруженность ракеты (ТВР)
        self.TWR = 0

    def bg_update(self, screen):
        self.bg_rect.centery += self.v_speed/10

    def update_rocket(self):
        #Изменение состояния объекта Rocket. Положение, поворот, скорость и т.д.

        #Расчет тяговооруженности ракеты
        self.TWR = (self.enginePower*1000)/((self.dryMass+self.fuelMass)*self.g)

        if self.hight:
            if self.tleft and self.angle < 50:
                self.angle += 0.5
                self.rotated_image, self.rotated_rect = self.rotate(self.image, self.angle)
            elif self.tright and self.angle > -50:
                self.angle -= 0.5
                self.rotated_image, self.rotated_rect = self.rotate(self.image, self.angle)

    def rotate(self, surface, angle):
        #Изменение поворота объекта Rocket
        rotated_image = pygame.transform.rotozoom(surface, angle, 1)
        rotated_rect = rotated_image.get_rect(center = (self.rotated_rect.centerx, self.rotated_rect.centery))
        return rotated_image, rotated_rect

    def output(self):
        #Вывод объекта на экран
        self.screen.blit(self.rotated_image, self.rotated_rect)

    def output_bg(self):
        self.screen.blit(self.bg,self.bg_rect)
