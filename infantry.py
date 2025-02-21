INFANTRY_MOVEMENT = 4
class Infantry:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.hp = 8
        self.attack_power = 1
        self.range = 18
        self.Infantry = INFANTRY_MOVEMENT
        self.selected = False
        self.moved = False


    def move(self, dx, dy):
        if abs(dx) + abs(dy) > self.Infantry:
            return
        self.x += dx
        self.y += dy
        self.moved = True




ACTION = []
for i in range(-INFANTRY_MOVEMENT,INFANTRY_MOVEMENT+1):
    for j in range(-(INFANTRY_MOVEMENT - abs(i)),INFANTRY_MOVEMENT - abs(i)+1):
        ACTION.append((i,j))

if __name__ == '__main__':
    # a = Infantry(5,7)
    print(ACTION)


