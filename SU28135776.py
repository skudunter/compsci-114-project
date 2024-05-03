import sys
import stdio

# global vars that are updated in the check input validation function
NUM_ROWS = 10
NUM_COLUMNS = 10
GUI_MODE = False
initial_board_state = []
errors = {
    "num_arg": "ERROR: Invalid number of arguments",
    "invalid_arg": "ERROR: Invalid argument",
    "invalid_input": "ERROR: Invalid input",
    "field_not_free": "ERROR: Field {} {} not free",
    "field_not_on_board": "ERROR: Field {} {} not on board",
    "sink_wrong_position": "ERROR: Sink in the wrong position",
    "piece_wrong_position": "ERROR: Piece in the wrong position",
    "sink_next_to_sink": "ERROR: Sink cannot be next to another sink",
    "cannot_move_beyond_board": "ERROR: Cannot move beyond the board",
    "piece_type_invalid": "ERROR: Invalid piece type {}",
    "object_type_invalid": "ERROR: Invalid object type {}",
}


def check_input_validation():
    # check if the number of arguments and type is correct
    global NUM_ROWS, NUM_COLUMNS, GUI_MODE
    if len(sys.argv) != 4:
        stdio.writeln(errors["num_arg"])
        sys.exit(1)
    try:
        NUM_ROWS, NUM_COLUMNS, GUI_MODE = map(int, sys.argv[1:])
        if NUM_ROWS not in [8, 9, 10] or NUM_COLUMNS not in [8, 9, 10] or GUI_MODE not in [0, 1]:
            raise ValueError
    except ValueError:
        stdio.writeln(errors["invalid_arg"])
        sys.exit(1)


def print_board(board):
    # prints the board to the console
    def get_row_separator():
        return '   +--' + '--'.join(['+' for _ in range(num_cols)])

    def get_piece_display(row, col):
        piece = board[row][col]
        if piece == ' ':
            return '  '
        elif piece == 's':
            return ' s'
        elif piece == 'x':
            return ' x'
        elif piece.isalpha():
            return ' ' + piece
        elif len(piece) == 2:
            return piece
        return "  "

    num_rows = len(board)
    num_cols = len(board[0])

    stdio.writeln('    ' + '  '.join(map(str, range(num_cols))))
    stdio.writeln(get_row_separator())

    for i in range(num_rows):
        out = ' ' + str(num_rows - i-1) + ' |'
        for j in range(num_cols):
            out += get_piece_display(i, j) + '|'
        stdio.writeln(out)
        stdio.writeln(get_row_separator())


def check_sink_range(row, col):
    # check if sink in outer 3 columns and rows
    return not ((2 < col < NUM_COLUMNS - 3) and (2 < row < NUM_ROWS - 3))


def check_piece_range(row, col):
    # check if piece not in outer 3 columns and rows
    return ((2 < col < NUM_COLUMNS - 3) and (2 < row < NUM_ROWS - 3))


def check_index_on_board(row, col):
    # checks if the given index is on the board
    return 0 <= row < NUM_ROWS and 0 <= col < NUM_COLUMNS


def check_piece_type(piece_object, piece_type):
    # checks whether the peice type is valid according to the program spesifications
    if (piece_object == 's'):
        if (piece_type not in ['1', '2']):
            return False
    elif (piece_object in ['l', 'x', 'd']):
        if (piece_type not in ['a', 'b', 'c', 'd']):
            return False
    return True


def check_sink_adjacent(row, col, board):
    # checks if sinks are placed next to each others
    return any([
        col > 0 and board[row][col-1] == 's',
        col < len(board[0]) - 1 and board[row][col+1] == 's',
        row > 0 and board[row-1][col] == 's',
        row < len(board) - 1 and board[row+1][col] == 's'
    ])


def handle_sink_input(symbols, board, y, x):
    if (check_sink_range(y, x)):
        if board[y][x] == ' ':
            if symbols[1] == "2":
                if all(check_index_on_board[i][j] for i in range(y - 1, y + 1) for j in range(x, x + 2)):
                    if all(board[i][j] == ' ' for i in range(y - 1, y + 1) for j in range(x, x + 2)):
                        board[y][x] = 's'
                        board[y][x + 1] = 's'
                        board[y - 1][x] = 's'
                        board[y - 1][x + 1] = 's'
                    else:
                        print("ERROR: Field not free")
                        exit()
                else:
                    print("ERROR: Sink in the wrong position")
                    exit()
            elif symbols[1] == "1":
                if not check_sink_adjacent(y, x, board):
                    board[y][x] = 's'
                else:
                    print("ERROR: Sink cannot be next to another sink")
                    exit()
            else:
                print("ERROR: Invalid sink size")
                exit()
        else:
            print("ERROR: Field not free")
            exit()
    else:
        print("ERROR: Sink in the wrong position")
        exit()


def handle_piece_input(symbols, board, y, x):
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
                                row = NUM_ROWS - 1 - \
                                    (index // NUM_COLUMNS)
                                column = index % NUM_COLUMNS
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


def handle_blocked_field(symbols, board, y, x):
    if (board[y][x] == " "):
        board[y][x] = 'x'
    else:
        stdio.writeln(
            errors["field_not_free"].format(symbols[1], symbols[2]))
        exit()


def get_board_setup_from_commandline():
    # get the board setup from the command line and populate the 2D array
    board = [[' ' for _ in range(NUM_COLUMNS)] for _ in range(NUM_ROWS)]

    while True:
        if not stdio.hasNextLine():
            break
        line = stdio.readLine().strip()
        if '#' in line:
            # Exit the loop if '#' is found in the line
            break
        symbols = line.split(" ")

        if (len(symbols) not in [3, 4]):
            stdio.writeln(errors["invalid_input"])
            sys.exit(1)
        if (check_index_on_board(int(symbols[len(symbols)-1]), int(symbols[len(symbols)-2])) == False):
            stdio.writeln(errors["field_not_on_board"].format(
                symbols[2], symbols[3]))
            sys.exit(1)
        if (symbols[0] not in ["x", "l", "d", "s"]):
            stdio.writeln(errors["object_type_invalid"].format(symbols[0]))
            sys.exit(1)

        x = int(symbols[len(symbols)-1])
        y = (NUM_ROWS-1 - int(symbols[len(symbols)-2])) % NUM_ROWS

        if (len(symbols) == 4):
            if (check_piece_type(symbols[0], symbols[1])):
                if (symbols[0] == "s"):
                    # a sink
                    handle_sink_input(symbols, board, y, x)
                else:
                    # a piece
                    handle_piece_input(symbols, board, y, x)
            else:
                stdio.writeln(
                    errors["piece_type_invalid"].format(symbols[1]))
                exit()
        else:
            # a blocked field
            handle_blocked_field(symbols, board, y, x)
    return board


def get_player_from_board(symbols, board):
    # is run once to determine the player from the first move
    if (len(symbols) == 3):
        x = int(symbols[1])
        y = (NUM_ROWS-1 - int(symbols[0])) % NUM_ROWS

        if (check_index_on_board(int(symbols[0]), int(symbols[1]))):
            if (board[y][x] in ["a", "b", "c", "d"]):
                return "light"
            else:
                return "dark"
        else:
            stdio.writeln("ERROR: Field " +
                          symbols[0] + " " + symbols[1] + " not on board")
            exit()
    else:
        stdio.writeln("Error: Illegal argument")
        exit()


def move_a_piece(symbols, direction, board, isInCheckMode=False):
    # moves 'a' piece
    x = int(symbols[1])
    y = (NUM_ROWS-1 - int(symbols[0])) % NUM_ROWS

    if (direction == 'u'):
        # move up
        if (y > 0):
            if (board[y-1][x] == 's'):
                if not isInCheckMode:
                    board[y][x] = ' '
                return 1
            elif (board[y-1][x] == ' '):
                if not isInCheckMode:
                    board[y-1][x] = board[y][x]
                    board[y][x] = ' '
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln(
                        "ERROR: Field " + str(int(symbols[0]) + 1) + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
        return 0
    elif (direction == 'd'):
        # move down
        if (y < NUM_ROWS-1):
            if (board[y+1][x] == 's'):
                if not isInCheckMode:
                    board[y][x] = ' '
                return 1
            elif (board[y+1][x] == ' '):
                if not isInCheckMode:
                    board[y+1][x] = board[y][x]
                    board[y][x] = ' '
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln(
                        "ERROR: Field " + str(int(symbols[0]) - 1) + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
        return 0
    elif (direction == 'l'):
        # move left
        if (x > 0):
            if (board[y][x-1] == 's'):
                if not isInCheckMode:
                    board[y][x] = ' '
                return 1
            elif (board[y][x-1] == ' '):
                if not isInCheckMode:
                    board[y][x-1] = board[y][x]
                    board[y][x] = ' '
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln(
                        "ERROR: Field " + symbols[0] + " " + str(int(symbols[1]) - 1) + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln(
                    "ERROR: Cannot move beyond the board")
                exit()
        return 0
    elif (direction == 'r'):
        # move right
        if (board[y][x+1] == 's'):
            if not isInCheckMode:
                board[y][x] = ' '
            return 1
        elif (x < NUM_COLUMNS-1):
            if (board[y][x+1] == ' '):
                if not isInCheckMode:
                    board[y][x+1] = board[y][x]
                    board[y][x] = ' '
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln(
                        "ERROR: Field " + symbols[0] + " " + str(int(symbols[0]) + 1) + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    return 0


def move_b_piece(symbols, direction, board, isInCheckMode=False):
    # 1x1x2
    x = int(symbols[1])
    y = (NUM_ROWS - 1 - int(symbols[0])) % NUM_ROWS

    # make index to check against
    index = str(((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1]))
    if (int(index.strip()) < 10):
        index = " " + \
            index

    def get_orientation(row, col, board):
        # returns the orientation of the piece
        # orientation can be vertical, horizontal-x, or horizontal-y
        try:
            if board[row][col + 1] == str(index):
                return "horizontal-x"
        except IndexError:
            pass
        try:
            if board[row - 1][col] == str(index):
                return "horizontal-y"
        except IndexError:
            pass

        return "vertical"  # default to vertical

    orientation = get_orientation(y, x, board)

    # actually do the movement code
    if direction == 'u':
        # move up
        if (orientation == "vertical"):
            if (y > 1):
                if (board[y-1][x] == " " and board[y-2][x] == " "):
                    # fields are empty
                    locale_index = str(
                        ((int(symbols[0])+1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-1][x] = board[y][x]
                        board[y-2][x] = str(locale_index)
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y-1][x] == "s" and board[y-2][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        if (orientation == "horizontal-x"):
            if (y > 0):
                if (board[y-1][x] == " " and board[y-1][x+1] == " "):
                    locale_index = str(
                        ((int(symbols[0])+1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-1][x] = board[y][x]
                        board[y-1][x+1] = str(locale_index)
                        board[y][x] = " "
                        board[y][x+1] = " "
                    else:
                        return 1
                elif (board[y-1][x] == "s" and board[y-1][x+1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        if (orientation == "horizontal-y"):
            if (y > 1):
                if (board[y-2][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])+2) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-2][x] = board[y][x]
                        board[y][x] = " "
                        board[y-1][x] = " "
                    else:
                        return 1
                elif (board[y-2][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free ")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    elif (direction == 'd'):
        if orientation == "vertical":
            if (y < NUM_ROWS-2):
                if (board[y+1][x] == " " and board[y+2][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])-2) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+2][x] = board[y][x]
                        board[y+1][x] = str(locale_index)
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s" and board[y+2][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (y < NUM_ROWS-1):
                if (board[y+1][x] == " " and board[y+1][x+1] == " "):
                    locale_index = str(
                        ((int(symbols[0])-1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+1][x] = board[y][x]
                        board[y+1][x+1] = str(locale_index)
                        board[y][x] = " "
                        board[y][x+1] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s" and board[y+1][x+1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (y < NUM_ROWS-1):
                if (board[y+1][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])-1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+1][x] = board[y][x]
                        board[y][x] = " "
                        board[y-1][x] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    elif (direction == 'l'):
        # move left
        if (orientation == "vertical"):
            if (x > 1):
                if (board[y][x-1] == " " and board[y][x-2] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-2)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-2] = board[y][x]
                        board[y][x-1] = str(locale_index)
                        board[y][x] = " "
                elif (board[y][x-1] == "s" and board[y][x-2] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (x > 0):
                if (board[y][x-1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-1] = board[y][x]
                        board[y][x] = " "
                        board[y][x+1] = " "
                    else:
                        return 1
                elif (board[y][x-1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (x > 0):
                if (board[y][x-1] == " " and board[y-1][x-1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-1] = board[y][x]
                        board[y-1][x-1] = locale_index
                        board[y][x] = " "
                        board[y-1][x] = " "
                    else:
                        return 1
                elif (board[y][x-1] == "s" and board[y-1][x-1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()

            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    elif (direction == "r"):
        if (orientation == "vertical"):
            if (x < NUM_COLUMNS-2):
                if (board[y][x+1] == " " and board[y][x+2] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+1] = board[y][x]
                        board[y][x+2] = locale_index
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y][x+1] == "s" and board[y][x+2] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (x < NUM_COLUMNS-2):
                if (board[y][x+2] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+2)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+2] = board[y][x]
                        board[y][x] = " "
                        board[y][x+1] = " "
                    else:
                        return 1
                elif (board[y][x+2] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (x < NUM_COLUMNS-1):
                if (board[y][x+1] == " " and board[y-1][x+1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+1] = board[y][x]
                        board[y-1][x+1] = locale_index
                        board[y][x] = " "
                        board[y-1][x] = " "
                    else:
                        return 1
                elif (board[y][x+1] == "s" and board[y-1][x+1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                    return 2
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    return 0


def move_c_piece(symbols, direction, board, isInCheckMode=False):
    # 1x1x3
    x = int(symbols[1])
    y = (NUM_ROWS - 1 - int(symbols[0])) % NUM_ROWS

    # make index to check against
    index = str(((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1]))
    if (int(index.strip()) < 10):
        index = " " + \
            index

    def get_orientation(row, col, board):
        # returns the orientation of the piece
        # orientation can be vertical,horizontal-x or horizontal-y
        try:
            if board[row][col + 1] == str(index):
                return "horizontal-x"
            if board[row-1][col] == str(index):
                return "horizontal-y"
        except IndexError:
            pass
        return "vertical"  # default to vertical

    orientation = get_orientation(y, x, board)

    # actually do the movement code
    if direction == 'u':
        # move up
        if (orientation == "vertical"):
            if (y > 2):
                if (board[y-1][x] == " " and board[y-2][x] == " " and board[y-3][x] == " "):
                    # fields are empty
                    locale_index = str(
                        ((int(symbols[0])+1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-1][x] = board[y][x]
                        board[y-2][x] = str(locale_index)
                        board[y-3][x] = str(locale_index)
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y-1][x] == "s" and board[y-2][x] == "s" and board[y-3][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        if (orientation == "horizontal-x"):
            if (y > 0):
                if (board[y-1][x] == " " and board[y-1][x+1] == " " and board[y-1][x+2] == " "):
                    locale_index = str(
                        ((int(symbols[0])+1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-1][x] = board[y][x]
                        board[y-1][x+1] = str(locale_index)
                        board[y-1][x+2] = str(locale_index)
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    else:
                        return 1
                elif (board[y-1][x] == "s" and board[y-1][x+1] == "s" and board[y-1][x+2] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        if (orientation == "horizontal-y"):
            if (y > 0):
                if (board[y-3][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])+3) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y-3][x] = board[y][x]
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    else:
                        return 1
                elif (board[y-3][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()

            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()

    elif (direction == 'd'):
        if orientation == "vertical":
            if (y < NUM_ROWS-3):
                if (board[y+1][x] == " " and board[y+2][x] == " " and board[y+3][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])-3) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+3][x] = board[y][x]
                        board[y+2][x] = str(locale_index)
                        board[y+1][x] = str(locale_index)
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s" and board[y+2][x] == "s" and board[y+3][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (y < NUM_ROWS-1):
                if (board[y+1][x] == " " and board[y+1][x+1] == " " and board[y+1][x+2] == " "):
                    locale_index = str(
                        ((int(symbols[0])-1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+1][x] = board[y][x]
                        board[y+1][x+1] = str(locale_index)
                        board[y+1][x+2] = str(locale_index)
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s" and board[y+1][x+1] == "s" and board[y+1][x+2] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (y < NUM_ROWS-1):
                if (board[y+1][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])-1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y+1][x] = board[y][x]
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    else:
                        return 1
                elif (board[y+1][x] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    elif (direction == 'l'):
        # move left
        if (orientation == "vertical"):
            if (x > 2):
                if (board[y][x-1] == " " and board[y][x-2] == " " and board[y][x-3] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-3)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-1] = locale_index
                        board[y][x-2] = locale_index
                        board[y][x-3] = board[y][x]
                        board[y][x] = " "
                    else:
                        return 1
                elif (board[y][x-1] == "s" and board[y][x-2] == "s" and board[y][x-3] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (x > 0):
                if (board[y][x-1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-1] = board[y][x]
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    else:
                        return 1
                elif (board[y][x-1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (x > 0):
                if (board[y][x-1] == " " and board[y-1][x-1] == " " and board[y-2][x-1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x-1] = board[y][x]
                        board[y-1][x-1] = locale_index
                        board[y-2][x-1] = locale_index
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    else:
                        return 1
                elif (board[y][x-1] == "s" and board[y-1][x-1] == "s" and board[y-2][x-1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    elif (direction == "r"):
        if (orientation == "vertical"):
            if (x < NUM_COLUMNS-3):
                if (board[y][x+1] == " " and board[y][x+2] == " " and board[y][x+3] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+1] = board[y][x]
                        board[y][x+2] = locale_index
                        board[y][x+3] = locale_index
                        board[y][x] = " "
                elif (board[y][x+1] == "s" and board[y][x+2] == "s" and board[y][x+3] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-x"):
            if (x < NUM_COLUMNS-3):
                if (board[y][x+3] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+3)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+3] = board[y][x]
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    else:
                        return 1
                elif (board[y][x+3] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y][x+1] = " "
                        board[y][x+2] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
        elif (orientation == "horizontal-y"):
            if (x < NUM_COLUMNS-1):
                if (board[y][x+1] == " " and board[y-1][x+1] == " " and board[y-2][x+1] == " "):
                    locale_index = str(
                        ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+1)
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if not isInCheckMode:
                        board[y][x+1] = board[y][x]
                        board[y-1][x+1] = locale_index
                        board[y-2][x+1] = locale_index
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    else:
                        return 1
                elif (board[y][x+1] == "s" and board[y-1][x+1] == "s" and board[y-2][x+1] == "s"):
                    # piece is sinked
                    if not isInCheckMode:
                        board[y][x] = " "
                        board[y-1][x] = " "
                        board[y-2][x] = " "
                    return 3
                else:
                    if not isInCheckMode:
                        stdio.writeln("ERROR: Field " +
                                      symbols[0] + " " + symbols[1] + " not free")
                        exit()
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Cannot move beyond the board")
                    exit()
    return 0


def move_d_piece(symbols, direction, board, isInCheckMode=False):
    # 2x2x2
    x = int(symbols[1])
    y = (NUM_ROWS - 1 - int(symbols[0])) % NUM_ROWS

    if (direction == "u"):
        # move up
        if (y > 3):
            if (board[y-2][x] == "s" and board[y-3][x] == "s" and board[y-2][x+1] == "s" and board[y-3][x+1] == "s"):
                # piece is sinked return 2 points
                if not isInCheckMode:
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                return 4
            if (board[y-2][x] == " " and board[y-3][x] == " " and board[y-2][x+1] == " " and board[y-3][x+1] == " "):
                locale_index = str(
                    ((int(symbols[0])+2) * NUM_COLUMNS) + int(symbols[1]))
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                if not isInCheckMode:
                    board[y-2][x] = board[y][x]
                    board[y-3][x] = locale_index
                    board[y-2][x+1] = locale_index
                    board[y-3][x+1] = locale_index
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    elif (direction == "d"):
        # move down
        if (y < NUM_ROWS-3):
            if (board[y+1][x] == "s" and board[y+2][x] == "s" and board[y+1][x+1] == "s" and board[y+2][x+1] == "s"):
                # piece is sinked return 2 points
                if not isInCheckMode:
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                return 4
            if (board[y+1][x] == " " and board[y+2][x] == " " and board[y+1][x+1] == " " and board[y+2][x+1] == " "):
                locale_index = str(
                    ((int(symbols[0])-2) * NUM_COLUMNS) + int(symbols[1]))
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                if not isInCheckMode:
                    board[y+1][x] = locale_index
                    board[y+2][x] = board[y][x]
                    board[y+1][x+1] = locale_index
                    board[y+2][x+1] = locale_index
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    elif (direction == "l"):
        # move left
        if (x > 2):
            if (board[y][x-1] == "s" and board[y][x-2] == "s" and board[y-1][x-1] == "s" and board[y-1][x-2] == "s"):
                # piece is sinked return 2 points
                if not isInCheckMode:
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                return 4
            if (board[y][x-1] == " " and board[y][x-2] == " " and board[y-1][x-1] == " " and board[y-1][x-2] == " "):
                locale_index = str(
                    ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-2)
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                if not isInCheckMode:
                    board[y][x-1] = locale_index
                    board[y][x-2] = board[y][x]
                    board[y-1][x-1] = locale_index
                    board[y-1][x-2] = locale_index
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    elif (direction == "r"):
        # move right
        if (x < NUM_COLUMNS-4):
            if (board[y][x+2] == "s" and board[y][x+3] == "s" and board[y-1][x+2] == "s" and board[y-1][x+3] == "s"):
                # piece is sinked return 2 points
                if not isInCheckMode:
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                return 4
            if (board[y][x+2] == " " and board[y][x+3] == " " and board[y-1][x+2] == " " and board[y-1][x+3] == " "):
                locale_index = str(
                    ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+2)
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                if not isInCheckMode:
                    board[y][x+2] = board[y][x]
                    board[y][x+3] = locale_index
                    board[y-1][x+2] = locale_index
                    board[y+-1][x+3] = locale_index
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y-1][x] = " "
                    board[y-1][x+1] = " "
                else:
                    return 1
            else:
                if not isInCheckMode:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
        else:
            if not isInCheckMode:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    return 0


def can_player_move(board, player):
    # check if the current player can move and return a boolean
    # TODO implement sink moves
    for i in range(len(board)):
        for j in range(len(board[i])):
            if (player == "light"):
                if (board[i][j] in ['a', 'b', 'c', 'd']):
                    if (board[i][j] == 'a'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_a_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == 'b'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_b_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == 'c'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_c_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == 'd'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_d_piece([i, j, direction], direction, board, True) != 0):
                                return True
            else:
                if (board[i][j] in ['A', 'B', 'C', 'D']):
                    if (board[i][j] == 'A'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_a_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == 'B'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_b_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == "C"):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_c_piece([i, j, direction], direction, board, True) != 0):
                                return True
                    elif (board[i][j] == 'D'):
                        for direction in ['u', 'd', 'l', 'r']:
                            if (move_d_piece([i, j, direction], direction, board, True) != 0):
                                return True
    return False


def return_copy_of_board(board):
    # return a copy of the board because python passes by object reference and does werird stuff
    new_board = [[0 for i in range(len(board[0]))] for j in range(len(board))]
    for i in range(len(board)):
        for j in range(len(board[i])):
            new_board[i][j] = board[i][j]
    return new_board


def do_game_loop(board):
    # main function that does all the logic for the actual game loop, checking for wins and losses or partial games
    player = 'light'
    moves_made = 0
    light_sink_moves = 2
    dark_sink_moves = 2
    black_freezes = 0
    white_freezes = 0
    white_total = 0
    dark_total = 0
    total_moves = 0
    initial_board_state = return_copy_of_board(board)

    while True:
        num_pieces = 0
        for i in range(len(board)):
            for j in range(len(board[i])):
                if (board[i][j] in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D']):
                    num_pieces += 1  # count the number of pieces on the board

        if (num_pieces == 0 and total_moves == 0):
            stdio.writeln("Light loses")
            exit()
        if not stdio.hasNextLine():
            break
        # get input from stdio
        line = stdio.readLine().strip()

        symbols = line.split(" ")

        total_moves += 1

        # move pieces
        if (len(symbols) == 3):
            # valid input
            if (check_index_on_board(int(symbols[0]), int(symbols[1]))):
                # piece is on the board
                x = int(symbols[1])
                y = (NUM_ROWS-1 - int(symbols[0])) % NUM_ROWS
                if (board[y][x] in ['a', 'b', 'c', 'd', 'A', 'B', 'C', 'D', "s"]):
                    # piece is a piece or a sink
                    if ((player == "light" and board[y][x] in ['a', 'b', 'c', 'd']) or (player == "dark" and board[y][x] in ['A', 'B', 'C', 'D'])):
                        # piece is corresponding to the correct player
                        direction = symbols[2]
                        if (direction in ['u', 'd', 'l', 'r']):
                            # valid direction, move can be made
                            piece_being_moved = board[y][x]
                            if (piece_being_moved == "s"):
                                # check if the player has sink moves left
                                if (player == "light"):
                                    if (light_sink_moves > 0):
                                        light_sink_moves -= 1
                                        moves_made += 1
                                        # sink is being moved
                                    else:
                                        stdio.writeln(
                                            "ERROR: No sink moves left")
                                        exit()
                                else:
                                    if (dark_sink_moves > 0):
                                        dark_sink_moves -= 1
                                        moves_made += 1
                                        # sink is being moved
                                    else:
                                        stdio.writeln(
                                            "ERROR: No sink moves left")
                                        exit()
                            elif (piece_being_moved == 'a') or (piece_being_moved == 'A'):
                                moves_made += 1
                                # 1x1x1 piece
                                if player == "light":
                                    white_total += move_a_piece(
                                        symbols, direction, board)
                                else:
                                    dark_total += move_a_piece(
                                        symbols, direction, board)
                            elif (piece_being_moved == 'b') or (piece_being_moved == 'B'):
                                # 1x1x2 piece
                                moves_made += 1
                                if player == "light":
                                    white_total += move_b_piece(
                                        symbols, direction, board)
                                else:
                                    dark_total += move_b_piece(
                                        symbols, direction, board)
                            elif (piece_being_moved == 'c') or (piece_being_moved == 'C'):
                                # 1x1X3 piece
                                moves_made += 1
                                if player == "light":
                                    white_total += move_c_piece(
                                        symbols, direction, board)
                                else:
                                    dark_total += move_c_piece(
                                        symbols, direction, board)
                            elif (piece_being_moved == 'd') or (piece_being_moved == 'D'):
                                # 2x2x2 piece
                                if moves_made == 0:
                                    moves_made += 2
                                    if player == "light":
                                        white_total += move_d_piece(
                                            symbols, direction, board)
                                    else:
                                        dark_total += move_d_piece(
                                            symbols, direction, board)
                                else:
                                    stdio.writeln(
                                        "ERROR: Cannot move a 2x2x2 piece on the second move")
                                    exit()
                        else:
                            stdio.writeln(
                                "ERROR: Invalid direction " + direction)
                            exit()
                    else:
                        stdio.writeln(
                            "ERROR: Piece does not belong to the correct player")
                        exit()
                else:
                    stdio.writeln("ERROR: No piece on field " +
                                  symbols[0] + " " + symbols[1])
                    exit()
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[0] + " " + symbols[1] + " not on board")
                exit()
        else:
            stdio.writeln("Error: Illegal argument")
            exit()

        # check if the player moves back to original position
        if (initial_board_state == board and moves_made >= 2):
            stdio.writeln(
                "ERROR: Piece cannot be returned to starting position")
            exit()

        print_board(board)

        # if not can_player_move(board, player):
        # if player == 'light':
        #     stdio.writeln("Dark wins!")
        #     exit()
        # else:
        #     stdio.writeln("Light wins!")
        #     exit()

        if (moves_made >= 2):

            # check if the player moves back to original position
            if (initial_board_state == board):
                stdio.writeln(
                    "ERROR: Piece cannot be returned to starting position")
                exit()

            # check if the player's turn is over
            initial_board_state = return_copy_of_board(board)
            moves_made = 0

            # reverse who is the  player                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                             player
            if (player == 'light'):
                player = 'dark'
            else:
                player = 'light'

            # check if the next player can move
            # if not can_player_move(board, player):
            #     if (player == 'light'):
            #         stdio.writeln("Dark wins!")
            #         stdio.writeln("Light loses")
            #         exit()
            #     else:
            #         stdio.writeln("Light wins!")
            #         stdio.writeln("Dark loses")
            #         exit()

          # win conditions
        if (white_total >= 4):
            stdio.writeln("Light wins!")
            exit()
        elif (dark_total >= 4):
            stdio.writeln("Dark wins!")
            exit()


def main():
    # make sure the input fits the criteria and updates the global vars,NUM_ROWS,NUM_COLUMS,GUI_MODE
    check_input_validation()

    # read input from the commandline and update the board accordingly
    board = get_board_setup_from_commandline()
    print_board(board)

    # do the main game logic
    do_game_loop(board)


if __name__ == "__main__":
    main()
