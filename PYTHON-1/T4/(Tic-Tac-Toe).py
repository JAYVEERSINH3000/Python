import streamlit as st
import random

# Initialize session state
if 'board' not in st.session_state:
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
if 'current_player' not in st.session_state:
    st.session_state.current_player = 'X'  # Human is X, AI is O
if 'winner' not in st.session_state:
    st.session_state.winner = None
if 'scores' not in st.session_state:
    st.session_state.scores = {'Human': 0, 'AI': 0, 'Draws': 0}
if 'difficulty' not in st.session_state:
    st.session_state.difficulty = 'Easy'

def check_winner(board):
    # Check rows, columns, diagonals
    for i in range(3):
        if board[i][0] == board[i][1] == board[i][2] != '':
            return board[i][0]
        if board[0][i] == board[1][i] == board[2][i] != '':
            return board[0][i]
    if board[0][0] == board[1][1] == board[2][2] != '':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != '':
        return board[0][2]
    return None

def is_draw(board):
    return all(cell != '' for row in board for cell in row) and not check_winner(board)

def minimax(board, depth, is_maximizing):
    winner = check_winner(board)
    if winner == 'O':  # AI wins
        return 10 - depth
    elif winner == 'X':  # Human wins
        return depth - 10
    elif is_draw(board):
        return 0

    if is_maximizing:  # AI's turn (O)
        max_eval = -float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    eval = minimax(board, depth + 1, False)
                    board[i][j] = ''
                    max_eval = max(max_eval, eval)
        return max_eval
    else:  # Human's turn (X)
        min_eval = float('inf')
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'X'
                    eval = minimax(board, depth + 1, True)
                    board[i][j] = ''
                    min_eval = min(min_eval, eval)
        return min_eval

def ai_move(board, difficulty):
    if difficulty == 'Easy':
        # Random move
        empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == '']
        return random.choice(empty_cells) if empty_cells else None
    else:  # Hard: Use minimax
        best_score = -float('inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if board[i][j] == '':
                    board[i][j] = 'O'
                    score = minimax(board, 0, False)
                    board[i][j] = ''
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        return best_move

# Title and settings
st.title("Tic-Tac-Toe with AI")
st.session_state.difficulty = st.selectbox("Difficulty", ["Easy", "Hard"], index=0 if st.session_state.difficulty == "Easy" else 1)

# Display scores
st.write(f"Scores - Human: {st.session_state.scores['Human']} | AI: {st.session_state.scores['AI']} | Draws: {st.session_state.scores['Draws']}")

# Display the board
st.write(f"Current Player: {st.session_state.current_player}")
cols = st.columns(3)
for i in range(3):
    for j in range(3):
        if cols[j].button(st.session_state.board[i][j] or ' ', key=f"{i}-{j}", disabled=st.session_state.winner is not None or st.session_state.current_player == 'O'):
            if st.session_state.board[i][j] == '' and not st.session_state.winner:
                st.session_state.board[i][j] = 'X'
                st.session_state.winner = check_winner(st.session_state.board)
                if not st.session_state.winner and not is_draw(st.session_state.board):
                    st.session_state.current_player = 'O'
                    # AI move
                    move = ai_move(st.session_state.board, st.session_state.difficulty)
                    if move:
                        st.session_state.board[move[0]][move[1]] = 'O'
                        st.session_state.winner = check_winner(st.session_state.board)
                        if not st.session_state.winner and not is_draw(st.session_state.board):
                            st.session_state.current_player = 'X'
                st.rerun()

# Check for winner or draw and update scores
if st.session_state.winner:
    if st.session_state.winner == 'X':
        st.success("You win!")
        st.session_state.scores['Human'] += 1
    else:
        st.error("AI wins!")
        st.session_state.scores['AI'] += 1
elif is_draw(st.session_state.board):
    st.info("It's a draw!")
    st.session_state.scores['Draws'] += 1

# Reset button
if st.button("Reset Game"):
    st.session_state.board = [['' for _ in range(3)] for _ in range(3)]
    st.session_state.current_player = 'X'
    st.session_state.winner = None
    st.rerun()