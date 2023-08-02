#!/usr/bin/env python3
# -*- codeing: utf-8
"""存储记分牌类的模块"""
import pygame.font


class Scoreboard:
    """显示游戏得分信息的类"""

    def __init__(self, settings, screen, stats) -> None:
        """初始化记分牌属性"""
        self.screen = screen
        self.screen_rect = screen.get_rect()
        self.settings = settings
        self.stats = stats

        # 显示得分时所用的字体
        self.text_color = (230, 230, 200)
        self.font = pygame.font.SysFont(None, 48)

        # 准备初始得分图像
        self.prep_score()
        self.prep_high_score()

    def prep_score(self):
        """将得分渲染为一幅图像"""
        round_score = int(round(self.stats.score, -1))
        score_str = "Score:" + "{:,}".format(round_score)
        self.score_image = self.font.render(score_str, True, self.text_color)

        # 将得分放于屏幕左上角
        self.score_rect = self.score_image.get_rect()
        self.score_rect.left = self.screen_rect.left + 20
        self.score_rect.top = 20

    def prep_high_score(self):
        """将最高得分渲染为一幅图像"""
        self.stats.high_score = int(round(self.stats.high_score, -1))
        score_str = "High Score:" + "{:,}".format(self.stats.high_score)
        self.high_score_image = self.font.render(
            score_str, True, self.text_color
        )

        # 将得分放于屏幕左上角
        self.high_score_rect = self.high_score_image.get_rect()
        self.high_score_rect.left = self.score_rect.left
        self.high_score_rect.top = self.score_rect.bottom + 10

    def show_score(self):
        """在屏幕上显示得分"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.high_score_image, self.high_score_rect)
