import pyxel

SCREEN_WIDTH = 160
SCREEN_HEIGHT =120
SWORD_INTERVAL = 15
GAME_OVER_DISPLAY_TIME = 60
START_SCENE = 'start'
PLAY_SCENE = 'play'

class Sword:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed
    
    def update(self):
        if self.y < SCREEN_HEIGHT:
            self.y += self.speed
    
    def draw(self):
        pyxel.blt(self.x, self.y, 0, 8, 0, 8, 16, pyxel.COLOR_BLACK)

class App:
    def __init__(self):
        pyxel.init(SCREEN_WIDTH, SCREEN_HEIGHT, title='ピクセルゲーム')
        pyxel.mouse(True)
        pyxel.load('my_resource.pyxres')
        self.jp_font = pyxel.Font('umplus_j10r.bdf')
        pyxel.playm(0, loop = True)
        self.current_scene = START_SCENE
        pyxel.run(self.update, self.draw)
    
    def reset_play_scene(self):
        self.player_x = SCREEN_WIDTH // 2
        self.player_y = SCREEN_HEIGHT * 4 // 5
        self.player_vy = 0
        self.swords = []
        self.is_collision = False
        self.game_over_display_timer = GAME_OVER_DISPLAY_TIME
        self.sword_speed_level = 1  # 剣の落下速度のレベル
        self.initial_sword_speed = 2  # 剣の初期落下速度
        self.sword_spawn_level = 1 # 剣の出現数を管理するレベル
        self.initial_sword_interval = 15 # 剣の初期出現間隔
        self.score = 0  # スコアを初期化

    def update_start_scene(self):
        if pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
            self.reset_play_scene()
            self.current_scene = PLAY_SCENE
    
    def update_play_scene(self):
        #ゲームオーバー時
        if self.is_collision:
            if self.game_over_display_timer > 0:
                self.game_over_display_timer -= 1
            else:
                self.current_scene = START_SCENE
            return
                
        # プレイヤーの移動
        if pyxel.btn(pyxel.KEY_RIGHT) and self.player_x < SCREEN_WIDTH - 12:
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_D) and self.player_x < SCREEN_WIDTH - 12:
            self.player_x += 1
        elif pyxel.btn(pyxel.KEY_LEFT) and self.player_x > - 4:
            self.player_x -= 1
        elif pyxel.btn(pyxel.KEY_A) and self.player_x > - 4:
            self.player_x -= 1
        
        # ジャンプ機能の追加
        # 地面にいるときのみジャンプ可能
        if pyxel.btnp(pyxel.KEY_SPACE) and self.player_y == SCREEN_HEIGHT * 4 // 5:
            self.player_vy = -4  # ジャンプの初速度
        
        # プレイヤーのY座標を更新
        self.player_y += self.player_vy
        
        # 重力
        if self.player_y < SCREEN_HEIGHT * 4 // 5:
            self.player_vy += 0.2  # 重力加速度
        
        # 地面との衝突判定
        if self.player_y >= SCREEN_HEIGHT * 4 // 5:
            self.player_y = SCREEN_HEIGHT * 4 // 5
            self.player_vy = 0
            
         # 剣の落下速度の変更
        if self.sword_speed_level < 3 and pyxel.frame_count % (10 * 60) == 0:
            self.sword_speed_level += 1
            
        current_speed = self.initial_sword_speed * self.sword_speed_level
        
        # 剣の出現数の変更
        if self.sword_spawn_level < 3 and pyxel.frame_count % (10 * 60) == 0:
            self.sword_spawn_level += 1
        
        current_interval = self.initial_sword_interval // self.sword_spawn_level
        
        # 剣を追加
        if pyxel.frame_count % current_interval == 0:
            self.swords.append(Sword(pyxel.rndi(0, SCREEN_WIDTH - 8), 0, current_speed))
        
        # 剣の落下
        for sword in self.swords.copy():
            sword.update()
        
            # 当たり判定
            if (self.player_x <= sword.x <= self.player_x + 8 and
                self.player_y <= sword.y <= self.player_y + 8):
                self.is_collision = True
                
            # 画面外の剣を削除し、スコアを更新
            if sword.y >= SCREEN_HEIGHT:
                self.swords.remove(sword)
                if self.score < 9999:  # スコアが最大値に達していないかチェック
                    self.score += 10
    
    def update(self):
        if pyxel.btnp(pyxel.KEY_ESCAPE):
            pyxel.quit()
        
        if self.current_scene == START_SCENE:
            self.update_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.update_play_scene()
    
    def draw_start_scene(self):
        pyxel.blt(0, 0, 0, 32, 0, 160, 120)
        pyxel.text(SCREEN_WIDTH // 10, SCREEN_HEIGHT // 10,
                   'Click to Start', pyxel.COLOR_ORANGE, self.jp_font)
    
    def draw_play_scene(self):
        pyxel.cls(pyxel.COLOR_DARK_BLUE)
        
        # スコアの表示
        pyxel.text(5, 5, 'SCORE: ' + str(self.score), pyxel.COLOR_WHITE)
        
        # 剣
        for sword in self.swords:
            sword.draw()
            
        # プレイヤー
        pyxel.blt(self.player_x, self.player_y, 0, 16, 0, 16, 16, pyxel.COLOR_BLACK)
        
        if self.is_collision:
            pyxel.text(SCREEN_WIDTH // 2 - 15, SCREEN_HEIGHT // 2,
                       'GAME OVER', pyxel.COLOR_RED)
            # ゲームオーバー時に最終スコアを表示
            pyxel.text(SCREEN_WIDTH // 2 - 20, SCREEN_HEIGHT // 2 + 10,
                       'FINAL SCORE: ' + str(self.score), pyxel.COLOR_RED)
   
    def draw(self):
        if self.current_scene == START_SCENE:
            self.draw_start_scene()
        elif self.current_scene == PLAY_SCENE:
            self.draw_play_scene()

App()