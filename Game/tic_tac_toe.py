import tkinter as tk
from tkinter import messagebox
import math
import random

# --- Constants ---
EMPTY = ' '
PLAYER_X = 'X'
PLAYER_O = 'O'
BOARD_SIZE = 3
AI_DELAY = 500  # milliseconds
BUTTON_FONT = ('Arial', 24, 'bold')
STATUS_FONT = ('Arial', 14, 'bold')
BG_COLOR = '#1e1e1e'
BUTTON_BG = '#2e2e2e'
BUTTON_FG_X = '#e74c3c'  # Red for X
BUTTON_FG_O = '#3498db'  # Blue for O
HOVER_BG = '#3e3e3e'
WIN_LINE_BG = '#27ae60'  # Green highlight


class TicTacToeApp:
    """Modern Tic Tac Toe game with Human vs AI and AI vs AI using Minimax with Alpha-Beta pruning."""
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.configure(bg=BG_COLOR)

        self.board = initial_state()
        self.current_player = PLAYER_X
        self.buttons = [[None]*BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.game_mode = "human_vs_computer"
        self.first_move_done = False

        self.create_widgets()

    # --- UI Setup ---
    def create_widgets(self):
        # Board Frame
        board_frame = tk.Frame(self.root, bg=BG_COLOR)
        board_frame.pack(pady=20)

        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                btn = tk.Button(
                    board_frame,
                    text=EMPTY,
                    font=BUTTON_FONT,
                    width=5,
                    height=2,
                    bg=BUTTON_BG,
                    fg='white',
                    activebackground=HOVER_BG,
                    command=lambda i=i, j=j: self.make_move(i, j)
                )
                btn.grid(row=i, column=j, padx=5, pady=5)
                self.buttons[i][j] = btn

        # Status Label
        self.status_label = tk.Label(self.root, text="Player X's turn", font=STATUS_FONT, bg=BG_COLOR, fg='white')
        self.status_label.pack(pady=10)

        # Control Buttons
        control_frame = tk.Frame(self.root, bg=BG_COLOR)
        control_frame.pack(pady=10)
        tk.Button(control_frame, text="Human vs Computer", command=self.set_human_vs_computer).grid(row=0, column=0, padx=5)
        tk.Button(control_frame, text="Computer vs Computer", command=self.set_computer_vs_computer).grid(row=0, column=1, padx=5)
        tk.Button(control_frame, text="Reset", command=self.reset_game).grid(row=0, column=2, padx=5)

    # --- Game Mode Handlers ---
    def set_human_vs_computer(self):
        self.game_mode = "human_vs_computer"
        self.reset_game()

    def set_computer_vs_computer(self):
        self.game_mode = "computer_vs_computer"
        self.reset_game()
        self.root.after(AI_DELAY, self.play_computer_vs_computer)

    def reset_game(self):
        self.board = initial_state()
        self.current_player = PLAYER_X
        self.first_move_done = False
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(text=EMPTY, state=tk.NORMAL, bg=BUTTON_BG, fg='white')
        self.status_label.config(text="Player X's turn")

    # --- Gameplay ---
    def make_move(self, i, j):
        if terminal(self.board) or self.board[i][j] != EMPTY:
            return

        # Update board
        self.board = result(self.board, (i, j))
        self.update_button(i, j)

        # Check winner
        winner_player = winner(self.board)
        if winner_player:
            self.status_label.config(text=f"{winner_player} wins!")
            self.highlight_winner(winner_player)
            self.disable_buttons()
        elif terminal(self.board):
            self.status_label.config(text="It's a draw!")
        else:
            self.current_player = player(self.board)
            self.status_label.config(text=f"Player {self.current_player}'s turn")
            if self.game_mode == "human_vs_computer" and self.current_player == PLAYER_O:
                self.root.after(AI_DELAY, self.computer_move)

    def update_button(self, i, j):
        symbol = self.current_player
        fg_color = BUTTON_FG_X if symbol == PLAYER_X else BUTTON_FG_O
        self.buttons[i][j].config(text=symbol, state=tk.DISABLED, fg=fg_color)

    def computer_move(self):
        if terminal(self.board):
            return
        if not self.first_move_done:
            move = random.choice(list(actions(self.board)))
            self.first_move_done = True
        else:
            _, move = minimax(self.board, math.inf, float('-inf'), float('inf'), True, PLAYER_O)

        if move:
            self.make_move(*move)

    def play_computer_vs_computer(self):
        if terminal(self.board):
            return
        current_player = self.current_player
        if not self.first_move_done:
            move = random.choice(list(actions(self.board)))
            self.first_move_done = True
        else:
            _, move = minimax(self.board, math.inf, float('-inf'), float('inf'), True, current_player)

        if move:
            self.make_move(*move)

        self.current_player = PLAYER_O if current_player == PLAYER_X else PLAYER_X
        self.root.after(AI_DELAY, self.play_computer_vs_computer)

    # --- Utility ---
    def disable_buttons(self):
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                self.buttons[i][j].config(state=tk.DISABLED)

    def highlight_winner(self, player_symbol):
        """Highlight the winning line."""
        # Check rows
        for i in range(BOARD_SIZE):
            if all(self.board[i][j] == player_symbol for j in range(BOARD_SIZE)):
                for j in range(BOARD_SIZE):
                    self.buttons[i][j].config(bg=WIN_LINE_BG)
                return
        # Check columns
        for j in range(BOARD_SIZE):
            if all(self.board[i][j] == player_symbol for i in range(BOARD_SIZE)):
                for i in range(BOARD_SIZE):
                    self.buttons[i][j].config(bg=WIN_LINE_BG)
                return
        # Check diagonals
        if all(self.board[i][i] == player_symbol for i in range(BOARD_SIZE)):
            for i in range(BOARD_SIZE):
                self.buttons[i][i].config(bg=WIN_LINE_BG)
            return
        if all(self.board[i][BOARD_SIZE-1-i] == player_symbol for i in range(BOARD_SIZE)):
            for i in range(BOARD_SIZE):
                self.buttons[i][BOARD_SIZE-1-i].config(bg=WIN_LINE_BG)
            return


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


def minimax(board, depth, alpha, beta, maximizing_player, player_symbol):
    if terminal(board) or depth == 0:
        return evaluate_board(board, player_symbol), None

    best_move = None
    if maximizing_player:
        max_eval = float("-inf")
        for action in actions(board):
            eval_score, _ = minimax(result(board, action), depth-1, alpha, beta, False, player_symbol)
            if eval_score > max_eval:
                max_eval = eval_score
                best_move = action
            alpha = max(alpha, max_eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float("inf")
        for action in actions(board):
            eval_score, _ = minimax(result(board, action), depth-1, alpha, beta, True, player_symbol)
            if eval_score < min_eval:
                min_eval = eval_score
                best_move = action
            beta = min(beta, min_eval)
            if beta <= alpha:
                break
        return min_eval, best_move


def evaluate_board(board, player_symbol):
    opponent = PLAYER_X if player_symbol == PLAYER_O else PLAYER_O
    if winner(board) == player_symbol:
        return 1
    elif winner(board) == opponent:
        return -1
    return 0


# --- Run Game ---
if __name__ == "__main__":
    root = tk.Tk()
    app = TicTacToeApp(root)
    root.mainloop()
