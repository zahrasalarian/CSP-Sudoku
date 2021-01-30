# def isValid(i, j, x, board):
#     # check row
#     for col in range(9):
#         if board[i][col] == x:
#             return False
#
#     # check column
#     for row in range(9):
#         if board[row][j] == x:
#             return False
#
#     # check block
#     startrow = i - i % 3
#     startcol = j - j % 3
#
#     p = startrow
#     while p <= startrow + 2:
#         l = startcol
#         while l <= startcol + 2:
#             if board[p][l] == x:
#                 return False
#             l += 1
#         p += 1
#
#     return True
#
#
# def solveSudokuHelper(i, j, board):
#     if i == 8 and j == 8:
#         if board[i][j] != 0:
#             for row in board:
#                 for ele in row:
#                     print(ele, end=" ")
#                 print()
#         else:
#             for x in range(1, 10):
#                 if isValid(i, j, x, board) is True:
#                     board[i][j] = x
#                     for row in board:
#                         for ele in row:
#                             print(ele, end=" ")
#                         print()
#                     board[i][j] = 0
#         print()
#         return
#
#     if j > 8:
#         solveSudokuHelper(i + 1, 0, board)
#         return
#
#     if board[i][j] == 0:
#         for x in range(1, 10):
#             if isValid(i, j, x, board) is True:
#                 board[i][j] = x
#                 solveSudokuHelper(i, j + 1, board)
#                 board[i][j] = 0
#     else:
#         solveSudokuHelper(i, j + 1, board)
#     return
#
#
# def solveSudoku(board):
#     solveSudokuHelper(0, 0, board)
#
#
# board = []
# for i in range(9):
#     print("Enter space separated elements of row {}".format(i))
#     row = [int(x) for x in input().strip().split()]
#     board.append(row)
# print()
# solveSudoku(board)

r = 're'
new = r[0] + 'a'
print(new)