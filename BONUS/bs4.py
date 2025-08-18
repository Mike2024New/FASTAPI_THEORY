"""
Как python, преобразует данные для передачи по сети?
1. Выполняется преобразование строку с нужной кодировкой (в примере функция convert_string_to_string_bytes)
2. Далее эта строка преобразуется в набор чисел (байт) от 1 до 255 (в примере функция
convert_string_byte_to_list_digital_bytes).
3. За тем строка из этих чисел уже преобразуется в двоичную систему, данные которой уже и передаются по сети, в примере
это функция convert_bytes_programming_to_bynary.
"""


def convert_string_to_string_bytes(string_in, encoding="utf-8"):
    """перевод обычной строки в байты"""
    string_byte = string_in.encode(encoding)
    return string_byte


def convert_string_byte_to_list_digital_bytes(string_byte_in):
    """
    конвертация из строки байтов в числовые данные
    """
    bytes_data = []
    for byte in string_byte_in:
        bytes_data.append(byte)
    return bytes_data


def convert_bytes_programming_to_bynary(bytes_list_in):
    """конвертация из списка чисел в байты,
    например: [1,255,2,8] будет ['00000001', '11111111', '00000010', '00001000']"""
    binary_bytes_in = []
    for i in bytes_list_in:
        binary_bytes_in.append(format(i, '08b'))
    return binary_bytes_in


if __name__ == '__main__':
    string_original = "Привет"
    string_bytes = convert_string_to_string_bytes(string_in=string_original)
    bytes_digital = convert_string_byte_to_list_digital_bytes(string_byte_in=string_bytes)
    binary_bytes = convert_bytes_programming_to_bynary(bytes_list_in=bytes_digital)
    print(f"1.Оригинальная строка:\n\t{string_original}")
    print(f"2.Строка переведенная в байт строку:\n\t{string_bytes}")
    print(f"3.Строка переведенная в числовой набор от 0 до 255: \n\t{bytes_digital}")
    print(f"4.Двоичное представление оригинальной строки (так оно и передаётся по сети):\n\t{binary_bytes}")
