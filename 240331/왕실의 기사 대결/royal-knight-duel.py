# 빈칸, 함정, 벽, 바깥도 벽
# 판 위에 기사들이 있음
# 위치 기준 h * w 의 크기, 체력은 k


# 상 하 좌 우 이동가능
#       -1,0      
# 0,-1   0,0   0,1
#        1,0


# 이동시 기사가 있다면 연쇄적으로 한 칸 밀려남
# 그런데 그 방향의 끝에 벽이 있으면 모든 기사는 이동할 수 없음


# 이동후 밀친경우 -> 밀려난 기사들은 피해를 입음
# 함정 수만큼 피해를 입음
# 체력 이상의 대미지를 받은 경우 체스판에서 사라져야함

import sys
from collections import deque

L, N, Q = map(int, sys.stdin.readline().split(' '))

chess = [[2 for _ in range(L + 2)]]

for i in range(1, L + 1):
    chess.append([2])
    chess[i].extend(list(map(int, list(sys.stdin.readline().split(' ')))))
    chess[i].append(2)
chess.append([2 for _ in range(L + 2)])

knight_graph = [[0 for _ in range(L + 2)] for _ in range(L + 2)]
knight_pos_rc = [[0, 0] for _ in range(N + 1)]
knight_hw = [[0, 0] for _ in range(N + 1)]
health = [0 for _ in range(N + 1)]
health_init = [0 for _ in range(N + 1)]
move = {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}

stack = deque()
stack_set = set()
stack_move = deque()


def knight_graph_draw(_i):
    r, c, h, w = knight_pos_rc[_i][0], knight_pos_rc[_i][1], knight_hw[_i][0], knight_hw[_i][1]
    for i in range(h):
        for j in range(w):
            knight_graph[r + i][c + j] = _i


def knight_graph_clear(_i):
    r, c, h, w = knight_pos_rc[_i][0], knight_pos_rc[_i][1], knight_hw[_i][0], knight_hw[_i][1]
    for i in range(h):
        for j in range(w):
            knight_graph[r + i][c + j] = 0


for i in range(1, N + 1):
    r, c, h, w, k = map(int, sys.stdin.readline().split(' '))
    knight_pos_rc[i][0], knight_pos_rc[i][1] = r, c
    knight_hw[i][0], knight_hw[i][1] = h, w
    knight_graph_draw(i)
    health[i] = k
    health_init[i] = k

order_id = []
for i in range(Q):
    order_id.append(list(map(int, sys.stdin.readline().split())))


def check(_i, dir):
    flag = True
    stack.append(_i)
    stack_set.add(_i)
    while flag:
        flag = False
        r, c, h, w = knight_pos_rc[stack[-1]][0], knight_pos_rc[stack[-1]][1], knight_hw[stack[-1]][0], knight_hw[stack[-1]][1]
        if dir == 0:
            dr, dc = -1, 0
            # 위 -1, 0

            # 벽이 아니면
            for i in range(w):
                # 이동할는 곳이 벽이면
                if chess[r + dr][c + dc + i] == 2:
                    stack.clear()
                    stack_set.clear()
                    stack_move.clear()
                    return False
                    # 움직임은 없던걸로
                # 다음칸에 기사가 있으면
                next_i = knight_graph[r + dr][c + dc + i]
                if next_i:
                    # 처음 보는 기사이면 담기
                    if next_i not in stack_set:
                        stack.append(next_i)
                        stack_set.add(next_i)
                        stack_move.append(next_i)
                        flag = True

        # {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        elif dir == 1:
            dr, dc = 0, 1
            # 오른쪽 0, 1

            # 벽이 아니면
            for i in range(h):
                # 이동할는 곳이 벽이면
                if chess[r + dr + i][c + dc + w - 1] == 2:
                    stack.clear()
                    stack_set.clear()
                    stack_move.clear()
                    return False
                    # 움직임은 없던걸로

                # 다음칸에 기사가 있으면
                next_i = knight_graph[r + dr + i][c + dc + w - 1]
                if next_i:
                    # 처음 보는 기사이면 담기
                    if next_i not in stack_set:
                        stack.append(next_i)
                        stack_set.add(next_i)
                        stack_move.append(next_i)
                        flag = True

        # {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        elif dir == 2:
            dr, dc = 1, 0
            # 아래 1, 0

            for i in range(w):
                # 이동할는 곳이 벽이면
                if chess[r + dr + h - 1][c + dc + i] == 2:
                    stack.clear()
                    stack_set.clear()
                    stack_move.clear()
                    return False
                    # 움직임은 없던걸로

                # 다음칸에 기사가 있으면
                next_i = knight_graph[r + dr + h - 1][c + dc + i]
                if next_i:
                    # 처음 보는 기사이면 담기
                    if next_i not in stack_set:
                        stack.append(next_i)
                        stack_set.add(next_i)
                        stack_move.append(next_i)
                        flag = True

        # {0: (-1, 0), 1: (0, 1), 2: (1, 0), 3: (0, -1)}
        elif dir == 3:
            dr, dc = 0, -1
            # 왼쪽 0, -1

            # 벽이 아니면
            for i in range(h):
                # 이동할는 곳이 벽이면
                if chess[r + dr + i][c + dc] == 2:
                    stack.clear()
                    stack_set.clear()
                    stack_move.clear()
                    return False
                    # 움직임은 없던걸로

                # 다음칸에 기사가 있으면
                next_i = knight_graph[r + dr + i][c + dc]
                if next_i:
                    # 처음 보는 기사이면 담기
                    if next_i not in stack_set:
                        stack.append(next_i)
                        stack_set.add(next_i)
                        stack_move.append(next_i)
                        flag = True
    while stack:
        _i = stack.pop()
        stack_set.remove(_i)
        knight_graph_clear(_i)

        # 이동
        knight_pos_rc[_i][0] += dr
        knight_pos_rc[_i][1] += dc
        knight_graph_draw(_i)
    return True


for _i, d in order_id:
    if health[_i] < 1:
        continue

        #인덱스 방향
    move = check(_i, d)

    if not move:
        continue

    while stack_move:
        i = stack_move.pop()
        # 죽은 기사는 신경쓰지 않기, 움직인 기사도 신경쓰지 않기
        if health[i] < 1 or i == _i:
            continue
        damage = 0
        r, c = knight_pos_rc[i][:]
        h, w = knight_hw[i][:]
        for dr in range(h):
            for dc in range(w):
                if chess[r + dr][c + dc] == 1:
                    damage += 1
        health[i] -= damage

        if health[i] < 1:
            knight_graph_clear(i)

answer = 0
for i in range(1, N + 1):
    if health[i] >= 1:
        answer += (health_init[i] - health[i])
print(answer)