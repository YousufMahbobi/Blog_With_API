from flask import Flask, jsonify, request
from flask_cors import CORS
from util.validation import is_valid_post, is_valid_title, is_valid_content
from util.id_generator import generate_id
from util.is_id_exists import is_id_exists

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

POSTS = [
    {"id": 1, "title": "First post", "content": "This is the first post."},
    {"id": 2, "title": "Second post omg", "content": "This is the second post."},
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

@app.route('/api/posts/<int:post_id>', methods=['DELETE'])
def delete_post(post_id):
    id_exists , post = is_id_exists(post_id, POSTS)
    if not id_exists:
        return jsonify({'error': 'Post not found'}), 404
    POSTS.remove(post)

    return jsonify({'message': f'Post with id {post_id} has been deleted successfully.'}), 200

@app.route('/api/posts/<int:post_id>', methods=['GET'])
def edit_post(post_id):
    id_exists, post = is_id_exists(post_id, POSTS)
    if not is_id_exists:
        return jsonify({'error': 'Post not found'}), 404

    return jsonify({'id': post['id'], 'title': post['title'], 'content': post['content']}), 200

@app.route('/api/posts/<int:post_id>', methods=['PUT'])
def update_post(post_id):
    post_data = request.get_json()
    id_exists, post = is_id_exists(post_id, POSTS)

    if not is_id_exists:
        return jsonify({'error': 'Post not found'}), 404

    title = post['title']
    if 'title' in post_data and post_data['title']:
        valid_flag, message = is_valid_title(post_data)
        if not valid_flag:
            return jsonify({'error': message}), 400

        title = post_data['title']

    content = post['content']
    if 'content' in post_data and post_data['content']:
        valid_flag, message = is_valid_content(post_data)
        if not valid_flag:
            return jsonify({'error': message}), 400
        content = post_data['content']


    post.update({'title': title, 'content': content})

    return jsonify(post), 200



@app.route('/api/posts/search', methods=['GET'])
def search_posts():
    title_query = request.args.get('title', '').lower()
    content_query = request.args.get('content', '').lower()

    results = []
    for post in POSTS:
        title_match = title_query in post['title'].lower() if title_query else True
        content_match = content_query in post['content'].lower() if content_query else True

        if title_match and content_match:
            results.append(post)

    return jsonify(results), 200



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5002, debug=True)
