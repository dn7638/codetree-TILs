# n * n 격자
# 술래는 정중앙 -> n은 홀수
# m 명의 도망자 -> 좌우(오른쪽) / 상하(아래쪽)
# h개의 나무
# 도망자 동시에 움직임 -> 술래가 움직임 => 1턴씩 k번 반복
# 도망자는 술래와 거리가 3 이하일때만 움직임 , 이때 거리는 맨해탄 거리

# 도망자의 움직임 규칙
### 현재 바라보고 있는 방향으로 1칸
##### 격자를 안벗어나면 : 술래가 있으면 X, 이외에는 해당칸으로 이동
##### 격자를  벗어나면 : 방향을 반대로 틀기 -> 이후 술래가 없으면 바라보는 방향으로 이동

# 술래의 움직임 규칙
## 위 -> 달팽이 모양으로 움직임
## 끝에 닿으면 다시 거꾸로 중심으로 이동 -> 다시 중심에 오면 처음처럼 다시 이동
## 방향 트는 지점이면 바로 방향을 틈
## 이후 시야(바라보는 방향으로 3칸)에 있는 도망자를 잡음
## 나무가 있으면 거기있는애는 안잡힘

import sys

flag = [False for _ in range(10001)]
cnt = 0
temp = 1
while cnt < 10000:
    for i in range(2):
        cnt += temp
        if cnt > 10000:
            break
        flag[cnt] = True
        if i == 1:
            temp += 1

# 격자, 도망자수, 나무수, 턴수
n, m, h, k = map(int, sys.stdin.readline().split(' '))
# n은 홀수임


domang = [list(map(int, sys.stdin.readline().split(' '))) for _ in range(m)]
trees = [list(map(int, sys.stdin.readline().split(' '))) for _ in range(h)]
sulae = [n // 2 + 1, n // 2 + 1]
sulae_direction = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
sulae_outside = [True]

graph_tree = [[0 for _ in range(n + 1)] for _ in range(n + 1)]

for x, y in trees:
    graph_tree[x][y] = 1

# 3가지 그래프 완성
domang_move = {1: (0, 1), 2: (1, 0), -1: (0, -1), -2: (-1, 0)}

def innate(x, y):
    if 1 <= x <= n and 1 <= y <= n:
        return True
    else:
        return False


dir_flag = 0
move_cnt = 0
answer = 0
for turn in range(1, k + 1):
    # 도망자 움직임
    # x, y, d
    # d : 1 -> 좌우 -> 1 : 우 / -1 : 좌
    # d : 2 -> 상하 -> 2 : 하 / -2 : 상
    for idx, do in enumerate(domang):
        x, y, d = do[:]
        if x == 0 and y == 0:
            continue
        if 3 < abs(x - sulae[0]) + abs(y - sulae[1]):
            continue

        (dx, dy) = domang_move[d]
        next_x, next_y = x + dx, y + dy

        # 격자 내부
        if innate(next_x, next_y):
            if next_x == sulae[0] and next_y == sulae[1]:
                continue
            else:
                domang[idx][0], domang[idx][1] = next_x, next_y

        # 격자 외부
        else:
            d = -d
            domang[idx][2] = d
            (dx, dy) = domang_move[d]
            next_x, next_y = x + dx, y + dy
            if next_x == sulae[0] and next_y == sulae[1]:
                continue
            else:
                domang[idx][0], domang[idx][1] = next_x, next_y

    # 술래 위치 이동 및 방향 전환

    # 술래가 바깥으로 향하는 중이라면
    if sulae_outside[0]:
        dx, dy = sulae_direction[dir_flag]
        # 이동
        sulae[0] += dx
        sulae[1] += dy
        move_cnt += 1
        # 1,1 위치면
        if sulae[0] == 1 and sulae[1] == 1:
            dir_flag = 2
            sulae_outside[0] = False
        # 방향 전환하는 곳이면 방향 전환
        elif flag[move_cnt]:
            dir_flag = (dir_flag + 1) % 4
            
    # 안쪽으로 이동중
    else:
        dx, dy = sulae_direction[dir_flag]
        # 이동
        sulae[0] += dx
        sulae[1] += dy
        move_cnt -= 1
        # 중앙 위치면
        if sulae[0] == (n // 2 + 1) and sulae[1] == (n // 2 + 1):
            dir_flag = 0
            sulae_outside[0] = True
        # 방향 전환하는 곳이면 방향 전환
        elif flag[move_cnt]:
            dir_flag = (dir_flag - 1) % 4
            

    # 술래가 바라보는 방향
    look_x, look_y = sulae_direction[dir_flag]

    # 방향기준 3명 확인
    caught_num = 0
    for num in range(3):
        check_x, check_y = sulae[0] + look_x * num, sulae[1] + look_y * num
        # 바깥이면 그만
        if not innate(check_x, check_y):
            break

        
        for idx, do in enumerate(domang):
            x, y, d = do[:]
            if x == 0 and y == 0:
                continue
            # 사람 한명 잡으면 / graph_tree[] 가 1이면 나무가 있음
            if x == check_x and y == check_y and graph_tree[check_x][check_y] == 0:
                domang[idx][0], domang[idx][1] = 0, 0
                caught_num += 1
    answer += (caught_num * turn)
print(answer)