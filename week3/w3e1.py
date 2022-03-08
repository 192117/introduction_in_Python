class FileReader:

    def __init__(self, path):
        self.path = path


    def read(self):
        try:
            with open(self.path, 'r') as file:
                answer = file.read()
                return answer
        except FileNotFoundError:
            return ''