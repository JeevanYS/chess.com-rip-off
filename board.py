from pieces import *
from legalities import LegRook, LegKnight, LegBishop, LegPawn, LegKing, LegCastling, is_in_check, is_in_checkmate, checkLegal
from popup import *
import copy
from stockfish import Stockfish

stockfish = Stockfish(path="stockfish")

class Board:
    def __init__(self,mode,botrating,ty):
        if(mode=='bot' and ty!='undo'):
            self.brate = botrating
            stockfish.set_elo_rating(botrating)
            #print(f"Bot Rating Set to: {botrating}")
        self.default_board = [['qr', 'n', 'b', 'q', 'k', 'b', 'n', 'kr'],
                                ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                [' ', ' ', ' ', ' ', ' ', ' ', ' ', ' '],
                                ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                                ['QR', 'N', 'B', 'Q', 'K', 'B', 'N', 'KR']]
        self.board = self.default_board
        self.moves = 0
        self.history=[]
        if ty!='undo':
            self.promotion_list=[]
            self.count=0
        for i in range(len(self.default_board)):
            for j in range(len(self.default_board[i])):
                if(i <= 1):
                   team = 0
                elif(i>=6):
                    team = 1
                else:
                    team = 2
                self.default_board[i][j] = Pieces(self.default_board[i][j], team)

    def get(self,x1,y1):
        return self.board[y1][x1]
    
    def get_eval(self):
        return stockfish.get_evaluation()

    def getFen(self):
        fen = ""
        for i in range(len(self.board)):
            for j in self.board[i]:
                fen+=j.code
            if i<len(self.board):
                fen+="/"
        for i in range(8,0,-1):
            fen = fen.replace(" "*i, str(i))
        fen = fen.replace("qr","r")
        fen = fen.replace("kr","r")
        fen = fen.replace("QR","R")
        fen = fen.replace("KR","R")
        return fen[:-1]
    
    def rec_history(self,x1,y1,x2,y2,piece,is_prom='no'):
        self.history.append([x1, y1, x2, y2, piece,is_prom])
        #print(self.history)
        
    def reset(self,mode,ty,brat=0):
        self.brate = brat
        if(mode=='bot'):
            self.__init__(mode,self.brate,ty)
        elif(mode=='p&p'):
            self.__init__(mode,0,ty)
        
    def undo(self,mode,col,legal):
        #print("="*40)
        l = len(self.history)
        if(l==1 and col=='w'):
            self.history.pop()
            if mode == 'bot':
                self.reset(mode,'undo')
            else:
                self.reset(mode,'undo',self.brate)
        elif(l>0):
            if self.history[l-1][5]=='yes':
                self.promotion_list.pop()
            self.history.pop()
            if(mode=='bot' and l>0 and legal=='NC'):
                self.history.pop()
            self.h=copy.deepcopy(self.history)
            self.reset(mode,'undo')
            for i in range(len(self.h)):
                #print("-"*40)
                self.edit(self.h[i][0],self.h[i][1],self.h[i][2],self.h[i][3],"undo",mode)
            self.count=0

            #print("="*40)
            
    def edit(self, x1, y1, x2, y2,ty,mode,col='b'):
        
        if(self.moves%2==1 and ty!="undo" and mode=="bot" and col=='b'):
            gf = self.getFen()
            stockfish.set_fen_position(gf+" b")
            x1,y1,x2,y2=self.move(stockfish.get_best_move())
            if (x1,x2,y1,y2)==0:
                return 'GO'
            #print(gf)
        elif(self.moves%2==0 and ty!="undo" and mode=="bot" and col=='w'):
            gf = self.getFen()
            stockfish.set_fen_position(gf+" w")
            x1,y1,x2,y2=self.move(stockfish.get_best_move())
            if (x1,x2,y1,y2)==0:
                return 'GO'
            #print(gf)
            
        piece = self.board[y1][x1]
        t_piece = self.board[y2][x2]
        cl=checkLegal(self,x1,y1,x2,y2, piece,self.moves,self.history)  
        
        if(cl==3): #Castling
            if(is_in_check(self,self.moves+1) and ty!="undo"):
                return False
            self.board[y2][x2-1 if x1<x2 else x2+1] = Pieces(piece.code, piece.team)
            self.board[y2][x2-2 if x1<x2 else x2+2] = Pieces(t_piece.code, t_piece.team)
            self.board[y2][x2] = Pieces(" ", 2)
            self.board[y1][x1] = Pieces(" ", 2)
            self.moves += 1
            self.rec_history(x1,y1,x2,y2,piece.code)
            if(is_in_check(self,self.moves) and ty!="undo"):
                cm=is_in_checkmate(self,self.moves,self.history)
                if cm:
                    self.undo(mode, col,'C')
                    return 'GO'
                self.undo(mode, col,'C')
                return False
            
        elif(cl==4): #En Passant
            self.board[y2][x2] = Pieces(piece.code, piece.team)
            self.board[y1][x1] = Pieces(" ", 2)
            self.board[y1][x2] = Pieces(" ", 2)
            self.moves += 1
            self.rec_history(x1,y1,x2,y2,piece.code)
            if(is_in_check(self,self.moves) and ty!="undo"):
                cm=is_in_checkmate(self,self.moves,self.history)
                if cm:
                    self.undo(mode, col,'C')
                    return 'GO'
                self.undo(mode, col,'C')
                return False
            
        elif(cl==5): #Pawn Promotion
            if ty!='undo':
                self.board[y2][x2] = Pieces(promotion_popup(piece.team), piece.team)
                self.promotion_list.append(self.board[y2][x2])
                '''for i in self.promotion_list:
                    print(i.code,end=',')
                print()'''
            if(ty=='undo'):
                self.count+=1
                self.board[y2][x2]=self.promotion_list[self.count-1]
            self.board[y1][x1] = Pieces(" ", 2)
            self.moves += 1
            self.rec_history(x1,y1,x2,y2,self.board[y2][x2].code,'yes')
            if(is_in_check(self,self.moves) and ty!="undo"):
                cm=is_in_checkmate(self,self.moves,self.history)
                if cm:
                    self.undo(mode, col,'C')
                    return 'GO'
                self.undo(mode, col,'C')
                return False
            
        elif(cl): #Normal
            self.board[y2][x2] = Pieces(piece.code, piece.team)
            self.board[y1][x1] = Pieces(" ", 2)
            self.moves += 1
            self.rec_history(x1,y1,x2,y2,piece.code)
            if(is_in_check(self,self.moves) and ty!="undo"):
                cm=is_in_checkmate(self,self.moves,self.history)
                if piece.code.lower()=='k' and cm==False:
                    self.undo(mode,col,'C')
                    cm=is_in_checkmate(self,self.moves+1,self.history)
                    if cm:
                        return'GO'
                if cm:
                    self.undo(mode, col,'C')
                    return 'GO'
                self.undo(mode, col,'C')
                return False
        if(self.moves%2==1 and ty!="undo" and mode=="bot" and col=="b"):
            self.edit(x1, y1, x2, y2,"normal",mode,col)
        elif(self.moves%2==0 and ty!="undo" and mode=="bot" and col=="w"):
            self.edit(x1, y1, x2, y2,"normal",mode,col)
            
    def move(self, s:str):
        if s is None:   #Stockfish returning NULL value --> Bot Defeated
            return 0,0,0,0
        #print(self.moves)
        return int(ord(s[0])-96)-1, 8-int(s[1]), int(ord(s[2])-96)-1, 8-int(s[3])
    
