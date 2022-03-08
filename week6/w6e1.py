import asyncio


class ClientServerProtocol(asyncio.Protocol):

    metric_data = dict()


    def process_data(self, data):
        try:
            parse_data = data.rstrip("\n").split()
            if parse_data[0] == "put":
                if len(parse_data) <= 4:
                    key, value, timestamp = parse_data[1], float(parse_data[2]), int(parse_data[3])
                    return self.put(key, value, timestamp)
                else:
                    return "error\nwrong command\n\n"
            elif parse_data[0] == "get":
                if len(parse_data) <= 2:
                    key = parse_data[1]
                    return self.get(key)
                else:
                    return "error\nwrong command\n\n"
            else:
                return "error\nwrong command\n\n"
        except Exception:
            return "error\nwrong command\n\n"


    def put(self, key, value, timestamp):
        if key == '*':
            return 'error\nwrong command\n\n'
        elif key not in ClientServerProtocol.metric_data:
            ClientServerProtocol.metric_data.setdefault(key, [[timestamp, value],])
        else:
            flag = 0
            for values in ClientServerProtocol.metric_data[key]:
                if values[0] == timestamp:
                    values[1] = value
                    flag = 1
            if flag == 0:
                ClientServerProtocol.metric_data[key].append([timestamp, value])
        return "ok\n\n"


    def get(self, key_value):
        answer_get = "ok\n"
        if key_value == "*":
            if len(ClientServerProtocol.metric_data.keys()) != 0:
                for key, values in ClientServerProtocol.metric_data.items():
                    for value in values:
                        answer_get += "{} {} {}\n".format(key, value[1], value[0])
        else:
            if key_value in ClientServerProtocol.metric_data:
                for value in ClientServerProtocol.metric_data[key_value]:
                        answer_get += "{} {} {}\n".format(key_value, value[1], value[0])
        return answer_get + "\n"


    def connection_made(self, transport):
        self.transport = transport


    def data_received(self, data):
        resp = self.process_data(data.decode())
        self.transport.write(resp.encode())


def run_server(host, port):
    loop = asyncio.get_event_loop()
    coro = loop.create_server(
        ClientServerProtocol,
        host, port
    )

    server = loop.run_until_complete(coro)

    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass

    server.close()
    loop.run_until_complete(server.wait_closed())
    loop.close()
