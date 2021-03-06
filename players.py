import datetime
import game
import sys

class Human:
    def __init__(self, player_num):
        player_num = player_num

    def pick_move(self, state):
        print "\n"
        state.board.print_board()
        print "\n"
        print "Please enter a move in the form of 'e4-e5' without quotations."

        #player_move = game.State( game.Board(1), 2)
        player_move = None
        next_states = state.find_next_states()


        #print "number of next states: " + str(len(next_states))

        first_try = True
        while player_move not in next_states:
            if not first_try:
                print "Please enter a legal move."
            first_try = False
            move = raw_input("Your Move: ")
            move.replace(" ", "")

            letters = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
            if len(move) != 5 or move[0] not in letters or move[3] not in letters:
                continue
        
            x1 = letters.index(move[0])
            y1 = state.board.rows - int(move[1])
            x2 = letters.index(move[3])
            y2 = state.board.rows - int(move[4])


            if x1 < 0 or x1 > state.board.rows or y1 < 0 or y1 > state.board.columns or state.board.at(x2,y2) == state.player_to_move:
                continue

            new_board = state.board.move(x1, y1, x2, y2)
            players = [0, 2, 1]
            player_move = game.State(new_board, players[state.player_to_move])

        assert player_move is not None

        return player_move

class AI:

    def __init__(self, player_num, cut_off_depth, strategy, search_type):
        self.player_num = player_num 
        self.evaluation_function = self.evaluation_picker(strategy)
        self.search = self.search_picker(search_type)
        self.cut_off_depth = cut_off_depth
        self.transposition_table = {}
        self.nodes_expanded = 0
        self.cur_nodes_expanded = 0
        self.avg_num_nodes_expanded = 0
        self.avg_move_time = 0

    def pick_move(self, state):
        a = datetime.datetime.now().replace(microsecond=0)

        ret =  self.search(self, state, 0)

        b = datetime.datetime.now().replace(microsecond=0)
        if self.avg_move_time == 0:
            self.avg_move_time = b-a
        else:
            self.avg_move_time = (self.avg_move_time+b-a)/2

        if self.avg_num_nodes_expanded == 0:
            self.avg_num_nodes_expanded = self.cur_nodes_expanded
        else:
            self.avg_num_nodes_expanded = (self.avg_num_nodes_expanded+self.cur_nodes_expanded)/2

        self.nodes_expanded += self.cur_nodes_expanded
        self.cur_nodes_expanded = 0
        
        return ret


    def search_picker(self, search_type):
        def cutoff_test(state, depth):
            return depth == self.cut_off_depth or state.utility()

        def better_state(min_or_max):
            def better_state_func((s1, i1), (s2, i2)):
                val = min_or_max(i1, i2)
                if i1 == val:
                    return (s1, i1)
                else:
                    return (s2, i2)
            return better_state_func

        def minimax_search(self, state, depth):
            
            def minimax(cur_state, depth):
                self.cur_nodes_expanded += 1
                if cutoff_test(cur_state, depth):
                    return self.evaluation_function(self, cur_state)
                if cur_state.player_to_move == 1:
                    return max( [minimax(st, depth+1) for st in cur_state.find_next_states()] )
                else:
                    return min( [minimax(st, depth+1) for st in cur_state.find_next_states()] )


            
            #print "my choices:" + str([ minimax ( st, depth+1) for st in state.find_next_states()])
            #print ""

            #print "eval: " + str( minimax( state, 0))

            if state.player_to_move == 1:
                my_move = reduce(better_state(max), [ (st, minimax ( st, depth+1)) for st in state.find_next_states()])
            else: #player == 2:
                my_move  = reduce(better_state(min), [ (st, minimax ( st, depth+1)) for st in state.find_next_states()])
            #print "                             value of picked move: " + str(my_move[1])
            return my_move[0]

        #only keep track of the states at depth 1
        def alpha_beta_search(self, state, depth):

            def reorder_moves(sts, comp):
            #def reorder_moves(sts):
                def higher_or_equal_priority(lhs, rhs):
                    return lhs[1] == comp(lhs[1], rhs[1])
                    #return lhs.board.num_1 + lhs.board.num_2 - rhs.board.num_2 - rhs.board.num_2 <= 0

                if len(sts) <= 1:
                    return sts
                pivot = sts.pop()
                left = [x for x in sts if higher_or_equal_priority(x, pivot)]
                right = [x for x in sts if not higher_or_equal_priority(x, pivot)]
                return left + [pivot] + right


            def alpha_beta(cur_state, depth, alpha, beta):
                self.cur_nodes_expanded += 1

                if cutoff_test(cur_state, depth):
                    #if cur_state.player_to_move == 1:
                        #return self.evaluation_function(self, cur_state)
                    #else: #player 2
                    return self.evaluation_function(self, cur_state)

                #next_states = cur_state.find_next_states()
                #reordered_moves = reorder_moves(next_states)
                #states_and_values = zip(next_states, [self.evaluation_function(self, st) for st in next_states])

                if cur_state.player_to_move == 1:
                    val = -sys.maxint -1
                    #reordered_moves = [x[0] for x in reorder_moves(states_and_values, max)]
                    for st in cur_state.find_next_states():
                    #for st in reordered_moves:
                        val = max(val, alpha_beta(st, depth+1, alpha, beta))
                        if val >= beta:
                            return val
                        alpha = max(alpha, val)

                    return val
                if cur_state.player_to_move == 2:
                    val = sys.maxint
                    #reordered_moves = [x[0] for x in reorder_moves(states_and_values, min)]
                    for st in cur_state.find_next_states():
                    #for st in reordered_moves:
                        val = min(val, alpha_beta(st, depth+1, alpha, beta))
                        if val <= alpha:
                            return val
                        beta = min(beta, val)
                    return val

            #print "eval: " + str( alpha_beta( state, 0, -sys.maxint-1, sys.maxint))


            if state.player_to_move == 1:

                my_move = reduce(better_state(max), [ (st, alpha_beta ( st, depth+1, -sys.maxint-1, sys.maxint)) for st in state.find_next_states()])
            else: #player == 2:
                my_move = reduce(better_state(min), [ (st, alpha_beta ( st, depth+1, -sys.maxint-1, sys.maxint)) for st in state.find_next_states()])
            #print "                             value of picked move: " + str(my_move[1])
            return my_move[0]


        if search_type == "minimax":
            return minimax_search
        elif search_type == "alphabeta":
            return alpha_beta_search

    def evaluation_picker(self, evaluation_strategy):
        def on_board(board, x, y):
            return x >= 0 and y >=0 and x < board.columns and y < board.rows

        def evaluation_offensive(state):
            if state.board.num_1 == 0:
                return -sys.maxint -1
            if state.board.num_2 == 0:
                return sys.maxint

            val_p1 = 0
            val_p2 = 0

            for y in range(0, state.board.rows):
                for x in range(0, state.board.columns):

                    if state.board.at(x,y) == 1:
                        if y == 0:
                            return sys.maxint

                        #feature for existing
                        val_p1 += 15

                        #feature for how far along the piece is
                        val_p1 += (state.board.rows -1- y) * .5
                        
                        #feature for what it is attacking (enemy, ally, or empty)
                        if on_board(state.board, x-1, y-1):
                            if state.board.at(x-1,y-1) == 2: #enemy
                                val_p1 += 2
                            elif state.board.at(x-1,y-1) == 1: #ally
                                val_p1 += 2
                            elif state.board.at(x-1,y-1) == 0: #empty
                                val_p1 += 1

                        if on_board(state.board, x+1, y-1):
                            if state.board.at(x+1,y-1) == 2: #enemy
                                val_p1 += 2
                            elif state.board.at(x+1,y-1) == 1: #ally
                                val_p1 += 2
                            elif state.board.at(x+1,y-1) == 0: #empty
                                val_p1 += 1

                        #feature for what is in front 
                        if on_board(state.board, x, y-1):
                            if state.board.at(x,y-1) == 2: #enemy
                                val_p1 += 0
                            elif state.board.at(x,y-1) == 1: #ally
                                val_p1 += 0.25
                            elif state.board.at(x,y-1) == 0: #empty
                                val_p1 += 0.5

                        #feature for what is to the side
                        if on_board(state.board, x-1, y):
                            if state.board.at(x-1,y) == 2: #enemy
                                val_p1 += 0
                            elif state.board.at(x-1,y) == 1: #ally
                                val_p1 += 0.25
                            elif state.board.at(x-1,y) == 0: #empty
                                val_p1 += 0

                        if on_board(state.board, x+1, y):
                            if state.board.at(x+1,y) == 2: #enemy
                                val_p1 += 0
                            elif state.board.at(x+1,y) == 1: #ally
                                val_p1 += 0.25
                            elif state.board.at(x+1,y) == 0: #empty
                                val_p1 += 0

                        #feature for being on home row
                        if y == state.board.rows - 1:
                            val_p1 += .25

                    elif state.board.at(x,y) == 2:
                        if y == state.board.rows-1:
                            return -sys.maxint - 1

                        #print str( (x,y)) + ": " + str(state.board.at(x,y))

                        #feature for existing
                        val_p2 += 15

                        #feature for how far along the piece is
                        val_p2 += y * .5
                        
                        #print "val2: " + str(val_p2)
                        #feature for what it is attacking (enemy, ally, or empty)
                        if on_board(state.board, x-1, y+1):
                            if state.board.at(x-1,y+1) == 1: #enemy
                                val_p2 += 2
                            elif state.board.at(x-1,y+1) == 2: #ally
                                val_p2 += 2
                            elif state.board.at(x-1,y+1) == 0: #empty
                                val_p2 += 1

                        if on_board(state.board, x+1, y+1):
                            if state.board.at(x+1,y+1) == 1: #enemy
                                val_p2 += 2
                            elif state.board.at(x+1,y+1) == 2: #ally
                                val_p2 += 2
                            elif state.board.at(x+1,y+1) == 0: #empty
                                val_p2 += 1

                        #feature for what is in front 
                        if on_board(state.board, x, y+1):
                            if state.board.at(x,y+1) == 1: #enemy
                                val_p2 += 0
                            elif state.board.at(x,y+1) == 2: #ally
                                val_p2 += 0.25
                            elif state.board.at(x,y+1) == 0: #empty
                                val_p2 += 0.5

                        #feature for what is to the side
                        if on_board(state.board, x-1, y):
                            if state.board.at(x-1,y) == 1: #enemy
                                val_p2 += 0
                            elif state.board.at(x-1,y) == 2: #ally
                                val_p2 += 0.25
                            elif state.board.at(x-1,y) == 0: #empty
                                val_p2 += 0

                        if on_board(state.board, x+1, y):
                            if state.board.at(x+1,y) == 1: #enemy
                                val_p2 += 0
                            elif state.board.at(x+1,y) == 2: #ally
                                val_p2 += 0.25
                            elif state.board.at(x+1,y) == 0: #empty
                                val_p2 += 0

                        #feature for being on home row
                        if y == 0:
                            val_p2 += .25

            #print str(val_p1)
            #print str(val_p2)
            return val_p1 - val_p2

        def evaluation_defensive(state):
            if state.board.num_1 == 0:
                return -sys.maxint -1
            if state.board.num_2 == 0:
                return sys.maxint

            val_p1 = 0
            val_p2 = 0

            for y in range(0, state.board.rows):
                for x in range(0, state.board.columns):

                    if state.board.at(x,y) == 1:
                        if y == 0:
                            return sys.maxint

                        #feature for existing
                        val_p1 += 7

                        #feature for how far along the piece is
                        val_p1 += (state.board.rows -1- y) * .3
                        
                        #feature for what it is attacking (enemy, ally, or empty)
                        if on_board(state.board, x-1, y-1):
                            if state.board.at(x-1,y-1) == 2: #enemy
                                val_p1 += 1.5
                            elif state.board.at(x-1,y-1) == 1: #ally
                                val_p1 += 2
                            elif state.board.at(x-1,y-1) == 0: #empty
                                val_p1 += 1

                        if on_board(state.board, x+1, y-1):
                            if state.board.at(x+1,y-1) == 2: #enemy
                                val_p1 += 1.5
                            elif state.board.at(x+1,y-1) == 1: #ally
                                val_p1 += 2
                            elif state.board.at(x+1,y-1) == 0: #empty
                                val_p1 += 1

                        #feature for what is in front 
                        if on_board(state.board, x, y-1):
                            if state.board.at(x,y-1) == 2: #enemy
                                val_p1 += 0.25
                            elif state.board.at(x,y-1) == 1: #ally
                                val_p1 += 0.25
                            elif state.board.at(x,y-1) == 0: #empty
                                val_p1 += 0

                        #feature for what is to the side
                        if on_board(state.board, x-1, y):
                            if state.board.at(x-1,y) == 2: #enemy
                                val_p1 += -0.25
                            elif state.board.at(x-1,y) == 1: #ally
                                val_p1 += 0.25
                            elif state.board.at(x-1,y) == 0: #empty
                                val_p1 += 0

                        if on_board(state.board, x+1, y):
                            if state.board.at(x+1,y) == 2: #enemy
                                val_p1 += -0.25
                            elif state.board.at(x+1,y) == 1: #ally
                                val_p1 += 0.5
                            elif state.board.at(x+1,y) == 0: #empty
                                val_p1 += 0

                        #feature for being on home row
                        if y == state.board.rows - 1:
                            val_p1 += .25

                    elif state.board.at(x,y) == 2:
                        if y == state.board.rows-1:
                            return -sys.maxint - 1

                        #print str( (x,y)) + ": " + str(state.board.at(x,y))

                        #feature for existing
                        val_p2 += 7

                        #feature for how far along the piece is
                        val_p2 += y * .3
                        
                        #print "val2: " + str(val_p2)
                        #feature for what it is attacking (enemy, ally, or empty)
                        if on_board(state.board, x-1, y+1):
                            if state.board.at(x-1,y+1) == 1: #enemy
                                val_p2 += 1.5
                            elif state.board.at(x-1,y+1) == 2: #ally
                                val_p2 += 2
                            elif state.board.at(x-1,y+1) == 0: #empty
                                val_p2 += 1

                        if on_board(state.board, x+1, y+1):
                            if state.board.at(x+1,y+1) == 1: #enemy
                                val_p2 += 1.5
                            elif state.board.at(x+1,y+1) == 2: #ally
                                val_p2 += 2
                            elif state.board.at(x+1,y+1) == 0: #empty
                                val_p2 += 1

                        #feature for what is in front 
                        if on_board(state.board, x, y+1):
                            if state.board.at(x,y+1) == 1: #enemy
                                val_p2 += 0.25
                            elif state.board.at(x,y+1) == 2: #ally
                                val_p2 += 0.25
                            elif state.board.at(x,y+1) == 0: #empty
                                val_p2 += 0

                        #feature for what is to the side
                        if on_board(state.board, x-1, y):
                            if state.board.at(x-1,y) == 1: #enemy
                                val_p2 += -0.25
                            elif state.board.at(x-1,y) == 2: #ally
                                val_p2 += 0.25
                            elif state.board.at(x-1,y) == 0: #empty
                                val_p2 += 0

                        if on_board(state.board, x+1, y):
                            if state.board.at(x+1,y) == 1: #enemy
                                val_p2 += -0.25
                            elif state.board.at(x+1,y) == 2: #ally
                                val_p2 += 0.5
                            elif state.board.at(x+1,y) == 0: #empty
                                val_p2 += 0

                        #feature for being on home row
                        if y == 0:
                            val_p2 += .25

            #print str(val_p1)
            #print str(val_p2)
            return val_p1 - val_p2


        if evaluation_strategy == "offensive":
            eval_func = evaluation_offensive
        elif evaluation_strategy == "defensive":
            eval_func = evaluation_defensive

        def evaluate(self, state):
            grid_as_tuple = tuple([tuple(row) for row in state.board.grid])
            if (grid_as_tuple, state.player_to_move) in self.transposition_table:
                return self.transposition_table[ ((grid_as_tuple), state.player_to_move)]

            evaluation = eval_func(state)

            self.transposition_table[ ((grid_as_tuple), state.player_to_move)] = evaluation
            return evaluation

        return evaluate


