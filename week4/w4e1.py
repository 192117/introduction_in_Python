import tempfile
import os
import random


class File:

    def __init__(self, file_path):
        self.position = 0
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            open(self.file_path, "w").close()

    def read(self):
        with open(self.file_path, "r") as file:
            return file.read()

    def write(self, content):
        with open(self.file_path, "w") as file:
            return file.write(content)

    def __str__(self):
        return os.path.abspath(self.file_path)

    def __add__(self, other):
        new_path = os.path.join(tempfile.gettempdir(), str(random.random()) + ".txt")
        new_file = File(new_path)
        new_file.write(self.read() + other.read())
        return new_file

    def __iter__(self):
        return self

    def __next__(self):
        with open(self.file_path, "r") as file:
            file.seek(self.position)
            line = file.readline()
            if not line:
                self.position = 0
                raise StopIteration
            self.position = file.tell()
            return line
