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
        elif len(piece) == 2:
            # number representing peice
            return piece
        return "  "

    # write all the numbers at the top
    stdio.writeln('    ' + '  '.join([str(i) for i in range(num_cols)]))
    stdio.writeln(get_row_separator())

    for i in range(num_rows):
        out = ' ' + str(num_rows - i-1) + ' |'
        for j in range(num_cols):
            out += get_piece_display(i, j) + '|'
        stdio.writeln(out)
        stdio.writeln(get_row_separator())


def check_sink_range(row, col):
    if ((col > 2) and (col < NUM_COLUMNS - 3) and (row > 2) and (row < NUM_ROWS - 3)):
        return False
    else:
        return True


def check_peice_range(row, col):
    if ((col > 2) and (col < NUM_COLUMNS - 3) and (row > 2) and (row < NUM_ROWS - 3)):
        return True
    else:
        return False


def check_index_on_board(row, col):
    if (row not in range(0, NUM_ROWS) or col not in range(0, NUM_COLUMNS)):
        return False
    return True


def check_peice_type(peice_object, peice_type):
    if (peice_object == 's'):
        if (peice_type not in ['1', '2']):
            return False
    elif (peice_object in ['l', 'x', 'd']):
        if (peice_type not in ['a', 'b', 'c', 'd']):
            return False
    return True


def get_board_setup_from_commandline():

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
            if (check_index_on_board(int(symbols[2]), int(symbols[3]))):
                if (symbols[0] in ['l', 'd', 's']):
                    if (check_peice_type(symbols[0], symbols[1])):
                        if (symbols[0] == "s"):
                            # a sink
                            if (check_sink_range(int(symbols[2]), int(symbols[3]))):
                                x = int(symbols[3])
                                y = (9 - int(symbols[2])) % 9
                                if (board[y][x] == ' '):
                                    board[y][x] = "s"
                                else:
                                    stdio.writeln(
                                        "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                    exit()

                                if (symbols[1] == "2"):
                                    # a 2x2 sink
                                    if (check_sink_range(x+1, y)):
                                        if (check_sink_range(x, y-1)):
                                            if (check_sink_range(x+1, y-1)):
                                                if (board[y][x+1] == ' ' and board[y-1][x] == ' ' and board[y-1][x+1] == ' '):
                                                    board[y][x+1] = "s"
                                                    board[y-1][x] = "s"
                                                    board[y-1][x+1] = "s"
                                                else:
                                                    stdio.writeln(
                                                        "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                                    exit()
                                            else:
                                                stdio.writeln(
                                                    "ERROR: Sink in the wrong position")
                                                exit()
                                        else:
                                            stdio.writeln(
                                                "ERROR: Sink in the wrong position")
                                            exit()
                                    else:
                                        stdio.writeln(
                                            "ERROR: Sink in the wrong position")
                                        exit()
                            else:
                                stdio.writeln(
                                    "ERROR: Sink in the wrong position")
                                exit()
                        else:
                            # a peice
                            x = int(symbols[3])
                            y = (9 - int(symbols[2])) % 9
                            if (check_peice_range(int(symbols[2]), int(symbols[3]))):
                                if board[y][x] == ' ':  # empty field
                                    if (symbols[0] == 'l'):
                                        board[y][x] = symbols[1].lower()
                                        if (symbols[1] == "d"):
                                            if (board[y][x+1] == " " and board[y-1][x] == " " and board[y-1][x+1] == " "):
                                                if (check_peice_range(x+1, y)):
                                                    if (check_peice_range(x, y-1)):
                                                        if (check_peice_range(x+1, y-1)):
                                                            index = (
                                                                int(symbols[2]) * NUM_COLUMNS) + int(symbols[3])
                                                            # pad the index on the right by a space if it is one digit
                                                            if (index < 10):
                                                                index = " " + \
                                                                    str(index)
                                                            board[y][x +
                                                                     1] = str(index)
                                                            board[y -
                                                                  1][x] = str(index)
                                                            board[y-1][x +
                                                                       1] = str(index)
                                                        else:
                                                            stdio.writeln(
                                                                "ERROR: Piece in the wrong position")
                                                            exit()
                                                    else:
                                                        stdio.writeln(
                                                            "ERROR: Piece in the wrong position")
                                                        exit()
                                                else:
                                                    stdio.writeln(
                                                        "ERROR: Piece in the wrong position")
                                                    exit()
                                            else:
                                                stdio.writeln(
                                                    "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                                exit()
                                    elif (symbols[0] == 'd'):
                                        board[y][x] = symbols[1].upper()
                                        if symbols[1] == "d":
                                            if (board[y][x+1] == " " and board[y-1][x] == " " and board[y-1][x+1] == " "):
                                                if (check_peice_range(x+1, y)):
                                                    if (check_peice_range(x, y-1)):
                                                        if (check_peice_range(x+1, y-1)):
                                                            index = (
                                                                int(symbols[2]) * NUM_COLUMNS) + int(symbols[3])
                                                            # pad the index on the right by a space if it is one digit
                                                            if (index < 10):
                                                                index = " " + \
                                                                    str(index)
                                                            board[y][x +
                                                                     1] = str(index)
                                                            board[y -
                                                                  1][x] = str(index)
                                                            board[y-1][x +
                                                                       1] = str(index)
                                                        else:
                                                            stdio.writeln(
                                                                "ERROR: Piece in the wrong position")
                                                            exit()
                                                    else:
                                                        stdio.writeln(
                                                            "ERROR: Piece in the wrong position")
                                                        exit()
                                                else:
                                                    stdio.writeln(
                                                        "ERROR: Piece in the wrong position")
                                                    exit()
                                            else:
                                                stdio.writeln(
                                                    "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                                exit()
                                else:
                                    stdio.writeln(
                                        "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                    exit()
                            else:
                                stdio.writeln(
                                    "ERROR: Piece in the wrong position")
                                exit()
                    else:
                        stdio.writeln(
                            "ERROR: Invalid piece type " + symbols[1])
                        exit()
                else:
                    stdio.writeln("ERROR: Invalid object type " + symbols[0])
                    exit()
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[2] + " " + symbols[3] + " not on board")
                exit()
        elif (len(symbols) == 3):
            # a blocked field
            board[symbols[1]][symbols[2]] = 'x'
        else:
            stdio.writeln("ERROR: Invalid input")
            exit()
    return board


def check_piece_upright(row, col, board):
    try:
        upright = not (board[row][col] in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D'] and (row != 9 and (
            board[row+1][col] == str((row * len(board) + col)) or board[row][col+1] == str((row * len(board) + col)))))
    except:
        upright = False
    stdio.writeln(upright)


def main():
    # make sure the input fits the criteria and updates the global vars,NUM_ROWS,NUM_COLUMS,GUI_MODE
    check_input_validation()

    # read input from the commandline and update the board accordingly
    board = get_board_setup_from_commandline()
    print_board(board)
    # main game loop
    # while not GAME_OVER:
    #     pass


if __name__ == "__main__":
    main()
