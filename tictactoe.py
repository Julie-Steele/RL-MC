import random
cleanboard = [None for _ in range(9)]


    

def play_game(board):
    potential_moves = []
    #potential moves
    player = "X" if board.count("X") == board.count("O") else "O"
    
    # print(board)
    for i, x in enumerate(board):
        if x is None:
            pot_move = board.copy()
            pot_move[i] = player
            score = try_games(pot_move)
            potential_moves.append((score, pot_move))
    
    #could try sampling here 
    if player == "X":
        best_move = max(potential_moves, key = lambda x: x[0])
    else:
        best_move = min(potential_moves, key = lambda x: x[0])
        
    return best_move[1]


def try_games(board, num_trials=100):
    # [X wins is 1, O wins is 0, tie is 0.5]
    scores = []
    for i in range(num_trials):
        sim_board = board.copy()
        fill = fill_board(sim_board)
        if check_winner(fill) == "tie":
            res = 0.5
        elif check_winner(fill) == "X":
            res = 1
        else:
            res = 0
        
        scores.append(res)
    
    return sum(scores)/num_trials
        


def fill_board(board):
    #note this mutates the board
    num_empty = board.count(None)
    if num_empty == 0:
        return board
    
    rand_idx = random.choice([i for i, x in enumerate(board) if x == None])
    if num_empty % 2 == 1:
        board[rand_idx] = "X"
        return fill_board(board)
    else: #O move
        board[rand_idx] = "O"
        return fill_board(board)
        

def check_winner(board):
    for i in range(3):
        if board[i] == board[i+3] == board[i+6] != None:
            return board[i]
        if board[3*i] == board[3*i+1] == board[3*i+2] != None:
            return board[3*i]
    if board[0] == board[4] == board[8] != None:
        return board[0]
    if board[2] == board[4] == board[6] != None:
        return board[2]
    return "tie"

if __name__ =="__main__":
    
    
    wins = [0, 0, 0]
    
    num_games = 100
    for game in range(num_games):
        if game % num_games/10 == 0:
            print(game, "games played")
        test_board = cleanboard.copy()
        best_move = test_board
        for i in range(9):
            best_move = play_game(best_move)
            # print(best_move)
        
        # print(check_winner(best_move))	

        if check_winner(best_move) == "X":
            wins[0] += 1
        elif check_winner(best_move) == "O":
            wins[1] += 1
        else:
            wins[2] += 1
    
    print("X wins, O wins, ties")
    print(wins[0]/num_games, wins[1]/num_games, wins[2]/num_games)
    
    
    