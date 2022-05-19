import sys
import pygame
from settings import Settings
from ship import Ship
from bullet import Bullet
from alien import Alien
from game_stats import GameStats
from time import sleep
from button import Button


class AlienInvasion:
    """管理游戏资源和行为的类"""

    def __init__(self):
        """初始化游戏并创建游戏资源"""
        pygame.init()
        self.settings = Settings()
        self.stats = GameStats(self)
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        #        在全屏模式下运行
        #        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        self.settings.screen_width = self.screen.get_rect().width
        self.settings.screen_height = self.screen.get_rect().height

        pygame.display.set_caption("Alien Invasion")

        self.play_button = Button(self, "Play")

        self.ship = Ship(self)
        self.bullets = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.died_aliens = pygame.sprite.Group()

        pygame.time.set_timer(self.settings.FIRE_EVENT, self.settings.fire_event_time)
        pygame.time.set_timer(self.settings.ALIEN_CREATE_EVENT, self.settings.alien_create_event_time)
        pygame.time.set_timer(self.settings.ALIEN_MOVE_EVENT, self.settings.alien_move_event_time)
        pygame.time.set_timer(self.settings.BURST_EVENT, self.settings.burst_event_time)

    def run_game(self):
        """开始游戏的主循环"""
        while True:
            # 监视键盘和鼠标事件
            self._check_events()
            if self.stats.game_active:
                self.ship.update()
                self.bullets.update()

            # 删除消失的元素
            self._check_disappear_element()

            self._collide()
            self.clock.tick(self.settings.FPS)
            self._update_screen()

    def _check_events(self):
        """响应按键和鼠标事件"""

        for event in pygame.event.get():
            key_press = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)
            elif self.stats.game_active and key_press[pygame.K_SPACE] and event.type == self.settings.FIRE_EVENT:
                self._fire_bullet()
            if event.type == self.settings.BURST_EVENT:
                for alien in self.died_aliens:
                    self.aliens.remove(alien)
            if self.stats.game_active and event.type == self.settings.ALIEN_CREATE_EVENT:
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

    def _collide(self):
        """碰撞事件"""
        dict_alien_bullet = pygame.sprite.groupcollide(self.bullets, self.aliens, True, False)
        for alien_sprites in dict_alien_bullet.values():
            for alien_sprite in alien_sprites.copy():
                alien_sprite.update(False)
                self.died_aliens.add(alien_sprite)

        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

    def _check_disappear_element(self):
        """删除消失在界面的元素"""
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)
        #            print(len(self.bullets))

        for alien in self.aliens.copy():
            if alien.rect.bottom >= self.screen.get_height():
                self.aliens.remove(alien)

    def _update_screen(self):
        """更新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for alien in self.aliens.sprites():
            alien.blitme()

        # 如果游戏还没有开始就绘制开始按钮
        if not self.stats.game_active:
            self.play_button.draw_button()
        # 让最近绘制的屏幕可见
        pygame.display.flip()

    def _ship_hit(self):
        """响应飞船被外星人撞到"""
        # ship_left减1
        self.stats.ships_left -= 1

        self.aliens.empty()
        self.bullets.empty()

        if self.stats.ships_left <= 0:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)
        sleep(0.5)
        self.ship.center_ship()

    def _check_play_button(self, mouse_pos):
        """玩家单击play按钮开始新游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            self.stats.reset_stats()
            self.stats.game_active = True

            self.aliens.empty()
            self.bullets.empty()

            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)


if __name__ == "__main__":
    ai = AlienInvasion()
    ai.run_game()
