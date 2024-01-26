import copy
import random

import pygame
import sys
pygame.init()
screen = pygame.display.set_mode((1000, 800))
pygame.display.set_caption("Chess")

black_queen = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-queen.png")
black_queen = pygame.transform.scale(black_queen, (85, 85))
small_black_queen = pygame.transform.scale(black_queen, (40, 40))

# Repeat the process for other black pieces
black_king = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-king.png")
black_king = pygame.transform.scale(black_king, (85, 85))
small_black_king = pygame.transform.scale(black_king, (40, 40))

black_bishop = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-bishop.png")
black_bishop = pygame.transform.scale(black_bishop, (85, 85))
small_black_bishop = pygame.transform.scale(black_bishop, (40, 40))

black_knight = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-knight.png")
black_knight = pygame.transform.scale(black_knight, (85, 85))
small_black_knight = pygame.transform.scale(black_knight, (40, 40))

black_rook = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-rook.png")
black_rook = pygame.transform.scale(black_rook, (85, 85))
small_black_rook = pygame.transform.scale(black_rook, (40, 40))

black_pawn = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\black-pawn.png")
black_pawn = pygame.transform.scale(black_pawn, (85, 85))
small_black_pawn = pygame.transform.scale(black_pawn, (40, 40))

white_queen = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-queen.png")
white_queen = pygame.transform.scale(white_queen, (85, 85))
small_white_queen = pygame.transform.scale(white_queen, (40, 40))

# Repeat the process for other white pieces
white_king = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-king.png")
white_king = pygame.transform.scale(white_king, (85, 85))
small_white_king = pygame.transform.scale(white_king, (40, 40))

white_bishop = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-bishop.png")
white_bishop = pygame.transform.scale(white_bishop, (85, 85))
small_white_bishop = pygame.transform.scale(white_bishop, (40, 40))

white_knight = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-knight.png")
white_knight = pygame.transform.scale(white_knight, (85, 85))
small_white_knight = pygame.transform.scale(white_knight, (40, 40))

white_rook = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-rook.png")
white_rook = pygame.transform.scale(white_rook, (85, 85))
small_white_rook = pygame.transform.scale(white_rook, (40, 40))

white_pawn = pygame.image.load("C:\\Users\\david\\Downloads\\pieces-basic-png\\white-pawn.png")
white_pawn = pygame.transform.scale(white_pawn, (85, 85))
small_white_pawn = pygame.transform.scale(white_pawn, (40, 40))


def display_board():
    screen.fill("white")
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2:
            pygame.draw.rect(screen, "pink", [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, "pink", [700 - (column * 200), row * 100, 100, 100])


def display_pieces():
    for i in range(len(white_images)):
        screen.blit(white_images[i], (white_locations[i][0] * 100 + 8, white_locations[i][1] * 100 + 8))
    for i in range(len(black_images)):
        screen.blit(black_images[i], (black_locations[i][0] * 100 + 8, black_locations[i][1] * 100 + 8))
    if selected:
        pygame.draw.rect(screen, "light green", (x_coord * 100, y_coord * 100, 100, 100), 2)


def draw_check(king):
    pygame.draw.rect(screen, "dark red", (king[0] * 100 + 1, king[1] * 100 + 1, 100, 100), 5)


def draw_captured():
    for i in range(len(white_capture)):
        captured_piece = white_capture[i]
        index = pieces_list.index(captured_piece)
        screen.blit(small_white_pieces[index], (925, 5 + 50 * i))
    for i in range(len(black_capture)):
        captured_piece = black_capture[i]
        index = pieces_list.index(captured_piece)
        screen.blit(small_black_pieces[index], (825, 750 - 50 * i))


def draw_moves(moves, castles):
    if not moves:
        return
    for i in range(len(moves)):
        pygame.draw.circle(screen, "light blue", (moves[i][0] * 100 + 50, moves[i][1] * 100 + 50), 5)
    if not castles:
        return
    for i in range(len(castles)):
        pygame.draw.circle(screen, "light blue", (castles[i][0] * 100 + 50, castles[i][1] * 100 + 50), 5)
# valid_moves = [(row, col) for row in range(8) for col in range(2, 7)]


def make_move(locations, op_locations, op_images, pieces, captured, check, support_pieces):
    if check:
        if click_coords in support_pieces:
            return True, True
    elif click_coords in locations:
        return True, True
    if selected and click_coords in valid_moves:
        locations[selection] = click_coords
        if click_coords in op_locations:
            piece = op_locations.index(click_coords)
            op_locations.pop(piece)
            op_images.pop(piece)
            captured.append(pieces[piece])
            pieces.pop(piece)
        return False, False
    else:
        return False, True


def check_piece(index, pieces, coords, color):
    if pieces[index] == "pawn":
        return check_pawn(coords, color)
    elif pieces[index] == "right_rook":
        return check_rook(coords, color)
    elif pieces[index] == "left_rook":
        return check_rook(coords, color)
    elif pieces[index] == "bishop":
        return check_bishop(coords, color)
    elif pieces[index] == "knight":
        return check_knight(coords, color)
    elif pieces[index] == "queen":
        return check_queen(coords, color)
    elif pieces[index] == "king":
        return check_king(coords, color)
    else:
        return []


def check_pawn(position, color):
    moves_list = []
    if color == "w":
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] - 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        if (position[0] + 1, position[1] - 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
    if color == "b":
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] - 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        if (position[0] + 1, position[1] + 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
    return moves_list


def check_rook(position, color):
    moves_list = []
    if color == "w":
        locations = white_locations
        op_locations = black_locations
    else:
        locations = black_locations
        op_locations = white_locations
    for i in range(4):
        if i == 1 or i == 0:
            pos = position[0]
            x = True
        else:
            pos = position[1]
            x = False
        run = True
        for mod in range(1, 8):
            if i == 1 or i == 2:
                mod *= -1
            new_position = pos + mod
            if x:
                new_coord = (new_position, position[1])
            else:
                new_coord = (position[0], new_position)

            if new_position > 7 or new_position < 0 or new_coord in locations:
                run = False
                continue
            elif new_coord in op_locations and run:
                moves_list.append(new_coord)
                run = False
                continue
            elif run:
                moves_list.append(new_coord)
    return moves_list


def check_knight(position, color):
    moves_list = []
    if color == "w":
        locations = white_locations
    else:
        locations = black_locations
    for j in range(2):
        for i in range(1, 5):
            if i > 2:
                y = 2
            else:
                y = -2
            if i % 2 == 0:
                x = 1
            else:
                x = -1
            if j == 1:
                z = y
                y = x
                x = z
            new_pos = (position[0] + x, position[1] + y)
            if new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7 or new_pos in locations:
                continue
            else:
                moves_list.append(new_pos)
    return moves_list


def check_bishop(position, color):
    moves_list = []
    if color == "w":
        locations = white_locations
        op_locations = black_locations
    else:
        locations = black_locations
        op_locations = white_locations
    for i in range(4):
        run = True
        for mod in range(1, 8):
            if i == 1:
                mod *= -1
            if i == 2:
                new_y_position = position[1] - mod
            else:
                new_y_position = position[1] + mod
            if i == 3:
                new_x_position = position[0] - mod
            else:
                new_x_position = position[0] + mod
            new_coord = (new_x_position, new_y_position)

            if new_coord[0] > 7 or new_coord[0] < 0 or new_coord[1] > 7 or new_coord[1] < 0 or new_coord in locations:
                run = False
                continue
            elif new_coord in op_locations and run:
                moves_list.append(new_coord)
                run = False
                continue
            elif run:
                moves_list.append(new_coord)
    return moves_list


def check_queen(position, color):
    diag_list = check_bishop(position, color)
    acr_list = check_rook(position, color)
    moves_list = diag_list + acr_list
    return moves_list


def check_king(position, color):
    moves_list = []
    if color == "w":
        locations = white_locations
    else:
        locations = black_locations
    target_moves = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    for i in range(len(target_moves)):
        new_pos = (position[0] + target_moves[i][0], position[1] + target_moves[i][1])
        if new_pos[0] < 0 or new_pos[0] > 7 or new_pos[1] < 0 or new_pos[1] > 7 or new_pos in locations:
            continue
        else:
            moves_list.append(new_pos)
    return moves_list


def checked_help(active_pieces, location, color, op_pieces, op_location, op_color):
    checked_helpers = {}
    helpers_list = []
    for pieces in range(len(active_pieces)):
        origin_loc = location[pieces]
        valid = check_piece(pieces, active_pieces, origin_loc, color)
        if en_passent_indexes:
            if len(en_passent_indexes) == 2:
                if pieces == en_passent_indexes[0] or pieces == en_passent_indexes[1]:
                    valid.append(en_passent_take)
            else:
                if pieces == en_passent_indexes[0]:
                    valid.append(en_passent_take)
        if not valid:
            continue
        for move in valid:
            pop = False
            if move in op_location:
                pop_index = op_location.index(move)
                loc_before_pop = op_location[pop_index]
                before_pop = op_pieces[pop_index]
                op_pieces[pop_index] = "none"
                op_location[pop_index] = (1, 1)
                pop = True
            location[pieces] = move
            if not entire_check(op_pieces, op_location, move, op_color):
                if origin_loc in checked_helpers:
                    checked_helpers[origin_loc] = checked_helpers[origin_loc] + [move]
                else:
                    checked_helpers[origin_loc] = [move]
            if pop:
                op_pieces[pop_index] = before_pop
                op_location[pop_index] = loc_before_pop
            location[pieces] = origin_loc
    support = list(checked_helpers.keys())
    if not support:
        print("CHECKMATE")
        pygame.quit()
        sys.exit()
    return support, checked_helpers


def entire_check(pieces, locations, move, color):
    if color != "w":
        king = white_pieces.index("king")
        king_location = white_locations[king]
    else:
        king = black_pieces.index("king")
        king_location = black_locations[king]
    for index in range(len(pieces)):
        coords = locations[index]
        if coords == move:
            continue
        hit_squares = check_piece(index, pieces, coords, color)
        if not hit_squares:
            continue
        if king_location in hit_squares:
            return True
    else:
        return False


def valid(active_pieces, location, color):
    valid = {}
    popped = False
    for pieces in range(len(active_pieces)):
        origin_loc = location[pieces]
        temp_valid = check_piece(pieces, active_pieces, origin_loc, color)
        if en_passent_indexes:
            if len(en_passent_indexes) == 2:
                if pieces == en_passent_indexes[0] or pieces == en_passent_indexes[1]:
                    temp_valid.append(en_passent_take)
            else:
                if pieces == en_passent_indexes[0]:
                    temp_valid.append(en_passent_take)
        if not temp_valid:
            continue
        for move in temp_valid:
            location[pieces] = move
            if color != "w":
                if move in white_locations:
                    dex = white_locations.index(move)
                    white_locations[dex] = (-1, -1)
                    before = white_pieces[dex]
                    white_pieces[dex] = "none"
                    popped = True
                check = entire_check(white_pieces, white_locations, move, "w")
                if popped:
                    white_pieces[dex] = before
                    white_locations[dex] = move
                    popped = False
            else:
                if move in black_locations:
                    dex = black_locations.index(move)
                    black_locations[dex] = (-1, -1)
                    before = black_pieces[dex]
                    black_pieces[dex] = "none"
                    popped = True
                check = entire_check(black_pieces, black_locations, move, "b")
                if popped:
                    black_pieces[dex] = before
                    black_locations[dex] = move
                    popped = False
            if check:
                location[pieces] = origin_loc
                continue
            else:
                if origin_loc in valid:
                    valid[origin_loc] = valid[origin_loc] + [move]
                else:
                    valid[origin_loc] = [move]

            location[pieces] = origin_loc
    support = list(valid.keys())
    if not support:
        print("STALEMATE")
        pygame.quit()
        sys.exit()
    return support, valid


def check_castle(king, short, long, pieces, locations, color):
    moves = []
    all_squares = []
    short_squares = []
    long_squares = []
    move_squares = []
    if not king:
        return moves
    elif not short and not long:
        return moves
    if short:
        if color == "w":
            short_squares = [(5, 0), (6, 0)]
        else:
            short_squares = [(5, 7), (6, 7)]
        all_squares = copy.deepcopy(short_squares)
    if long:
        if color == "w":
            long_squares = [(1, 0), (2, 0), (3, 0)]
        else:
            long_squares = [(1, 7), (2, 7), (3, 7)]
    if all_squares:
        all_squares += long_squares
    else:
        all_squares = long_squares
    all_locations = white_locations + black_locations
    for i in range(len(all_squares)):
        if all_squares[i] not in all_locations:
            for index in range(len(pieces)):
                coords = locations[index]
                hit_squares = check_piece(index, pieces, coords, color)
                if not hit_squares:
                    continue
                if all_squares[i] not in hit_squares:
                    moves.append((all_squares[i]))
                    break
    if not moves:
        return moves
    if long:
        if set(long_squares).issubset(set(moves)):
            move_squares = [long_squares[1]]
    if short:
        if set(short_squares).issubset(set(moves)):
            move_squares += [short_squares[1]]
    return move_squares


def make_castle(coords, pieces, location):
    if coords == (6, 7):
        rook_pos = (5, 7)
        rook_index = pieces.index("right_rook")
    elif coords == (2, 7):
        rook_pos = (3, 7)
        rook_index = pieces.index("left_rook")
    elif coords == (6, 0):
        rook_pos = (5, 0)
        rook_index = pieces.index("right_rook")
    elif coords == (2, 0):
        rook_pos = (3, 0)
        rook_index = pieces.index("left_rook")
    king_index = pieces.index("king")
    location[king_index] = coords
    location[rook_index] = rook_pos


def pawn_upgrade(images, pieces, locations, selection, color):
    if color == "w":
        limit = 0
    else:
        limit = 7
    if locations[selection][1] != limit:
        return
    pieces[selection] = "queen"
    if limit:
        images[selection] = black_queen
    else:
        images[selection] = white_queen


def en_passent_check(selection, locations, op_locations, op_pieces, color):
    pawn_push = locations[selection]
    indexes = []
    pawn_take = (-1, -1)
    if color == "w":
        if pawn_loc[1] - pawn_push[1] != 2:
            return [], (-1, -1)
    else:
        if pawn_push[1] - pawn_loc[1] != 2:
            return [], (-1, -1)
    x = [pawn_push[0] - 1, pawn_push[0] + 1]
    for push in x:
        if (push, pawn_push[1]) in op_locations:
            index = op_locations.index((push, pawn_push[1]))
            if op_pieces[index] == "pawn":
                if color == "w":
                    pawn_take = (pawn_push[0], pawn_push[1] + 1)
                else:
                    pawn_take = (pawn_push[0], pawn_push[1] - 1)
                indexes.append(index)
    return indexes, pawn_take


def make_en_passent(pieces, locations, images, color):
    if click_coords == en_passent_take:
        if color == "w":
            mod = 1
        else:
            mod = -1
        pos = (en_passent_take[0], en_passent_take[1] + mod)
        index = locations.index(pos)
        locations.pop(index)
        images.pop(index)
        pieces.pop(index)


def generator(select):
    if check:
        if select:
            for i in actual_valid[click_coords]:
                if i in white_locations:
                    return i
            return actual_valid[click_coords][0]
        else:
            for i in checked_helpers:
                for j in actual_valid[i]:
                    if j in white_locations:
                        return i
            return checked_helpers[random.randint(0, len(val_pieces) - 1)]
    if select:
        if castle_moves:
            return castle_moves[0]
        for i in val_mov[click_coords]:
            if i in white_locations:
                return i
        return val_mov[click_coords][0]
    else:
        for i in val_pieces:
            for j in val_mov[i]:
                if j in white_locations:
                    return i
        return val_pieces[random.randint(0, len(val_pieces) - 1)]

while True:
    white_pieces = ["left_rook", "knight", "bishop", "queen", "king", "bishop", "knight", "right_rook", "pawn",
                    "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

    black_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0), (0, 1),
                       (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]

    black_pieces = ["left_rook", "knight", "bishop", "queen", "king", "bishop", "knight", "right_rook", "pawn",
                    "pawn", "pawn", "pawn", "pawn", "pawn", "pawn", "pawn"]

    white_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7), (0, 6),
                       (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]

    white_images = [white_rook, white_knight, white_bishop, white_queen, white_king, white_bishop,
                    white_knight, white_rook, white_pawn, white_pawn, white_pawn, white_pawn, white_pawn,
                    white_pawn, white_pawn, white_pawn]

    black_images = [black_rook, black_knight, black_bishop, black_queen, black_king, black_bishop,
                    black_knight, black_rook, black_pawn, black_pawn, black_pawn, black_pawn, black_pawn,
                    black_pawn, black_pawn, black_pawn]

    # Small White Pieces
    small_white_pieces = [small_white_rook, small_white_rook, small_white_knight, small_white_bishop,
                          small_white_queen, small_white_king, small_white_pawn]

    # Small Black Pieces
    small_black_pieces = [small_black_rook, small_black_rook, small_black_knight, small_black_bishop,
                          small_black_queen, small_black_king, small_black_pawn]
    pieces_list = ["right_rook", "left_rook", "knight", "bishop", "queen", "king", "pawn"]

    check = False
    valid_moves = []
    castle_moves = []
    selected = False
    white = True
    selection = 1
    king_loc = (-1, -1)
    checked_helpers = []
    w_castle_k = True
    w_castle_long = True
    w_castle_short = True
    b_castle_k = True
    b_castle_long = True
    b_castle_short = True
    w_castle = True
    b_castle = True

    white_capture = []
    black_capture = []
    en_passent_indexes = []
    game = True
    while game:
        if not white:
            click_coords = generator(selected)
            x_coord = click_coords[0]
            y_coord = click_coords[1]
            selected, black = make_move(black_locations, white_locations, white_images, white_pieces, white_capture,
                                        check, checked_helpers)
            if selected:
                selection = black_locations.index(click_coords)
                if black_pieces[selection] == "pawn":
                    pawn_loc = black_locations[selection]
                else:
                    pawn_loc = []
                if check:
                    if click_coords in checked_helpers:
                        valid_moves = actual_valid[click_coords]
                    else:
                        valid_moves = []
                else:
                    val_pieces, val_mov = valid(black_pieces, black_locations, "b")
                    if click_coords in val_pieces:
                        if b_castle and black_pieces[selection] == "king":
                            castle_moves = check_castle(b_castle_k, b_castle_short, b_castle_long, white_pieces,
                                                        white_locations, "w")
                        else:
                            castle_moves = []
                        valid_moves = val_mov[click_coords]
                    else:
                        valid_moves = []
                        castle_moves = []
            else:
                if click_coords in valid_moves:
                    if en_passent_indexes:
                        if len(en_passent_indexes) == 2:
                            if selection == en_passent_indexes[0] or selection == en_passent_indexes[1]:
                                make_en_passent(white_pieces, white_locations, white_images, "b")
                        else:
                            if selection == en_passent_indexes[0]:
                                make_en_passent(white_pieces, white_locations, white_images, "b")
                    if black_pieces[selection] == "pawn":
                        en_passent_indexes, en_passent_take = en_passent_check(selection, black_locations,
                                                                               white_locations, white_pieces, "b")
                        pawn_upgrade(black_images, black_pieces, black_locations, selection, "b")
                    if black_pieces[selection] == "king":
                        b_castle_k = False
                    if black_pieces[selection] == "left_rook":
                        b_castle_long = False
                    if black_pieces[selection] == "right_rook":
                        b_castle_short = False
                    check = entire_check(black_pieces, black_locations, (-1, -1), "b")
                    if check:
                        checked_helpers, actual_valid = checked_help(white_pieces, white_locations, "w",
                                                                     black_pieces, black_locations, "b")
                        king_loc = white_locations[white_pieces.index("king")]
                elif castle_moves:
                    if click_coords in castle_moves:
                        b_castle = False
                        make_castle(click_coords, black_pieces, black_locations)
                        black = False
                        check = entire_check(black_pieces, black_locations, (-1, -1), "b")
                        if check:
                            checked_helpers, actual_valid = checked_help(white_pieces, white_locations, "w",
                                                                         black_pieces, black_locations, "b")
                        king_loc = white_locations[white_pieces.index("king")]
                valid_moves = []
                castle_moves = []
                val_pieces, val_mov = valid(white_pieces, white_locations, "w")
            if not black:
                white = True
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("RESIGN")
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                if white:
                    selected, white = make_move(white_locations, black_locations, black_images, black_pieces, black_capture,
                                                check, checked_helpers)
                    if selected:
                        selection = white_locations.index(click_coords)
                        if white_pieces[selection] == "pawn":
                            pawn_loc = white_locations[selection]
                        else:
                            pawn_loc = []
                        if check:
                            if click_coords in checked_helpers:
                                valid_moves = actual_valid[click_coords]

                            else:
                                valid_moves = []
                        else:
                            val_pieces, val_mov = valid(white_pieces, white_locations, "w")
                            if click_coords in val_pieces:
                                if w_castle and white_pieces[selection] == "king":
                                    castle_moves = check_castle(w_castle_k, w_castle_short, w_castle_long, black_pieces,
                                                                black_locations, "b")
                                else:
                                    castle_moves = []
                                valid_moves = val_mov[click_coords]
                            else:
                                valid_moves = []
                                castle_moves = []
                    else:
                        if click_coords in valid_moves:
                            if en_passent_indexes:
                                if len(en_passent_indexes) == 2:
                                    if selection == en_passent_indexes[0] or selection == en_passent_indexes[1]:
                                        make_en_passent(black_pieces, black_locations, black_images, "w")
                                else:
                                    if selection == en_passent_indexes[0]:
                                        make_en_passent(black_pieces, black_locations, black_images, "w")
                            if white_pieces[selection] == "pawn":
                                en_passent_indexes, en_passent_take = en_passent_check(selection, white_locations,
                                                                                     black_locations, black_pieces, "w")
                                pawn_upgrade(white_images, white_pieces, white_locations, selection, "w")
                            if white_pieces[selection] == "king":
                                w_castle_k = False
                            if white_pieces[selection] == "left_rook":
                                w_castle_long = False
                            if white_pieces[selection] == "right_rook":
                                w_castle_short = False
                            check = entire_check(white_pieces, white_locations, (-1, -1), "w")
                            if check:
                                checked_helpers, actual_valid = checked_help(black_pieces, black_locations, "b",
                                                                             white_pieces, white_locations, "w")
                                king_loc = black_locations[black_pieces.index("king")]
                        elif castle_moves:
                            if click_coords in castle_moves:
                                w_castle = False
                                make_castle(click_coords, white_pieces, white_locations)
                                white = False
                                check = entire_check(white_pieces, white_locations, (-1, -1), "w")
                                if check:
                                    checked_helpers, actual_valid = checked_help(black_pieces, black_locations, "b",
                                                                                 white_pieces, white_locations, "w")
                                    king_loc = black_locations[black_pieces.index("king")]
                        valid_moves = []
                        castle_moves = []
                        val_pieces, val_mov = valid(black_pieces, black_locations, "b")
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game = False
        pygame.display.update()
        display_board()
        display_pieces()
        draw_moves(valid_moves, castle_moves)
        draw_captured()
        if check:
            draw_check(king_loc)
