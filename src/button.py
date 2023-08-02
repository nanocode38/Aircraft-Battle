#!/usr/bin/env python3
# -*- codeing: utf-8
"""存储Button类的模块"""

import pygame.font


class Button:
    """存储按钮的类"""

    def __init__(self, screen, msg, y, color, typeface="SimHei") -> None:
        """初始化按钮属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()

        # 设置按钮尺寸及其他属性
        self.width, self.height = 200, 50
        self.button_color = color
        self.text_color = (255, 255, 255)
        self.font = pygame.font.SysFont(typeface, 40)

        # 设置按钮rect属性，并使其居中
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.center = self.screen_rect.center
        self.rect.centery += y

        # 按钮标签创建
        self.prep_msg(msg)

    def prep_msg(self, msg):
        """将文字渲染为图像，并使其在按钮上居中"""
        self.msg_image = self.font.render(
            msg, True, self.text_color)
        self.msg_image_rect = self.msg_image.get_rect()
        self.msg_image_rect.center = self.rect.center

    def draw(self):
        """绘制一个用颜色填充的按钮，再绘制文本"""
        self.screen.fill(self.button_color, self.rect)
        self.screen.blit(self.msg_image, self.msg_image_rect)
        return
