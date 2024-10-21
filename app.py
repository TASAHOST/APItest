from flask import Flask, request, jsonify

app = Flask(__name__)
users = {}

@app.route('/users', methods=['POST'])
def create_user():
    user_id = len(users) + 1
    user_data = request.json
    users[user_id] = user_data
    return jsonify({'id': user_id, 'user': user_data}), 201

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify({'id': user_id, 'user': user})
    else:
        return jsonify({'error': 'User not found'}), 404

@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return '', 204
    else:
        return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)