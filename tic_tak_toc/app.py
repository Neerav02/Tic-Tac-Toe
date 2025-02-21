from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Function to initialize an empty board
def initialize_board():
    return [['' for _ in range(3)] for _ in range(3)]

# Global game state
game_state = {
    'board': initialize_board(),
    'turn': 'X',  # X starts first
    'winner': None
}

# Function to check for a winner
def check_winner(player):
    board = game_state['board']
    
    # Check rows & columns
    for i in range(3):
        if all(board[i][j] == player for j in range(3)) or all(board[j][i] == player for j in range(3)):
            return True

    # Check diagonals
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)):
        return True

    return False

# Home route
@app.route('/')
def index():
    return render_template('index.html', board=game_state['board'], turn=game_state['turn'], winner=game_state['winner'])

# Handle player moves
@app.route('/move/<int:row>/<int:col>', methods=['POST'])
def make_move(row, col):
    if game_state['board'][row][col] == '' and game_state['winner'] is None:
        game_state['board'][row][col] = game_state['turn']

        # Check for a winner
        if check_winner(game_state['turn']):
            game_state['winner'] = game_state['turn']
        else:
            # Switch turns
            game_state['turn'] = 'O' if game_state['turn'] == 'X' else 'X'

    return jsonify({'board': game_state['board'], 'winner': game_state['winner'], 'turn': game_state['turn']})

# Reset game route
@app.route('/reset', methods=['POST'])
def reset_game():
    game_state['board'] = initialize_board()
    game_state['turn'] = 'X'
    game_state['winner'] = None
    return jsonify({'board': game_state['board'], 'turn': game_state['turn'], 'winner': game_state['winner']})

if __name__ == '__main__':
    app.run(debug=True)