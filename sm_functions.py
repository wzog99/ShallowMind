     #################################
     ### DATA COLLECTION FUNCTIONS ###
     #################################

# List of Data Collection functions:
    # get_move_list
    # white_results
    # clean_fen
    # get_bitwise
    # get_white_win_bs
    # get_white_lose_bs
    # get_draw_bs
    
    
#####################################################################################    

import numpy as np
import pandas as pd
import itertools
import chess
        
def get_move_list(move_string): #### input is a string 
    '''
    Takes a move string that was striped from a PGN format, and removes unwanted characters and conserves SAN format.
    
    Input: String of plain text moves in string format
    Output: List of SAN moves
    
    '''
    testing = move_string 
    testing = testing[0:-2]  ### remove last 2 characters == '\n'
    testing = testing.split('. ')
    
    for i in range(len(testing)):
        testing[i] = testing[i].split(' ')
    for i in testing:
        try:
            del(i[2])
        except:
            continue
    del(testing[0])

    simplelist = list(itertools.chain.from_iterable(testing))
    return(simplelist)


#####################################################################################


def white_results(result_string_list):
    '''
    Reformats and standardizes stripped result info from chess game in PGN/TXT format
    
    Input: list of strings - (results text with line breaks included '\n'
    Output: win, lose, draw in list format
    
    '''
    white_result_list = []
    for i in range(len(result_string_list)):
            result = result_string_list[i][:-1]
            result = result.replace('1-0', 'win')
            result = result.replace('0-1', 'lose')
            result = result.replace('1/2-1/2', 'draw')
            white_result_list.append(result)
    return(white_result_list)


#####################################################################################


def clean_fen(string):
    '''
    Takes a Forsyth-Edwards Notation, with extraneous features, and simplifies it to a list of piece and position on the board [r,n,b,q,k,b,n,r,p,p,p,p,p,p,p,p,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,P,P,P,P,P,P,P,P,R,N,B,Q,K,B,N,R]
    
    Input: FEN string
    Output: 64 length list of strings, with piece position encoded
    '''
    string = string.replace('8','1'*8)
    string = string.replace('7','1'*7)
    string = string.replace('6','1'*6)
    string = string.replace('5','1'*5)
    string = string.replace('4','1'*4)
    string = string.replace('3','1'*3)
    string = string.replace('2','1'*2)
    string = string.replace('1','1'*1)
    string = string.replace('/','')
    string_list = [i for i in string]
    return(string_list)


#####################################################################################


def get_bitwise(board_state):
    '''
    Takes a 64 length list and decomposes it into 6 - 64 length arrays with bitwise encoding, -1,0,1

    Input: 64 length list of board states with piece encoding (r,n,b,q,k,p,R,N,B,Q,K,P,1)
    Output: 6 - 64 length arrays depicting board states with values -1,0,1
    '''
    
    bs = board_state 
    r_ray = np.zeros(64)
    n_ray = np.zeros(64)
    b_ray = np.zeros(64)
    q_ray = np.zeros(64)
    k_ray = np.zeros(64)
    p_ray = np.zeros(64)
    
    for i in range(64):
        if bs[i] == 'r':
            r_ray[i] = -1
        if bs[i] == 'R':
            r_ray[i] = 1 
        
        if bs[i] == 'b':
            b_ray[i] = -1
        if bs[i] == 'B':
            b_ray[i] = 1
        
        if bs[i] == 'n':
            n_ray[i] = -1
        if bs[i] == 'N':
            n_ray[i] = 1 
    
        if bs[i] == 'q':
            q_ray[i] = -1
        if bs[i] == 'Q':
            q_ray[i] = 1
    
        if bs[i] == 'k':
            k_ray[i] = -1
        if bs[i] == 'K':
            k_ray[i] = 1 
        
        if bs[i] == 'p':
            p_ray[i] = -1
        if bs[i] == 'P':
            p_ray[i] = 1 
    master_ray = np.array((r_ray, n_ray, b_ray, q_ray, k_ray, p_ray))
    return(master_ray)


#####################################################################################


def get_white_win_bs(game): ### i from white_win 
    '''
    Gets pairs of 'before-and-after' boardstates where white is making the move
    
    Input: List of game moves
    Output: List of before and after boardstates for white, where white wins
    '''
    
    board = chess.Board()

    board_state = None
    game_board_states = []


    for i in range(len(game)):
        bs = board.board_fen() ### creates current board state, in FEN "rnbqkbnr/pppppppp....
        board_state = np.array(clean_fen(bs)) ### return
        game_board_states.append(board_state)
        board.push_san(game[i])
        
    white_wins = []
    i = 0
    while i < len(game_board_states):
        try:
            white_wins.append((get_bitwise(game_board_states[i]).astype(int), get_bitwise(game_board_states[i + 1]).astype(int)))
            i += 2
        except:
            break
    return(white_wins)


#####################################################################################



def get_white_lose_bs(game): 
    '''
    Gets pairs of 'before-and-after' boardstates where black is making the move
    
    Input: List of game moves
    Output: List of before and after boardstates for black, where black wins
    '''
    
    board = chess.Board()

    board_state = None
    game_board_states = []

    for i in range(len(game)):
        bs = board.board_fen() ### creates current board state, in FEN "rnbqkbnr/pppppppp....
        board_state = np.array(clean_fen(bs)) ### return
        game_board_states.append(board_state)
        board.push_san(game[i])
    

    white_losses = []
    i = 1
    while i < len(game_board_states):
        try:
            white_losses.append((get_bitwise(game_board_states[i]).astype(int), get_bitwise(game_board_states[i + 1]).astype(int)))
            i += 2
        except:
            break
    return(white_losses)


#####################################################################################


def get_draw_bs(game):  ### probably wont use it - dont want neutral positions
    '''
    Gets pairs of 'before-and-after' boardstates for both black and white 
    
    Input: List of game moves
    Output: List of before and after boardstates for both black and white
    '''
    board = chess.Board()

    board_state = None
    game_board_states = []

    for i in range(len(game)):
        bs = board.board_fen() ### creates current board state, in FEN "rnbqkbnr/pppppppp....
        arr = np.array(clean_fen(bs))
        game_board_states.append(arr)  
        board.push_san(game[i])
    
    draws = []     
    for i in range(len(game_board_states)):
        try:
            draws.append((game_board_states[i], game_board_states[i+1]))
        except:
            break
    return(draws)


#####################################################################################


def get_board_state_array(move_list): ### i from all move_list
    '''
    Gets board states in arrray format
    
    input: list of moves
    output: board states in array format
    '''
    
    game = move_list
    board = chess.Board()
    #game = all_san_list[0]   


    board_state_list = []

    for move in game:
        try:
            bs = board.board_fen() ### creates current board state, in FEN "rnbqkbnr/pppppppp....
            board_array = np.array(clean_fen(bs)) ### return
            board_state_list.append(board_array)
            board.push_san(move)
        except:
            board_state_list.append(0)
            break
    return(board_state_list)


#####################################################################################


def get_fen_from_bitwise(game):
    """
    Takes an individual board state in the bitwise format (6 arrays with 64 positions), and returns the game in FEN, a notation that python-chess recognizes
    
    input: 1 board state in bitwise format: a grouping of 6 arrays with 64 positions
    output: 1 FEN string 
    """
    
    game # range(j, 6)
    fena = np.zeros(64, dtype=int) #((r_ray, n_ray, b_ray, q_ray, k_ray, p_ray))
    for j in range(6):             # Iterate through each piece's board state 
        for i in range(64):        # Iterate through each position in each board state
            if j == 0:
                fena[i] = game[j][i]
            if j == 1:
                fena[i] += game[j][i] * (j+1)
            if j == 2:
                fena[i] += game[j][i] * (j+1)
            if j == 3:
                fena[i] += game[j][i] * (j+1)
            if j == 4:
                fena[i] += game[j][i] * (j+1)
            if j == 5:
                fena[i] += game[j][i] * (j+1)
        
    fena = fena.astype(str)

    fena = np.char.replace(fena, '1', 'R')
    fena = np.char.replace(fena, '-R', 'r')

    fena = np.char.replace(fena, '2', 'N')
    fena = np.char.replace(fena, '-N', 'n')

    fena = np.char.replace(fena, '3', 'B')
    fena = np.char.replace(fena, '-B', 'b')

    fena = np.char.replace(fena, '4', 'Q')
    fena = np.char.replace(fena, '-Q', 'q')

    fena = np.char.replace(fena, '5', 'K')
    fena = np.char.replace(fena, '-K', 'k')

    fena = np.char.replace(fena, '6', 'P')
    fena = np.char.replace(fena, '-P', 'p')

    fena = np.char.replace(fena, '0', '1') # Seems wierd, but I need to add up the open spaces somehow....

    fene = list(itertools.chain.from_iterable(fena))

    # Need to break chain at 8 characters
    fene.insert(8 , '/') 
    fene.insert(17, '/')
    fene.insert(26, '/')
    fene.insert(35, '/')
    fene.insert(44, '/')
    fene.insert(53, '/')
    fene.insert(62, '/')


    # Replacing consecutive empty spaces with the product
    fene = ''.join(fene)
    fene = fene.replace('1' * 8, '8')
    fene = fene.replace('1' * 7, '7')
    fene = fene.replace('1' * 6, '6')
    fene = fene.replace('1' * 5, '5')
    fene = fene.replace('1' * 4, '4')
    fene = fene.replace('1' * 3, '3')
    fene = fene.replace('1' * 2, '2')
    fene = fene.replace('1' * 1, '1')
    return(fene)


#####################################################################################
#####################################################################################



     ######################################
     ### RUN AI AND PLAY GAME FUNCTIONS ###
     ######################################
    
# List OF RUN AI AND PLAY GAME FUNCTIONS:
    # run_AI
    
    
#####################################################################################


def run_AI(board, turn):
    """
    Plays the game as the AI, given the turn and current board
    
    input: board (in python-chess format)
    output: the best move in uci format
    
    """
    
    legal_boards = []
    l = []
    
    boardfen = board.fen()
    for move in [str(i) for i in list(board.legal_moves)]:
        current_board = chess.Board(boardfen)
        
        future_move = chess.Move.from_uci(str(move))
        current_board.push(future_move)
        current_board = str(current_board)
        current_board = current_board.replace('\n', ' ')
        current_board = current_board.replace('.', '1')
        current_board = current_board.split(' ')
        legal_boards.append((future_move, get_bitwise(current_board)))
    
    pred_df = pd.DataFrame(legal_boards, columns = ['move', 'bitwise'])
    pred_df['rook'] = [ pred_df['bitwise'][i][0] for i in range(len(pred_df)) ]
    pred_df['night'] = [ pred_df['bitwise'][i][1] for i in range(len(pred_df)) ]
    pred_df['bishop'] = [ pred_df['bitwise'][i][2] for i in range(len(pred_df)) ]
    pred_df['queen'] = [ pred_df['bitwise'][i][3] for i in range(len(pred_df)) ]
    pred_df['king'] = [ pred_df['bitwise'][i][4] for i in range(len(pred_df)) ]
    pred_df['pawn'] = [ pred_df['bitwise'][i][5] for i in range(len(pred_df)) ]
    pred_df = pred_df.drop('bitwise', axis=1)
    
    ### Need column names for expanded df
    rook_cols = []
    for i in range(64):
        rook_cols.append('rook_'+ str(i))
    night_cols = []
    for i in range(64):
        night_cols.append('night_'+ str(i))
    bishop_cols = []
    for i in range(64):
        bishop_cols.append('bishop_'+ str(i))    
    queen_cols = []
    for i in range(64):
        queen_cols.append('queen_'+ str(i))
    king_cols = []
    for i in range(64):
        king_cols.append('king_'+ str(i))
    pawn_cols = []
    for i in range(64):
        pawn_cols.append('pawn_'+ str(i))
    
    
    ### Expanding individual board state dfs 
    
    dfr = pd.DataFrame(pred_df['rook'].values.tolist(), columns = rook_cols)
    dfn = pd.DataFrame(pred_df['night'].values.tolist(), columns = night_cols)
    dfb = pd.DataFrame(pred_df['bishop'].values.tolist(), columns = bishop_cols)
    dfq = pd.DataFrame(pred_df['queen'].values.tolist(), columns = queen_cols)
    dfk = pd.DataFrame(pred_df['king'].values.tolist(), columns = king_cols)
    dfp = pd.DataFrame(pred_df['pawn'].values.tolist(), columns = pawn_cols)
    
    ### Encoding current turn into a seperate turn_df
    
    placeholder = pd.Series([i for i in range(len(pred_df))])
    turn_df= pd.DataFrame(placeholder, index= range(len(pred_df)), columns=['white_turn'])
    if turn % 2 == False:
        ones = [1 for i in range(len(pred_df))]
        turn_df['white_turn'] = ones
    else:
        zeros = [0 for i in range(len(pred_df))]
        turn_df['white_turn'] = zeros
        
    ### Merging dfs
    
    df_merged = turn_df
    df_merged = pd.merge(df_merged, dfr, how='outer', right_index=True, left_index=True)
    df_merged = pd.merge(df_merged, dfn, how='outer', right_index=True, left_index=True)
    df_merged = pd.merge(df_merged, dfb, how='outer', right_index=True, left_index=True)
    df_merged = pd.merge(df_merged, dfq, how='outer', right_index=True, left_index=True)
    df_merged = pd.merge(df_merged, dfk, how='outer', right_index=True, left_index=True)
    df_merged = pd.merge(df_merged, dfp, how='outer', right_index=True, left_index=True)

    ### Running the model over the possible moves and selecting the best move availible 
    
    move_and_score = []
    best_move = ('NaN', -100)
    
    for i in range(len(legal_boards)):
        m_and_s = (str(legal_boards[i][0]), np.asscalar(model.predict(df_merged)[i][0]))
        move_and_score.append(m_and_s)
        if m_and_s[1] > best_move[1]:
            best_move = m_and_s
            
    current_board = board
    return(best_move)