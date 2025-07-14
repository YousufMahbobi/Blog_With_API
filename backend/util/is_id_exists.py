def is_id_exists(target_id, data_list):
    for item in data_list:
        if item['id'] == target_id:
            return True, item
    return False, None