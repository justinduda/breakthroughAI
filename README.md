# breakthroughAI
Artificial Intelligence player for the game Breakthrough


Code structure and algorithms:

	Initial State: Board as read in from input file, with pieces on opposite sides of the board. 

	Evalution Function features: (for piece)
		-how many spaces it is attacking
		-how far along the piece is (backrow gives best value)
		-value for existing at all
		-how many enemy pieces it isattacking
		-how many squares it is guarding
		-how many vertical connections to your other pieces
		-how many horizontal connections to your other pieces
		-how many pieces of yours you are protecting
		-how many spaces it can move to
		-whether it is on your home row

		how many opponents pieces are in this column too		

	not-per pieces:
		-penalize columns without any of your pieces on it
		-

	vertical connections are good
	horizonal connections are good
	runners
	num pieces

	
	offensive: attacking pieces with high defense score

-------------------------------------------------------------
first implementation:
	num_pieces + how far along your pieces are

	

STUFF TO DO:
-


