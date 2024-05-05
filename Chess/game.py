from logic import Logic
from player import Player
from chessboard import Chessboard
from constants import * 
import random
import time

 
class Game:
 def main():
        # initialize the game
        player = Player("Undefined")
        board = Chessboard()
        logic = Logic("None")
        board.initialize()
        board.draw()
        opositeColor = {"White": "Black",
                        "Black": "White"}
        turn = 2
        # loop that runs the whole game
        while (True):
            # time.sleep(0.5)
            # decide whose turn is
            if turn % 2 == 0:
                player.color = "White"
            else:
                player.color = "Black"
            # update variables values
            logic.toMoveColor = player.color
            logic.moves = []
            logic.valid_moves = []
            logic.table = board.table
            
            # look for a possible draw or stalemate
            if logic.insufficientMaterial() or logic.drawnByRepetition():
                print("  The game ends in a draw")
                break
            
            # get all possible moves for the respective player
            logic.generate_moves()        
            
            if logic.game_over():
                break
            
            else:
                # if king is in check it will print the possible moves, as a little hint to the player
                if logic.kingInCheck():
                    logic.give_hint()
                while(True):
                    # get either input or random moves
                    # (logic.x1, logic.y1, logic.x2, logic.y2) = random.choice(logic.valid_moves) # Uncomment this line to get random choices
                    logic.x1, logic.y1, logic.x2, logic.y2 = player.get_input(board.table) # Comment this line to get random choices
                    # update castling and en passant according to the input
                    logic.updateCastling()
                    logic.printInfo()
                    x1, y1, x2, y2 = logic.x1, logic.y1, logic.x2, logic.y2
                    # update chessboard
                    if (x1,y1,x2,y2) in logic.valid_moves:
                        logic.trackPreviousMove[opositeColor[player.color]] = "None"
                        logic.updatePieceMovements()
                        moved = board.table[x1][y1]
                        # also updates the chessboard in case of promotion
                        if (x2 == MAX_HEIGHT and moved == B_PAWN) or (x2 == MIN_HEIGHT and moved == W_PAWN):
                            logic.pawn_reach_end()
                        else:    
                            board.table[x2][y2] = moved
                            board.table[x1][y1] = " "
                        board.draw()
                        turn += 1 
                        break
                    else:
                        print("  Invalid Move, play again\n")

    main()
