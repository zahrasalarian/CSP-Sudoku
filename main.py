import numpy as np
import sys
from copy import deepcopy

sys.setrecursionlimit(1500)

n = 0
m = 0
colors = []
def main():
    global n, m
    global colors
    m, dim = map(int, input().split())
    n = dim
    colors = input().split()
    colors_removed_from_dom = {}
    numbers_removed_from_dom = {}
    cards = []
    for _ in range(n):
        cards_temp = input().split()
        cards.append(cards_temp)
    cards = np.array(cards)

    for i in range(n):
        for j in range(n):
            if cards[i, j][1] != '#':
                cards_temp = deepcopy(cards)
                colors_removed_from_dom = remove_color_from_dom(cards_temp, colors_removed_from_dom, i, j, cards[i, j][1])
            if cards[i, j][0] != '*':
                cards_temp = deepcopy(cards)
                numbers_removed_from_dom = remove_numbers_from_dom(cards_temp, numbers_removed_from_dom, i, j, cards[i, j][0])
                print(numbers_removed_from_dom)
                print("what?")
    #print(colors_removed_from_dom)
    if solve_sudoku(cards, colors, colors_removed_from_dom, numbers_removed_from_dom):
        print(cards)
    else:
        print("No solution")

def mrv(availabls, colors_removed_from_dom):
    availables_mrv = {}
    for cell in availabls:
        loc = str(cell[0]) + str(cell[1])
        if loc in colors_removed_from_dom:  
            availables_mrv[loc] = m - len(colors_removed_from_dom[loc])
        else:
            availables_mrv[loc] = m
    return availables_mrv

def degree(availables, cards):
    availables_degree = {}
    for cell in availables:
        count = 0
        row = int(cell[0])
        col = int(cell[1])
        loc = cell
        neighbours = get_neighbours(int(cell[0]), int(cell[1]))
        for i in range(len(neighbours)):
            if neighbours[i] == 1:
                if i == 0:
                    if cards[row, col-1][1] == '#':
                        count += 1
                elif i == 1:
                    if cards[row-1, col][1] == '#':
                        count += 1
                elif i == 2:
                    if cards[row, col+1][1] == '#':
                        count += 1
                elif i == 3:
                    if cards[row+1, col][1] == '#':
                        count += 1
        availables_degree[loc] = count
    return availables_degree
        

def find_unassigned_block(cards, location, colors_removed_from_dom):
    availables = []
    for i in range(n):
        for j in range(n):
            if cards[i, j][1] == '#' or cards[i, j][0] == '*':
                #location[0] = i
                #location[1] = j
                availables.append([i,j])
                #return True
    #print(availables)
    if len(availables) == 0:
        return False
    else:
        availables_mrv = mrv(availables, colors_removed_from_dom)
        key_min = min(availables_mrv.keys(), key=(lambda k: availables_mrv[k]))
        min_mrv = availables_mrv[key_min]
        min_locs = []
        for key, value in availables_mrv.items():
            if value == min_mrv:
                min_locs.append(key)
        if len(min_locs) == 1:
            location[0] = int(key_min[0])
            location[1] = int(key_min[1])
            #print(location)
            #print(availables_mrv)
            #print("dard {}".format(min_mrv))
            return True
        else:
            cards_degree = deepcopy(cards)
            availables_degree = degree(min_locs, cards_degree)
            key_max = max(availables_degree.keys(), key=(lambda k: availables_degree[k]))
            max_degree = availables_degree[key_max]
            location[0] = int(key_max[0])
            location[1] = int(key_max[1])
            #print(location)
            #print(availables_mrv)
            #print(availables_degree)
            #print("dard {}".format(max_degree))
            return True

        

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

def get_neighbours(row, col):
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
    
    return neighbours


def used_color_in_neighbours(cards, row, col, num, color):

    neighbours = get_neighbours(row, col)

    # check neighbours
    #print("************")
    #print("num = {} , color = {}".format(num,color))
    color_index = colors.index(color)
    mark = False
    for i in range(len(neighbours)):
        if neighbours[i] == 1:
            if i == 0:
                #print("num1 = {} , color1 = {}".format(cards[row, col-1][0],cards[row, col-1][1]))
                if cards[row, col-1][1] != '#':
                    if cards[row, col-1][1] == color or (cards[row, col-1][0] != '*' and int(num) <= int(cards[row, col-1][0]) and color_index < colors.index(cards[row, col-1][1])) or (cards[row, col-1][0] != '*' and int(num) >= int(cards[row, col-1][0]) and color_index > colors.index(cards[row, col-1][1])):                   
                        mark = True
                        break
            elif i == 1:
                #print("num2 = {} , color2 = {}".format(cards[row-1, col][0],cards[row-1, col][1]))
                if cards[row-1, col][1] != '#':
                    if cards[row-1, col][1] == color or (cards[row-1, col][0] != '*' and int(num) <= int(cards[row-1, col][0]) and color_index < colors.index(cards[row-1, col][1])) or (cards[row-1, col][0] != '*' and int(num) >= int(cards[row-1, col][0]) and color_index > colors.index(cards[row-1, col][1])):
                        mark = True
                        break
            elif i == 2:
                #print("num3 = {} , color3 = {}".format(cards[row, col+1][0],cards[row, col+1][1]))
                if cards[row, col+1][1] != '#':
                    if cards[row, col+1][1] == color or (cards[row, col+1][0] != '*' and int(num) <= int(cards[row, col+1][0]) and color_index < colors.index(cards[row, col+1][1])) or (cards[row, col+1][0] != '*' and int(num) >= int(cards[row, col+1][0]) and color_index > colors.index(cards[row, col+1][1])):
                        mark = True
                        break
            elif i == 3:
                #print("num4 = {} , color4 = {}".format(cards[row+1, col][0],cards[row+1, col][1]))
                if cards[row+1, col][1] != '#':
                    if cards[row+1, col][1] == color or (cards[row+1, col][0] != '*' and int(num) <= int(cards[row+1, col][0]) and color_index < colors.index(cards[row+1, col][1])) or (cards[row+1, col][0] != '*' and int(num) >= int(cards[row+1, col][0]) and color_index > colors.index(cards[row+1, col][1])):
                        mark = True
                        break
    # remove color from neighbors dom if the color is valid for curr cell
    #if mark == False:
        #print("yes")
    return mark


def check_location_is_safe(cards, row, col, num, color):
    cards_temp = deepcopy(cards)
    number_val = not used_in_row(cards_temp, row, num) and not used_in_col(cards_temp, col, num)
    color_val = not used_color_in_neighbours(cards_temp, row, col, num, color)
    validity = [number_val, color_val]
    return validity

def remove_color_from_dom(cards, colors_removed_from_dom, row, col, color):
    neighbours = get_neighbours(row, col)
    new_removed = deepcopy(colors_removed_from_dom)
    row = int(row)
    col = int(col)

    for i in range(len(neighbours)):
        if neighbours[i] == 1:
            if i == 0:
                loc = str(row) + str(col-1)
                if cards[int(row), int(col-1)][1] == '#' :
                    if loc not in new_removed:
                        new_removed[loc] = [color]
                    elif color not in new_removed[loc]:
                        new_removed[loc].append(color)
                        if len(new_removed[loc]) == m:
                            return None
            elif i == 1:
                loc = str(row-1) + str(col)
                if cards[int(row-1), int(col)][1] == '#' :
                    if loc not in new_removed:
                        new_removed[loc] = [color]
                    elif color not in new_removed[loc]:
                        new_removed[loc].append(color)
                        if len(new_removed[loc]) == m:
                            return None
            elif i == 2:
                if cards[int(row), int(col+1)][1] == '#' :
                    loc = str(row) + str(col+1)
                    if loc not in new_removed:
                        new_removed[loc] = [color]
                    elif color not in new_removed[loc]:
                        new_removed[loc].append(color)
                        if len(new_removed[loc]) == m:
                            return None
            elif i == 3:
                if cards[int(row+1), int(col)][1] == '#' :
                    loc = str(row+1) + str(col)
                    if loc not in new_removed:
                        new_removed[loc] = [color]
                    elif color not in new_removed[loc]:
                        new_removed[loc].append(color)
                        if len(new_removed[loc]) == m:
                            return None
    return new_removed
def remove_numbers_from_dom(cards, numbers_removed_from_dom, row, col, number):
    new_removed = deepcopy(numbers_removed_from_dom)
    row = int(row)
    col = int(col)
    number = int(number)
    # row
    for column in range(n):
        if column != col and cards[row, column][0] == '*':
            loc = str(row) + str(column)
            if loc not in new_removed:
                new_removed[loc] = [number]
            elif number not in new_removed[loc]:
                new_removed[loc].append(number)
                if len(new_removed[loc]) == n:
                    return None
    # col
    for r in range(n):
        if r != row and cards[r, col][0] == '*':
            loc = str(r) + str(col)
            if loc not in new_removed:
                new_removed[loc] = [number]
            elif number not in new_removed[loc]:
                new_removed[loc].append(number)
                if len(new_removed[loc]) == n:
                    return None
    return new_removed


def solve_sudoku(cards, colors, colors_removed_from_dom, numbers_removed_from_dom):
    l = [0, 0]
    cards_temp = deepcopy(cards)
    if(not find_unassigned_block(cards_temp, l, colors_removed_from_dom)):
        return True
    row = l[0]
    col = l[1]
    print(row, col)
    #print(numbers_removed_from_dom)
    last_num = cards[row, col][0]
    last_color = cards[row, col][1]
    for num in range(1, n+1):
        loc = str(row) + str(col)
        mark = False
        if loc in numbers_removed_from_dom:
            if num in numbers_removed_from_dom[loc]:
                mark = True
        if mark == False:
            print(numbers_removed_from_dom)
            updated_removed_number_dom = deepcopy(numbers_removed_from_dom)
            for color in colors:
                updated_removed_color_dom = deepcopy(colors_removed_from_dom)
                mark = False
                if loc in colors_removed_from_dom: 
                    if color in colors_removed_from_dom[loc]:
                        mark = True
                if mark == False:
                    new_num = None
                    new_color = None
                    validity = check_location_is_safe(cards, row, col, num, color)
                    if validity[0] and cards[row, col][0] == '*':
                        new_num = str(num)
                        cards_temp = deepcopy(cards)
                        updated_removed_number_dom = remove_numbers_from_dom(cards_temp, numbers_removed_from_dom, row, col, num)
                        if updated_removed_number_dom is None:   
                            continue
                   
                    if validity[1] and cards[row, col][1] == '#':
                        new_color = color
                        cards_temp = deepcopy(cards)
                        updated_removed_color_dom = remove_color_from_dom(cards_temp, colors_removed_from_dom, row, col, color)
                        if updated_removed_color_dom is None:
                            continue
                    
                    #print(updated_removed_color_dom)
                    if new_color is None and new_num is None:
                        continue
                    elif new_color is None and new_num is not None:
                        value = str(new_num) + cards[row, col][1]
                        cards[row, col] = value
                        if solve_sudoku(cards, colors, updated_removed_color_dom, updated_removed_number_dom):
                            return True
                    elif new_color is not None and new_num is None:
                        value = cards[row, col][0] + new_color
                        cards[row, col] = value
                        if solve_sudoku(cards, colors, updated_removed_color_dom, updated_removed_number_dom):
                            return True
                    else:
                        value = new_num + new_color
                        cards[row, col] = value
                        if solve_sudoku(cards, colors, updated_removed_color_dom, updated_removed_number_dom):
                            return True
                cards[row, col] = last_num + last_color
            cards[row, col] = last_num + last_color

    return False

if __name__=="__main__":
    main()