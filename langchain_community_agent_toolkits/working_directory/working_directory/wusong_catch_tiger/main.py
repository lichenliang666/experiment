import pygame
import random
import time

# 初始化 pygame
pygame.init()

# 游戏设置
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# 颜色定义
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
ORANGE = (255, 165, 0)

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 40
        self.speed = 5
        
    def move(self, keys):
        if keys[pygame.K_LEFT] and self.x > 0:
            self.x -= self.speed
        if keys[pygame.K_RIGHT] and self.x < SCREEN_WIDTH - self.width:
            self.x += self.speed
        if keys[pygame.K_UP] and self.y > 0:
            self.y -= self.speed
        if keys[pygame.K_DOWN] and self.y < SCREEN_HEIGHT - self.height:
            self.y += self.speed
    
    def draw(self, screen):
        # 绘制武松（蓝色方块）
        pygame.draw.rect(screen, BLUE, (self.x, self.y, self.width, self.height))
        # 添加标签
        font = pygame.font.Font(None, 24)
        text = font.render("武松", True, BLACK)
        screen.blit(text, (self.x - 10, self.y - 25))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Tiger:
    def __init__(self):
        self.width = 35
        self.height = 35
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = random.randint(0, SCREEN_HEIGHT - self.height)
        self.spawn_time = time.time()
        self.lifetime = 3.0  # 老虎存在3秒
        
    def is_expired(self):
        return time.time() - self.spawn_time > self.lifetime
    
    def draw(self, screen):
        # 绘制老虎（橙色方块）
        pygame.draw.rect(screen, ORANGE, (self.x, self.y, self.width, self.height))
        # 添加标签
        font = pygame.font.Font(None, 24)
        text = font.render("老虎", True, BLACK)
        screen.blit(text, (self.x - 10, self.y - 25))
    
    def get_rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("武松打虎")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # 游戏对象
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.tigers = []
        self.score = 0
        self.last_tiger_spawn = time.time()
        self.tiger_spawn_interval = random.uniform(1.0, 3.0)  # 随机生成间隔
        
        # 字体
        self.font = pygame.font.Font(None, 36)
        self.small_font = pygame.font.Font(None, 24)
        
    def spawn_tiger(self):
        current_time = time.time()
        if current_time - self.last_tiger_spawn > self.tiger_spawn_interval:
            self.tigers.append(Tiger())
            self.last_tiger_spawn = current_time
            self.tiger_spawn_interval = random.uniform(1.0, 3.0)
    
    def update(self):
        # 获取按键状态
        keys = pygame.key.get_pressed()
        
        # 更新玩家
        self.player.move(keys)
        
        # 生成新老虎
        self.spawn_tiger()
        
        # 更新老虎（移除过期的）
        self.tigers = [tiger for tiger in self.tigers if not tiger.is_expired()]
        
        # 检测碰撞
        player_rect = self.player.get_rect()
        for tiger in self.tigers[:]:  # 使用切片复制列表
            if player_rect.colliderect(tiger.get_rect()):
                self.tigers.remove(tiger)
                self.score += 1
    
    def draw(self):
        self.screen.fill(WHITE)
        
        # 绘制游戏对象
        self.player.draw(self.screen)
        for tiger in self.tigers:
            tiger.draw(self.screen)
        
        # 绘制分数
        score_text = self.font.render(f"分数: {self.score}", True, BLACK)
        self.screen.blit(score_text, (10, 10))
        
        # 绘制说明
        instructions = [
            "使用方向键控制武松移动",
            "抓到老虎得1分",
            "老虎会在3秒后消失"
        ]
        
        for i, instruction in enumerate(instructions):
            text = self.small_font.render(instruction, True, BLACK)
            self.screen.blit(text, (10, SCREEN_HEIGHT - 80 + i * 25))
        
        pygame.display.flip()
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
    
    def run(self):
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()