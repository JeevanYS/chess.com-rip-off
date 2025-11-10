#legalities.py
from pieces import *

'''
0 - black
1 - white
2 - empty
i - y-axis
j - x-axis
'''

def LegRook(board, x1, y1, x2, y2):
    
    if board.board[y2][x2].team == 2 or board.board[y2][x2].team != board.board[y1][x1].team:
        if x1 == x2:
            for i in range(min(y1, y2) + 1, max(y1, y2)):
                if board.board[i][x1].team != 2:
                    return False  # Piece in between
            return True
        elif y1 == y2:
            for i in range(min(x1, x2) + 1, max(x1, x2)):
                if board.board[y1][i].team != 2:
                    return False  # Piece in between
            return True  
    return False
        
def LegKnight(board, x1, y1, x2, y2):
    
    x_step = abs(x2 - x1)
    y_step = abs(y2 - y1)
    if x1 == x2 or y1 == y2:
        return False  # Knights don't move in straight lines
    if x_step + y_step == 3:
        if board.board[y2][x2].team != board.board[y1][x1].team:
            return True
    return False

def LegBishop(board, x1, y1, x2, y2):
    piece_team = board.board[y1][x1].team
    target_team = board.board[y2][x2].team

    if piece_team == target_team:
        return False
    
    if abs(x2 - x1) != abs(y2 - y1):  # Bishop must move diagonally
        return False

    x_step = 1 if x2 > x1 else -1
    y_step = 1 if y2 > y1 else -1

    x, y = x1 + x_step, y1 + y_step
    while x != x2 and y != y2:
        if board.board[y][x].team != 2:  # If not empty, path is blocked
            return False
        x += x_step
        y += y_step

    return True

def LegPawn(board, x1, y1, x2, y2):
    piece_team = board.board[y1][x1].team
    target_team = board.board[y2][x2].team

    if piece_team == target_team:
        #print("Trying to attack own piece")
        return False

    if piece_team == 1:  # White Pawn
        if y2 == y1 - 1 and x1 == x2 and target_team == 2:
            return 5 if y2==0 else True  # Normal Move
        elif y2 == y1 - 2 and x1 == x2 and y1 == 6 and board.board[y1 - 1][x1].team == 2 and target_team == 2:
            return 1  # First Move (2 Steps)
        elif y1==3 and y2==2 and abs(x2-x1)==1 and board.board[y1][x2].code.lower() == "p" and target_team == 2:
            return 4 # En passant
        elif y2 == y1 - 1 and abs(x2 - x1) == 1 and target_team == 0:
            return 5 if y2==0 else 1 # Capture Move - 5 for Pawn Promotion, 1 for normal Capture

    elif piece_team == 0:  # Black Pawn
        if y2 == y1 + 1 and x1 == x2 and target_team == 2:
            return 5 if y2==7 else 1 # Normal Move
        elif y2 == y1 + 2 and x1 == x2 and y1 == 1 and board.board[y1 + 1][x1].team == 2 and target_team == 2:
            return 1 # First Move (2 Steps)
        elif y1==4 and y2==5 and abs(x2-x1)==1 and board.board[y1][x2].code.lower() == "p" and target_team == 2:
            return 4 # En passant
        elif y2 == y1 + 1 and abs(x2 - x1) == 1 and target_team == 1:
            return 5 if y2==7 else 1 # Capture Move - 5 for Pawn Promotion, 1 for normal Capture
    #print("Invalid Pawn Move!")
    return False

def LegCastling(board, x1, y1, x2, y2,his):
    for i in range(len(his)):
        if(board.board[y2][x2].code in his[i] or board.board[y1][x1].code in his[i]):
            return False
    if y1 == y2:
        for i in range(min(x1, x2) + 1, max(x1, x2)):
            if board.board[y1][i].team != 2:
                return False  # Piece in between
        return 3  
        
def LegKing(board, x1, y1, x2, y2):
    target_team = board.board[y2][x2].team
    piece_team = board.board[y1][x1].team
    if (target_team != piece_team):
        x_step = abs(x2 - x1)
        y_step = abs(y2 - y1)
        if x_step <= 1 and y_step <= 1:
            return True
    return False

def find_king(board, color):
    for i in range(8):
        for j in range(8):
            piece = board.board[i][j].code.lower()
            if piece == 'k' and board.board[i][j].team == color:
                return j, i  # x, y format

def is_in_check(board, turn):
    d_team = turn % 2
    king_pos = find_king(board, d_team)
    king_x, king_y = king_pos

    for i in range(8):
        for j in range(8):
            attacker = board.board[i][j]
            if attacker.team == d_team or attacker.team == 2:
                continue
            p = attacker.code.lower()
            
            if p == "q" and (LegBishop(board, j, i, king_x, king_y) or LegRook(board, j, i, king_x, king_y)):
                #print("Check by Q at", j, i)
                return True
            if p == "b" and LegBishop(board, j, i, king_x, king_y):
                #print("Check by B at", j, i)
                return True
            if p == "r" and LegRook(board, j, i, king_x, king_y):
                #print("Check by R at", j, i)
                return True
            if p == "n" and LegKnight(board, j, i, king_x, king_y):
                #print("Check by N at", j, i)
                return True
            if p == "p" and LegPawn(board, j, i, king_x, king_y):
                #print("Check by P at", j, i)
                return True
            if p == "k" and LegKing(board, j, i, king_x, king_y):
                #print("Check by K at", j, i)
                return True

    return False

def checkLegal(board, x1, y1, x2, y2, piece, moves,his):
        if(moves % 2 == 0 and piece.team != 1): return False
        if(moves % 2 == 1 and piece.team != 0): return False
        p=board.board[y2][x2].code.lower()
            
        if(board.board[y1][x1].team != board.board[y2][x2].team and p!='k'):
            if(piece.code.lower() == "n"):
                return LegKnight(board, x1,y1,x2,y2)
                
            elif(piece.code.lower() == "b"):
                return LegBishop(board, x1, y1, x2, y2)
                
            elif("r" in piece.code.lower()):
                return LegRook(board, x1, y1, x2, y2)
                
            elif(piece.code.lower() == "p"):
                return LegPawn(board, x1, y1, x2, y2)
                
            elif(piece.code.lower() == "q"):
                return (LegRook(board, x1, y1, x2, y2) or LegBishop(board, x1,y1,x2,y2))
                
            elif(piece.code.lower() == "k"):
                return LegKing(board, x1, y1, x2, y2)
            
        elif(board.board[y1][x1].team == board.board[y2][x2].team and 'r' in p and piece.code.lower() == "k"):
                return LegCastling(board, x1, y1, x2, y2,his)
            
        return False


import copy
def is_in_checkmate(board, turn, history):
    d_team = turn % 2
    for y1 in range(8):
        for x1 in range(8):
            piece = board.board[y1][x1]
            if piece.team != d_team:
                continue
            for y2 in range(8):
                for x2 in range(8):
                    if x1 == x2 and y1 == y2:
                        continue
                    if checkLegal(board, x1, y1, x2, y2, piece, turn+1, history):
                        temp_board = copy.deepcopy(board)
                        temp_board.board[y2][x2] = Pieces(piece.code, piece.team)
                        temp_board.board[y1][x1] = Pieces(" ", 2)
                        temp_board.moves = turn + 1
                        if not is_in_check(temp_board, turn):
                            #print(x1,y1,'->',x2,y2)
                            
                            return False  # Found a move that escapes check
    return True

    