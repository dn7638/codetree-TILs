m, t = map(int, input().rstrip().split(' '))
pac_location = list(map(int, input().rstrip().split(' ')))
monster_graph = [[0 for _ in range(4)] for _ in range(4)]
siche_graph = [[0 for _ in range(4)] for _ in range(4)]

# x,y 에 어떤 몬스터가 있는지~
monster_dict = {}
# for i in range(4):
#     for j in range(4):
#         monster_dict[(i, j)] = []

# 상태
# 4 : 알
# 3 : 일반
# 2 : 시체
# 0 : (소멸됨)
for i in range(m):
    x, y, d = map(int, input().rstrip().split(' '))
    monster_dict[i] = [x, y, d, 3]
    monster_graph[x][y] += 1

# -1,-1  -1,0  -1,1
#  0,-1   0,0   0,1
#  1,-1   1,0   1,1

direction = {
    1: (-1, 0),
    2: (-1, -1),
    3: (0, -1),
    4: (1, -1),
    5: (1, 0),
    6: (1, 1),
    7: (0, 1),
    8: (-1, 1),
}

def innate(x,y):
    if 0<=x<=4 and 0<=y<=4:
        return True
    else:
        return False

alive_monster = [m]
created_monster = [m]
for turn in t:
    created_temp = []
    for key, value in monster_dict.items():
        x, y, d, status = value[:]

        if status == 3:
            created_temp.append([x, y, d, 4])
            for i in range(8):
                d = (d + i - 1) % 8 + 1
                dx, dy = direction[d]
                next_x, next_y = x + dx, y + dy
                if innate(next_x, next_y) and not (next_x == pac_location[0] and next_y == pac_location[1]) and siche_graph[next_x][next_y] == 0:
                    x, y = next_x, next_y
                    monster_dict[key] = [x,y,d, status]
                    break
                    #진행
        elif status == 2:

        elif status == 4:

        elif status == 0:

    for i in created_temp:
        monster_dict[created_monster[0]] = i
        created_monster[0] += 1