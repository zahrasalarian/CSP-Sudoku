import numpy as np
import sys
sys.setrecursionlimit(1500)

n = 0
def main():
    global n
    m, dim = map(int, input().split())
    n = dim
    colors = input().split()
    colors_removed_from_dom = {}
    cards = []
    for i in range(n):
        cards_temp = input().split()
        cards.append(cards_temp)
    cards = np.array(cards)
    if solve_sudoku(cards, colors):
        print(cards)
    else:
        print("No solution")

def find_unassigned_block(cards, location):
    for i in range(n):
        for j in range(n):
            if cards[i, j][0] == '*' or cards[i, j][1] == '#':
                location[0] = i
                location[1] = j
                return True
    return False

def used_in_row(cards, row, num):
    for i in range(n):
        if cards[row, i][0] == str(num):
            return True
    return False

def used_in_col(cards, col, num):
    for i in range(n):
        if cards[i, col][0] == str(num):
            return True
    return False

def used_color_in_neighbours(cards, row, col, color):

    # first block is for left neighbour, second is from up, third is for right and last one is for down.
    neighbours = []
    # r == 0
    if row == 0 and col == 0:
        neighbours = [0,0,1,1]
    elif row == 0 and 0 < col < n - 1:
        neighbours = [1,0,1,1]
    elif row == 0 and col == n - 1:
        neighbours = [1,0,0,1]
    # r == n - 1
    elif row == n - 1 and col == 0:
        neighbours = [0,1,1,0]
    elif row == n - 1 and 0 < col < n - 1:
        neighbours = [1,1,1,0]
    elif row == n - 1 and col == n - 1:
        neighbours = [1,1,0,0]
    # c == 0
    elif 0 < row < n - 1 and col == 0:
        neighbours = [0,1,1,1]
    # c == n - 1
    elif 0 < row < n - 1 and col == n - 1:
        neighbours = [1,1,0,1]
    else:
        neighbours = [1,1,1,1]

    # check neighbours
    mark = False
    for i in range(len(neighbours)):
        if neighbours[i] == 1:
            if i == 0:
                if cards[row, col-1][1] == color:
                    mark = True
                    break
            elif i == 1:
                if cards[row-1, col][1] == color:
                    mark = True
                    break
            elif i == 2:
                if cards[row, col+1][1] == color:
                    mark = True
                    break
            elif i == 3:
                if cards[row+1, col][1] == color:
                    mark = True
                    break
    return mark


def check_location_is_safe(cards, row, col, num, color):
    num = not used_in_row(cards, row, num) and not used_in_col(cards, col, num)
    color = not used_color_in_neighbours(cards, row, col, color)
    validity = [num, color]
    return validity


def solve_sudoku(cards, colors):
    l = [0, 0]
    if(not find_unassigned_block(cards, l)):
        return True
    row = l[0]
    col = l[1]
    for num in range(1, n+1):
        last_num = cards[row, col][0]
        last_color = cards[row, col][1]
        for color in colors:
            new_num = None
            new_color = None
            validity = check_location_is_safe(cards, row, col, num, color)
            if validity[0] and cards[row, col][0] == '*':
                new_num = str(num)
            if validity[1] and cards[row, col][1] == '#':
                new_color = color
            
            if new_color is None and new_num is None:
                continue
            elif new_color is None and new_num is not None:
                value = str(new_num) + cards[row, col][1]
                cards[row, col] = value
                if solve_sudoku(cards, colors):
                    return True
            elif new_color is not None and new_num is None:
                    value = cards[row, col][0] + new_color
                    cards[row, col] = value
                    if solve_sudoku(cards, colors):
                        return True
            else:
                    value = new_num + new_color
                    cards[row, col] = value
                    if solve_sudoku(cards, colors):
                        return True
            cards[row, col] = last_num + '#'
        cards[row, col] = '*' + last_color

    return False

if __name__=="__main__":
    main()