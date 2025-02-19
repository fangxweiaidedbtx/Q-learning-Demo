from game.panal import BOARD_WIDTH,BOARD_HEIGHT


class Tank:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 75
        self.attack_power = 2
        self.range = 17
        self.movement = 7
        self.size = (3, 3)
        self.route = []

    def move(self, path):
        new_x = self.x + path[0]
        new_y = self.y + path[1]
        for x in range(min(self.x, new_x), max(self.x, new_x) + 1):
            self.route.append((x, self.y))
        self.x = new_x
        for y in range(min(self.y, new_y), max(self.y, new_y) + 1):
            self.route.append((self.x, y))
        self.y = new_y


    def attack(self, target_x, target_y):
        affected_area = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                affected_area.append((self.x + dx, self.y + dy))
                affected_area.append((self.x + dx, target_y + dy))
                affected_area.append((target_x + dx, self.y + dy))
                affected_area.append((target_x + dx, target_y + dy))
        return affected_area

    def crush(self, grid_x, grid_y,player_units):
        die_units = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                x = grid_x + dx
                y = grid_y + dy
                if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
                    for index,infantry in enumerate(player_units):
                        if infantry.x == x and infantry.y == y:
                            die_units.append(index)
                            infantry.hp = 0

        return die_units



class TankAI:
    def __init__(self, tank, board):
        self.tank = tank
        self.board = board

    def decide_movement(self, infantry_units: list):
        # 计算坦克距离最近的步兵
        min_distance = 1000
        target_infantry = None
        for infantry in infantry_units:
            distance = abs(infantry.x - self.tank.x) + abs(infantry.y - self.tank.y)
            if distance < min_distance and infantry.hp > 0:
                min_distance = distance
                target_infantry = infantry
        # 计算坦克的移动方向
        dx = target_infantry.x - self.tank.x
        dy = target_infantry.y - self.tank.y
        if abs(dx) + abs(dy) > self.tank.movement:
            # 超出移动范围，选择最短路径
            path = self.find_shortest_path(self.tank.x, self.tank.y, target_infantry.x, target_infantry.y, self.tank)
            self.tank.move(path)
        else:
            self.tank.move((dx, dy))

    def find_shortest_path(self, start_x, start_y, end_x, end_y,tank):
        dx = end_x - start_x
        dy = end_y - start_y
        if abs(dx) - tank.movement > 0:
            return (tank.movement*dx//abs(dx), 0)
        else:
            return (dx,(tank.movement-abs(dx))*dy//abs(dy))


    def decide_attack(self, infantry_units: list):
        # 计算坦克攻击范围内有哪些单位
        for infantry in infantry_units:
            if infantry.hp <= 0:
                continue
            if abs(infantry.x - self.tank.x) + abs(infantry.y - self.tank.y) <= self.tank.range:
                infantry.hp -= self.tank.attack_power
                break


