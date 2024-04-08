# N * M 
# 총 K 턴 반복
# 턴당 4가지 액션
# 부서지지 않은 포탑이 1개가 되면 그 즉시 중지

# 턴당 액션 4가지
## 1. 공격자 선정
### 가장 약한 포탑 -> 공격자, 공격력 N + M 만큼 증가
### 공격력 가장 낮음
### 2개 이상이면, 가장 최근에 공격한 포탑
### 이런게 2개 이상이면, 각 포탑 위치의 행과 열의 합이 가장 큰 포탑
### 열값이 가장 큰 포탑
# 우선순위 -> 공격력이 가장 약한 포탑, 가장 최근에 공격한 포탑, 행과 열의 합이 큰, 열값이 가장 큰

## 2. 공격자의 공격
### 가장 강한 포탑이 공격 대상
### 우선순위 -> 공격력이 가장 높은 포탑, 가장 오래전에 공격한 포탑, 행과 열의 합이 가장 작은 포탑, 열 값이 가장 작은 포탑

### 레이저 공격
#### 최단 거리 -> 우하좌상 가능
####
### 포탄 공격
####

### 포탑 정비

import sys
from collections import deque

N, M, K = map(int, sys.stdin.readline().split(' '))
visited = [[False for _ in range(M)]for _ in range(N)] 

graph = [list(map(int, sys.stdin.readline().split(' '))) for _ in range(M)]
recent = [[ 0 for _ in range(M)]for _ in range(N)]
attack_stack = []

def attack_func(idx):
    next_damage, next_recent, next_sum, next_x, next_y = 5001, 0, 0, 0, 0
    for r in range(N):
        for c in range(M):
            cur_damage, cur_recent, cur_sum, cur_x, cur_y = graph[r][c], recent[r][c], r+c, r, c
            if cur_damage == 0:
                continue
            if cur_damage < next_damage:
                next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
            elif cur_damage == next_damage:
                if cur_recent > next_recent:
                    next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
                elif cur_recent == next_recent:
                    if cur_sum > next_sum:
                        next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
                    elif cur_sum == next_sum:
                        if cur_x > next_x:
                            next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
    
    graph[next_x][next_y] += (N + M)
    recent[next_x][next_y] = idx
    attack_stack.append((next_x, next_y))
    return (next_x, next_y)



## 2. 공격자의 공격
### 가장 강한 포탑이 공격 대상
### 우선순위 -> 공격력이 가장 높은 포탑, 가장 오래전에 공격한 포탑, 행과 열의 합이 가장 작은 포탑, 열 값이 가장 작은 포탑

def target_func(atk_x, atk_y):
    next_damage, next_recent, next_sum, next_x, next_y = 0, 1000, 21, 11, 11
    for r in range(N):
        for c in range(M):
            if r == atk_x and c == atk_y:
                continue
            cur_damage, cur_recent, cur_sum, cur_x, cur_y = graph[r][c], recent[r][c], r+c, r, c
            if cur_damage == 0:
                continue
            if cur_damage > next_damage:
                next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
            elif cur_damage == next_damage:
                if cur_recent < next_recent:
                    next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
                elif cur_recent == next_recent:
                    if cur_sum < next_sum:
                        next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
                    elif cur_sum == next_sum:
                        if cur_x < next_x:
                            next_damage, next_sum, next_x, next_y = cur_damage, cur_sum, cur_x, cur_y
    
    return (next_x, next_y)

move = [(0,1),(1,0),(0,-1),(-1,0)]

def raser_func(src_x, src_y, dest_x, dest_y):
    for i in range(N):
        for j in range(M):
            visited[i][j] = False

    temp_route = []
    queue = deque()
    queue.append((src_x,src_y, []))

    while queue:
        (cur_x, cur_y, rt) = queue.popleft()

        if cur_x == dest_x and cur_y == dest_y:
            for a, b in rt:
                attack_stack.append((a,b))
            return True

        for dx, dy in move:
            next_x, next_y = (cur_x + dx) % N, (cur_y + dy) % M
            if not visited[next_x][next_y] and graph[next_x][next_y] > 0:
                temp = rt[:]
                temp.append((next_x,next_y))
                queue.append((next_x, next_y, temp))
                visited[next_x][next_y] = True
                temp_route.append((next_x, next_y))

    return False

move_around = [[-1,-1],[-1,0],[-1,1],[0,-1],[0,1],[1,-1],[1,0],[1,1]]
# -1,-1  -1,0  -1,1
#  0,-1   0,0   0,1
#  1,-1   1,0   1,1

def bomb_func(src_x, src_y, dest_x, dest_y, damage):
    graph[dest_x][dest_y] -= damage
    if graph[dest_x][dest_y] < 0:
        graph[dest_x][dest_y] = 0
    
    for dx, dy in move_around:
        next_x, next_y = (src_x+dx)%N, (src_y+dy)%M
        if next_x == src_x and next_y == src_y:
            continue
        graph[next_x][next_y] -= (damage//2)
        if graph[next_x][next_y] < 0:
            graph[next_x][next_y] = 0
        attack_stack.append((next_x,next_y))
    attack_stack.append((dest_x,dest_y))

for turn_num in range(K):
    attack_stack.clear()

    # 공격자 선정
    atk_tower_x, atk_tower_y = attack_func(turn_num)
    atk_damage = graph[atk_tower_x][atk_tower_y]

    # 공격 대상 선정
    tar_tower_x, tar_tower_y = target_func(atk_tower_x, atk_tower_y)

    # 공격 종류 설정
    is_raser = raser_func(atk_tower_x, atk_tower_y, tar_tower_x, tar_tower_y)
    if is_raser:
        graph[tar_tower_x][tar_tower_y] -= atk_damage
        if graph[tar_tower_x][tar_tower_y] < 0:
            graph[tar_tower_x][tar_tower_y] = 0

        for i in range(1, len(attack_stack)-1):
            x, y = attack_stack[i][0], attack_stack[i][1]
            graph[x][y] -= (atk_damage // 2)
            if graph[x][y] < 0:
                graph[x][y] = 0
    else:
        bomb_func(atk_tower_x, atk_tower_y, tar_tower_x, tar_tower_y, atk_damage)

    temp = 0
    for i in range(M):
        for j in range(N):
            if graph[i][j] > 0:
                temp += 1
    if temp == 1:
        break

    # 정비
    for i in range(M):
        for j in range(N):
            if graph[i][j] <= 0:
                continue
            graph[i][j] += 1

    for i,j in attack_stack:
        if graph[i][j] <= 0:
            continue
        graph[i][j] -= 1

    
temp = 0
for i in range(M):
    for j in range(N):
        if temp < graph[i][j]:
            temp = graph[i][j]

print(temp)