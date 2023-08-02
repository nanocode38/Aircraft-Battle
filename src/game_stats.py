#!/usr/bin/env python3
# -*- codeing: utf-8
"""放置游戏统计信息跟踪类的模块"""
import pickle


class GameStats(object):
    """跟踪游戏统计信息"""

    def __init__(self, settings) -> None:
        """初始化统计信息"""
        self.settings = settings
        with open("..\\score.dat", "rb") as f:
            self.high_score = pickle.load(f)
        self.is_gameover = True
        self.reset_score()

    def reset_score(self):
        """初始化在游戏运行期间可能变化的统计信息"""
        self.score = 0
