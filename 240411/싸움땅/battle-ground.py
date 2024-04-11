# n * n 격자에서 진행
# 빈 격자에 플레이어들 위치
# 각각의 격자에는 무기들이 있음
# 총은 공격력 / 플레이어는 초기 능력치

# 하나의 라운드
# 첫번째 플레이어부터 향하고 있는 방향대로 한 칸 만큼 이동 / 격자를 벗어나는 경우 반대 방향으로 방향을 바꾸어 1만큼 이동
# 이동한 곳에 플레이어가 없다면 -> 총이 있는지 확인, 총이 있다면 총을 획득 -> 이미 총이 있다면 공격력이 큰 총을 획득하고, 기존 총은 격자에 다시놈
# 이동한 곳에 플레이어가 있다면 -> 싸움, 초기 능력치 + 총의 공격력을 비교하여 큰 플레이어가 승리, 초기 능력치가 더 우선
# 초기 능력치와 가지고있는 총의 공격력의 합의 차이만큼 포인트로 획득
# 승리한 칸에 떨어져 있는 총들과 운래 들고있던 총 중 가장 공력력이 높은 총을 획득

# 진 플레이어는 총을 격자에 내려놓고, 우너래 방향대로 한칸 이동, 이동하려는 칸에 다른 플레이어가 있거나 범위 밖인 경우 오른쪽으로 90도씩 회전하여 빈칸이 보이는 순간 이동
# 가장 공격력이 높은 총을 획득

import sys

n, m, k = map(int, sys.stdin.readline().rstrip().split(' '))

gun_graph = [[0 for _ in range(n+1)]]

for i in range(n):
    a = [0]
    a.extend(list(map(int, sys.stdin.readline().split(' '))))
    gun_graph.append(a)
    
# x,y d : 방향,s : 초기 능력치
gun_of_player = [0 for _ in range(m)]
point = [0 for _ in range(m)]
players = [list(map(int, sys.stdin.readline().rstrip().split(' ')))for _ in range(m)]
player_graph = [[-1 for _ in range(n+1)]for _ in range(n+1)]

for i, player in enumerate(players):
    player_graph[player[0]][player[1]] = i
direction = {0 : (-1,0), 1 : (0,1), 2 : (1,0), 3 : (0,-1)}

guns = [[0,0,0]]
for i in range(n+1):
    for j in range(n+1):
        if gun_graph[i][j] != 0:
            guns.append([i,j, gun_graph[i][j]])

# guns : i번째 총에 대하여 x,y, 총의 공격력

# i번 사람이, x,y로 이동했을때 총을 얻는 함수
def get_gun(i, x, y):
    # 총이 없는 경우
    cur_gun = gun_of_player[i]
    if cur_gun != 0:
        guns[cur_gun][0] = x
        guns[cur_gun][1] = y

    # 가장 큰 총 구하기
    max_score = 0
    max_idx = 0
    for idx, gun in enumerate(guns):
        if idx == 0:
            continue
        gun_x, gun_y, gun_score = gun[0], gun[1], gun[2]
        if gun_x == x and gun_y == y:
            if max_score < gun_score:
                max_score = gun_score
                max_idx = idx

    gun_of_player[i] = max_idx
    return max_idx, max_score
        

def innate(r, c):
    if 1<= r<= n and 1<=c<=n:
        return True
    else:
        return False

for z in range(k):

    for idx, player in enumerate(players):
        x, y, d, s = player
        dx, dy = direction[d]
        next_x, next_y = x+dx, y+dy
        if not innate(next_x,next_y):
            d = (d+2)%4
            dx, dy = direction[d]
            next_x, next_y = x+dx, y+dy
            players[idx][2] = d
            
        
        players[idx][0], players[idx][1] = next_x, next_y
        player_graph[x][y] = -1
        if player_graph[next_x][next_y] == -1:
            # 해당 칸에 플레이어가 없으면
            
            player_graph[next_x][next_y] = idx
            get_gun(idx, next_x, next_y)
    


        else:
            #있으면 싸우기
            # idx플레이어와 origin플레이어가 싸움
            
            origin = player_graph[next_x][next_y]
            origin_d, origin_s = players[origin][2:]
            origin_gun_score = guns[gun_of_player[origin]][2]
            idx_gun_score = guns[gun_of_player[idx]][2]

            origin_power = origin_s + origin_gun_score
            idx_power = s + idx_gun_score
            if origin_power < idx_power:
                winner = idx
                loser = origin
            elif origin_power > idx_power:
                winner = origin
                loser = idx
            elif origin_power == idx_power:
                if origin_s > s:
                    winner = origin
                    loser = idx
                else:
                    winner = idx
                    loser = origin

            point[winner] += abs(origin_power - idx_power)

            # 싸운 이후
            x, y = next_x, next_y
            loser_gun = gun_of_player[loser]
            guns[loser_gun][0], guns[loser_gun][1] = x, y
            gun_of_player[loser] = 0
            player_graph[x][y] = winner

            cur_dir = players[loser][2]
            for i in range(4):
                temp = (cur_dir + i)%4
                dx, dy = direction[temp]
                next_x, next_y = x + dx, y + dy
                if innate(next_x, next_y):
                    if player_graph[next_x][next_y] == -1:
                        players[loser][0], players[loser][1] = next_x, next_y
                        players[loser][2] = temp
                        player_graph[next_x][next_y] = loser
                        get_gun(loser, next_x, next_y)
                        break
            
            get_gun(winner, x, y)



for i in point:
    print(i, end=' ')