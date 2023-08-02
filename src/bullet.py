#!/usr/bin/env python3
# -*- codeing: utf-8
"""管理飞船子弹的模块"""
import pygame
from pygame.sprite import Sprite


class Bullet(Sprite):
    """管理飞船子弹的一个类"""

    def __init__(self, settings, screen, ship, mode):
        """在船的当前位置,创建一个子弹对象"""
        super(Bullet, self).__init__()
        self.screen = screen

        # 先在(0,0)创建子弹矩形,然后设置正确的位置
        self.rect = pygame.Rect(
            0, 0, settings.bullet_height, settings.bullet_width
        )
        self.rect.centery = ship.rect.centery
        self.rect.right = ship.rect.left

        # 存储一个小数值子弹的位置
        self.x = float(self.rect.x)

        self.color = settings.bullet_color
        self.speed_factor = settings.bullet_speed_factor[mode]

    def update(self):
        """更新子弹在屏幕上的移动"""
        # 子弹的小数点位置更新
        self.x -= self.speed_factor
        # 矩形的位置更新
        self.rect.x = self.x

    def draw_bullet(self):
        """在屏幕上绘制子弹"""
        pygame.draw.rect(self.screen, self.color, self.rect)
