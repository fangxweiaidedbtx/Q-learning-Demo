import os
import sys
import pathlib
project_root = os.path.abspath("../")
sys.path.append(project_root)
import random
import time
from game.infantry import Infantry,ACTION
from game.tank import *
from game.panal import *
pygame.init()


def transform_state(unit, tank):
    dx = tank.x - unit.x
    dy = tank.y - unit.y
    return (dx,dy,unit.hp)


screen = ui_init()
clock = pygame.time.Clock()


class QLearningAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = self.create_q_table()
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def get_q_value(self, state, action):
        if abs(state[0]) > 20 and abs(state[1]) > 20:
            state = (int(state[0] / abs(state[0]) * 20), int(state[1] / abs(state[1]) * 20), state[2])
        elif abs(state[0]) > 20:
            state = (int(state[0] / abs(state[0]) * 20), state[1], state[2])
        elif abs(state[1]) > 20:
            state = (state[0], int(state[1] / abs(state[1]) * 20), state[2])
        return self.q_table.get(state).get(action)

    def choose_action(self, state):
        if random.uniform(0, 1) < self.epsilon:
            return random.choice(ACTION)
        else:
            q_values = [self.get_q_value(state, action) for action in ACTION]
            max_q = max(q_values)
            best_actions = [a for a, q in zip(ACTION, q_values) if q == max_q]
            return random.choice(best_actions)

    def update_q_table(self, state, action, reward, new_state):
        current_q = self.get_q_value(state, action)
        future_q = max([self.get_q_value(new_state, a) for a in ACTION])
        new_q = current_q + self.alpha * (reward + self.gamma * future_q - current_q)
        self.q_table[state][action] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

    def create_q_table(self):
        # 如果q_table.pkl存在，则加载,使用pathlib
        import pickle
        if pathlib.Path('q_table.pkl').exists():
            print('load q_table.pkl')
            with open('q_table.pkl', 'rb') as f:
                q_table = pickle.load(f)
            return q_table
        state = []
        for i in range(-20, 20 + 1):
            for j in range(-20, 20 + 1):
                state.append((i, j))
        result = {}
        for i in state:
            for j in [0, 2, 4, 6, 8]:
                result[(i[0], i[1], j)] = {}
                for k in ACTION:
                    result[(i[0], i[1], j)][k] = 0
        return result


class Environment:
    def __init__(self):
        self.game_end = False
        self.player_units = [Infantry(random.randint(BOARD_WIDTH // 2, BOARD_WIDTH // 4 * 3), random.randint(int(BOARD_HEIGHT*0.3), int(BOARD_HEIGHT*0.7))) for _ in
                             range(10)]
        self.tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
        self.tank_ai = TankAI(self.tank, None)
        self.states = []

        for i in self.player_units:
            self.states.append(transform_state(i, self.tank))

    def reset(self):
        self.game_end = False
        self.player_units = [Infantry(random.randint(BOARD_WIDTH // 2, BOARD_WIDTH // 4 * 3), random.randint(int(BOARD_HEIGHT*0.3), int(BOARD_HEIGHT*0.7))) for _ in
                             range(10)]
        self.tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
        self.tank_ai = TankAI(self.tank, None)

    def step(self, actions, use_screen=False):
        rewards = [0 for i in range(10)]
        for index, unit in enumerate(self.player_units):
            unit.move(actions[index][0], actions[index][1])

        under_crush_units = []
        self.tank_ai.decide_movement(self.player_units)
        for x, y in self.tank.route:
            for i in self.tank.crush(x, y, self.player_units):
                # 被碾压了但是未被记录
                if i not in under_crush_units:
                    under_crush_units.append(i)
        for index in under_crush_units:
            rewards[index] -= 35
        self.tank.route = []
        self.tank_ai.decide_attack(self.player_units)
        for index, infantry in enumerate(self.player_units):
            if infantry.hp <= 0:
                continue
            if abs(infantry.x - self.tank.x) + abs(infantry.y - self.tank.y) <= infantry.range:
                self.tank.hp -= infantry.attack_power
                rewards[index] += 6
            else:
                rewards[index] -= 1
        if use_screen:
            game_end = check_victory_conditions(self.tank, self.player_units, screen)
        else:
            game_end = check_victory_conditions(self.tank, self.player_units)
        self.states = []
        for i in self.player_units:
            self.states.append(transform_state(i, self.tank))
        if game_end:
            print(game_end)

        return self.states, rewards, game_end

infantry_image = pygame.image.load("unit.png")
infantry_image = pygame.transform.scale(infantry_image, (CELL_WIDTH, CELL_HEIGHT))

tank_image = pygame.image.load("tank.png")
tank_image = pygame.transform.scale(tank_image, (CELL_WIDTH * 3, CELL_HEIGHT * 3))
def show_state(player_units, tank):
    screen.fill((0, 0, 0))
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
        screen.blit(infantry_image, rect.topleft)
        # pygame.draw.rect(screen, BLUE, rect)
        pygame.draw.rect(screen, BLACK, rect, 1)

    # 绘制坦克
    tank_rect = pygame.Rect(
        tank.x * CELL_WIDTH - CELL_WIDTH,
        tank.y * CELL_HEIGHT - CELL_HEIGHT,
        CELL_WIDTH * tank.size[0],
        CELL_HEIGHT * tank.size[1]
    )
    # pygame.draw.rect(screen, RED, tank_rect)
    screen.blit(tank_image, tank_rect.topleft)
    pygame.draw.rect(screen, BLACK, tank_rect, 1)

    draw_hp_panel(tank, player_units, screen)
    pygame.display.update()
    clock.tick(5)



SHOW_TIME = 10
env = Environment()
agent = QLearningAgent(env)
num_episodes = 800
show_state(env.player_units, env.tank)

for episode in range(num_episodes):
    # 重置环境
    env.reset()
    if episode > num_episodes - SHOW_TIME:
        show_state(env.player_units, env.tank)
    total_reward = 0

    while True:
        try:
            # 获取当前状态
            current_states = [transform_state(unit, env.tank) for unit in env.player_units]
            actions = []
            # 选择动作
            for idx, state in enumerate(current_states):
                if state is not None:  # 确保状态合法
                    action = agent.choose_action(state)
                    actions.append(action)
            # 执行动作并获取新状态和奖励
            next_states, rewards, done = env.step(actions, episode > num_episodes - SHOW_TIME)
            # 更新Q表
            for idx, (state, action, reward, next_state) in enumerate(
                    zip(current_states, actions, rewards, next_states)):
                if abs(state[0]) > 20 and abs(state[1]) > 20:
                    state = (int(state[0] / abs(state[0]) * 20), int(state[1] / abs(state[1]) * 20), state[2])
                elif abs(state[0]) > 20:
                    state = (int(state[0] / abs(state[0]) * 20), state[1], state[2])
                elif abs(state[1]) > 20:
                    state = (state[0], int(state[1] / abs(state[1]) * 20), state[2])
                agent.update_q_table(state, action, reward, next_state)
            total_reward += sum(rewards)
            # 检查游戏是否结束
            if done:
                # 打印训练信息
                print(f"Episode {episode + 1}: Total Reward = {total_reward}! ")
                break
            if episode > num_episodes - SHOW_TIME:
                show_state(env.player_units, env.tank)
        except :
            pass
    # 衰减探索率
    agent.decay_epsilon()

pygame.quit()


