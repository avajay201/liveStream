from flask import Flask
from flask_sock import Sock
import sqlite3
import json

app = Flask(__name__)
sock = Sock(app)
DB_PATH = 'db.sqlite3'
streams = {}

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Enables fetching rows as dictionaries
    return conn

def stream_exists(stream):
    """Check if the stream exists in the Stream model."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM stream_stream WHERE unique_key = ?", (stream,))
    result = cursor.fetchone()
    conn.close()
    return result[0] > 0

@sock.route('/ws/<stream>/')
def chat(ws, stream):
    # Check if the stream exists
    if not stream_exists(stream):
        ws.send(json.dumps({'type': 'error', 'message': 'Stream does not exist'}))
        ws.close()
        return

    # Add WebSocket connection to the room
    if stream not in streams:
        streams[stream] = []

    streams[stream].append(ws)

    try:
        while True:
            data = ws.receive()
            if data:
                message = json.loads(data)
                print('Message from client:', message)

                # Broadcast the message to all clients in the room
                for client in streams[stream]:
                    try:
                        client.send(json.dumps({
                            'sender': message.get('sender', 'Anonymous'),
                            'message': message.get('message', '')
                        }))
                    except:
                        streams[stream].remove(client)
    except:
        # Clean up WebSocket on disconnect
        streams[stream].remove(ws)

if __name__ == '__main__':
    app.run(debug=True)
