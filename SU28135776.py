import sys
import stdio

# global vars that are updated in the check input validation function
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
        # returns the string to display for a given piece
        piece = board[row][col]
        if piece == ' ':
            # empty field
            return '  '
        elif piece == 's':
            # sink field
            return ' s'
        elif piece == 'x':
            # blocked field
            return ' x'
        elif piece.islower():
            # piece is light
            return ' ' + piece
        elif piece.isupper():
            # peice is dark
            return ' ' + piece
        elif len(piece) == 2:
            # number representing bottom left most piece
            return piece
        return "  "

    # write all the numbers at the top
    stdio.writeln('    ' + '  '.join([str(i) for i in range(num_cols)]))
    stdio.writeln(get_row_separator())

    # display the board
    for i in range(num_rows):
        out = ' ' + str(num_rows - i-1) + ' |'
        for j in range(num_cols):
            out += get_piece_display(i, j) + '|'
        stdio.writeln(out)
        stdio.writeln(get_row_separator())


def check_sink_range(row, col):
    # checks if the sink is within the outer 3 columns and rows
    if ((col > 2) and (col < NUM_COLUMNS - 3) and (row > 2) and (row < NUM_ROWS - 3)):
        return False
    else:
        return True


def check_piece_range(row, col):
    # checks if the piece is not within the outer 3 columns and rows
    if ((col > 2) and (col < NUM_COLUMNS - 3) and (row > 2) and (row < NUM_ROWS - 3)):
        return True
    else:
        return False


def check_index_on_board(row, col):
    # checks if a peice is legitimately on the board
    if (row not in range(0, NUM_ROWS) or col not in range(0, NUM_COLUMNS)):
        return False
    return True


def check_piece_type(piece_object, piece_type):
    # checks whether the peice type is valid according to the program spesifications
    if (piece_object == 's'):
        if (piece_type not in ['1', '2']):
            return False
    elif (piece_object in ['l', 'x', 'd']):
        if (piece_type not in ['a', 'b', 'c', 'd']):
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
            # either a piece or a sink
            if (check_index_on_board(int(symbols[2]), int(symbols[3]))):
                # piece or sink is on the board
                # symbols[0] is the object type and symbols[1] is the piece type
                if (symbols[0] in ['l', 'd', 's']):
                    # valid object type
                    if (check_piece_type(symbols[0], symbols[1])):
                        # peice type aligns to object type
                        if (symbols[0] == "s"):
                            # a sink
                            if (check_sink_range(int(symbols[2]), int(symbols[3]))):
                                # sink is within the outer 3 columns and rows
                                x = int(symbols[3])
                                y = (9 - int(symbols[2])) % 10
                                if (board[y][x] == ' '):
                                    # empty field
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
                                                    # all fields are empty
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
                            # a piece
                            x = int(symbols[3])
                            y = (9 - int(symbols[2])) % 10
                            if (check_piece_range(int(symbols[2]), int(symbols[3]))):
                                # piece is not within the outer 3 columns and rows
                                if board[y][x] == ' ':
                                    # empty field
                                    # symbol var that represents the piece type and if it is dark or light
                                    symbol = ''
                                    if (symbols[0] == 'l'):
                                        symbol = symbols[1].lower()
                                    elif (symbols[0] == 'd'):
                                        symbol = symbols[1].upper()
                                    board[y][x] = symbol
                                    if (symbols[1] == "d"):
                                        # 2x2 piece
                                        if (board[y][x+1] == " " and board[y-1][x] == " " and board[y-1][x+1] == " "):
                                            # all fields empty
                                            if (check_piece_range(x+1, y)):
                                                if (check_piece_range(x, y-1)):
                                                    if (check_piece_range(x+1, y-1)):
                                                        # all fields are within the inner board

                                                        # index representing the bottom left most field of that piece
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
            x = int(symbols[2])
            y = (9 - int(symbols[1])) % 10
            if (check_index_on_board(int(symbols[1]), int(symbols[2]))):
                # blocked field is on the board
                if (symbols[0] == "x"):
                    # just making sure it is a blocked field
                    if (board[y][x] == " "):
                        # empty field
                        board[y][x] = 'x'
                    else:
                        stdio.writeln(
                            "ERROR: Field " + symbols[1] + " " + symbols[2] + " not free")
                        exit()
                else:
                    stdio.writeln("ERROR: Invalid object type " + symbols[0])
                    exit()
        else:
            stdio.writeln("ERROR: Invalid input")
            exit()
        print_board(board)
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
    # print_board(board)


if __name__ == "__main__":
    main()
