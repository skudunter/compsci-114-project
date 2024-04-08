import sys
import stdio

# global vars that are updated in the check input validation function
NUM_ROWS = 10
NUM_COLUMNS = 10
GUI_MODE = False


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
    stdio.writeln("")


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


def check_sink_adjacent(row, col, board):
    # checks if the sink is adjacent to a sink
    try:
        if (col > 0 and board[row][col-1] == 's') or \
           (col < len(board[0]) - 1 and board[row][col+1] == 's') or \
           (row > 0 and board[row-1][col] == 's') or \
           (row < len(board) - 1 and board[row+1][col] == 's'):
            return True
    except IndexError:
        pass
    return False


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
                                y = (NUM_ROWS-1 - int(symbols[2])) % NUM_ROWS
                                if (board[y][x] == ' '):
                                    # empty field
                                    if (symbols[1] == "2"):
                                        # a 2x2 sink
                                        if (check_sink_range(x+1, y)):
                                            if (check_sink_range(x, y-1)):
                                                if (check_sink_range(x+1, y-1)):
                                                    # all fields are within the outer 3 columns or rows
                                                    if (board[y][x+1] == ' ' and board[y-1][x] == ' ' and board[y-1][x+1] == ' '):
                                                        # all fields are empty
                                                        if (not check_sink_adjacent(y, x, board)):
                                                            if (not check_sink_adjacent(y, x+1, board)):
                                                                if (not check_sink_adjacent(y-1, x, board)):
                                                                    if (not check_sink_adjacent(y-1, x+1, board)):
                                                                        # no sinks adjaceant to this sink
                                                                        board[y][x] = "s"
                                                                        board[y][x +
                                                                                 1] = "s"
                                                                        board[y -
                                                                              1][x] = "s"
                                                                        board[y-1][x +
                                                                                   1] = "s"
                                                                    else:
                                                                        stdio.writeln(
                                                                            "ERROR: Sink cannot be next to another sink")
                                                                        exit()
                                                                else:
                                                                    stdio.writeln(
                                                                        "ERROR: Sink cannot be next to another sink")
                                                                    exit()
                                                            else:
                                                                stdio.writeln(
                                                                    "ERROR: Sink cannot be next to another sink")
                                                                exit()
                                                        else:
                                                            stdio.writeln(
                                                                "ERROR: Sink cannot be next to another sink")
                                                            exit()
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
                                        # a 1x1 sink
                                        if (not check_sink_adjacent(y, x, board)):
                                            # no sinks adjaceant to this sink
                                            board[y][x] = "s"
                                        else:
                                            stdio.writeln(
                                                "ERROR: Sink cannot be next to another sink")
                                            exit()
                                else:
                                    stdio.writeln(
                                        "ERROR: Field " + symbols[2] + " " + symbols[3] + " not free")
                                    exit()
                            else:
                                stdio.writeln(
                                    "ERROR: Sink in the wrong position")
                                exit()
                        else:
                            # a piece
                            x = int(symbols[3])
                            y = (NUM_ROWS-1 - int(symbols[2])) % NUM_ROWS
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
    return board


def get_player_from_board(symbols, board) -> str:
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


def move_a_piece(symbols, direction, board) -> int:
    # moves 'a' piece
    x = int(symbols[1])
    y = (NUM_ROWS-1 - int(symbols[0])) % NUM_ROWS

    if (direction == 'u'):
        # move up
        if (y > 0):
            if (board[y-1][x] == 's'):
                board[y][x] = ' '
                return 1
            elif (board[y-1][x] == ' '):
                board[y-1][x] = board[y][x]
                board[y][x] = ' '
            else:
                stdio.writeln(
                    "ERROR: Field " + symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln(
                "ERROR: Cannot move beyond the board")
            exit()
        return 0
    elif (direction == 'd'):
        # move down
        if (y < NUM_ROWS-1):
            if (board[y+1][x] == 's'):
                board[y][x] = ' '
                return 1
            elif (board[y+1][x] == ' '):
                board[y+1][x] = board[y][x]
                board[y][x] = ' '
            else:
                stdio.writeln(
                    "ERROR: Field " + symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln(
                "ERROR: Cannot move beyond the board")
            exit()
        return 0
    elif (direction == 'l'):
        # move left
        if (x > 0):
            if (board[y][x-1] == 's'):
                board[y][x] = ' '
                return 1
            elif (board[y][x-1] == ' '):
                board[y][x-1] = board[y][x]
                board[y][x] = ' '
            else:
                stdio.writeln(
                    "ERROR: Field " + symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln(
                "ERROR: Cannot move beyond the board")
            exit()
        return 0
    elif (direction == 'r'):
        # move right
        if (board[y][x+1] == 's'):
            board[y][x] = ' '
            return 1
        elif (x < NUM_COLUMNS-1):
            if (board[y][x+1] == ' '):
                board[y][x+1] = board[y][x]
                board[y][x] = ' '
            else:
                stdio.writeln(
                    "ERROR: Field " + symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln(
                "ERROR: Cannot move beyond the board")
            exit()
    return 0


def move_b_piece(symbols, direction, board) -> int:
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
            if (y > 1):
                if (board[y-1][x] == " " and board[y-2][x] == " "):
                    # fields are empty
                    locale_index = str(
                        ((int(symbols[0])+1) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    board[y-1][x] = board[y][x]
                    board[y-2][x] = str(locale_index)
                    board[y][x] = " "
                elif (board[y-1][x] == "s" and board[y-2][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y-1][x] = board[y][x]
                    board[y-1][x+1] = str(locale_index)
                    board[y][x] = " "
                    board[y][x+1] = " "
                elif (board[y-1][x] == "s" and board[y-1][x+1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
        if (orientation == "horizontal-y"):
            if (y > 0):
                if (board[y-2][x] == " "):
                    locale_index = str(
                        ((int(symbols[0])+2) * NUM_COLUMNS) + int(symbols[1]))
                    if (int(locale_index.strip()) < 10):
                        locale_index = " " + \
                            locale_index
                    board[y-2][x] = board[y][x]
                    board[y][x] = " "
                    board[y-1][x] = " "
                elif (board[y-2][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+2][x] = board[y][x]
                    board[y+1][x] = str(locale_index)
                    board[y][x] = " "
                elif (board[y+1][x] == "s" and board[y+2][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+1][x] = board[y][x]
                    board[y+1][x+1] = str(locale_index)
                    board[y][x] = " "
                    board[y][x+1] = " "
                elif (board[y+1][x] == "s" and board[y+1][x+1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+1][x] = board[y][x]
                    board[y][x] = " "
                    board[y-1][x] = " "
                elif (board[y+1][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = locale_index
                    board[y][x-2] = board[y][x]
                    board[y][x] = " "
                elif (board[y][x-1] == "s" and board[y][x-2] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = board[y][x]
                    board[y][x] = " "
                    board[y][x+1] = " "
                elif (board[y][x-1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = board[y][x]
                    board[y-1][x-1] = locale_index
                    board[y][x] = " "
                    board[y-1][x] = " "
                elif (board[y][x-1] == "s" and board[y-1][x-1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
            else:
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
                    board[y][x+1] = board[y][x]
                    board[y][x+2] = locale_index
                    board[y][x] = " "
                elif (board[y][x+1] == "s" and board[y][x+2] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x+2] = board[y][x]
                    board[y][x] = " "
                    board[y][x+1] = " "
                elif (board[y][x+2] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x+1] = board[y][x]
                    board[y-1][x+1] = locale_index
                    board[y][x] = " "
                    board[y-1][x] = " "
                elif (board[y][x+1] == "s" and board[y-1][x+1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    return 0


def move_c_piece(symbols, direction, board) -> int:
    #1x1x3
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
                    board[y-1][x] = board[y][x]
                    board[y-2][x] = str(locale_index)
                    board[y-3][x] = str(locale_index)
                    board[y][x] = " "
                elif (board[y-1][x] == "s" and board[y-2][x] == "s" and board[y-3][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y-1][x] = board[y][x]
                    board[y-1][x+1] = str(locale_index)
                    board[y-1][x+2] = str(locale_index)
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                elif (board[y-1][x] == "s" and board[y-1][x+1] == "s" and board[y-1][x+2] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y-3][x] = board[y][x]
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                elif (board[y-3][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+3][x] = board[y][x]
                    board[y+2][x] = locale_index
                    board[y+1][x] = locale_index
                    board[y][x] = " "
                elif (board[y+1][x] == "s" and board[y+2][x] == "s" and board[y+3][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+1][x] = board[y][x]
                    board[y+1][x+1] = str(locale_index)
                    board[y+1][x+2] = str(locale_index)
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                elif (board[y+1][x] == "s" and board[y+1][x+1] == "s" and board[y+1][x+2] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y+1][x] = board[y][x]
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                elif (board[y+1][x] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = locale_index
                    board[y][x-2] = locale_index
                    board[y][x-3] = board[y][x]
                    board[y][x] = " "
                elif (board[y][x-1] == "s" and board[y][x-2] == "s" and board[y][x-3] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = board[y][x]
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                elif (board[y][x-1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x-1] = board[y][x]
                    board[y-1][x-1] = locale_index
                    board[y-2][x-1] = locale_index
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                elif (board[y][x-1] == "s" and board[y-1][x-1] == "s" and board[y-2][x-1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
            else:
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
                    board[y][x+1] = board[y][x]
                    board[y][x+2] = locale_index
                    board[y][x+3] = locale_index
                    board[y][x] = " "
                elif (board[y][x+1] == "s" and board[y][x+2] == "s" and board[y][x+3] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x+3] = board[y][x]
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                elif (board[y][x+3] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y][x+1] = " "
                    board[y][x+2] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
                    exit()
            else:
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
                    board[y][x+1] = board[y][x]
                    board[y-1][x+1] = locale_index
                    board[y-2][x+1] = locale_index
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                elif (board[y][x+1] == "s" and board[y-1][x+1] == "s" and board[y-2][x+1] == "s"):
                    # piece is sinked
                    board[y][x] = " "
                    board[y-1][x] = " "
                    board[y-2][x] = " "
                    return 1
                else:
                    stdio.writeln("ERROR: Field " +
                                  symbols[0] + " " + symbols[1] + " not free")
            else:
                stdio.writeln("ERROR: Cannot move beyond the board")
                exit()
    return 0

def move_d_piece(symbols, direction, board) -> int:
    # 2x2x2
    x = int(symbols[1])
    y = (NUM_ROWS - 1 - int(symbols[0])) % NUM_ROWS

    if (direction == "u"):
        # move up
        if (y > 3):
            if (board[y-2][x] == "s" and board[y-3][x] == "s" and board[y-2][x+1] == "s" and board[y-3][x+1] == "s"):
                # piece is sinked return 2 points
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 2
            if (board[y-2][x] == " " and board[y-3][x] == " " and board[y-2][x+1] == " " and board[y-3][x+1] == " "):
                locale_index = str(
                    ((int(symbols[0])+2) * NUM_COLUMNS) + int(symbols[1]))
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index

                board[y-2][x] = board[y][x]
                board[y-3][x] = locale_index
                board[y-2][x+1] = locale_index
                board[y-3][x+1] = locale_index
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 0
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            exit()
    elif (direction == "d"):
        # move down
        if (y < NUM_ROWS-3):
            if (board[y+1][x] == "s" and board[y+2][x] == "s" and board[y+1][x+1] == "s" and board[y+2][x+1] == "s"):
                # piece is sinked return 2 points
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 2
            if (board[y+1][x] == " " and board[y+2][x] == " " and board[y+1][x+1] == " " and board[y+2][x+1] == " "):
                locale_index = str(
                    ((int(symbols[0])-2) * NUM_COLUMNS) + int(symbols[1]))
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                board[y+1][x] = locale_index
                board[y+2][x] = board[y][x]
                board[y+1][x+1] = locale_index
                board[y+2][x+1] = locale_index
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 0
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            exit()
    elif (direction == "l"):
        # move left
        if (x > 2):
            if (board[y][x-1] == "s" and board[y][x-2] == "s" and board[y-1][x-1] == "s" and board[y-1][x-2] == "s"):
                # piece is sinked return 2 points
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 2
            if (board[y][x-1] == " " and board[y][x-2] == " " and board[y-1][x-1] == " " and board[y-1][x-2] == " "):
                locale_index = str(
                    ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])-2)
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                board[y][x-1] = locale_index
                board[y][x-2] = board[y][x]
                board[y-1][x-1] = locale_index
                board[y-1][x-2] = locale_index
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 0
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            exit()
    elif (direction == "r"):
        # move right
        if (x < NUM_COLUMNS-4):
            if (board[y][x+2] == "s" and board[y][x+3] == "s" and board[y-1][x+2] == "s" and board[y-1][x+3] == "s"):
                # piece is sinked return 2 points
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 2
            if (board[y][x+2] == " " and board[y][x+3] == " " and board[y-1][x+2] == " " and board[y-1][x+3] == " "):
                locale_index = str(
                    ((int(symbols[0])) * NUM_COLUMNS) + int(symbols[1])+2)
                if (int(locale_index.strip()) < 10):
                    locale_index = " " + \
                        locale_index
                board[y][x+2] = board[y][x]
                board[y][x+3] = locale_index
                board[y-1][x+2] = locale_index
                board[y+-1][x+3] = locale_index
                board[y][x] = " "
                board[y][x+1] = " "
                board[y-1][x] = " "
                board[y-1][x+1] = " "
                return 0
            else:
                stdio.writeln("ERROR: Field " +
                              symbols[0] + " " + symbols[1] + " not free")
                exit()
        else:
            stdio.writeln("ERROR: Cannot move beyond the board")
            exit()


def do_game_loop(board):
    # main function that does all the logic for the actual game loop, checking for wins and losses or partial games
    player = ''
    moves_made = 0
    light_sink_moves = 2
    dark_sink_moves = 2
    black_freezes = 0
    white_freezes = 0
    white_total = 0
    dark_total = 0
    initial_board_state = board
    while True:
        # win conditions
        if (white_total >= 4):
            stdio.writeln("Light wins!")
            stdio.writeln("Dark loses")
            exit()
        elif (dark_total >= 4):
            stdio.writeln("Dark wins!")
            stdio.writeln("Light loses")
            exit()
        # get input from stdio
        line = stdio.readLine().strip()
        symbols = line.split(" ")

        # do basic checks to the input and update the player at the beginning of the game
        if (player == ''):
            player = get_player_from_board(symbols, board)

        # check if the player's turn is over
        if (moves_made >= 2):
            initial_board_state = board
            moves_made = 0
            # reverse who is the player
            if (player == 'light'):
                player = 'dark'
            else:
                player = 'light'

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
                                        "ERROR: Cannot move 2x2X2 piece on the second move")
                                    exit()

                        else:
                            stdio.writeln(
                                "Error: Invalid direction " + direction)
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
        if(initial_board_state == board and moves_made >= 2):
            stdio.writeln("ERROR: Piece cannot be returned to the starting position")
            exit()
        print_board(board)

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
