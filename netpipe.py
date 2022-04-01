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
