def from_hex_to_string(data: str):
    tem = []

    for i in range(0, len(data), 3):
        tem.append(
            chr(
                int(data[i:i + 3], 16)
                ).encode("CP1251")
            )

    return b''.join(tem).decode("CP1251")


def from_hex_to_binary(data: str):
    tem = []

    for i in range(0, len(data), 2):
        tem.append(bytes.fromhex(data[i:i + 2]))

    return b''.join(tem)
