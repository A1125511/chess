def path_show(piece, board, start, end):
    valid_moves = []

    for row in range(8):
        for col in range(8):
            target = (row, col)
            if piece.is_valid_move(board, start, target):
                valid_moves.append(target)
    
    return valid_moves
