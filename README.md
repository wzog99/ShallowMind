# ShallowMind
An endeavor into chess AI 

### Overview
In its escense I am creating a position evaluator, that when passed a chess board with the location of all the pieces, it will compute a positional value. When deciding whether or not to make a move, it will parse through the board states, restrained by the legal moves it can make, and then decide which move to make based on which has the highest positional advantage.

### Challenges
- How do you evaluate position? 
- How to obtain the data?
    - Games
        - Which games do you use? Grandmaster? Novice? Does it matter?
    - Positional value
        - Integrating StockFish chess engine with Python and Google Cloud Computing platform
- ML Models as an alternative
- Neural Network structure
- NN overfitting / underfitting

### Process
- Data processing and preparation
    - Over 250 Million games avalible
        - Chose a subset ~ 3M grandmaster games
    - Games are played in Standard algebraic notation (SAN) i.e. ( 1. d4 e6 2. c4 d5 3. Nf3 Nf6...)
    - Utilize Python-chess module for parsing through moves in each game
    - Each move creates a new board state; using python-chess, I'm able to get each board state in Forsyth-Edwards Notation (FEN) 
    - Clean and process FEN states to get the board states in a standardized (1,64) array
    - Convert (1,64) array into 6- (1,64) bitwise arrays with each board pretaining to a chess piece (pawn, rook, night, bishop, queen, king)
    - Integrate Stockfish with Python for position evaluation. This will return a float that corresponds with how good or bad the current board state is given where pieces are located.
        - Big limitation of Stockfish is the computation time required to compute alpha-beta tree searches.
    - **NOTE: At this point, the data consists of a 6 arrays, and a Stockfish evaluated position score
