#!/usr/bin/env python3
# -*- codeing: utf-8
import os
import random
import sys
from time import sleep
from tkinter import Tk
import tkinter
import random as rd
import pickle

import pygame
from pyhelper import RGBColor as Color
from pyhelper.pgwidgets import TextButton as Button
from pyhelper.pgwidgets import TextButtonConfig as ButtonConfig
from pyhelper.pghelper import BackgroundSound
from pyhelper.TKhelper import tkmessagebox
from pyhelper.gamehelper import Timer

from settings import Settings
from ship import Ship
from bullet import Bullet
from plane import Plane
from game_stats import GameStats
from images import GameOverImage, Boom, SoundButton
from scoreboard import Scoreboard


class Game:
    """管理资产和行为的游戏整体类"""

    def __init__(self):
        """初始化游戏,创建游戏资源"""
        os.system("cls")
        pygame.init()
        pygame.mixer.init()
        self.settings = Settings()

        self._game_over_time = False
        self._next_time = 0
        self.is_one_game_over = True
        self.music_is_playing_back = True

        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height
        self.screen_rect = self.screen.get_rect()
        pygame.display.set_caption("飞机大战")
        icon = pygame.image.load("..\\resources\\images\\Logo.png")
        pygame.display.set_icon(icon)

        self.main_clock = pygame.time.Clock()
        button_config = ButtonConfig(self.screen)
        button_config.set_config('width', 200)
        button_config.set_config('height', 50)
        # 字体对照
        # 新细明体：PMingLiU
        # 细明体：MingLiU
        # 标楷体：DFKai - SB
        # 黑体：SimHei
        # 宋体：SimSun
        # 新宋体：NSimSun
        # 仿宋：FangSong
        # 楷体：KaiTi
        # 仿宋：GB2312：FangSong_GB2312
        # 楷体：GB2312：KaiTi_GB2312
        # 微软正黑体：Microsoft JhengHei
        # 微软雅黑体：Microsoft YaHei
        button_config.font = 'KaiTi'
        button_config.button_color = [Color.LineGreen, ]
        button_config.text = '简单模式'
        easy_button = Button(button_config)
        easy_button.rect.center = self.screen_rect.center
        easy_button.rect.y += -90

        button_config.button_color = [Color.Blue, ]
        button_config.text = '普通模式'
        med_button = Button(button_config)
        med_button.rect.center = self.screen_rect.center
        med_button.rect.y += -30

        button_config.button_color = [(255, 255, 0), ]
        button_config.text = '困难模式'
        diff_button = Button(button_config)
        diff_button.rect.center = self.screen_rect.center
        diff_button.rect.y += +30

        button_config.button_color = [Color.Red, ]
        button_config.text = '地狱模式'
        hell_button = Button(button_config)
        hell_button.rect.center = self.screen_rect.center
        hell_button.rect.y += +90


        self.play_buttons = {
            "easy": easy_button,
            "medium": med_button,
            "diff": diff_button,
            "sdiff": hell_button,
        }
        self.mode = "easy"
        self.timer = Timer()
        self.ship = Ship(self.settings, self.screen)
        self.boom = Boom(self.screen, self.ship)
        self.planes = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.stats = GameStats(self.settings)
        self.sb = Scoreboard(self.settings, self.screen, self.stats)
        self.game_over_text = GameOverImage(self.screen)
        button_config.button_color = [(100, 233, 255),]
        button_config.text = 'Help'
        button_config.font = 'Console'
        self.help_button = Button(button_config)
        self.help_button.rect.centerx = self.screen_rect.centery
        self.help_button.rect.bottom = self.screen_rect.bottom - 18
        self.music_is_playing = True
        self.music_button = SoundButton(self.screen, self.music_is_playing)
        self.music = BackgroundSound("..\\resources\\sounds\\background.mid")
        self.music.play()

    def run_game(self):
        """开始游戏主循环"""
        starts_point = [(10, 10), (50, 50)]
        len_starts = self.settings.screen_width * self.settings.screen_height // 400 - 10
        for i in range(len_starts):
            rect = (
                random.randint(10, self.settings.screen_width - 10),
                random.randint(5, self.settings.screen_height - 5))
            starts_point.append(rect)
        self.timer.start()


        while True:
            if not self._game_over_time:
                self._draw_screen(len_starts, starts_point)
            self._check_events()
            if not self.stats.is_gameover:
                self.ship.update()
                self._add_planes()
                self._update_planes()
                self._update_bullets()
            if not self._game_over_time:
                self._update_screen()
            self._check_anythins()
            self.main_clock.tick(self.settings.FPS)


    def _get_time(self):
        return round(self.timer.get_time(10) * self.settings.FPS, 0)

    def _draw_screen(self, len_starts, starts_point):
        starts = pygame.image.load(
            "..\\resources\\images\\sceen.bmp"
        ).convert()



        self.screen.fill(Color.Black)
        for i in range(len_starts):
            self.screen.blit(starts, starts_point[i])

    def _exit(self):
        """退出游戏"""
        sl = tkmessagebox('askyesno', '退出确认', '真的要退出游戏吗?')
        if sl == 1:
            with open("score.dat", "wb") as f:
                pickle.dump(self.stats.high_score, f)
            sys.exit(0)

    #!事件！
    #!事件！
    #!事件！
    #!事件！
    def _check_events(self):
        """响应按键和鼠标事件"""
        for event in pygame.event.get():
            self._check_play_button(event)
            self._check_help_button(event)
            if event.type == pygame.QUIT:
                self._exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            if event.type == pygame.MOUSEBUTTONUP:
                self._check_music_button_button(*event.pos)

    def _check_keydown_events(self, event):
        """响应按键"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == 27:  # ESC
            self._exit()
        if event.key == pygame.K_SPACE:
            if self.music_is_playing:
                self.music.stop()
            else:
                self.music.play()
            self.music_is_playing = not self.music_is_playing

    def _check_keyup_events(self, event):
        """相应松开按键"""
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _check_play_button(self, event):
        """检查是否点击Play按钮并作出响应"""
        if self._game_over_time:
            return
        if not self.stats.is_gameover:
            return
        if self.play_buttons["easy"].update(event):
            self.mode = "easy"
        elif self.play_buttons["medium"].update(event):
            self.mode = "medium"
        elif self.play_buttons["diff"].update(event):
            self.mode = "diff"
        elif self.play_buttons["sdiff"].update(event):
            self.mode = "sdiff"
        else:
            return

        # 重置游戏统计信息
        self.ship.is_hidden = False
        self.boom.is_hidden = True
        self.stats.reset_score()
        self.stats.is_gameover = False

        # 更新记分牌图像
        self.sb.prep_score()

        # 清空敌机列表与子弹列表
        self.bullets.empty()
        self.planes.empty()
        # 使Game Over处于不可见状态，并居中飞船
        self.game_over_text.hidden = True
        self.ship.center_ship()
        # 重置游戏速度设置
        self.settings.init_dynamic_settings()
 
    def _check_help_button(self, event):
        """检查是否点击Help按钮并作出响应"""
        if not self.help_button.update(event):
            return
        if not self.stats.is_gameover:
            return
        help_text = "飞机大战游戏帮助：\n"
        help_text += "1.用上下方向键操控屏幕右侧飞机，躲避或击杀敌机。\n"
        help_text += "2.红色敌机要打五枪才能完全消灭，后面依次类推，强到弱顺序：红、橙、紫、蓝、绿\n"
        help_text += "3.敌机会跟踪我方飞船，并保证不被子弹射中。\n"
        help_text += "4.敌机速度将随时间流逝越来越快。\n"
        help_text += "5.每击中一枪就加分，每枪分数、飞船速度和子弹速度也会随时间加快。\n"
        help_text += "6.按空格键开启或关闭背景音乐。\n"

        tk = Tk()
        tk.title("Game Help")
        tk.resizable(0, 0)
        tk.wm_attributes("-topmost", 1)
        canvas = tkinter.Canvas(tk, width=700, height=500, bd=0, highlightthickness=0)
        canvas.pack()
        canvas.create_text(250, 70, text=help_text, fill="blue")
        tk.update_idletasks()
        tk.update()

        def on_close_window():
            tk.destroy()

        tk.protocol("WM_DELETE_WINDOW", on_close_window)
        tk.mainloop()

    def _check_music_button_button(self, mouse_x, mouse_y):
        """响应按下music_button"""
        if not self.music_button.rect.collidepoint(mouse_x, mouse_y):
            return
        if self.music_is_playing:
            self.music.stop()
        else:
            self.music.play()
        self.music_is_playing = not self.music_is_playing

    def _check_bullet_plane_collisions(self):
        """对子弹-敌机碰撞做出反应"""
        # 移除所有碰撞过的子弹和外星人.

        collisions = pygame.sprite.groupcollide(self.bullets, self.planes, True, False)

        if collisions:
            for planes in collisions.values():
                for plane in planes:
                    self.settings.bulletsound.play()
                    if plane.life <= 1:
                        self.stats.score += self.settings.plane_points * len(planes)
                        self.sb.prep_score()
                        self.planes.remove(plane)
                    else:
                        plane.life -= 1
                        plane.update()
                        plane.blitme()
                check_high_score(self.stats, self.sb)

    #!子弹
    #!子弹
    #!子弹
    #!子弹
    def _automatic_firing(self):
        """⏲计时并自动发射子弹"""
        if self._get_time() % self.settings.bulletFiringRate == 0:
            new_bullet = Bullet(
                self.settings, self.screen, self.ship, self.mode
            )
            self.bullets.add(new_bullet)

    #!敌机
    #!敌机
    #!敌机
    #!--------------------------------------------------------------------------------------!#

    def _add_planes(self):
        """⏲计时并自动创建敌机"""
        if (
            self._get_time() % rd.randint(
                self.settings.aircraft_creation_rate_min[self.mode],
                self.settings.aircraft_creation_rate_max[self.mode],)== 0):
            new_plane = Plane(
                self.settings, self.screen, self.ship, self.mode
            )
            self.planes.add(new_plane)

    #!飞船
    #!飞船
    #!飞船
    #!飞船
    #!-------------------------------------------------------------------------------------!#
    def _game_over(self):
        """响应游戏结束"""
        self.stats.is_gameover = True
        self.settings.shiphitsound.play()
        self.music_is_playing_back = False
        if self.music_is_playing:
            self.music.stop()
            self.music_is_playing_back = True
        self.ship.is_hidden = True
        self.boom.is_hidden = False
        self.boom.draw()
        for bul in self.bullets:
            bul.draw_bullet()
        self.sb.show_score()
        pygame.display.flip()
        self._game_over_time = True
        self._next_time = self._get_time() + 8 * self.settings.FPS
    #!更新
    #!更新
    #!更新
    #!更新
    def _update_planes(self):
        """更新敌机位置并清除不需要的敌机"""
        for plane in self.planes.sprites():
            plane.update()
            plane.blitme()

        for plane in self.planes.copy().sprites():
            if plane.rect.top >= self.settings.screen_height:
                self.planes.remove(plane)
            if pygame.sprite.spritecollideany(self.ship, self.planes):
                if self.stats.is_gameover:
                    return
                self._game_over()
            for plane in self.planes:
                if plane.rect.left == self.screen_rect.right:
                    self.planes.remove(plane)


    def _update_bullets(self):
        """更新子弹位置,清除旧子弹"""
        self.bullets.update()
        self._check_bullet_plane_collisions()
        # 处理掉已经消失的子弹
        # 更新子弹位置
        for bullet in self.bullets.copy():
            if bullet.rect.left <= 0:
                self.bullets.remove(bullet)

    def _update_screen(self):
        """使最近绘制的屏幕可见"""
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        self._automatic_firing()
        self.ship.blitme()
        self.boom.draw()
        for plane in self.planes:
            plane.blitme()
        # 显示得分
        self.sb.show_score()
        self.game_over_text.draw()
        if self.stats.is_gameover:
            if not self._game_over_time:
                for key in self.play_buttons.keys():
                    self.play_buttons[key].draw()
                self.help_button.draw()
        self.music_button.draw()
        pygame.display.flip()

    def _check_anythins(self):
        """每次循环都要检查的事项"""
        self.timer.update()
        self.music_button.musicisplaying = self.music_is_playing
        if self._get_time() % (20 * 100) == 0:
            self.settings.increase_speed()
        if self._game_over_time and self._get_time() >= self._next_time:
            if self.is_one_game_over:
                print("as")
                self._next_time += 3 * 60
                self.settings.gameoversound1.play()
                self.settings.gameoversound2.play()
                self.game_over_text.hidden = False
                self.game_over_text.draw()
                self.sb.prep_high_score()
                self.sb.prep_score()
                self.is_one_game_over = False
                pygame.display.update()
            else:
                self._game_over_time = False
                if self.music_is_playing_back:
                    self.music.play()
                self.is_one_game_over = True



def check_high_score(stats, sb):
    """检查是否诞生了最高得分"""

    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


if __name__ == "__main__":
    # 创建一个游戏实例，并运行游戏.
    si = Game()
    si.run_game()