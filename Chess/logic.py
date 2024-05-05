from constants import *
import random
class Logic:
    def __init__(self,table):
        self.table = table
        self.x1 = -1
        self.y1 = -1
        self.x2 = -1
        self.y2 = -1
        self.moves = []
        self.fifty_move_counter = 0
        self.valid_moves = []
        self.has_RookL_moved_White = False
        self.has_RookR_moved_White = False
        self.has_RookL_moved_Black = False
        self.has_RookR_moved_Black = False
        self.has_KingW_moved = False
        self.has_KingB_moved = False
        self.toMoveColor = "None"
        self.opositeColor = {"White": "Black",
                             "Black": "White",
                             " ": "Ignore"}
        self.choose = {
            W_PAWN: self.wpawn,
            W_KNIGHT: self.knight,
            W_KING: self.king,
            W_QUEEN: self.queen,
            W_ROOK: self.rook,
            W_BISHOP: self.bishop,
            B_PAWN: self.bpawn,
            B_KNIGHT: self.knight,
            B_KING: self.king,
            B_QUEEN: self.queen,
            B_ROOK: self.rook,
            B_BISHOP: self.bishop,
        }
        self.can_cast = {
            "White": True,
            "Black": True
        }
        self.trackPreviousMove = {
            "White": "None",
            "Black": "None"    
        }
        self.fens = {}
    
    def generate_moves(self):
        for i, row in enumerate(self.table):
            for j, piece in enumerate(row):
                if self.getPieceColor(piece) == self.toMoveColor :
                    self.x1, self.y1,= i, j
                    piece_type = self.table[self.x1][self.y1]
                    self.choose[piece_type]()         
        self.notInCheckMoves()
    
    def drawnByRepetition(self):
        position = ""
        for row in self.table:
            for piece in row:
                color = self.getPieceColor(piece)
                if color == "Black" or color == "White" or piece == " ":
                    position += piece
        if position in self.fens:
            self.fens[position] += 1
            if self.fens[position] == 3:
                return True
        else:
            self.fens[position] = 1
        return False
    
    def game_over(self):
        if self.valid_moves == []:
            for i, row in enumerate(self.table):
                for j, piece in enumerate(row):
                    if (piece == W_KING and self.toMoveColor == "White") or (piece == B_KING and self.toMoveColor == "Black"):
                        self.x = i
                        self.y = j
            if self.king_safe():
                print("  The game ends in a stalemate!")
                
            else:
                print(f'  {self.opositeColor[self.toMoveColor]} pieces win!!')
            return True 
        return False
            
    def updateCastling(self):
        if self.can_cast[self.toMoveColor]:
            self.can_cast["Black"] = False if self.has_KingB_moved else True
            self.can_cast["White"] = False if self.has_KingW_moved else True
            if self.validCastling():
                self.can_cast[self.toMoveColor] = False               
         

    def insufficientMaterial(self):
        counter = 0
        for row in self.table:
            for piece in row:
                if piece == W_KING or piece == B_KING:
                    counter += 1
                elif self.getPieceColor(piece) == "White" or self.getPieceColor(piece) == "Black":
                    counter += 1 
        if counter == 2 or self.fifty_move_counter == 100:
            return True 
        return False 
    
    def updatePieceMovements(self):
        piece = self.table[self.x1][self.y1]
        if piece == W_ROOK:
            if self.y1 == MAX_WIDTH:
                self.has_RookR_moved_White = True
            else:
                self.has_RookL_moved_White = True
        elif piece == B_ROOK:
            if self.y1 == MAX_WIDTH:
               self.has_RookR_moved_Black = True
            else:
                self.has_RookL_moved_Black = True 
        elif piece == W_KING:
            self.has_KingW_moved = True
        elif piece == B_KING:
            self.has_KingB_moved = True
    
    def validCastling(self): 
        if self.y2 == (MAX_WIDTH - 1) and ((not self.has_KingW_moved and (not self.has_RookR_moved_White)) or (not self.has_KingB_moved and (not self.has_RookR_moved_Black))):
            moved = self.table[self.x1][self.y1]
            target = self.table[self.x2][self.y2+1]
            if ((moved == W_KING and target == W_ROOK) or (moved == B_KING and target == B_ROOK)): 
                directions = [(0,1),(0,2)]
                for c1, c2 in directions:
                    self.x = self.x1 + c1
                    self.y = self.y1 + c2
                    possibleMove = self.table[self.x][self.y] 
                    if possibleMove != " " or (not self.king_safe()):
                        break
                else:
                    self.table[self.x1][self.y1+1] = target
                    self.table[self.x1][self.y2+1] = " "
                    self.valid_moves.append((self.x1,self.y1,self.x2,self.y2))
                    return True
        
        elif self.y2 == (MIN_WIDTH + 1) and ((not self.has_KingW_moved and not self.has_RookL_moved_White) or (not self.has_KingB_moved and not self.has_RookL_moved_Black)):
            moved = self.table[self.x1][self.y1]
            target = self.table[self.x2][self.y2-1]
            if ((moved == W_KING and target == W_ROOK) or (moved == B_KING and target == B_ROOK)): 
                directions = [(0,-1),(0,-2),(0,-3)]
                for c1, c2 in directions:
                    self.x = self.x1 + c1
                    self.y = self.y1 + c2
                    possibleMove = self.table[self.x][self.y]
                    if possibleMove != " " or (not self.king_safe()):
                        break
                else:
                    self.table[self.x1][self.y1-2] = moved
                    self.table[self.x1][self.y1-1] = target
                    self.table[self.x1][self.y1] = " "
                    self.table[self.x2][self.y2-1] = " "
                    self.valid_moves.append((self.x1,self.y1,self.x2,self.y2))
                    return True
        return False
    
    def getPieceColor(self, piece):
        if piece in [W_ROOK, W_KNIGHT, W_BISHOP, W_QUEEN, W_KING, W_PAWN]:
            return "White"
        elif piece in [B_ROOK, B_KNIGHT, B_BISHOP, B_QUEEN, B_KING, B_PAWN]:
            return "Black"
        return " "
        

    def king_safe(self):

        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for c1, c2 in directions:
            x = self.x + c1
            y = self.y + c2
            while MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color != self.toMoveColor and (target == B_QUEEN or target == W_QUEEN or target == B_ROOK or target == W_ROOK):
                    return False
                elif target != " ":
                    break
                x += c1 
                y += c2 
    
        
        directions = [(1,1),(-1,-1),(-1,1),(1,-1)]
        for c1, c2 in directions:
            x = self.x + c1
            y = self.y + c2
            while MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color != self.toMoveColor and (target == B_QUEEN or target == W_QUEEN or target == B_BISHOP or target == W_BISHOP):
                    return False
                elif target != " ":
                   break
                x += c1 
                y += c2
                        

        if (self.toMoveColor == "White"):
            x = self.x - 1
            y = self.y + 1
            if (y <= MAX_WIDTH and x >= MIN_HEIGHT and self.table[x][y] == B_PAWN):
                return False
            x = self.x - 1
            y = self.y - 1
            if (y >= MIN_WIDTH and x >= MIN_HEIGHT and self.table[x][y] == B_PAWN):
                return False
        
        if (self.toMoveColor == "Black"):
            x = self.x + 1
            y = self.y + 1
            if (y <= MAX_WIDTH and x <= MAX_HEIGHT and self.table[x][y] == W_PAWN):
                return False
            x = self.x + 1
            y = self.y - 1
            if (y >= MIN_WIDTH and x <= MAX_HEIGHT and self.table[x][y] == W_PAWN):
                return False
        
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for c1, c2 in directions:
            x = self.x + c1
            y = self.y + c2
            if MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color != self.toMoveColor and (target == W_KNIGHT or target == B_KNIGHT):
                    return False
        return True
    
    
    def notInCheckMoves(self):
        self.valid_moves = []
        for move in self.moves:
            moved = self.table[move[0]][move[1]]
            target = self.table[move[2]][move[3]]
            self.table[move[2]][move[3]] = moved
            self.table[move[0]][move[1]] = " "
            for i, row in enumerate(self.table):
                for j, piece in enumerate(row):
                    if (piece == W_KING and self.toMoveColor == "White") or (piece == B_KING and self.toMoveColor == "Black"):
                        self.x = i
                        self.y = j
            if self.king_safe():
                self.valid_moves.append(move) 
            self.table[move[0]][move[1]] = moved
            self.table[move[2]][move[3]] = target
        
        
            

    def wpawn(self):
        
        if self.x1 == (MAX_HEIGHT - 1) and self.table[self.x1-1][self.y1] == " " and self.table[self.x1-2][self.y1] == " ":
            self.moves.append((self.x1, self.y1, self.x1-2, self.y1))
        
        if self.x1 > MIN_HEIGHT and self.table[self.x1-1][self.y1] == " ":
            self.moves.append((self.x1, self.y1, self.x1-1, self.y1)) 
            
        directions = [(-1,-1),(-1,1)]
        for c1, c2 in directions:
            x = self.x1 + c1
            y = self.y1 + c2
            if MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if target != W_KING and target!= B_KING and piece_color == "Black":
                    self.moves.append((self.x1, self.y1 , x, y))
                
                    

    
        
    def bpawn(self):
        
        if self.x1 == (MIN_HEIGHT + 1) and self.table[self.x1+1][self.y1] == " " and self.table[self.x1+2][self.y1] == " ":
                self.moves.append((self.x1, self.y1, self.x1+2, self.y1))
                
        if self.x1 < MAX_HEIGHT and self.table[self.x1+1][self.y1] == " ":
            self.moves.append((self.x1, self.y1, self.x1+1, self.y1)) 
        
        directions = [(1,-1),(1,1)]
        for c1, c2 in directions:
            x = self.x1 + c1
            y = self.y1 + c2
            if MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if target != W_KING and target != B_KING and piece_color == "White":
                    self.moves.append((self.x1, self.y1 , x, y))
                
    
    
    def operateEnPassand(self):
        
        if (self.x2,self.y2) == (self.x1+2,self.y1) and (self.x1 == MIN_HEIGHT + 1) and self.table[self.x1][self.y1] == B_PAWN:
            self.trackPreviousMove["Black"] = (self.x1+2,self.y1)
        if (self.x2,self.y2) == (self.x1-2,self.y1) and (self.x1 == MAX_HEIGHT - 1) and self.table[self.x1][self.y1] == W_PAWN:
            self.trackPreviousMove["White"] = (self.x1-2,self.y1) 
        
        moved = self.table[self.x1][self.y1]
        target = self.table[self.x2][self.y2]
        turn = self.opositeColor[self.toMoveColor]
        
        if self.trackPreviousMove[turn] != "None" and ((self.x1 - self.x2 == 1 and self.toMoveColor == "White") or (self.x2 - self.x1 == 1 and self.toMoveColor == "Black")):
            (x,y) = self.trackPreviousMove[turn]
            if abs(x - self.x2) == 1 and y == self.y2 and self.y2 != self.y1:
                self.piecetype = self.table[x][y]
                self.table[x][y] = " "
                self.table[self.x2][self.y2] = moved
                self.table[self.x1][self.y1] = " "
                if not self.kingInCheck():
                    self.valid_moves.append((self.x1,self.y1,self.x2,self.y2))
                    self.table[self.x1][self.y1] = moved
                    self.table[self.x2][self.y2] = target
                    
                    return True
                self.table[self.x1][self.y1] = moved
                self.table[self.x2][self.y2] = target
        
        return False
                         

    
    def knight(self):
        
        directions = [(2,1),(2,-1),(-2,1),(-2,-1),(1,2),(1,-2),(-1,2),(-1,-2)]
        for c1, c2 in directions:
            x = self.x1 + c1
            y = self.y1 + c2
            if MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                piece = self.table[x][y]
                piece_color = self.getPieceColor(piece)
                if piece_color != self.toMoveColor and piece != W_KING and piece != B_KING:
                    self.moves.append((self.x1, self.y1, x, y))
   
    
    def rook(self):
        
        directions = [(1,0),(-1,0),(0,1),(0,-1)]
        for c1, c2 in directions:
            x = self.x1 + c1 
            y = self.y1 + c2
            while MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color == " " and target != W_KING and target != B_KING:
                    self.moves.append((self.x1, self.y1, x, y))
                    x += c1
                    y += c2
                elif piece_color == self.opositeColor[self.toMoveColor] and target != W_KING and target != B_KING:
                    self.moves.append((self.x1, self.y1, x, y))
                    break
                else:
                    break
        
   
    def bishop(self):
        directions = [(-1,1),(1,1),(-1,-1),(1,-1)]
        for c1, c2 in directions:
            x = self.x1 + c1
            y = self.y1 + c2
            while MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color == " " and target != W_KING and target != B_KING:
                    self.moves.append((self.x1, self.y1, x, y))
                    x += c1
                    y += c2
                elif piece_color == self.opositeColor[self.toMoveColor] and target != W_KING and target != B_KING:
                    self.moves.append((self.x1, self.y1, x, y))
                    break
                else:
                    break


    def queen(self):
        self.rook()
        self.bishop()

   
    def king(self):
        directions = [(1,0),(-1,0),(0,-1),(0,1),(1,1),(-1,-1),(1,-1),(-1,1)]
        for c1, c2 in directions:
            x = self.x1 + c1
            y = self.y1 + c2
            flag = 1
            if MIN_HEIGHT <= x <= MAX_HEIGHT and MIN_WIDTH <= y <= MAX_WIDTH:
                target = self.table[x][y]
                piece_color = self.getPieceColor(target)
                if piece_color != self.toMoveColor and target != W_KING and target != B_KING:
                    for c3, c4 in directions:
                        i = x + c3
                        j = y + c4
                        if MIN_HEIGHT <= i <= MAX_HEIGHT and MIN_WIDTH <= j <= MAX_WIDTH:
                            target1 = self.table[i][j]
                            if (self.toMoveColor == "White" and target1 == B_KING) or (self.toMoveColor == "Black" and target1 == W_KING):
                                flag = 0
                    if flag:
                        self.moves.append((self.x1,self.y1,x,y))     
        
    def pawn_reach_end(self):
        promote = {
        "White": [W_KNIGHT, W_QUEEN, W_ROOK, W_BISHOP],
        "Black": [B_KNIGHT, B_QUEEN, B_ROOK, B_BISHOP]
        }
        self.table[self.x1][self.y1] = " "
        # userInput = random.choice([1,2,3,4]) # Uncomment this line to get random choices
        userInput = int(input("  Promote to any of these pieces.\n  1: Knight\n  2: Queen\n  3: Rook\n  4: Bishop\n  Type the number: ")) # comment this line to get random choices
        self.table[self.x2][self.y2] = promote[self.toMoveColor][userInput-1]
    
    def kingInCheck(self):
        for i, row in enumerate(self.table):
            for j, piece in enumerate(row):
                if (piece == W_KING and self.toMoveColor == "White") or (piece == B_KING and self.toMoveColor == "Black"):
                    self.x = i
                    self.y = j
        if not self.king_safe():
            return True
        return False        
    
    def give_hint(self):
        valid = self.convert()
        print(f'  Your king is in check!\n  Available moves:\n  {valid}')

    def convert(self):
        valid = []
        for move in self.valid_moves:
            valid.append((chr(move[1] + ord('A') - 1) + str(8 - move[0])) + "-" + ((chr(move[3] + ord('A') - 1)) + str(8 - move[2])))
        return valid
    
    def printInfo(self):
        moved = self.table[self.x1][self.y1]
        target = self.table[self.x2][self.y2]
        self
        if self.operateEnPassand():
            target = self.piecetype
        
        capturedPiece = "None" if target == " " else target
        movedPiece = "None" if moved == " " else moved
        if capturedPiece == "None" and (movedPiece != B_PAWN and movedPiece != W_PAWN):
            self.fifty_move_counter += 1
        else:
            self.fifty_move_counter = 0
        print(f'  Moved: {movedPiece} {RESET_COLOR}  Captured: {capturedPiece} {RESET_COLOR}')

   
    