import random
import time
from game.infantry import Infantry
from game.tank import *
from game.panal import *

# 初始化Pygame
pygame.init()

game_end = False


def start_ui():
    global game_end
    screen = ui_init()
    ui_init()
    clock = pygame.time.Clock()
    # 初始化单位
    player_units = [Infantry(random.randint(BOARD_WIDTH // 2, BOARD_WIDTH // 4 * 3), random.randint(int(BOARD_HEIGHT*0.3), int(BOARD_HEIGHT*0.7))) for _ in
                        range(10)]
    tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
    tank_ai = TankAI(tank, None)

    selected_unit = None

    while not game_end:
        screen.fill(BLACK)
        # 处理事件
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_end = True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                grid_x = mouse_pos[0] // CELL_WIDTH
                grid_y = mouse_pos[1] // CELL_HEIGHT

                if event.button == 1:
                    for infantry in player_units:
                        if infantry.x == grid_x and infantry.y == grid_y and not infantry.selected:
                            selected_unit = infantry
                            infantry.selected = True
                        else:
                            infantry.selected = False
                elif event.button == 3 and selected_unit is not None:
                    # 玩家指令：移动
                    dx = grid_x - selected_unit.x
                    dy = grid_y - selected_unit.y
                    if abs(dx) + abs(dy) <= selected_unit.Infantry and not selected_unit.moved:
                        selected_unit.move(dx, dy)
                    # 更新屏幕
                    pygame.display.update()
                    clock.tick(60)
                    selected_unit.selected = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # next round
                    tank_ai.decide_movement(player_units)
                    for x,y in tank.route:
                        tank.crush(x,y,player_units)
                    tank.route = []
                    tank_ai.decide_attack(player_units)
                    for infantry in player_units:
                        if infantry.hp <= 0:
                            continue
                        infantry.moved = False
                        if abs(infantry.x - tank.x) + abs(infantry.y - tank.y) <= infantry.range:
                            tank.hp -= infantry.attack_power
        # 绘制网格
        for x in range(BOARD_WIDTH):
            for y in range(BOARD_HEIGHT):
                rect = pygame.Rect(x * CELL_WIDTH, y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
                pygame.draw.rect(screen, "#2F4F4F", rect, 1)

        # 绘制单位
        for infantry in player_units:
            rect = pygame.Rect(infantry.x * CELL_WIDTH, infantry.y * CELL_HEIGHT, CELL_WIDTH, CELL_HEIGHT)
            if infantry.hp <= 0:
                continue
            if infantry.selected:
                pygame.draw.rect(screen, GREEN, rect)
            elif not infantry.moved:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, "#4444AA", rect)
            pygame.draw.rect(screen, BLACK, rect, 1)

        # 绘制坦克
        tank_rect = pygame.Rect(
            tank.x * CELL_WIDTH - CELL_WIDTH,
            tank.y * CELL_HEIGHT - CELL_HEIGHT,
            CELL_WIDTH * tank.size[0],
            CELL_HEIGHT * tank.size[1]
        )
        pygame.draw.rect(screen, RED, tank_rect)
        pygame.draw.rect(screen, BLACK, tank_rect, 1)

        draw_hp_panel(tank,player_units,screen)
        # 环境结算
        game_end = check_victory_conditions(tank,player_units,screen)

        # 更新屏幕
        pygame.display.flip()
        clock.tick(2)


def start_no_ui():
    global game_end
    game_end = False
    player_units = [Infantry(random.randint(0, BOARD_WIDTH // 2), random.randint(0, BOARD_HEIGHT)) for _ in range(10)]
    tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
    tank_ai = TankAI(tank, None)
    while not game_end:
        # player_units AI
        pass

        tank_ai.decide_movement(player_units)
        for x, y in tank.route:
            tank.crush(x, y, player_units)
        tank.route = []
        tank_ai.decide_attack(player_units)
        for infantry in player_units:
            if infantry.hp <= 0:
                continue
            infantry.moved = False
            if abs(infantry.x - tank.x) + abs(infantry.y - tank.y) <= infantry.range:
                tank.hp -= infantry.attack_power
        game_end = check_victory_conditions(tank,player_units,False)
        for i in player_units:
            print(i.hp,end="\t")
        print(f"\ntank position {tank.x},{tank.y} \n")
        time.sleep(0.5)
    return game_end

# result = start_no_ui()
# print(result)

if __name__ == '__main__':
    start_ui()
