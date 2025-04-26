import rclpy
from rclpy.node import Node
import random

PLAYER = 'X'
AI = 'O'

class TicTacToe(Node):
    def __init__(self):
        super().__init__('tictactoe_node')
        self.board = [' '] * 9
        self.difficulty = self.select_difficulty()
        self.play_game()

    def select_difficulty(self):
        while True:
            print("\nChoose AI Difficulty:\n1. Easy\n2. Medium\n3. Hard")
            choice = input("Enter 1/2/3: ")
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("Invalid input. Try again.")

    def print_board(self):
        print("\n")
        for i in range(3):
            print(f" {self.board[i*3]} | {self.board[i*3+1]} | {self.board[i*3+2]} ")
            if i < 2:
                print("---|---|---")

    def is_winner(self, board, player):
        win_cond = [(0,1,2),(3,4,5),(6,7,8),
                    (0,3,6),(1,4,7),(2,5,8),
                    (0,4,8),(2,4,6)]
        return any(all(board[i] == player for i in combo) for combo in win_cond)

    def is_draw(self):
        return ' ' not in self.board

    def get_valid_moves(self):
        return [i for i, cell in enumerate(self.board) if cell == ' ']

    def player_move(self):
        while True:
            try:
                move = int(input("Enter your move (1-9): ")) - 1
                if move in self.get_valid_moves():
                    self.board[move] = PLAYER
                    break
                else:
                    print("Invalid move. Try again.")
            except:
                print("Please enter a valid number.")

    def ai_move(self):
        if self.difficulty == 1:
            move = random.choice(self.get_valid_moves())
        elif self.difficulty == 2:
            move = self.medium_ai()
        else:
            move = self.minimax(self.board, AI)['index']
        self.board[move] = AI
        print(f"AI placed at {move + 1}")

    def medium_ai(self):
        for move in self.get_valid_moves():
            board_copy = self.board[:]
            board_copy[move] = AI
            if self.is_winner(board_copy, AI):
                return move
        for move in self.get_valid_moves():
            board_copy = self.board[:]
            board_copy[move] = PLAYER
            if self.is_winner(board_copy, PLAYER):
                return move
        return random.choice(self.get_valid_moves())

    def minimax(self, board, player):
        opponent = PLAYER if player == AI else AI
        if self.is_winner(board, PLAYER):
            return {'score': -10}
        elif self.is_winner(board, AI):
            return {'score': 10}
        elif ' ' not in board:
            return {'score': 0}

        moves = []
        for i in self.get_valid_moves():
            move = {'index': i}
            board[i] = player
            result = self.minimax(board, opponent)
            move['score'] = result['score']
            board[i] = ' '
            moves.append(move)

        if player == AI:
            return max(moves, key=lambda x: x['score'])
        else:
            return min(moves, key=lambda x: x['score'])

    def play_game(self):
        print("\nTic-Tac-Toe: You (X) vs AI (O)")
        self.print_board()
        while True:
            self.player_move()
            self.print_board()
            if self.is_winner(self.board, PLAYER):
                print("You win!")
                break
            if self.is_draw():
                print("It's a draw!")
                break
            self.ai_move()
            self.print_board()
            if self.is_winner(self.board, AI):
                print("AI wins!")
                break
            if self.is_draw():
                print("It's a draw!")
                break

def main(args=None):
    rclpy.init(args=args)
    game = TicTacToe()
    rclpy.shutdown()
