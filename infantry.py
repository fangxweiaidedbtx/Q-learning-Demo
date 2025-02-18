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
        # 仅移动一步
        if abs(dx) + abs(dy) > self.Infantry:
            return
        self.x += dx
        self.y += dy
        self.moved = True

    # def get_state(self,tank,player_units):
    #     nearby = player_units[0]
    #     distense = 120
    #     for i in player_units:
    #         if distense > (i.x + i.y):
    #             nearby =  i
    #             distense = i.x + i.y
    #     return {
    #         "infantry":(self.x,self.y),
    #         "tank":(tank.x,tank.y),
    #         "nearby": nearby,
    #         "hp":self.hp
    #     }



ACTION = []
for i in range(-INFANTRY_MOVEMENT,INFANTRY_MOVEMENT+1):
    for j in range(-(INFANTRY_MOVEMENT - abs(i)),INFANTRY_MOVEMENT - abs(i)+1):
        ACTION.append((i,j))

if __name__ == '__main__':
    a = Infantry(5,7)



