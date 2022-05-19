import pygame


class Settings:
    """存储游戏中所有设置的类"""

    FIRE_EVENT = pygame.USEREVENT
    ALIEN_CREATE_EVENT = pygame.ACTIVEEVENT
    ALIEN_MOVE_EVENT = pygame.NUMEVENTS
    BURST_EVENT = pygame.NOEVENT
    FPS = 60

    def __init__(self):
        """初始化游戏的设置"""
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        self.ship_speed = 10
        self.ship_limit = 3

        self.bullet_speed = 15
        self.bullet_width = 100
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        self.alien_x_speed = 10
        self.alien_y_speed = 5

        self.fire_event_time = 200
        self.alien_create_event_time = 1000
        self.alien_move_event_time = 50
        self.burst_event_time = 200
