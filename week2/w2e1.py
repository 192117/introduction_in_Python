import os
import tempfile
import argparse
import json


def parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('--key')
    parser.add_argument('--val')
    return parser.parse_args()


def read(storage_path):
    if not os.path.exists(storage_path):
        return {}
    with open(storage_path, "r") as file:
        data = file.read()
        if data:
            return json.loads(data)
        else:
            return {}


def write(storage_path, data):
    with open(storage_path, "w") as file:
        file.write(json.dumps(data))


def put(storage_path, key, value):
    data = read(storage_path)
    data[key] = data.get(key, list())
    data[key].append(value)
    write(storage_path, data)


def get(storage_path, key):
    data = read(storage_path)
    return data.get(key, [])


def main(storage_path):
    arguments = parser()
    if arguments.key and arguments.val:
        put(storage_path, arguments.key, arguments.val)
    elif arguments.key:
        print(*get(storage_path, arguments.key), sep=", ")

if __name__ == "__main__":
    storage_path = os.path.join(tempfile.gettempdir(), 'storage.data')
    main(storage_path)