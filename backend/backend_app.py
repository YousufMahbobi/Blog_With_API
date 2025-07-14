from flask import Flask, jsonify, request
from flask_cors import CORS
from util.validation import is_valid_post
from util.id_generator import generate_id

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post", "content": "This is the second post."},
]


@app.route('/api/posts', methods=['GET', 'POST'])
def get_posts():
    if request.method == 'POST':
        post_data = request.get_json()

        is_valid, error_message = is_valid_post(post_data)
        if not is_valid:
            return jsonify({'error': error_message}), 400

        post_id = generate_id(len(POSTS))
        new_post = {
            'id': post_id,
            'title': post_data['title'],
            'content': post_data['content']
        }

        POSTS.append(new_post)

        return jsonify(new_post), 201

    return jsonify(POSTS)





if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
