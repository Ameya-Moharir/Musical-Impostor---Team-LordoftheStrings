# app.py
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_socketio import SocketIO, join_room, leave_room
from flask import session
import random
import string
import os
import time

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
socketio = SocketIO(app, cors_allowed_origins="*")

rooms = {}

MUSIC_FOLDER = 'static/music'  # Adjust this path as needed

print(f"MUSIC_FOLDER path: {MUSIC_FOLDER}")
print(f"Contents of MUSIC_FOLDER: {os.listdir(MUSIC_FOLDER)}")

def generate_room_code(length=6):
    return ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(length))

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        nickname = request.form.get('nickname')
        action = request.form.get('action')
        
        if action == 'create':
            room_code = generate_room_code()
            max_players = int(request.form.get('max_players', 5))  # Default to 5 if not provided
            rooms[room_code] = {'players': [nickname], 'max_players': max_players}  # Add the host to the players list
            return redirect(url_for('room', room_code=room_code, nickname=nickname))
        elif action == 'join':
            room_code = request.form.get('room_code')
            if room_code in rooms:
                if len(rooms[room_code]['players']) < rooms[room_code]['max_players']:
                    return redirect(url_for('room', room_code=room_code, nickname=nickname))
                else:
                    return "Room is full!"
            else:
                return "Room not found!"
    return render_template('index.html')

@app.route('/leave/<room_code>/<nickname>')
def leave_room_route(room_code, nickname):
    if room_code in rooms and nickname in rooms[room_code]['players']:
        rooms[room_code]['players'].remove(nickname)
        if len(rooms[room_code]['players']) == 0:
            del rooms[room_code]
    return redirect(url_for('index'))

@socketio.on('leave_room')
def on_leave_room(data):
    room_code = data['room_code']
    nickname = data['nickname']
    leave_room(room_code)
    if room_code in rooms and nickname in rooms[room_code]['players']:
        rooms[room_code]['players'].remove(nickname)
        socketio.emit('player_left', {'nickname': nickname}, to=room_code)
    if len(rooms[room_code]['players']) == 0:
        del rooms[room_code]

# @socketio.on('close_room')
# def on_close_room(data):
#     room_code = data['room_code']
#     if room_code in rooms:
#         socketio.emit('room_closed', to=room_code)
#         del rooms[room_code]

@socketio.on('close_room')
def on_close_room(data):
    room_code = data['room_code']
    if room_code in rooms:
        socketio.emit('room_closed', to=room_code)
        del rooms[room_code]
    print(f"Room {room_code} has been closed")  # Add this line for debugging

# Modify the room route to pass the host information
@app.route('/room/<room_code>/<nickname>')
def room(room_code, nickname):
    if room_code not in rooms:
        return "Room not found!"
    
    # Check if the player is already in the room, if not, add them
    if nickname not in rooms[room_code]['players']:
        rooms[room_code]['players'].append(nickname)
    
    is_host = nickname == rooms[room_code]['players'][0]  # The first player in the list is the host
    return render_template('room.html', room_code=room_code, nickname=nickname, is_host=is_host, players=rooms[room_code]['players'])

@app.route('/get_players/<room_code>')
def get_players(room_code):
    
    if room_code in rooms:
        return {'players': rooms[room_code]['players']}
    return {'players': []}

@app.route('/game/<room_code>/<nickname>')
def game(room_code, nickname):
    if room_code not in rooms:
        return "Room not found!", 404
    if nickname not in rooms[room_code]['players']:
        return "Player not found in this room!", 403
    
    is_impostor = rooms[room_code]['impostor'] == nickname
    return render_template('game.html', 
                           room_code=room_code, 
                           nickname=nickname, 
                           players=rooms[room_code]['players'],
                           is_impostor=is_impostor)

@socketio.on('join')
def on_join(data):
    room_code = data['room_code']
    nickname = data['nickname']
    join_room(room_code)
    join_room(nickname)  # Join a room specific to this player
    if room_code not in rooms:
        rooms[room_code] = {'players': [], 'max_players': 4}
    if nickname not in rooms[room_code]['players']:
        rooms[room_code]['players'].append(nickname)
    print(f"Player {nickname} joined room {room_code}")
    print(f"Current rooms: {rooms}")
    socketio.emit('join_confirmation', {'message': f'You ({nickname}) have joined room {room_code}'}, room=nickname)
    
    # If the game has already started, send the game_started event to the new player
    if rooms[room_code].get('game_started', False):
        impostor = rooms[room_code]['impostor']
        socketio.emit('game_started', {'impostor': impostor}, to=nickname)
        
    # debugging
    print(f"Current rooms: {rooms}")
    
@socketio.on('leave')
def on_leave(data):
    room_code = data['room_code']
    nickname = data['nickname']
    leave_room(room_code)
    rooms[room_code]['players'].remove(nickname)
    socketio.emit('player_left', {'nickname': nickname}, to=room_code)
    
@socketio.on('start_game')
def on_start_game(data):
    print("Received start_game event")
    room_code = data['room_code']
    if room_code in rooms:
        impostor = select_impostor(room_code)
        rooms[room_code]['game_started'] = True
        print(f"Starting game for room {room_code}, impostor: {impostor}")

        try:
            normal_category = random.choice(os.listdir(MUSIC_FOLDER))
            print(f"Selected normal category: {normal_category}")
            normal_song = get_random_song(normal_category)
            print(f"Selected normal song: {normal_song}")
            impostor_song = get_random_song(None, exclude_category=normal_category)
            print(f"Selected impostor song: {impostor_song}")

            for player in rooms[room_code]['players']:
                if player == impostor:
                    song_data = impostor_song
                else:
                    song_data = normal_song
                
                print(f"Emitting game_started to player: {player}")
                socketio.emit('game_started', {
                    'impostor': impostor,
                    'song': song_data
                }, room=player)
                print(f"Emission to {player} completed")

            print(f"Emitted game_started to all players in room {room_code}")
            
            # Emit to the entire room as well
            socketio.emit('game_started_room', {'message': 'Game has started'}, room=room_code)
            print(f"Emitted game_started_room to room {room_code}")
        except Exception as e:
            print(f"Error starting game: {str(e)}")
            import traceback
            traceback.print_exc()
    else:
        print(f"Room {room_code} not found")
        
    @socketio.on('ping')
    def handle_ping():
        print("Received ping")
        return "pong"

def select_impostor(room_code):
    if room_code in rooms and rooms[room_code]['players']:
        impostor = random.choice(rooms[room_code]['players'])
        rooms[room_code]['impostor'] = impostor
        return impostor
    return None

def get_random_song(category, exclude_category=None):
    categories = [d for d in os.listdir(MUSIC_FOLDER) if os.path.isdir(os.path.join(MUSIC_FOLDER, d))]
    if exclude_category:
        categories.remove(exclude_category)
    
    if category is None:
        category = random.choice(categories)
    
    category_path = os.path.join(MUSIC_FOLDER, category)
    songs = [f for f in os.listdir(category_path) if f.endswith('.mp3')]
    song = random.choice(songs)
    
    title, artist = song.split('-')
    return {
        'category': category,
        'filename': song,
        'path': f'static/music/{category}/{song}',
        'title': title.strip(),
        'artist': artist.strip()[:-4]  # Remove .mp3 extension
    }


if __name__ == '__main__':
    socketio.run(app, debug=True, host='0.0.0.0')