#Nhut Ly - CS540
import random
import copy
import time

class TeekoPlayer:
    """ An object representation for an AI game player for the game Teeko.
    """
    board = [[' ' for j in range(5)] for i in range(5)]
    pieces = ['b', 'r']
    move_count = 0

    def __init__(self):
        """ Initializes a TeekoPlayer object by randomly selecting red or black as its
        piece color.
        """
        self.my_piece = random.choice(self.pieces)
        self.opp = self.pieces[0] if self.my_piece == self.pieces[1] else self.pieces[1]

    def make_move(self, state):
        """ Selects a (row, col) space for the next move. You may assume that whenever
        this function is called, it is this player's turn to move.

        Args:
            state (list of lists): should be the current state of the game as saved in
                this TeekoPlayer object. Note that this is NOT assumed to be a copy of
                the game state and should NOT be modified within this method (use
                place_piece() instead). Any modifications (e.g. to generate successors)
                should be done on a deep copy of the state.

                In the "drop phase", the state will contain less than 8 elements which
                are not ' ' (a single space character).

        Return:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

        Note that without drop phase behavior, the AI will just keep placing new markers
            and will eventually take over the board. This is not a valid strategy and
            will earn you no points.
        """
        
        drop_phase = True   
        # TODO: detect drop phase
        countB = 0
        countR = 0
        for row in range(5):
            for col in range(5):
                if state[row][col] == 'b':
                    countB = countB + 1
                if state[row][col] == 'r':
                    countR = countR + 1
        if (countB == 4 and countR == 4):
            drop_phase = False

       
            # TODO: choose a piece to move and remove it from the board
            # (You may move this condition anywhere, just be sure to handle it)
            #
            # Until this part is implemented and the move list is updated
            # accordingly, the AI will not follow the rules after the drop phase!

            # I WANNA MAKE A MOVE => MAXVALUE COMES IN (FIGURE OUT )
           
        _, state_max = self.max_value(state, 0)  

        # select an unoccupied space randomly
        # TODO: implement a minimax algorithm to play better
      
       
        #when start

        #extracting the move by comparing the difference between old state and new state
        moved_row = 0
        moved_col = 0
        old_row = 0
        old_col = 0
        
        for row in range(5):
            for col in range(5): 
                if(state[row][col] != state_max[row][col]):
                    if(state_max[row][col] == self.my_piece):
                        moved_row = row
                        moved_col = col
                       # print(state_max)
                        break
                    
        for row in range(5):
            for col in range(5):
                if(state[row][col] != state_max[row][col]):
                    if(state[row][col] == self.my_piece):
                        old_row = row
                        old_col = col
                        break 

        move = []


        # when the place is taken, keep looking for another place for the mark
        #while not state[row][col] == ' ':
            #(row, col) = (random.randint(0,4), random.randint(0,4))

        # ensure the destination (row,col) tuple is at the beginning of the move list
        if drop_phase:
            move.insert(0, (moved_row, moved_col))
        else:
            #print("old_row: "+str(old_row) + "   | old_col: "+str(old_col))
            #print("moved_row: "+str(moved_row) + " | moved_col: "+str(moved_col))
            
            move.insert(0, (old_row, old_col))
            move.insert(0, (moved_row, moved_col))

        return move

   
       
   
    def opponent_move(self, move):
        """ Validates the opponent's next move against the internal board representation.
        You don't need to touch this code.

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.
        """
        # validate input
        if len(move) > 1:
            source_row = move[1][0]
            source_col = move[1][1]
            if source_row != None and self.board[source_row][source_col] != self.opp:
                self.print_board()
                print(move)
                raise Exception("You don't have a piece there!")
            if abs(source_row - move[0][0]) > 1 or abs(source_col - move[0][1]) > 1:
                self.print_board()
                print(move)
                raise Exception('Illegal move: Can only move to an adjacent space')
        if self.board[move[0][0]][move[0][1]] != ' ':
            raise Exception("Illegal move detected")
        # make move
        self.place_piece(move, self.opp)

    def place_piece(self, move, piece):
        """ Modifies the board representation using the specified move and piece

        Args:
            move (list): a list of move tuples such that its format is
                    [(row, col), (source_row, source_col)]
                where the (row, col) tuple is the location to place a piece and the
                optional (source_row, source_col) tuple contains the location of the
                piece the AI plans to relocate (for moves after the drop phase). In
                the drop phase, this list should contain ONLY THE FIRST tuple.

                This argument is assumed to have been validated before this method
                is called.
            piece (str): the piece ('b' or 'r') to place on the board
        """
        if len(move) > 1:
            self.board[move[1][0]][move[1][1]] = ' '
        self.board[move[0][0]][move[0][1]] = piece

    def print_board(self):
        """ Formatted printing for the board """
        for row in range(len(self.board)):
            line = str(row)+": "
            for cell in self.board[row]:
                line += cell + " "
            print(line)
        print("   A B C D E")

    def game_value(self, state):
        """ Checks the current board status for a win condition

        Args:
        state (list of lists): either the current state of the game as saved in
            this TeekoPlayer object, or a generated successor state.

        Returns:
            int: 1 if this TeekoPlayer wins, -1 if the opponent wins, 0 if no winner

        TODO: complete checks for diagonal and box wins
        """
        # check horizontal wins
        for row in range(5):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row][col+2] == state[row][col+3]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        # check vertical wins
        for col in range(5):
            for row in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col] == state[row+2][col] == state[row+3][col]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        # TODO: check \ diagonal wins
        for row in range(2):
            for col in range(2):
                if state[row][col] != ' ' and state[row][col] == state[row-1][col+1] == state[row-2][col+2] == state[row-3][col+3]:
                    if state[row][col] == self.my_piece:
                        return 1 
                    else:
                        return -1

        # TODO: check / diagonal wins
        for row in range(2):
            for col in range(3, 4, 1):
                if state[row][col] != ' ' and state[row][col] == state[row+1][col-1] == state[row+2][col-2] == state[row+3][col-3]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1

        # TODO: check box wins
        for row in range(4):
            for col in range(4):
                if state[row][col] != ' ' and state[row][col] == state[row][col+1] == state[row+1][col] == state[row+1][col+1]:
                    if state[row][col] == self.my_piece:
                        return 1
                    else:
                        return -1
        
        # no winner yet
        return 0 

    def succ(self, state):

        # if drop
        #   give out successors
        # if continued
        #   give out successors
        # how to figure out which turn?
        countB = 0
        countR = 0
        successors = []
        moved_states = []
        drop_phase = True
        for row in range(5):
            for col in range(5):
                if state[row][col] == 'b':
                    countB = countB + 1
                if state[row][col] == 'r':
                    countR = countR + 1
                
        if(countB == 4 and countR == 4):
            drop_phase = False

        if drop_phase == True:
            # same as during continued phase?
            for row in range(5):
                for col in range(5):
                    
                    if state[row][col]==' ':
                        # successor = []
                        # successor.append(row)
                        # successor.append(col)
                        # successors.append(successor)
                        copied_state = copy.deepcopy(state)
                        copied_state[row][col] = self.my_piece
                        successors.append(copied_state)



        if drop_phase == False:
            for row in range(5):
                for col in range(5):
                    if state[row][col]==self.my_piece:
                        # tile above
                        if(row > 0):
                            if state[row-1][col]==' ':
                                # successor = []
                                # successor.append(row-1)
                                # successor.append(col)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # tile left
                        if(col > 0):
                            if state[row][col-1]==' ':
                                # successor = []
                                # successor.append(row)
                                # successor.append(col-1)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # tile below
                        if(row < len(state)-1):
                            if state[row+1][col]==' ':
                                # successor = []
                                # successor.append(row+1)
                                # successor.append(col)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # tile right
                        if(col < len(state[row])-1):
                            if state[row][col+1]==' ':
                                # successor = []
                                # successor.append(row)
                                # successor.append(col+1)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # diag upleft
                        if(row > 0 and col > 0):
                            if state[row-1][col-1]==' ':
                                # successor = []
                                # successor.append(row-1)
                                # successor.append(col-1)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # diag upright
                        if(row > 0 and col < len(state[col])-1):
                            if state[row-1][col+1]==' ':
                                # successor = []
                                # successor.append(row-1)
                                # successor.append(col+1)
                                # successors.append[successor]
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # diag lowleft
                        if(row < len(state)-1 and col > 0):
                            if state[row+1][col-1]==' ':
                                # successor = []
                                # successor.append(row+1)
                                # successor.append(col-1)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)
                        # diage lowright
                        if(row < len(state)-1 and col < len(state)-1):
                            if state[row+1][col+1]==' ':
                                # successor = []
                                # successor.append(row+1)
                                # successor.append(col+1)
                                # successors.append(successor)
                                copied_state = copy.deepcopy(state)
                                copied_state[row][col] = self.my_piece
                                successors.append(copied_state)

        return successors


    def heuristic_game_value(self, state):
        terminate = self.game_value(state)
        if terminate != 0:
            return terminate

        human_score = 0.0
        ai_score = 0.0
        #2 in a row
        for row in range(5):
            for col in range(2):
                if state[row][col]!=' ' and state[row][col] == state[row][col+1]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.4, ai_score)
                    else:
                        human_score=max(0.4, human_score)
                    # make sure score is negative

        #2 in a col
        for col in range(5):
            for row in range(2):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.4, ai_score)
                    else:
                        human_score=max(0.4, human_score)

        #3 in a row
        for row in range(5):
            for col in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row][col+1] == state[row][col+2]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.8, ai_score)
                    else:
                        human_score=max(0.8, human_score)
        
        #3 in a col
        for col in range(5):
            for row in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col] == state[row+2][col]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.8, ai_score)
                    else:
                        human_score=max(0.8, human_score)
        

        #2 in \ diag
        for row in range(4):
            for col in range(4):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col+1]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.4, ai_score)
                    else:
                        human_score=max(0.4, human_score)

        #2 in / diag
        for row in range(4):
            for col in range (4,0, -1):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col-1]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.4, ai_score)
                    else:
                        human_score=max(0.4, human_score)

        #3 in \ diag
        for row in range(3):
            for col in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col+1] == state[row+2][col+2]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.8, ai_score)
                    else:
                        human_score=max(0.8, human_score)

        #3 in / diag
        for row in range(3):
            for col in range(4,2):
                if state[row][col]!=' ' and state[row][col] == state[row][col-1] == state[row][col-2]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.8, ai_score)
                    else:
                        human_score=max(0.8, ai_score)

        #3 in a square case 1:
        #**
        #*
        for row in range(4):
            for col in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row][col+1] == state[row+1][col]:
                    if state[row][col]==self.my_piece:
                        ai_score=max(0.8, ai_score)
                    else:
                        human_score=max(0.8, human_score)

        #3 in a square case 2:
        #**
        # *
        for row in range(4):
            for col in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row][col+1] == state[row+1][col+1]:
                    ai_score=max(0.8, ai_score)
                else:
                    human_score=max(0.8, human_score)
        
        #3 in a square case 3:
        #*
        #**
        for row in range(4):
            for col in range(3):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col] == state[row+1][col+1]:
                    ai_score=max(0.8, ai_score)
                else:
                    human_score=max(0.8, human_score)
        
        #3 in a square case 4:
        # *
        #**
        for row in range(4):
            for col in range(1, 5):
                if state[row][col]!=' ' and state[row][col] == state[row+1][col-1] == state[row+1][col]:
                    ai_score=max(0.8, ai_score)
                else:
                    human_score=max(0.8, human_score)



        return ai_score-human_score #make sure it is between -1 and 1

    def max_value(self, state, depth):
        terminate = self.game_value(state)
        negative_infinity = float('-inf')
        max_s = []

        # include depth check
        # should return after going down layers of the tree => heuristic function, based on depth variable,
        if (terminate == 1 or terminate == -1):
            # return terminate value of s'
            return terminate, state
        elif (depth == 3):
            return self.heuristic_game_value(state), state
        
        else:
            depth+=1
            alpha = negative_infinity
            for s in self.succ(state):
                min,_ = self.min_value(state, depth) 
                if alpha < min:
                    alpha = min
                    max_s = s
        return alpha, max_s

    def min_value(self, state, depth):
        terminate = self.game_value(state)
        positive_infinity = float('inf')
        min_s =[]
        if (terminate == 1 or terminate == -1):
            return terminate, state
        
        elif (depth == 3):
            return self.heuristic_game_value(state), state
        else:
            depth+=1
            beta = positive_infinity
            for s in self.succ(state):
                max,_ = self.max_value(state, depth)
                if beta > max:
                    beta = max
                    min_s = s
        return beta, min_s

    

    

############################################################################
#
# THE FOLLOWING CODE IS FOR SAMPLE GAMEPLAY ONLY
#
############################################################################
def main():
    print('Hello, this is Samaritan')
    ai = TeekoPlayer()
    piece_count = 0
    turn = 0

    # drop phase
    while piece_count < 8 and ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved at "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                player_move = input("Move (e.g. B3): ")
                while player_move[0] not in "ABCDE" or player_move[1] not in "01234":
                    player_move = input("Move (e.g. B3): ")
                try:
                    ai.opponent_move([(int(player_move[1]), ord(player_move[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        piece_count += 1
        turn += 1
        turn %= 2

    # move phase - can't have a winner until all 8 pieces are on the board
    while ai.game_value(ai.board) == 0:

        # get the player or AI's move
        if ai.my_piece == ai.pieces[turn]:
            ai.print_board()
            move = ai.make_move(ai.board)
            ai.place_piece(move, ai.my_piece)
            print(ai.my_piece+" moved from "+chr(move[1][1]+ord("A"))+str(move[1][0]))
            print("  to "+chr(move[0][1]+ord("A"))+str(move[0][0]))
        else:
            move_made = False
            ai.print_board()
            print(ai.opp+"'s turn")
            while not move_made:
                move_from = input("Move from (e.g. B3): ")
                while move_from[0] not in "ABCDE" or move_from[1] not in "01234":
                    move_from = input("Move from (e.g. B3): ")
                move_to = input("Move to (e.g. B3): ")
                while move_to[0] not in "ABCDE" or move_to[1] not in "01234":
                    move_to = input("Move to (e.g. B3): ")
                try:
                    ai.opponent_move([(int(move_to[1]), ord(move_to[0])-ord("A")),
                                    (int(move_from[1]), ord(move_from[0])-ord("A"))])
                    move_made = True
                except Exception as e:
                    print(e)

        # update the game variables
        turn += 1
        turn %= 2

    ai.print_board()
    if ai.game_value(ai.board) == 1:
        print("AI wins! Game over.")
    else:
        print("You win! Game over.")


if __name__ == "__main__":
    main()
