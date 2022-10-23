def get(path):
    file_str = ''
    try:
        with open(path, 'r', encoding='utf8') as f:
            file_str = f.read().strip()
    except Exception as e:
        print(e)
    return file_str


def put(data, path):
    try:
        with open(path, 'w', encoding='utf8') as f:
            file_str = f.write(str(data))
    except Exception as e:
        print(e)
