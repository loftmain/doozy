def get_refined_path(path):
    refined_path = path.split('file://')[1]
    return refined_path
