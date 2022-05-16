import pygame.image
from pygame.sprite import Sprite
import random


class Alien(Sprite):
    """外星人管理类"""

    def __init__(self, ai_game):
        """初始化外星人"""

        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.moving = bool(random.randrange(0, 2, 1))

        # 加载外星人图像并设置其rect属性
        self.image = pygame.image.load("images/alien.bmp")
        self.rect = self.image.get_rect()

        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 每个外星人最初都在屏幕左上角附近
        self.x = random.randrange(0, self.settings.screen_width-self.image.get_width(), self.image.get_width())
        self.y = 0

        self.rect.x = self.x
        self.rect.y = self.y

    def update(self, alive):
        if not alive:
            width = self.rect.width
            height = self.rect.height
            self.image = pygame.image.load("images/burst.bmp")
            self.image = pygame.transform.smoothscale(self.image, (width, height))
        if self.moving:
            if self.x >= self.settings.screen_width-self.image.get_width():
                self.moving = False
            self.x += self.settings.alien_x_speed
        if not self.moving:
            if self.rect.x <= 0:
                self.moving = True
            self.x -= self.settings.alien_x_speed
        self.y += self.settings.alien_y_speed

        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        self.screen.blit(self.image, self.rect)
