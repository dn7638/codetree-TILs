# n * n 격자
#
#
#
#
#
#
#
#

import sys

n, m, k = map(int, sys.stdin.readline().split(' '))

base = [[0] for _ in range(n+1)]
base[0].extend([0 for _ in range(n)])
for i in range(1, n+1):
    base[i].extend(list(map(int, sys.stdin.readline().split(' '))))

heads = []  
for i in range(1, n+1):
    for j in range(1, n+1):
        if base[i][j] == 1:
            heads.append([i,j])   


def innate(x, y):
    if 1<=x<=n and 1<=y<=n:
        return True
    else:
        return False

move = [[-1,0],[0,1],[1,0],[0,-1]]


# 1 2 2     | 2 2 2
# 3   2     | 1   2
# 2 2 2     |   2 2
#
# 1 4 4
# 3   4
# 4 4 4
#
# 1 4 4
# 2   4
# 3 4 4


def check_fun(x, y):
    # x, y에서 1을 찾아나가야함
 
   

    stack = []
    cur_x, cur_y = x, y
    head_x, head_y = 0,0
    tail_x, tail_y = 0,0
    flag = 0
    if base[x][y] == 1 :
        head_x, head_y = cur_x, cur_y
        flag = 1
    if base[x][y] == 3 :
        tail_x, tail_y = cur_x, cur_y
        flag = 2
    for dx, dy in move:
            next_x, next_y = cur_x + dx, cur_y + dy
            if not innate(next_x,next_y):
                continue
            if base[next_x][next_y] != 4 and base[next_x][next_y] != 0:
                stack.append([cur_x,cur_y,next_x,next_y])
    result = 1
    for cur_x, cur_y, next_x, next_y in stack:
        length = 1
        # 2 1
        while True:
            before_x, before_y = cur_x, cur_y
            cur_x, cur_y = next_x, next_y

            for dx, dy in move:
                next_x, next_y = cur_x + dx, cur_y + dy

                if not innate(next_x, next_y):
                    continue

                if next_x == before_x and next_y == before_y:
                    continue

                if base[next_x][next_y] != 4 and base[next_x][next_y] != 0:
                    length += 1
                    break
            
            # head 찾기
            if base[cur_x][cur_y] == 1:
                result += length
                head_x, head_y = cur_x, cur_y
                break

            # tail 찾기
            elif base[cur_x][cur_y] == 3:
                tail_x, tail_y = cur_x, cur_y
                break

        # head idx찾기
        head_idx = -1
        for idx, head in enumerate(heads):
            x, y = head[:]
            if x == head_x and y == head_y:
                head_idx = idx
                break

    base[head_x][head_y] = 3
    base[tail_x][tail_y] = 1
    heads[head_idx][0], heads[head_idx][1] = tail_x, tail_y
    #print(f'length : {length}')
    #print(f'result : {result}')
    if flag == 1:
        return 1
    return result**2

score = 0
# 1. 이동
for rnd in range(1,k+1):

    for i in range(m):
        cur_x, cur_y = heads[i][:]
        thereisfour = False
        # 4가 있다고 가정
        for dx, dy in move:
            next_x, next_y = cur_x + dx, cur_y + dy
            
            if not innate(next_x,next_y):
                continue
            if base[next_x][next_y] == 4:
                end_x, end_y = next_x, next_y
                thereisfour = True
            elif base[next_x][next_y] == 2 or base[next_x][next_y] == 3:
                behind_x, behind_y = next_x, next_y

            # 4가 없는 경우 다시 고려해야함, 그럼 3이 반대방향에 있다는 뜻
            if not thereisfour:        
                for dx, dy in move:
                    next_x, next_y = cur_x + dx, cur_y + dy
                    if not innate(next_x,next_y):
                        continue
                    if base[next_x][next_y] == 3:
                        end_x, end_y = next_x, next_y
                        thereisfour = False
                    elif base[next_x][next_y] == 2:
                        behind_x, behind_y = next_x, next_y

        end_value = base[end_x][end_y]
        base[end_x][end_y] = base[cur_x][cur_y]
        heads[i][0], heads[i][1] = end_x, end_y
        
    
        while True:
            x_tomove, y_tomove = cur_x, cur_y
            cur_x, cur_y = behind_x, behind_y

            for dx, dy in move:
                next_x, next_y = cur_x + dx, cur_y + dy
                if not innate(next_x,next_y):
                        continue
                if next_x == x_tomove and next_y == y_tomove:
                    continue
                if base[next_x][next_y] != 0 :
                    behind_x, behind_y = next_x, next_y
            
            base[x_tomove][y_tomove] = base[cur_x][cur_y]
            if base[behind_x][behind_y] == 1:
                base[cur_x][cur_y] = end_value
                break
            else:
                base[cur_x][cur_y] = base[behind_x][behind_y]

    # ((rnd-1) // n ) % 4 == 0일때 , 1 ,2, 3일때..
    #(rnd-1) % n + 1 행 출발 우측으로
    if ((rnd-1) // n ) % 4 == 0:
        start_x = (rnd-1) % n + 1
        for y in range(1, n+1):
            if base[start_x][y] != 0 and base[start_x][y] != 4:
                score += check_fun(start_x, y)
                break
        

    # (rnd-1) % n + 1 열 출발 위로
    elif ((rnd-1) // n ) % 4 == 1:
        start_y = (rnd-1) % n + 1
        for x in range(n, 0, -1):
            if base[x][start_y] != 0 and base[x][start_y] != 4:
                score += check_fun(x, start_y)
                break
        
    # (rnd-1) % n + 1 행 출발 좌로
    elif ((rnd-1) // n ) % 4 == 2:
        start_x = (rnd-1) % n + 1
        for y in range(n, 0, -1):
            if base[start_x][y] != 0 and base[start_x][y] != 4:
                score += check_fun(start_x, y)
                break
        
    # (rnd-1) % n + 1 열 출발 아래로
    elif ((rnd-1) // n ) % 4 == 3:
        start_y = (rnd-1) % n + 1
        for x in range(1, n+1):
            if base[x][start_y] != 0 and base[x][start_y] != 4:
                score += check_fun(x, start_y)
                break


print(score)

# 3 1
#   2

# 1 3 
#   2
    
    


# 현재 위치에서
# 다음위치를 잡고
# 다음 위치에 있는걸 저장하고
# 다음 위치로 현재 위치에 있는걸 옮기고





# 2. 공 던지기

# 3. 점수 획득하기

# 26 49
# 26 64 -> 90