     #################################
    ###  DATA COLLECTION FUNCTIONS  ###
     #################################
import numpy as np
import pandas as pd
import itertools
        
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





#####################################################################################



#####################################################################################