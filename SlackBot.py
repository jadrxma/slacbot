from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

# Initialize database connection
def get_db_connection():
    conn = sqlite3.connect('links.db')
    conn.row_factory = sqlite3.Row
    return conn

# Endpoint for Slack commands
@app.route('/slack/command', methods=['POST'])
def handle_command():
    data = request.form
    command_text = data.get('text', '')

    if command_text.startswith('add'):
        # Add a new link
        link = command_text.split(maxsplit=1)[1] if len(command_text.split()) > 1 else None
        if link:
            conn = get_db_connection()
            conn.execute('INSERT INTO links (url) VALUES (?)', (link,))
            conn.commit()
            conn.close()
            return jsonify({'response_type': 'in_channel', 'text': f'Link added: {link}'})
        else:
            return jsonify({'response_type': 'ephemeral', 'text': 'Please provide a link to add.'})

    elif command_text.startswith('list'):
        # List all links
        conn = get_db_connection()
        links = conn.execute('SELECT * FROM links').fetchall()
        conn.close()
        links_list = '\n'.join([link['url'] for link in links])
        return jsonify({'response_type': 'in_channel', 'text': f'Links:\n{links_list}'})

    return jsonify({'response_type': 'ephemeral', 'text': 'Invalid command'})


@app.route('/slack/events', methods=['POST'])
def slack_events():
    data = request.json  # This will contain the data sent by Slack
    if 'challenge' in data:
        # Respond to the challenge by returning the challenge value
        return jsonify({'challenge': data['challenge']})
    else:
        # Handle other events here
        return jsonify({'status': 'OK'})

if __name__ == '__main__':
    app.run(debug=True)

if __name__ == '__main__':
    app.run(debug=True)
