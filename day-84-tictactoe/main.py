def print_board(board):
    print("\n")
    print(f" {board[0]} | {board[1]} | {board[2]} ")
    print("---+---+---")
    print(f" {board[3]} | {board[4]} | {board[5]} ")
    print("---+---+---")
    print(f" {board[6]} | {board[7]} | {board[8]} ")
    print("\n")


def check_winner(board, player):
    win_conditions = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)              # Diagonals
    ]
    # In Python, comparison operators can be chained arbitrarily, 
    # and they all evaluate against each other pairwise using an implicit and.
    # (board[a] == board[b]) and (board[b] == board[c]) and (board[c] == player)
    return any(board[a] == board[b] == board[c] == player for a, b, c in win_conditions)


def play_game():
    # Initialize board with numbers 1-9 so players know which keys to press
    board = [str(i) for i in range(1, 10)]
    current_player = "X"
    moves_made = 0

    print("Welcome to Tic-Tac-Toe!")
    print("Enter a number (1-9) to place your mark.")

    # print board with numbers to give directions
    print_board(board)
    # prepare board with spaces only
    board = [str(' ') for i in range(1, 10)]

    while True:
        # print board with space and plays
        print_board(board)
        move = input(f"Player {current_player}, choose a position (1-9): ").strip()

        # Validate input
        if not move.isdigit() or not (1 <= int(move) <= 9):
            print("Invalid input. Please enter a number between 1 and 9.")
            continue

        index = int(move) - 1

        # Check if spot is already taken
        if board[index] in ["X", "O"]:
            print("That spot is already taken! Try another.")
            continue

        # Place mark
        board[index] = current_player
        moves_made += 1

        # Check win or draw
        if check_winner(board, current_player):
            print_board(board)
            print(f"Player {current_player} wins!")
            break
        elif moves_made == 9:
            print_board(board)
            print("It's a tie!")
            break

        # Switch turns
        current_player = "O" if current_player == "X" else "X"


if __name__ == "__main__":
    while True:
        play_game()
        again = input("Play again? (y/n): ").strip().lower()
        if again != "y":
            print("Thanks for playing!")
            break