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
    if solve_sudoku(cards):
        print(cards)
    else:
        print("No solution")

def find_unassigned_block(cards, location):
    for i in range(n):
        for j in range(n):
            if cards[i, j] == '*#' or cards[i, j][0] == '*':
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

def check_location_is_safe(cards, row, col, num):
    return not used_in_row(cards, row, num) and not used_in_col(cards, col, num)

def solve_sudoku(cards):
    l = [0, 0]
    if(not find_unassigned_block(cards, l)):
        return True
    row = l[0]
    col = l[1]
    for num in range(1, n+1):
        if check_location_is_safe(cards, row, col, num):
            value = str(num) + '#'
            cards[row, col] = value
            if solve_sudoku(cards):
                return True

            cards[row, col] = '*#'

    return False

if __name__=="__main__":
    main()