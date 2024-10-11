import click
import numpy as np


def create_board(rows: int, columns: int) -> np.ndarray:
    """
    Create a game board with the specified number of rows and columns.

    Args:
        rows (int): Number of rows in the board.
        columns (int): Number of columns in the board.

    Returns:
        np.ndarray: A numpy array representing the game board initialized with zeros.
    """
    return np.zeros((rows, columns), dtype=int)


def print_board(board: np.ndarray) -> None:
    """
    Print the current state of the game board to the console.

    Args:
        board (np.ndarray): The game board to be printed.
    """
    print("-" * (2 * board.shape[1] + 1))
    for row in reversed(board):
        print("|" + "|".join([str(cell) if cell != 0 else " " for cell in row]) + "|")
    print("-" * (2 * board.shape[1] + 1))
    print(" " + " ".join(map(str, range(1, board.shape[1] + 1))))


def drop_piece(board: np.ndarray, col: int, piece: int) -> int:
    """
    Place a piece on the game board.

    Args:
        board (np.ndarray): The game board where the piece will be dropped.
        col (int): The column index where the piece will be placed.
        piece (int): The piece identifier (1 or 2).

    Returns:
        int: The row index where the piece was placed.

    Raises:
        ValueError: If the column is full and no row is available.
    """
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            board[r][col] = piece
            return r
    raise ValueError("No available row in this column")


def is_column_valid(board: np.ndarray, col: int) -> bool:
    """
    Check if a column has space available for a new piece.

    Args:
        board (np.ndarray): The game board.
        col (int): The column index to check.

    Returns:
        bool: True if the column is available, False otherwise.
    """
    return board[-1][col] == 0


def has_winning_move(board: np.ndarray, piece: int) -> bool:
    """
    Check if the current piece has a winning move.

    Args:
        board (np.ndarray): The game board.
        piece (int): The piece identifier (1 or 2).

    Returns:
        bool: True if there is a winning move, False otherwise.
    """
    rows, columns = board.shape
    directions = [(0, 1), (1, 0), (1, 1), (1, -1)]
    for r in range(rows):
        for c in range(columns):
            if board[r][c] == piece:
                for dr, dc in directions:
                    if all(
                        0 <= r + i * dr < rows and 0 <= c + i * dc < columns and board[r + i * dr][c + i * dc] == piece
                        for i in range(4)
                    ):
                        return True
    return False


@click.command("Play Connect 4")
@click.option("--rows", default=6, help="Number of rows for the game board.")
@click.option("--columns", default=7, help="Number of columns for the game board.")
def play_game(rows: int, columns: int) -> None:
    """
    Run the main game loop for Connect 4.

    Args:
        rows (int): Number of rows for the game board.
        columns (int): Number of columns for the game board.
    """
    board = create_board(rows, columns)
    turn = 0
    print("Welcome to Connect 4!")
    print_board(board)

    while True:
        print(f"Player {turn + 1}'s turn (Piece = {turn + 1})")
        try:
            col = int(input(f"Select a column (1-{columns}): ")) - 1
            if col < 0 or col >= columns:
                raise ValueError(f"Invalid column. Please select a column between 1 and {columns}.")
            if not is_column_valid(board, col):
                raise ValueError("Column full. Try a different column.")
            drop_piece(board, col, turn + 1)
        except ValueError as e:
            print(e)
            continue

        print_board(board)
        if has_winning_move(board, turn + 1):
            print(f"Player {turn + 1} wins! Congratulations!")
            break
        turn = (turn + 1) % 2


if __name__ == "__main__":
    play_game()
