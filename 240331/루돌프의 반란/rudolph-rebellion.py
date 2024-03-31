import sys

N, M, P, C, D = map(int, sys.stdin.readline().split(' '))
R_r, R_c = map(int, sys.stdin.readline().split(' '))
santa = [0 for _ in range(P + 1)]
score = [0 for _ in range(P + 1)]
moveR = [[-1, -1], [-1, 0], [-1, 1], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1]]
moveS = [[-1, 0], [0, 1], [1, 0], [0, -1]]
graph = [[0 for _ in range(N + 1)] for _ in range(N + 1)]
# -1,-1  -1,0  -1,1
# 0,-1   0,0   0,1
# 1,-1   1,0   1,1
for _ in range(P):
    p, r, c = list(map(int, sys.stdin.readline().split(' ')))
    # r, c, 기절여부, 생존여부
    # 기절 여부 <= 0 이면 기절 아님
    # 충돌하면 기절 여부 = 2 가됨
    santa[p] = [r, c, 0, True]
santa[0] = [-2, -2, -2, False]
for i in range(1, P + 1):
    graph[santa[i][0]][santa[i][1]] = i


def action(santa, santa_idx, dr, dc):
    cur = santa_idx
    while True:
        flag = False
        for idx, rc in enumerate(santa):
            if idx == cur or not santa[idx][3]:
                continue
            r, c = rc[:2]
            if santa[cur][0] == r and santa[cur][1] == c:
                # graph[santa[cur][0]][santa[cur][1]] = 0
                santa[idx][0] += dr
                santa[idx][1] += dc
                santa_live_check(santa, idx)
                cur = idx
                flag = True
                break
        if not flag:
            break


def _action(santa, santa_idx, dr, dc):
    r, c = santa[santa_idx][0], santa[santa_idx][1]
    temp = 0
    if graph[r][c] != 0:
        temp = graph[r][c]
        graph[r][c] = santa_idx
    else:
        graph[r][c] = santa_idx

    while temp:
        r += dr
        c += dc
        santa[temp][0] = r
        santa[temp][1] = c
        if r < 1 or r > N or c < 1 or c > N:
            santa[temp][3] = False
            continue

        if graph[r][c] != 0 and santa[graph[r][c]][3]:
            _temp = graph[r][c]
            graph[r][c] = temp
            temp = _temp
        else:
            graph[r][c] = temp
            temp = 0


def distance(a, b, c, d):
    return (pow(a - c, 2) + pow(b - d, 2))


def santa_live_check(santa, santa_idx):
    if santa[santa_idx][0] < 1 or santa[santa_idx][0] > N or santa[santa_idx][1] < 1 or santa[santa_idx][1] > N:
        santa[santa_idx][3] = False
        return False
    return True


def close_santa(santa, R_r, R_c):
    temp = []
    for idx, info in enumerate(santa):
        r, c, stun, live = info[:]
        if not live:
            continue

        temp.append([-distance(R_r, R_c, r, c), r, c, idx])
    return max(temp)[3]
    # idx 리턴


def R_direction(S_r, S_c, R_r, R_c):
    temp = []
    for dr, dc in moveR:
        if R_r + dr - S_r == 0 and R_c + dc - S_c == 0:
            temp.append([0, dr, dc])
        else:
            temp.append([-pow(R_r + dr - S_r, 2) - pow(R_c + dc - S_c, 2), dr, dc])
    return max(temp)[1:3]
    # dr, dc 방향 리턴


def S_direction(santa, i, R_r, R_c):
    S_r, S_c = santa[i][:2]
    temp = []
    for idx, move in enumerate(moveS):
        dr, dc = move[:]
        if 1 <= S_r + dr <= N and 1 <= S_c + dc <= N:
            if graph[S_r + dr][S_c + dc] == 0:
                dis = distance(S_r + dr, S_c + dc, R_r, R_c)
                if distance(S_r, S_c, R_r, R_c) > dis:
                    temp.append([-dis, -idx, dr, dc])
    if temp:
        a, b = max(temp)[2:4]
        return True, a, b
    else:
        return False, 0, 0


# 턴수 M 만큼 반복할거임
for z in range(M):
    # for idx, i in enumerate(score):
    #     if idx == 0:
    #         continue
    #     print(i, end=' ')
    # print()

    # 루돌프의 움직임 :
    # - 가장 가까운 산타를 선택
    santa_idx = close_santa(santa, R_r, R_c)
    S_r, S_c = santa[santa_idx][0:2]
    # 가장 가까워지는 방향
    dr, dc = R_direction(S_r, S_c, R_r, R_c)
    # - 가장 가까운 산타(탈락하지 않은)를 향해 1칸 이동
    R_r += dr
    R_c += dc
    #
    # 충돌 구현
    # - 루돌프가 움직여서 충돌이 난 경우
    if R_r == S_r and R_c == S_c:
        # 루돌프가 이동해온 방향으로 C칸 산타 이동 -> 게임판 밖이면 out
        score[santa_idx] += C
        # 밀려난 칸에 다른 산타가 있는 경우 -> 산타 이동!!
        santa[santa_idx][0] += (dr * C)
        santa[santa_idx][1] += (dc * C)
        # 기절
        santa[santa_idx][2] = 2
        if santa_live_check(santa, santa_idx):
            # 상호작용 구현
            _action(santa, santa_idx, dr, dc)

    # 산타의 움직임
    # santa[p] = [r, c, 0, True]
    # print()
    for i in range(1, P + 1):
        if santa[i][2] > 0 or not santa[i][3]:
            continue
        ismove, dr, dc = S_direction(santa, i, R_r, R_c)
        # print(ismove, dr, dc)
        # - 산타는 루돌프에게 거리가 가장 가까워지는 방향으로 1칸 움직임 -> 상우하좌 순서
        # - 다른산타가 있거나 게임판 밖으로는 못움직임, 기절하면 못움직임,
        # - 루돌프로부터 가까워질 수 있는 방법이 없다면 산타 못움직임
        # - 상우하좌 중에 하나의 방향 선택
        if ismove:
            graph[santa[i][0]][santa[i][1]] = 0
            santa[i][0] += dr
            santa[i][1] += dc
            graph[santa[i][0]][santa[i][1]] = i
            # 충돌 발생
            if santa[i][0] == R_r and santa[i][1] == R_c:
                score[i] += D
                santa[i][0] += (-dr * D)
                santa[i][1] += (-dc * D)
                santa[i][2] = 2
                if santa_live_check(santa, i):
                    # 상호작용 구현
                    _action(santa, i, -dr, -dc)


        # print(santa[i])

        # 충돌 구현
        # - 산타가 움직여서 충돌이 난 경우 D만큼 점수획득
        # 자신이 이동해온 반대방향으로 D칸 밀려남
        # 밀려난 곳이 게임판 밖인 경우 탈락 -> 상호작용인경우 다음
        # 상호작용 구현
        # 해당 방향으로 1칸
    num = 0
    for idx, i in enumerate(santa):
        if idx == 0:
            continue
        santa[idx][2] -= 1
        if santa[idx][3] == False:
            num += 1
        else:
            score[idx] += 1
    if num == P:
        break

for idx, i in enumerate(score):
    if idx == 0:
        continue
    print(i, end=' ')
    # 루돌프가 움직여서 출동할 경우