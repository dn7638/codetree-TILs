# M 명 참가자
#
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # # # #
# # # # # # r,c #
# # # # # # # # #
# N * N

# 빈칸 : 이동 가능
# 벽 : 이동 X / 내구도 1~9, 회전할 때 내구 1 감소 -> 내구도가 0이되면 빈 칸으로 변경
# 출구 : 탈출구

# 초단위로 참가자 이동
# 맨하탄 거리로 최단 거리 정의
# 모든 참가자 동시 이동

# 상하좌우 이동 가능
#      -1,0
# 0,-1       0,1
#       1,0
# 벽이 없는 곳으로 이동 가능
# 출구까지 최단 거리가 가까워야함
# 상하 우선

# 이동 이후 회전
# 출구로부터 최단 거리의 참가자가 있는 위치를 골라야함
# 좌상단 r좌표 작은것, c좌표가 작은 것 우선

# K 초가 지나거나 모든 참가자가 탈출하면 게임 종료
# 모든 참가자들의 이동 거리 합 / 출구 좌표를 출력

import sys

# 입력값, 변수
N, M, K = map(int, sys.stdin.readline().split(' '))
graph = [[0] for _ in range(N + 1)]
players = []
player_exist = [True for _ in range(M)]
number_of_players = [M]
cnt = [0]
# 상 하 좌 우 순서..!
move = [(-1, 0), (1, 0), (0, -1), (0, 1)]

for i in range(N + 1):
    if i == 0:
        graph[i].extend([0 for _ in range(N)])
        continue
    graph[i].extend(list(map(int, sys.stdin.readline().split(' '))))
graph_temp = [[0 for _ in range(N + 1)] for _ in range(N + 1)]

for _ in range(M):
    players.append(list(map(int, sys.stdin.readline().split(' '))))

exit_location = list(map(int, sys.stdin.readline().split(' ')))

def Print(a):
    for i in range(1, len(a)):
        for j in range(1, len(a[0])):
            if i == exit_location[0] and j == exit_location[1]:
                print('E', end='')
                continue

            flag = True
            for player in players:
                if player[0] == i and player[1] == j:
                    print('P', end='')
                    flag = False
                    break
            if not flag:
                continue
            print(a[i][j], end='')
        print()


def player_move(i):  # i = 플레이어 넘버
    cur_x, cur_y = players[i][:]
    distance = abs(cur_x - exit_location[0]) + abs(cur_y - exit_location[1])

    for dx, dy in move:
        next_x, next_y = cur_x + dx, cur_y + dy
        next_distance = abs(next_x - exit_location[0]) + abs(next_y - exit_location[1])
        if next_distance < distance and graph[next_x][next_y] == 0:
            players[i][0], players[i][1] = next_x, next_y
            cnt[0] += 1
            if (next_x, next_y) == (exit_location[0], exit_location[1]):
                players[i][0], players[i][1] = 0,0
                player_exist[i] = False
                number_of_players[0] -= 1
            break


#
# 1,1 1,2 1,3 1,4 1,5
# 2,1 2,2 2,3 2,4 2,5
# 3,1 3,2 3,3 3,4 3,5
# 4,1 4,2 4,3 4,4 4,5
# 5,1 5,2 5,3 5,4 5,5
#
# 0,0 0,1 0,2 0,3 0,4
# 1,0 1,1 1,2 1,3 1,4

# graph_temp1 = [['a', 'a', 'b', 'b'],
#                ['a', 'a', 'e', 'f'],  # e 0,1
#                ['d', 'd', 'h', 'g'],  # g 2,3
#                ['d', 'd', 'c', 'c']]
#
# graph_temp2 = [[0, 0, 0, 0],
#                [0, 0, 0, 0],
#                [0, 0, 0, 0],
#                [0, 0, 0, 0]]


def rotate(start_x, start_y, last_x, last_y):
    # 디버깅
    # 1,2
    # 2,3
    # print('사각형')
    # print(start_x, start_y, last_x, last_y)
    # print(f'출구 : {exit_location}')

    k = last_x - start_x + 1  # 2
    changed = False
    for i in range(start_x, start_x + k):
        for j in range(start_y, start_y + k):
            graph_temp[j - start_y][k - 1 - (i - start_x)] = graph[i][j]
            if i == exit_location[0] and j == exit_location[1] and not changed:
                exit_location[0], exit_location[1] = j - start_y + start_x, k - 1 - (i - start_x) + start_y
                changed = True

    for i in range(start_x, start_x + k):
        for j in range(start_y, start_y + k):
            if graph_temp[i - start_x][j - start_y] == 0:
                graph[i][j] = graph_temp[i - start_x][j - start_y]
            else:
                graph[i][j] = graph_temp[i - start_x][j - start_y] - 1

    for idx, player in enumerate(players):
        # 이러면 회전해야함
        if start_x <= player[0] <= last_x and start_y <= player[1] <= last_y:
            players[idx][0], players[idx][1] = players[idx][1] - start_y + start_x, k - 1 - (
                        players[idx][0] - start_x) + start_y


for game_iter in range(K):
    # # # 디버깅
    # print(f'게임 진행 초 : {game_iter}')
    # Print(graph)
    # print(player_exist)

    # 모든 참가자 동시 이동
    for i, player in enumerate(players):
        # 탈출한 플레이어는 고려하지 않음
        if not player_exist[i]:
            continue
        player_move(i)
    # # 디버깅
    # print('이동후')
    # Print(graph)

    # 이동 이후 모든 플레이어가 다 나갔다면...?
    # 즉시 종료
    if number_of_players[0] <= 0:
        break

    # 모든 플레이어가 이동을 마침...!
    # 가장 작은 정사각형을 잡아야함

    next_distance = 3 * N
    next_x, next_y = 2 * N, 2 * N
    for i, player in enumerate(players):
        # 탈출한 플레이어는 고려하지 않음
        if not player_exist[i]:
            continue

        cur_x, cur_y = players[i][:]
        cur_distance = max(abs(cur_x - exit_location[0]), abs(cur_y - exit_location[1]))
        if next_distance > cur_distance:
            next_x, next_y = cur_x, cur_y
            next_distance = cur_distance
            ####
            start_x, last_x = min(next_x, exit_location[0]), max(next_x, exit_location[0])
            start_y, last_y = min(next_y, exit_location[1]), max(next_y, exit_location[1])
            if (last_x - start_x) == next_distance:
                # x좌표는 놔두고 적절한 y좌표만 확인
                while last_y - start_y != next_distance:
                    if start_y > 1:
                        start_y -= 1
                    else:
                        last_y += 1

            elif (last_y - start_y) == next_distance:
                # x좌표는 놔두고 적절한 y좌표만 확인
                while last_x - start_x != next_distance:
                    if start_x > 1:
                        start_x -= 1
                    else:
                        last_x += 1
                        #####

        elif next_distance == cur_distance:

            cur_start_x, cur_last_x = min(cur_x, exit_location[0]), max(cur_x, exit_location[0])
            cur_start_y, cur_last_y = min(cur_y, exit_location[1]), max(cur_y, exit_location[1])
            if (cur_last_x - cur_start_x) == next_distance:
                # x좌표는 놔두고 적절한 y좌표만 확인
                while cur_last_y - cur_start_y != next_distance:
                    if cur_start_y > 1:
                        cur_start_y -= 1
                    else:
                        cur_last_y += 1

            elif (cur_last_y - cur_start_y) == next_distance:
                # x좌표는 놔두고 적절한 y좌표만 확인
                while cur_last_x - cur_start_x != next_distance:
                    if cur_start_x > 1:
                        cur_start_x -= 1
                    else:
                        cur_last_x += 1
            if cur_start_x < start_x:
                start_x, start_y = cur_start_x, cur_start_y
            elif cur_start_x == start_x:
                if cur_start_y < start_y:
                    start_x, start_y = cur_start_x, cur_start_y

    # 디버깅
    if next_x > N or next_y > N:
        print('정사각형 선택 오류 발생')
    # 디버깅

    # 이제 선택된 정사각형을 바탕으로 회전해야함..!
    # 세로 길이가 최대이면
    start_x, last_x = min(next_x, exit_location[0]), max(next_x, exit_location[0])
    start_y, last_y = min(next_y, exit_location[1]), max(next_y, exit_location[1])
    if (last_x - start_x) == next_distance:
        # x좌표는 놔두고 적절한 y좌표만 확인
        while last_y - start_y != next_distance:
            if start_y > 1:
                start_y -= 1
            else:
                last_y += 1

    elif (last_y - start_y) == next_distance:
        # x좌표는 놔두고 적절한 y좌표만 확인
        while last_x - start_x != next_distance:
            if start_x > 1:
                start_x -= 1
            else:
                last_x += 1

    rotate(start_x, start_y, last_x, last_y)
    # # #디버깅
    # print('회전후')
    # Print(graph)
    # Print(players)
    # print(f'회전후 출구 : {exit_location}')
    # print('===============')
print(cnt[0])
print(' '.join(map(str, exit_location)))