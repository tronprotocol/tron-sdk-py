import base58


class ADDR(bytes):
    """TRON Address."""

    def __new__(cls, value):
        if isinstance(value, bytes) and len(value) == 21:
            return bytes.__new__(cls, value)
        elif isinstance(value, str):
            if value.startswith('T') and len(value) == 34:
                return bytes.__new__(cls, base58.b58decode_check(value))
            elif value.startswith('41') and len(value) == 21 * 2:
                return bytes.__new__(cls, bytes.fromhex(value))
            elif value.startswith('0x') and len(value) == 21 * 2:
                return bytes.__new__(cls, b'\x41' + bytes.fromhex(value[2:]))

        raise ValueError("invalid address")

    def __str__(self):
        return base58.b58encode_check(self).decode('ascii')


class HEX(bytes):
    """HEX string."""

    def __new__(cls, value):
        if isinstance(value, bytes):
            return bytes.__new__(cls, value)
        elif isinstance(value, str):
            if value.startswith('0x'):
                return bytes.__new__(cls, bytes.fromhex(value[2:]))
            else:
                return bytes.__new__(cls, bytes.fromhex(value))

        raise ValueError("invalid hex")

    def __str__(self):
        return self.hex()


if __name__ == "__main__":
    print(ADDR("TGoJRdYmPqpJkfzLsAbk8GymDADuK6G5i1"))
    print(ADDR("41dd2bcef00ddc0fb1cee5d9996c30200da54a2c43"))
    print(ADDR("0xdd2bcef00ddc0fb1cee5d9996c30200da54a2c43"))
    print(HEX("7471205387718f8454c8c3f70215165c249a06a2fccf9b753690307ab9fb3fd7"))
