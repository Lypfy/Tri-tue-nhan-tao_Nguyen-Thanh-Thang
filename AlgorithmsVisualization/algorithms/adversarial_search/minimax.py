import math

def check_winner(board):
    # Check rows, cols, diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] and board[i][0] != "":
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] and board[0][i] != "":
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != "":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != "":
        return board[0][2]
    
    # Check draw
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                return None  # Game not over
    return "Draw"

def get_available_moves(board):
    moves = []
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                moves.append((r, c))
    return moves

def minimax_score(board, is_maximizer, player_x="X", player_o="O"):
    winner = check_winner(board)
    if winner == player_x: return 10, None
    elif winner == player_o: return -10, None
    elif winner == "Draw": return 0, None

    moves = get_available_moves(board)
    best_move = None
    if is_maximizer:
        best_score = -math.inf
        for r, c in moves:
            board[r][c] = player_x
            score, _ = minimax_score(board, False, player_x, player_o)
            board[r][c] = ""
            if score > best_score:
                best_score = score
                best_move = (r, c)
        return best_score, best_move
    else:
        best_score = math.inf
        for r, c in moves:
            board[r][c] = player_o
            score, _ = minimax_score(board, True, player_x, player_o)
            board[r][c] = ""
            if score < best_score:
                best_score = score
                best_move = (r, c)
        return best_score, best_move

def alpha_beta_score(board, is_maximizer, alpha=-math.inf, beta=math.inf, player_x="X", player_o="O", depth=0, log_callback=None):
    winner = check_winner(board)
    if winner == player_x: return 10, None
    elif winner == player_o: return -10, None
    elif winner == "Draw": return 0, None

    moves = get_available_moves(board)
    best_move = None
    if is_maximizer:
        best_score = -math.inf
        for r, c in moves:
            board[r][c] = player_x
            score, _ = alpha_beta_score(board, False, alpha, beta, player_x, player_o, depth + 1, log_callback)
            board[r][c] = ""
            if score > best_score:
                best_score = score
                best_move = (r, c)
            alpha = max(alpha, best_score)
            
            if depth == 0 and log_callback:
                log_callback(f"[Gốc] Xét nước ({r},{c}) -> Điểm: {score} | Alpha: {alpha}, Beta: {beta}")
                
            if beta <= alpha:
                if depth <= 2 and log_callback:
                    log_callback(f"  [!] Cắt tỉa tại độ sâu {depth} (Alpha {alpha} >= Beta {beta})")
                break
        return best_score, best_move
    else:
        best_score = math.inf
        for r, c in moves:
            board[r][c] = player_o
            score, _ = alpha_beta_score(board, True, alpha, beta, player_x, player_o, depth + 1, log_callback)
            board[r][c] = ""
            if score < best_score:
                best_score = score
                best_move = (r, c)
            beta = min(beta, best_score)
            
            if depth == 0 and log_callback:
                log_callback(f"[Gốc] Xét nước ({r},{c}) -> Điểm: {score} | Alpha: {alpha}, Beta: {beta}")
                
            if beta <= alpha:
                if depth <= 2 and log_callback:
                    log_callback(f"  [!] Cắt tỉa tại độ sâu {depth} (Alpha {alpha} >= Beta {beta})")
                break
        return best_score, best_move
def minimax_generator(board, is_maximizer, player_x="X", player_o="O", depth=0):
    """
    Generator that yields intermediate steps of the minimax algorithm.
    Yields: {"board": board_state, "message": str, "eval": int, "action": str}
    Returns: best_score, best_move
    """
    winner = check_winner(board)
    if winner == player_x:
        yield {"board": board, "message": f"Nút lá: {player_x} thắng (Điểm: 10)", "action": "leaf"}
        return 10, None
    elif winner == player_o:
        yield {"board": board, "message": f"Nút lá: {player_o} thắng (Điểm: -10)", "action": "leaf"}
        return -10, None
    elif winner == "Draw":
        yield {"board": board, "message": "Nút lá: Hòa (Điểm: 0)", "action": "leaf"}
        return 0, None

    moves = get_available_moves(board)
    best_move = None

    if is_maximizer:
        best_score = -math.inf
        for r, c in moves:
            new_board = [row[:] for row in board]
            new_board[r][c] = player_x
            
            yield {"board": new_board, "message": f"Độ sâu {depth}: Maximizer ({player_x}) thử ô ({r},{c})", "action": "try", "target": (r, c)}
            
            if depth >= 1:
                score, _ = minimax_score(new_board, False, player_x, player_o)
            else:
                score = None
                gen = minimax_generator(new_board, False, player_x, player_o, depth + 1)
                while True:
                    try:
                        step = next(gen)
                        yield step
                    except StopIteration as e:
                        score, _ = e.value
                        break
            
            if score > best_score:
                best_score = score
                best_move = (r, c)
                
            yield {"board": board, "message": f"Độ sâu {depth}: {player_x} thử ({r},{c}) -> Điểm: {score}. Best hiện tại: {best_score}", "action": "backtrack"}
            
        yield {"board": board, "message": f"Độ sâu {depth}: Maximizer chọn {best_move} với điểm {best_score}", "action": "choose", "target": best_move}
        return best_score, best_move
    else:
        best_score = math.inf
        for r, c in moves:
            new_board = [row[:] for row in board]
            new_board[r][c] = player_o
            
            yield {"board": new_board, "message": f"Độ sâu {depth}: Minimizer ({player_o}) thử ô ({r},{c})", "action": "try", "target": (r, c)}
            
            if depth >= 1:
                score, _ = minimax_score(new_board, True, player_x, player_o)
            else:
                score = None
                gen = minimax_generator(new_board, True, player_x, player_o, depth + 1)
                while True:
                    try:
                        step = next(gen)
                        yield step
                    except StopIteration as e:
                        score, _ = e.value
                        break
                    
            if score < best_score:
                best_score = score
                best_move = (r, c)
                
            yield {"board": board, "message": f"Độ sâu {depth}: {player_o} thử ({r},{c}) -> Điểm: {score}. Best hiện tại: {best_score}", "action": "backtrack"}
            
        yield {"board": board, "message": f"Độ sâu {depth}: Minimizer chọn {best_move} với điểm {best_score}", "action": "choose", "target": best_move}
        return best_score, best_move

def play_tictactoe_ai_vs_ai():
    board = [["", "", ""], ["", "", ""], ["", "", ""]]
    current_player = "X"
    
    yield {"board": board, "message": "Bắt đầu AI vs AI", "action": "start"}
    
    while True:
        winner = check_winner(board)
        if winner:
            yield {"board": board, "message": f"Kết thúc: {winner}", "action": "end"}
            break
            
        is_max = (current_player == "X")
        yield {"board": board, "message": f"Lượt của {current_player}. Bắt đầu Minimax...", "action": "turn_start"}
        
        gen = minimax_generator(board, is_max, depth=0)
        best_move = None
        while True:
            try:
                step = next(gen)
                yield step
            except StopIteration as e:
                _, best_move = e.value
                break
                
        if best_move:
            board[best_move[0]][best_move[1]] = current_player
            yield {"board": board, "message": f"{current_player} đánh vào ô {best_move}", "action": "make_move", "target": best_move}
            
        current_player = "O" if current_player == "X" else "X"
