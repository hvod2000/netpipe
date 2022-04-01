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

    def write(self, obj):
        match obj:
            case str(text):
                self.write_uint(0)
                self.write_text(text)
            case bytes(byts):
                self.write_uint(1)
                self.write_bytes(byts)
            case int(numb):
                self.write_uint(2)
                self.write_uint(numb)

    def read(self):
        match self.read_uint():
            case 0:
                return self.read_text()
            case 1:
                return self.read_bytes()
            case 2:
                return self.read_uint()


def test_pipe():
    b1, b2 = bytearray(), bytearray()

    def s1_send(data):
        nonlocal b2
        b2 += data

    def s2_send(data):
        nonlocal b1
        b1 += data

    def s1_recv(size):
        nonlocal b1
        result = b1[:size]
        del b1[:size]
        return result

    def s2_recv(size):
        nonlocal b2
        result = bytes(b2[:size])
        del b2[:size]
        return result

    return Pipe(s1_send, s1_recv), Pipe(s2_send, s2_recv)


if __name__ == "__main__":
    p1, p2 = test_pipe()
    p1.write("Hello, world!")
    print(p2.read())
    p1.write(42)
    print(p2.read())
    p1.write(b"bytes")
    print(p2.read())
