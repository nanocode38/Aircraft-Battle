#!/usr/bin/env python3
# -*- codeing: utf-8
"""存储游戏单一图像类的模块"""
import pygame

import time


class GameOverImage:
    """Game Over图像类"""

    def __init__(self, screen) -> None:
        """初始化Game Over图像"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.hidden = True

        self.text_color = (255, 1, 0)
        self.font = pygame.font.SysFont(None, 200)
        a = 700

        self.image = self.font.render("Game Over!", True, self.text_color)
        self.rect = self.image.get_rect()
        self.rect.center = self.screen_rect.center
        self.rect.centery -= 120

    def draw(self):
        """画出Game Over"""
        if self.hidden:
            return
        self.screen.blit(self.image, self.rect)


class Boom:
    """爆炸图像"""

    def __init__(self, screen, ship) -> None:
        """初始化属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.ship = ship
        # 加载图像，并设置Rect值
        self.image = pygame.image.load("..\\resources\\images\\boom.png")
        self.rect = self.image.get_rect()

        self.is_hidden = True

        self.rect.center = ship.rect.center
        return

    def draw(self):
        """在对应位置画出爆炸"""
        self.rect.center = self.ship.rect.center
        if self.is_hidden:
            return
        self.screen.blit(self.image, self.rect)


class SoundButton:
    """控制背景音乐的按钮"""

    def __init__(self, screen, musicisplaying) -> None:
        """初始化属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        self.musicisplaying = musicisplaying
        self.image1 = pygame.image.load("..\\resources\\images\\musicbutton1.png")
        self.image2 = pygame.image.load("..\\resources\\images\\musicbutton2.png")
        self.rect = self.image1.get_rect()

        self.rect.top = self.screen_rect.top + 25
        self.rect.right = self.screen_rect.right - 100
        return

    def draw(self):
        """在指定位置画出按钮"""
        if self.musicisplaying:
            self.screen.blit(self.image1, self.rect)
        else:
            self.screen.blit(self.image2, self.rect)
