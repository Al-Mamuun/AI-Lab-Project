import math

# --- Constants ---
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_SIZE = 3

# --- Game Logic ---
def initial_state():
    return [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def player(board):
    count_x = sum(row.count(PLAYER_X) for row in board)
    count_o = sum(row.count(PLAYER_O) for row in board)
    return PLAYER_O if count_x > count_o else PLAYER_X

def actions(board):
    return {(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if board[i][j] == EMPTY}

def result(board, action):
    i, j = action
    if board[i][j] != EMPTY:
        raise Exception("Invalid move")
    new_board = [row[:] for row in board]
    new_board[i][j] = player(board)
    return new_board

def winner(board):
    for i in range(BOARD_SIZE):
        if all(board[i][j] == PLAYER_X for j in range(BOARD_SIZE)):
            return PLAYER_X
        if all(board[i][j] == PLAYER_O for j in range(BOARD_SIZE)):
            return PLAYER_O
        if all(board[j][i] == PLAYER_X for j in range(BOARD_SIZE)):
            return PLAYER_X
        if all(board[j][i] == PLAYER_O for j in range(BOARD_SIZE)):
            return PLAYER_O
    if all(board[i][i] == PLAYER_X for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE-1-i] == PLAYER_X for i in range(BOARD_SIZE)):
        return PLAYER_X
    if all(board[i][i] == PLAYER_O for i in range(BOARD_SIZE)) or all(board[i][BOARD_SIZE-1-i] == PLAYER_O for i in range(BOARD_SIZE)):
        return PLAYER_O
    return None

def terminal(board):
    return winner(board) is not None or all(cell != EMPTY for row in board for cell in row)

def evaluate_board(board, player_symbol):
    opponent = PLAYER_X if player_symbol == PLAYER_O else PLAYER_O
    if winner(board) == player_symbol:
        return 1
    elif winner(board) == opponent:
        return -1
    return 0

# --- Minimax with optional Alpha-Beta Pruning ---
minimax_counter = 0

def minimax_proof(board, depth, alpha, beta, maximizing_player, player_symbol, use_pruning=True):
    global minimax_counter
    minimax_counter += 1  # Count node visit

    if terminal(board) or depth == 0:
        return evaluate_board(board, player_symbol), None

    best_move = None
    if maximizing_player:
        max_eval = float("-inf")
        for action in actions(board):
            eval_score, _ = minimax_proof(result(board, action), depth-1, alpha, beta, False, player_symbol, use_pruning)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = action
            alpha = max(alpha, max_eval)
            if use_pruning and beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for action in actions(board):
            eval_score, _ = minimax_proof(result(board, action), depth-1, alpha, beta, True, player_symbol, use_pruning)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = action
            beta = min(beta, min_eval)
            if use_pruning and beta <= alpha:
                break
        return min_eval, best_move

# --- Test Proof Run ---
if __name__ == "__main__":
    # Partial game state (so tree is smaller & runs faster)
    # X | O |  
    #   | X |  
    #   |   |
    test_board = [
        ['X', 'O', EMPTY],
        [EMPTY, 'X', EMPTY],
        [EMPTY, EMPTY, EMPTY]
    ]

    search_depth = 6  # Limit depth so program runs quickly

    # --- Run without Alpha-Beta (Pure Minimax) ---
    minimax_counter = 0
    minimax_proof(test_board, search_depth, float('-inf'), float('inf'), True, player(test_board), use_pruning=False)
    nodes_minimax = minimax_counter

    # --- Run with Alpha-Beta ---
    minimax_counter = 0
    minimax_proof(test_board, search_depth, float('-inf'), float('inf'), True, player(test_board), use_pruning=True)
    nodes_alpha_beta = minimax_counter

    # --- Show Result ---
    print("🔎 Proof of Alpha-Beta Pruning Efficiency")
    print("-------------------------------------")
    print(f"Without Alpha-Beta (Pure Minimax): {nodes_minimax} nodes visited")
    print(f"With Alpha-Beta Pruning:          {nodes_alpha_beta} nodes visited")
    print("-------------------------------------")
    if nodes_alpha_beta < nodes_minimax:
        print("✅ RESULT: Alpha-Beta Pruning explored fewer nodes and is FASTER than pure Minimax.")
    else:
        print("⚠️ Something is wrong: Alpha-Beta should visit fewer nodes.")
