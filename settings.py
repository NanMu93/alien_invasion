import pygame


class Settings:
    """存储游戏中所有设置的类"""

    FIRE_EVENT = pygame.USEREVENT
    ALIEN_CREATE_EVENT = pygame.ACTIVEEVENT
    ALIEN_MOVE_EVENT = pygame.NUMEVENTS
    BURST_EVENT = pygame.NOEVENT

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)
        self.ship_speed = 1.0

        self.bullet_speed = 1.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        self.alien_x_speed = 10
        self.alien_y_speed = 5