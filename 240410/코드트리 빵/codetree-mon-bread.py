# 코드트리 빵
# m명의 사람
# n * n 격자 위에서 진행

# 최단거리(맨해탄) 우선순위 -1,0 0,-1 0,1 1,0
# 상 좌 우 하
#      -1,0
# 0,-1  0,0  0,1
#       1,0
#

import sys
from collections import deque

n, m = map(int, sys.stdin.readline().split(' '))

graph = [[0] for _ in range(n + 1)]
graph[0].extend([0 for _ in range(n)])
for i in range(1, n + 1):
    graph[i].extend(list(map(int, sys.stdin.readline().split(' '))))

store = [list(map(int, sys.stdin.readline().rstrip().split(' '))) for _ in range(m)]
# 0 이면 도착, 1이면 안도착 -> sum 가능
remain_num = [m]

# 2 : 바깥 , 1 : 내부 , 0 : 도착
status = [2 for _ in range(m)]
location = [[0, 0] for _ in range(m)]
move = [[-1, 0], [0, -1], [0, 1], [1, 0]]


def innate(x, y):
    if 1 <= x <= n and 1 <= y <= n:
        return True
    else:
        return False


def dfs(t):
    visited = [[False for _ in range(n + 1)] for _ in range(n + 1)]
    # t 번 사람...!
    # 편의점 위치
    store_x, store_y = store[t][:]
    # 편의점 위치랑 가장 가까운 1 을 찾아야함
    # graph 에서
    queue = deque()
    candidate = []
    queue.append((store_x, store_y, 0))

    min_depth = 1000000
    while queue:
        cur_x, cur_y, depth = queue.popleft()

        if depth > min_depth:
            candidate.sort()
            status[t] = 1
            cur_x, cur_y = candidate[0][:]
            location[t][0], location[t][1] = cur_x, cur_y
            graph[cur_x][cur_y] = -1
            break

        if graph[cur_x][cur_y] == 1:
            min_depth = min(depth, min_depth)
            candidate.append([cur_x, cur_y])

        for dx, dy in move:
            next_x, next_y = cur_x + dx, cur_y + dy
            # 범위 먼저
            if innate(next_x, next_y):
                # 이동 가능한 곳이며 방문하지 않았다면
                if graph[next_x][next_y] != -1 and not visited[next_x][next_y]:
                    queue.append((next_x, next_y, depth + 1))
                    visited[next_x][next_y] = True


_move = [[-1, 0], [0, -1], [0, 1], [1, 0]]


def bfs(dest_x, dest_y, store_x, store_y):
    visited = [[False for _ in range(n + 1)] for _ in range(n + 1)]
    # graph 에서
    queue = deque()

    queue.append((store_x, store_y))

    while queue:
        cur_x, cur_y = queue.popleft()
        for dx, dy in _move:
            next_x, next_y = cur_x + dx, cur_y + dy
            if next_x == dest_x and next_y == dest_y:
                return cur_x, cur_y
            # 범위 먼저
            if innate(next_x, next_y):
                # 이동 가능한 곳이며 방문하지 않았다면
                if graph[next_x][next_y] != -1 and not visited[next_x][next_y]:
                    queue.append((next_x, next_y))
                    visited[next_x][next_y] = True

t = 0  # time
while True:
    # 1번
    for i in range(m):
        # 2 : 바깥 , 1 : 내부 , 0 : 도착
        if status[i] != 1:
            continue
        cur_x, cur_y = location[i][0], location[i][1]
        store_x, store_y = store[i][0], store[i][1]

        next_x, next_y = bfs(cur_x, cur_y, store_x, store_y)
        location[i][0], location[i][1] = next_x, next_y

    # 이동 완료 후 체크
    for i in range(m):
        if status[i] != 1:
            continue

        if location[i][0] == store[i][0] and location[i][1] == store[i][1]:
            status[i] = 0
            # 이제 못감
            graph[store[i][0]][store[i][1]] = -1
            remain_num[0] -= 1
    # 2번

    # 3번
    # 베이스 캠프 가야함
    if t < m:
        dfs(t)  # 가고싶은 편의전과 가장 가까이 있는 베이스 캠프

    t += 1
    if remain_num[0] == 0:
        break
print(t)