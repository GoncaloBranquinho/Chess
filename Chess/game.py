from logic import Logic
from player import Player
from chessboard import Chessboard
from constants import * 
import random
import time

 
class Game:
    def __init__(self) -> None:
        self.player = Player("Undefined")
        self.board = Chessboard()
        self.logic = Logic("None")
        self.opositeColor = {"White": "Black",
                             "Black": "White"}
        self.main()
    
    def main(self):
        # initialize the game
        self.board.initialize()
        self.board.draw()
        turn = 2
        while (True):
            # time.sleep(0.5)

            if turn % 2 == 0:
                self.player.color = "White"
            else:
                self.player.color = "Black"
            
            self.logic.toMoveColor = self.player.color
            self.logic.moves = []
            self.logic.valid_moves = []
            self.logic.table = self.board.table
            
            if self.logic.insufficientMaterial() or self.logic.drawnByRepetition():
                print("  The game ends in a draw")
                break
            
            self.logic.generate_moves()        
            
            if self.logic.game_over():
                break
            
            else:
                if self.logic.kingInCheck():
                    self.logic.give_hint()
                while(True):
                    # (self.logic.x1, self.logic.y1, self.logic.x2, self.logic.y2) = random.choice(self.logic.valid_moves) # Uncomment this line to get random choices
                    self.logic.x1, self.logic.y1, self.logic.x2, self.logic.y2 = self.player.get_input(self.board.table) # Comment this line to get random choices
                    self.logic.updateCastling()
                    self.logic.printInfo()
                    x1, y1, x2, y2 = self.logic.x1, self.logic.y1, self.logic.x2, self.logic.y2

                    if (x1,y1,x2,y2) in self.logic.valid_moves:
                            self.logic.trackPreviousMove[self.opositeColor[self.player.color]] = "None"
                            self.logic.updatePieceMovements()
                            moved = self.board.table[x1][y1]
                            if (x2 == MAX_HEIGHT and moved == B_PAWN) or (x2 == MIN_HEIGHT and moved == W_PAWN):
                                self.logic.pawn_reach_end()
                            else:    
                                self.board.table[x2][y2] = moved
                                self.board.table[x1][y1] = " "
                            self.board.draw()
                            turn += 1 
                            break
                    else:
                        print("  Invalid Move, play again\n")

Game()