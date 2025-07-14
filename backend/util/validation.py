def is_valid_title(post_data):
    if not 'title' in post_data:
        return False, 'Post title is required.'

    title = post_data.get('title')

    if not isinstance(title, str) or not title.strip():
        return False, 'Title must be a non-empty string.'

    if len(title) < 5 or len(title) > 100:
        return False, 'Title must be between 5 and 100 characters.'

    return True, None

def is_valid_content(post_data):
    if not 'content' in post_data:
        return False, 'Post content is required.'

    content = post_data.get('content')

    if not isinstance(content, str) or not content.strip():
        return False, 'Content must be a non-empty string.'

    if len(content) < 10 or len(content) > 1000:
        return False, 'Content must be between 10 and 1000 characters.'

    return True, None

def is_object(post_data):
    if not isinstance(post_data, dict):
        return False, 'Post data must be a JSON object.'

    return True, None


def is_valid_post(post_data):
    valid_flag, message = is_object(post_data)
    if not valid_flag:
        return False, message
    valid_flag, message = is_valid_title(post_data)
    if not valid_flag:
        return False, message
    valid_flag, message = is_valid_content(post_data)
    if not valid_flag:
        return False, message

    return True, None




