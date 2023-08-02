#!/usr/bin/env python3
# -*- codeing: utf-8
"""含有飞船类的模块"""
import pygame
from pygame.sprite import Sprite


class Ship(Sprite):
    def __init__(self, settings, screen):
        """初始化飞船，并设置它的起始位置。"""
        super(Ship, self).__init__()
        self.screen = screen
        self.settings = settings

        # 加载飞船的图像，并获得它的外接矩形。
        self.image = pygame.image.load("..\\resources\\images\\ship.bmp")
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()
        self.image.set_colorkey((230, 230, 230))
        self.image = self.image.convert()
        self.image = self.image.convert_alpha()
        self.is_hidden = False

        # 在屏幕底部中央启动每艘飞船。
        self.rect.centery = self.screen_rect.centery
        self.rect.right = self.screen_rect.right

        # 为船的中心存储一个实数值。
        self.center = float(self.rect.centery)

        # 旗帜。
        self.moving_up = False
        self.moving_down = False

    def center_ship(self):
        """将船置于屏幕中央。"""
        # 在屏幕底部中央启动每艘飞船。
        self.center = self.screen_rect.centery
        self.rect.right = self.screen_rect.right

    def update(self):
        """根据移动旗帜更新飞船的位置。"""
        # 更新船的中心值，而不是矩形。
        if self.moving_up and self.rect.top > self.screen_rect.top:
            self.center -= self.settings.ship_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.center += self.settings.ship_speed_factor
        # 从self.center更新rect对象。
        self.rect.centery = self.center

    def blitme(self):
        """在屏幕上绘制飞船"""
        if self.is_hidden:
            return
        self.screen.blit(self.image, self.rect)
