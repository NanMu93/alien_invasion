class GameStats:
    """跟踪游戏的统计信息"""
    score: int
    kill_alien: int
    ships_left: int

    def __init__(self, ai_game):
        """初始化统计信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

        self.high_score = 0

    def reset_stats(self):
        """初始化游戏统计信息"""
        self.ships_left = self.settings.ship_limit
        self.kill_alien = 0
        self.score = 0
