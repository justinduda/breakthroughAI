from sys import argv
import players
import time

#This will be used as the actual game, and the state of the game
class Game:
    def __init__(self, board_option, player_one, player_two):
        self.player_to_move = 1
        self.players = (player_one, player_two)
        board = Board(board_option)
        self.current_state = State(board, 1)

    def play(self):
        #Play until someone wins
        util = 0
        #print str( self.players[0].evaluation_function( self.players[0], self.current_state))
        #return "Player 1"

        #self.current_state.board.set_grid(
        #               [[0,0,0,0,0,0,0,0],
        #                [0,0,0,0,0,0,0,0],
        #                [0,0,0,0,0,0,0,0],
        #                [0,0,0,2,2,0,0,0],
        #                [0,0,0,0,0,0,0,0],
        #                [0,0,0,0,0,0,0,0],
        #                [0,0,0,1,1,0,0,0],
        #                [0,0,0,0,0,0,0,0]]
        #               )
        #self.current_state.board.num_1 = 1
        #self.current_state.board.num_2 = 1

        while not util:
            self.current_state = self.players[self.player_to_move-1].pick_move(self.current_state)
            if self.player_to_move == 1:
                self.player_to_move = 2
            elif self.player_to_move == 2:
                self.player_to_move = 1
            util = self.current_state.utility()

            self.current_state.board.print_board()
            #time.sleep(.5)

         
        if util == 1:
            return "Player 1"
        elif util == -1:
            return "Player 2"
        
class Board:
    def __init__(self, board_option, old_board = None):
        self.board_option = board_option
        if board_option == 1: #8x8 board
            self.grid = [ [2, 2, 2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2, 2, 2],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1] ]
            self.rows = 8
            self.columns = 8
            self.num_1 = 16
            self.num_2 = 16
        elif board_option == 2: #10x5
            self.grid = [ [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                          [2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1] ]
            self.rows = 5
            self.columns = 10
            self.num_1 = 20
            self.num_2 = 20
        elif board_option == 3: 
            self.grid = [ list(sublist) for sublist in old_board.grid]
            self.rows = old_board.rows
            self.columns = old_board.columns
            self.num_1 = old_board.num_1
            self.num_2 = old_board.num_2

    def __eq__(self, other):
        return self.grid == other.grid

    def at(self, x, y):
        return self.grid[y][x]

    def set(self, x, y, num):
        self.grid[y][x] = num

    def set_grid(self, new_grid):
        self.grid = [list(sublist) for sublist in new_grid]

    def move(self, x1, y1, x2, y2):
        new_board = Board(3, self)

        if new_board.at(x2,y2) == 1:
            new_board.num_1 -= 1
        elif new_board.at(x2,y2) == 2:
            new_board.num_2 -= 1
        new_board.set(x2,y2, new_board.at(x1,y1))
        new_board.set(x1,y1, 0)
        return new_board

    def print_board(self):
        #print '-----------------------------------'
        row_num = self.rows
        for row in self.grid:
            print str(row_num) + "  " + "".join( [str(x) for x in row ])
            row_num -= 1
        print ""
        letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
        print "   " + "".join( letters[0:self.columns])
        #print '-----------------------------------'

 
class State:
    #   player 1 is first player (max)
    #   player 2 is second player (min)
    #   children is list of legal next states
    def __init__(self, board, player_to_move):
        self.player_to_move = player_to_move
        self.board = Board(3, board)

    def __eq__(self, other):
        return other is not None and self.player_to_move == other.player_to_move and self.board == other.board

    #returns 1 for player 1 win
    #returns -1 for player 2 win
    def utility(self):
        if self.board.num_1 == 0:
            return -1
        if self.board.num_2 == 0:
            return 1

        for x in self.board.grid[0]:
            if x == 1:
                return 1
        for x in self.board.grid[-1]:
            if x == 2:
                return -1
        return 0
       

    #sets self.children to a list of all possible subsequent legal states
    def find_next_states(self):
        #checks if on board and if players' piece is not already there
        def is_legal(x, y, player_to_move):
            return x >= 0 and x < self.board.columns and y >= 0 and y < self.board.rows and self.board.at(x,y) != player_to_move
        next_states = []

        for y in range (0, self.board.rows):
            for x in range(0, self.board.columns):
                if self.board.at(x,y) == self.player_to_move:
                    if self.player_to_move == 1:
                        if is_legal(x-1,y-1, 1):
                            next_states.append( State(  self.board.move(x, y, x-1,y-1), 2))
                        if is_legal(x,y-1, 1) and self.board.at(x,y-1) != 2:
                            next_states.append( State(  self.board.move(x, y, x,y-1), 2))
                        if is_legal(x+1,y-1, 1):
                            next_states.append( State(  self.board.move(x, y, x+1,y-1), 2))
                            
                    else: #player_to_move == 2:
                        if is_legal(x-1,y+1, 2):
                            next_states.append( State(  self.board.move(x, y, x-1,y+1), 1))
                        if is_legal(x,y+1, 2) and self.board.at(x,y+1) != 1:
                            next_states.append( State(  self.board.move(x, y, x,y+1), 1))
                        if is_legal(x+1,y+1, 2):
                            next_states.append( State(  self.board.move(x, y, x+1,y+1), 1))
        
        return next_states


def main():
    #player1 = players.Human(1)
    player1 = players.AI(1, 3, "offensive", "minimax")
    player2 = players.AI(2, 3, "defensive", "minimax")
    player3 = players.AI(1, 3, "offensive", "alphabeta")
    player4 = players.AI(2, 3, "defensive", "alphabeta")
    

    #game = Game(1, player1, player2)
    #winner = game.play()
    

    game = Game(1, player3, player4)
    winner = game.play()

    print "Winner is: " + winner

if __name__ == '__main__':
    main()
