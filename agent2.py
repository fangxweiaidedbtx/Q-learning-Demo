import os
import sys
project_root = os.path.abspath("../")
sys.path.append(project_root)
import random
import time
from game.infantry import Infantry,ACTION
from game.tank import *
from game.panal import *
pygame.init()


def get_nearby(infantry_units, unit):
    min_distance = 100
    target_infantry = None
    for infantry in infantry_units:
        distance = abs(infantry.x - unit.x) + abs(infantry.y - unit.y)
        if distance < min_distance and infantry.hp > 0:
            min_distance = distance
            target_infantry = infantry
    return (target_infantry.x, target_infantry.y)


def transform_state(unit, tank):
    dx = tank.x - unit.x
    dy = tank.y - unit.y
    return (dx,dy,unit.hp)


def create_q_table():
    state = []
    for i in range(-20, 20 + 1):
        for j in range(-20, 20 - i + 1):
            state.append((i, j))
    result = {}
    for i in state:
        for j in [0,2,4,6,8]:
            result[(i[0],i[1],j)] = {}
            for k in ACTION:
                result[(i[0], i[1], j)][k] = 0
    return result

class Environment:
    def __init__(self):
        self.game_end = False
        self.player_units = [Infantry(random.randint(0, BOARD_WIDTH // 2), random.randint(0, BOARD_HEIGHT)) for _ in
                        range(10)]
        self.tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
        self.tank_ai = TankAI(self.tank, None)
        self.states = []
        for i in self.player_units:
            self.states.append(transform_state(i,self.tank))

    def reset(self):
        self.game_end = False
        self.player_units = [Infantry(random.randint(0, BOARD_WIDTH // 2), random.randint(0, BOARD_HEIGHT)) for _ in
                        range(10)]
        self.tank = Tank(BOARD_WIDTH - 5, BOARD_HEIGHT // 2)
        self.tank_ai = TankAI(self.tank, None)

    def step(self, actions):
        rewards = [0 for i in range(10)]
        for index,unit in enumerate(self.player_units):
            unit.move(actions[index][0],actions[index][1])

        under_crush_units = []
        self.tank_ai.decide_movement(self.player_units)
        for x, y in self.tank.route:
            for i in self.tank.crush(x, y, self.player_units):
                #被碾压了但是未被记录
                if i not in under_crush_units:
                    under_crush_units.append(i)
        for index in under_crush_units:
            rewards[index] -= 30
        self.tank.route = []
        self.tank_ai.decide_attack(self.player_units)
        for index,infantry in enumerate(self.player_units):
            if infantry.hp <= 0:
                continue
            if abs(infantry.x - self.tank.x) + abs(infantry.y - self.tank.y) <= infantry.range:
                self.tank.hp -= infantry.attack_power
                # 给予奖励
                rewards[index] += 5

            else:
                rewards[index] -= 1
                # 给予副奖励
                pass

        game_end = check_victory_conditions(self.tank, self.player_units, False)
        for i in self.player_units:
            self.states.append(transform_state(i,self.tank))
            print(i.hp, end="\t")
        print(f"\ntank position {self.tank.x},{self.tank.y} ,tank hp:{self.tank.hp}")
        if game_end:
            print(game_end)

        return self.states,rewards,game_end


class QLearningAgent:
    def __init__(self, env):
        self.env = env
        self.q_table = {}
        self.alpha = 0.1
        self.gamma = 0.99
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995

    def get_q_value(self, state, action):
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
        self.q_table[(state, action)] = new_q

    def decay_epsilon(self):
        self.epsilon = max(self.epsilon * self.epsilon_decay, self.epsilon_min)

