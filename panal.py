import time

import pygame

# 设置窗口大小
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 1000

# 定义颜色
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)

# 定义网格大小
# GRID_SIZE = 20
BOARD_WIDTH = 100
BOARD_HEIGHT = 100

# 计算每个网格的实际像素大小
CELL_WIDTH = (WINDOW_WIDTH - 200)  // BOARD_WIDTH
CELL_HEIGHT = WINDOW_HEIGHT // BOARD_HEIGHT

PANEL_WIDTH = 200
PANEL_X = WINDOW_WIDTH - PANEL_WIDTH
# 创建窗口
def ui_init():
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    # pygame.display.set_caption("Turn-Based Strategy Game")
    return screen

def draw_hp_panel(tank,player_units,screen):
    # 绘制血量面板背景
    pygame.draw.rect(screen, (128, 128, 128), (PANEL_X, 0, PANEL_WIDTH, WINDOW_HEIGHT))
    # 显示坦克血量
    font = pygame.font.Font(None, 36)
    tank_hp_text = font.render(f"Tank HP: {tank.hp}", True, WHITE)
    screen.blit(tank_hp_text, (PANEL_X + 10, 10))
    # 显示步兵血量
    for i, infantry in enumerate(player_units):
        infantry_hp_text = font.render(f" {i + 1} HP: {infantry.hp}", True, WHITE)
        screen.blit(infantry_hp_text, (PANEL_X + 10, 50 + i * 30))



def check_victory_conditions(tank,player_units,use_ui=False,):
    # 检查胜利条件
    font = pygame.font.Font(None, 74)  # 使用默认字体，大小为74
    if  tank.hp <= 0:
        text = font.render("Player Wins!", True, GREEN)  # 绿色文字表示玩家胜利
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        # 清屏并绘制背景
        if use_ui:
            use_ui.fill(BLACK)  # 填充黑色背景
            use_ui.blit(text, text_rect)  # 绘制胜利或失败的文字
            pygame.display.flip()  # 更新屏幕
            # pygame.time.wait(2000)
            time.sleep(1)
        return "Player Wins!"
    elif all(infantry.hp <= 0 for infantry in player_units):
        text = font.render("Player Loses!", True, RED)   # 红色文字表示玩家失败
        text_rect = text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2))
        # 清屏并绘制背景
        if use_ui:
            use_ui.fill(BLACK)  # 填充黑色背景
            use_ui.blit(text, text_rect)  # 绘制胜利或失败的文字
            pygame.display.flip()  # 更新屏幕
            time.sleep(1)
            # pygame.time.wait(2000)
        return "Player Loses!"
    return False

