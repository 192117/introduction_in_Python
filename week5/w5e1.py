import time
import socket


class ClientError(Exception):
    pass


class Client:

    def __init__(self, host, port, timeout):
        self.host = host
        self.port = port
        self.timeout = timeout

    def connect(self, message_send):
        with socket.create_connection((self.host, self.port)) as sock:
            try:
                sock.sendall(message_send.encode("utf-8"))
                answer = sock.recv(1024).decode("utf-8")
            except socket.error:
                raise ClientError
            return answer

    def put(self, key, value, timestamp=None):
        timestamp = timestamp or int(time.time())
        data = "put {} {} {}\n".format(key, str(value), str(timestamp))
        answer = self.connect(data)
        if answer == "ok\n\n":
            pass
        elif answer == "error\nwrong command\n\n":
            raise ClientError

    def get(self, key):
        data_answer = dict()
        data = "get {}\n".format(key)
        answer = self.connect(data)
        if answer == "ok\n\n":
            return data_answer
        elif answer == "error\nwrong command\n\n":
            raise ClientError
        else:
            if "ok\n" in answer:
                if "\n\n" in answer:
                    parse_data = [row.split() for row in answer[3:-2].split("\n")]
                    for metric in parse_data:
                        if len(metric) > 1:
                            try:
                                data_answer[metric[0]] = data_answer.get(metric[0], list())
                                data_answer[metric[0]].append((int(metric[2]), float(metric[1])))
                                data_answer[metric[0]].sort(key=lambda value: value[0])
                            except Exception:
                                raise ClientError
                        else:
                            raise ClientError
                    if key == "*":
                        return data_answer
                    else:
                        return {key: data_answer.get(key)}
                else:
                    raise ClientError
            else:
                raise ClientError