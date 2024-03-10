import sys
import stdio

NUM_ROWS = 10
NUM_COLUMNS = 10
GUI_MODE = False
GAME_OVER = False


def check_input_validation():

    # checks whether the input conforms to the standards set out otherwise raises an error
    global NUM_ROWS, NUM_COLUMNS, GUI_MODE
    if len(sys.argv) > 4:
        stdio.writeln('ERROR: Too many arguments')
        sys.exit(1)
    elif len(sys.argv) < 4:
        stdio.writeln('ERROR: Too few arguments')
        sys.exit(1)
    try:
        if (int(sys.argv[3]) != 0) and (int(sys.argv[3]) != 1):
            raise ValueError
        if (int(sys.argv[1]) not in [8, 9, 10]):
            raise ValueError
        if (int(sys.argv[2]) not in [8, 9, 10]):
            raise ValueError
        NUM_ROWS = int(sys.argv[1])
        NUM_COLUMNS = int(sys.argv[2])
        GUI_MODE = bool(int(sys.argv[3]))
    except ValueError:
        stdio.writeln('ERROR: Invalid argument')
        sys.exit(1)


def print_board(board):
    # vars for the length and width of the board
    num_rows = len(board)
    num_cols = len(board[0])

    def get_row_separator():
        # returns a row separator string
        return '   +--' + '--'.join(['+' for _ in range(num_cols)])

    def get_piece_display(row, col):
        # TODO: Implement the row and col displays for the bootom left corner of peices
        # checks what peice is on the given square and returns the appropriate characters
        # s: represents a sink
        # x: represents a blocked field
        # a	1x1x1
        # b	1x1x2
        # c	1x1x3
        # d	2x2x2
        piece = board[row][col]
        if piece == ' ':
            return '  '
        elif piece == 's':
            return ' s'
        elif piece == 'x':
            return ' x'
        elif piece.islower():
            return ' ' + piece
        elif piece.isupper():
            return ' ' + piece
        return '  '

    stdio.writeln('')

    # write all the numbers at the top
    stdio.writeln('    ' + '  '.join([str(i) for i in range(num_cols)]))
    stdio.writeln(get_row_separator())

    for i in range(num_rows):
        out = ' ' + str(num_rows - i-1) + ' |'
        for j in range(num_cols):
            out += get_piece_display(i, j) + '|'
        stdio.writeln(out)
        stdio.writeln(get_row_separator())


def get_board_setup_from_commandline():
    stdio.writeln('')
    stdio.writeln('Enter board setup:')

    # init board 2d array
    board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

    while True:
        line = stdio.readLine().strip()
        if '#' in line:
            # Exit the loop if '#' is found in the line
            break
        symbols = line.split(" ")
        if (len(symbols) == 4):
            # either a peice or a sink
            try:
                if (symbols[0] == "s"):
                    # a sink
                    x = int(symbols[3])
                    y = (9 -int(symbols[2])) % 9
                    board[y][x] = "s"
                    if (symbols[1] == "2"):
                        # a 2x2 sink
                        board[y][x+1] = "s"
                        board[y-1][x] = "s"
                        board[y-1][x+1] = "s"
                        pass
                else:
                    # a peice
                    pass
            except:
                stdio.writeln("Error with board setup input")
                exit(1)
        elif (len(symbols) == 3):
          # a blocked field
            try:
                board[symbols[1]][symbols[2]] = 'x'
            except:
                stdio.writeln("Error with board setup input")
    return board


def main():
    # make sure the input fits the criteria and updates the global vars,NUM_ROWS,NUM_COLUMS,GUI_MODE
    check_input_validation()

    # read input from the commandline and update the board accordingly
    board = get_board_setup_from_commandline()

    print_board(board)
    # main game loop
    while not GAME_OVER:
        pass


if __name__ == "__main__":
    main()
