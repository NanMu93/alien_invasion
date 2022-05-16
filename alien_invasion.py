import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()

        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #        在全屏模式下运行
        #        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.died_aliens = pygame.sprite.Group()

        pygame.time.set_timer(self.settings.FIRE_EVENT, 200)
        pygame.time.set_timer(self.settings.ALIEN_CREATE_EVENT, 2000)
        pygame.time.set_timer(self.settings.ALIEN_MOVE_EVENT, 100)
        pygame.time.set_timer(self.settings.BURST_EVENT, 200)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()
            self.ship.update()
            self.bullets.update()

            # 删除消失的子弹
            for bullet in self.bullets.copy():
                if bullet.rect.bottom <= 0:
                    self.bullets.remove(bullet)
            #            print(len(self.bullets))

            for alien in self.aliens.copy():
                if alien.rect.bottom >= self.screen.get_height():
                    self.aliens.remove(alien)

            self._collide()
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""

        for event in pygame.event.get():
            key_press = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            elif key_press[pygame.K_SPACE] and event.type == self.settings.FIRE_EVENT:
                self._fire_bullet()
            if event.type == self.settings.BURST_EVENT:
                self.aliens.remove(self.died_aliens)
            if event.type == self.settings.ALIEN_CREATE_EVENT:
                self._create_alien()
            if self.aliens and event.type == self.settings.ALIEN_MOVE_EVENT:
                self.aliens.update(True)
            if event.type == pygame.KEYDOWN:
                self._check_keydown_event(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)

    def _check_keydown_event(self, event):
        if event.key == pygame.K_q:
            sys.exit()
        if event.key == pygame.K_RIGHT:
            # 向右移动飞船
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            # 向左移动飞船
            self.ship.moving_left = True
        if event.key == pygame.K_UP:
            # 向上移动飞船
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            # 向下移动飞船
            self.ship.moving_down = True

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        if event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _create_alien(self):
        new_alien = Alien(self)
        self.aliens.add(new_alien)

    def _burst(self, alien):
        alien.image = pygame.image.load("images/burst.bmp")

    def _collide(self):
        dict_alien_bullet = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        for alien_sprites in dict_alien_bullet.values():
            for alien_sprite in alien_sprites:
                alien_sprite.update(False)
                self.died_aliens = alien_sprite

    def _update_screen(self):
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.blitme()
        # 让最近绘制的屏幕可见
        pygame.display.flip()


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
