#!/usr/bin/env python3
# -*- codeing: utf-8
"""存储敌机Plane类"""
from pygame.sprite import Sprite
from pygame import image
import random as rd


class Plane(Sprite):
    """表示单个敌机的类"""

    def __init__(self, settings, screen, ship, mode):
        """初始化数据"""
        super(Plane, self).__init__()
        self.life = rd.randint(1, 10)
        self.ship = ship
        orange = settings.orange_odds[mode] + settings.red_odds[mode]
        puple = orange + settings.puple_odds[mode]
        blue = puple + settings.blue_odds[mode]
        green = blue + settings.green_odds[mode]
        if self.life >= 1 and self.life <= settings.red_odds[mode]:
            self.image = image.load("..\\resources\\images\\plane5.png")
            self.life = 5
        elif self.life > settings.red_odds[mode] and self.life <= orange:
            self.image = image.load("..\\resources\\images\\plane4.png")
            self.life = 4
        elif self.life > orange and self.life <= puple:
            self.image = image.load("..\\resources\\images\\plane3.png")
            self.life = 3
        elif self.life > puple and self.life <= blue:
            self.image = image.load("..\\resources\\images\\plane2.png")
            self.life = 2
        elif self.life > blue and self.life <= green:
            self.image = image.load("..\\resources\\images\\plane1.png")
            self.life = 1
        self.rect = self.image.get_rect()
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.speed_factor = settings.plane_speed_x[mode]
        self.speed_factor_y = settings.plane_speed_y[mode]
        self.rect.y = rd.randint(50, settings.screen_height - 50)
        self.rect.right = self.screen_rect.left
        self.x = self.rect.x
        self.y = self.rect.y

    def update(self):
        """更新敌机位置"""
        self.x += self.speed_factor
        self.rect.x = self.x
        if self.rect.bottom <= self.ship.center - 3:
            self.y += self.speed_factor_y
        elif self.rect.top >= self.ship.center + 3:
            self.y -= self.speed_factor_y
        if self.life == 5:
            self.image = image.load("..\\resources\\images\\plane5.png")
        elif self.life == 4:
            self.image = image.load("..\\resources\\images\\plane4.png")
        elif self.life == 3:
            self.image = image.load("..\\resources\\images\\plane3.png")
        elif self.life == 2:
            self.image = image.load("..\\resources\\images\\plane2.png")
        elif self.life == 1:
            self.image = image.load("..\\resources\\images\\plane1.png")
        self.rect.y = self.y

    def blitme(self):
        """在指定位置绘制敌机"""
        self.screen.blit(self.image, self.rect)
