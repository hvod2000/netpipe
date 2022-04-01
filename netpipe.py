class Pipe:
    def __init__(self, send_bytes, receive_bytes):
        self.send = send_bytes
        self.recv = receive_bytes

    def write_uint(self, number):
        result = []
        while number >= 128:
            result.append(128 + (number % 128))
            number //= 128
        result.append(number)
        self.send(bytes(result))

    def read_uint(self):
        result, digit = [], self.recv(1)[0]
        while digit >= 128:
            result.append(digit - 128)
            digit = self.recv(1)[0]
        result.append(digit)
        return sum(b * 128**i for i, b in enumerate(result))

    def write_text(self, data):
        self.write_bytes(data.encode())

    def read_text(self):
        return self.read_bytes().decode()

    def write_bytes(self, data):
        self.write_uint(len(data))
        self.send(data)

    def read_bytes(self):
        return self.recv(self.read_uint())
