from collections import deque

# N, M, K -> 100 * 1000 -> 100000따리

N, M, K = map(int, input().split(' '))

grid = [list(map(int, input().split(' '))) for _ in range(N)]
attack_time = [[-1 for _ in range(M)] for _ in range(N)]
attack_related = [[-1 for _ in range(M)] for _ in range(N)]


def print_grid():
    for i in grid:
        print(i)


# print_grid()

def find_attacker():
    attacker_list = []
    # append tuple (dmg, -attack_time, -(i+j), -i)
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0:
                attacker_list.append((grid[i][j], -attack_time[i][j], -(i + j), -j, i, j))

    attacker_list.sort()
    i, j = attacker_list[0][4:6]
    return (i, j)


def find_dest(src_x, src_y):
    dest_list = []
    # append tuple (dmg, -attack_time, -(i+j), -i)
    for i in range(N):
        for j in range(M):
            if i == src_x and j == src_y:
                continue

            if grid[i][j] > 0:
                dest_list.append((-grid[i][j], attack_time[i][j], (i + j), j, i, j))

    dest_list.sort()
    i, j = dest_list[0][4:6]
    return (i, j)


# 우하좌상
move = [[0, 1], [1, 0], [0, -1], [-1, 0]]
around = [
    [-1, -1], [-1, 0], [-1, 1],
    [0, -1], [0, 1],
    [1, -1], [1, 0], [1, 1]
]


# 상하좌우
# 부서진거 X
# 가장자리 막히면 반대편
def razer(src_x, src_y, dest_x, dest_y, time):
    visited = [[False for _ in range(M)] for _ in range(N)]
    before = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    queue = deque()
    queue.append((src_x, src_y))
    visited[src_x][src_y] = True

    is_route = False
    while queue:
        cur_x, cur_y = queue.popleft()

        if cur_x == dest_x and cur_y == dest_y:
            is_route = True
            break

        for dx, dy in move:
            next_x, next_y = cur_x + dx, cur_y + dy
            next_x = next_x % N
            next_y = next_y % M

            if grid[next_x][next_y] > 0 and not visited[next_x][next_y]:
                queue.append((next_x, next_y))
                visited[next_x][next_y] = True
                before[next_x][next_y] = [cur_x, cur_y]
    # 루트가 있으면 레이저 공격
    if is_route:
        
        route = []
        cur_x, cur_y = dest_x, dest_y
        route.append((cur_x, cur_y))
        while True:
            cur_x, cur_y = before[cur_x][cur_y][:]
            route.append((cur_x, cur_y))

            if cur_x == src_x and cur_y == src_y:
                break

        for i in range(1, len(route) - 1):
            x, y = route[i][:]
            if grid[x][y] > 0:
                grid[x][y] -= (grid[src_x][src_y] // 2)
                attack_related[x][y] = time
                if grid[x][y] <= 0:
                    grid[x][y] = 0

        grid[dest_x][dest_y] -= grid[src_x][src_y]
        attack_related[dest_x][dest_y] = time
        if grid[dest_x][dest_y] <= 0:
            grid[dest_x][dest_y] = 0

    # 루트가 없으면 포탄공격
    else:
        # 주변

        for dx, dy in around:
            next_x, next_y = src_x + dx, src_y + dy
            next_x = next_x % N
            next_y = next_y % M

            if grid[next_x][next_y] > 0:
                grid[next_x][next_y] -= grid[src_x][src_y] // 2
                attack_related[next_x][next_y] = time
                if grid[next_x][next_y] <= 0:
                    grid[next_x][next_y] = 0

        # 타겟
        grid[dest_x][dest_y] -= grid[src_x][src_y]
        attack_related[dest_x][dest_y] = time
        if grid[dest_x][dest_y] <= 0:
            grid[dest_x][dest_y] = 0

    attack_related[src_x][src_y] = time


def repair(src_x, src_y, dest_x, dest_y, time):
    for i in range(N):
        for j in range(M):
            if i == src_x and j == src_y:
                continue
            if i == dest_x and j == dest_y:
                continue
            if grid[i][j] > 0 and attack_related[i][j] != time:
                grid[i][j] += 1


def is_only_one():
    cnt = 0
    for i in range(N):
        for j in range(M):
            if grid[i][j] > 0:
                cnt += 1
    if cnt <= 1:
        return True
    else:
        return False


for i in range(K):
    # K번 반복
    # 1. 공격자 선정

    # 부서지지 않은 포탑에 대한 리스트를 만들어 정렬(혹은 힙큐 사용)
    # 1. 공격력이 가장 낮은 포탑
    # 2. 가장 최근에 공격한 포탑
    # 3. 행과 열의 합이 가장 큰 포탑
    # 4. 열의 값이 가장 큰 포탑

    src_x, src_y = find_attacker()

    grid[src_x][src_y] += (N + M)
    attack_time[src_x][src_y] = i

    # 2. 공격자 공격 (이 단계에서 피해 입은 포탑 정보 보관)

    # 공격 대상 선택
    # 1. 공격력이 가장 높은 포탑
    # 2. 공격한지 가장 오래된 포탑
    # 3. 행과 열의 합이 가장 작은 포탑
    # 4. 열 값이 가장 작은 포탑
    dest_x, dest_y = find_dest(src_x, src_y)

    # 2-1 레이저 공격
    # 2-2 포탄 공격

    razer(src_x, src_y, dest_x, dest_y, i)

    # 3. 포탑 부셔짐
    # 공격력이 0 이하가 된 포탑 제거
    # 남은 포탑 1개인지 확인
    if is_only_one():
        break
    # 4. 포탑 정비
    repair(src_x, src_y, dest_x, dest_y, i)

    #  공격과 무관한 포탑 공격력 1추가

answer = 0
for i in range(N):
    for j in range(M):
        if answer < grid[i][j]:
            answer = grid[i][j]

print(answer)