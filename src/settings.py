#!/usr/bin/env python3
# -*- codeing: utf-8
""""含有游戏设置类的模块"""
import pygame


class Settings:
    """存储游戏所有设置的类。"""

    def __init__(self):
        """初始化游戏静态设置"""
        # 场景设置
        self.screen_width = 1290
        self.sceen_height = 660

        # 子弹设置。
        self.bullet_width = 2
        self.bullet_height = 15
        self.bullet_color = (200, 255, 200)

        # 声音设置
        self.gameoversound1 = pygame.mixer.Sound("..\\resources\\sounds\\GameOver1.wav")
        self.gameoversound2 = pygame.mixer.Sound("..\\resources\\sounds\\gameover2.wav")
        self.shiphitsound = pygame.mixer.Sound("..\\resources\\sounds\\crash.wav")
        self.bulletsound = pygame.mixer.Sound("..\\resources\\sounds\\bullet.wav")


        # 游戏速度增加速度
        self.speedup_scale = 1.1
        self.score_scale = 1.5

        # 帧率
        self.FPS = 60

        self.init_dynamic_settings()

    def init_dynamic_settings(self):
        """初始化随游戏进行而变化的量"""
        self.ship_speed_factor = 1.4
        self.plane_points = 10
        self.plane_allowed_speed_max = 280
        self.plane_allowed_speed_min = 60
        # 子弹发射速率
        self.bulletFiringRate = 35
        #!===========================================================!#
        self.bullet_speed_factor = {
            "easy":  3.0,
            "medium":2.8,
            "diff":  2.5,
            "sdiff": 2.1,
        }
        #!------------------------------------------------------------!#
        self.green_odds = {
            "easy":  6,
            "medium":3,
            "diff":  1,
            "sdiff": 0,
        }
        self.blue_odds = {
            "easy":  2,
            "medium":2,
            "diff":  2,
            "sdiff": 1,
        }
        self.puple_odds = {
            "easy":  1,
            "medium":2,
            "diff":  1,
            "sdiff": 1,
        }
        self.orange_odds = {
            "easy":  1,
            "medium":2,
            "diff":  3,
            "sdiff": 2,
        }
        self.red_odds = {
            "easy":  0,
            "medium":1,
            "diff":  3,
            "sdiff": 6,
        }
        #!-------------------------------------------------------------------------!#
        self.plane_speed_y = {
            "easy":  0.2,
            "medium":0.3,
            "diff":  0.4,
            "sdiff": 0.6,
        }

        self.plane_speed_x = {
            "easy":  1.3,
            "medium":1.5,
            "diff":  1.8,
            "sdiff": 2.1,
        }


        self.aircraft_creation_rate_max = {
            "easy":  130,
            "medium":110,
            "diff":  100,
            "sdiff": 90,
        }
        self.aircraft_creation_rate_min = {
            "easy":self.aircraft_creation_rate_max["easy"] - 50,
            "medium":self.aircraft_creation_rate_max["medium"] - 50,
            "diff":self.aircraft_creation_rate_max["diff"] - 50,
            "sdiff":self.aircraft_creation_rate_max["sdiff"] - 50,
        }
    
    def increase_speed(self):
        """提高游戏速度设置"""
        for key in self.plane_speed_x.keys():
            self.bullet_speed_factor[key] *= self.speedup_scale
            self.aircraft_creation_rate_max[key] = self.aircraft_creation_rate_max[key] - 5
            self.aircraft_creation_rate_min[key] = self.aircraft_creation_rate_min[key] - 5
            self.plane_speed_x[key] *= self.speedup_scale
        self.ship_speed_factor *= self.speedup_scale
        self.bulletFiringRate = int(self.bulletFiringRate / self.speedup_scale)
        self.plane_points *= self.score_scale
        self.plane_allowed_speed_max += 5
        self.plane_allowed_speed_max += 5
