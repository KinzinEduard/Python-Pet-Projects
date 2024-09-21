import string
from transliterate import translit


class Password:
    ALPHABET = string.ascii_letters + string.digits
    DICT = {c: i for (i, c) in enumerate(ALPHABET)}
    N = len(ALPHABET)

    @staticmethod
    def add_underscore(text: str) -> str:
        new_text = ''
        for i, c in enumerate(text):
            new_text += c
            if i % 3 == 2:
                new_text += '_'
        return new_text

    @staticmethod
    def move_text(text: str, delta: int):
        new_text = ''
        for (i, c) in enumerate(text):
            new_text += text[(i - delta) % len(text)]
        return new_text

    @staticmethod
    def get_number(x: int) -> int:
        num = x
        if num < 0:
            return Password.N + num
        return num % Password.N

    @staticmethod
    def get_character(x: int):
        return Password.ALPHABET[Password.get_number(x)]

    @staticmethod
    def iter_word(text: str, x: int):
        new_text = ''
        for i, c in enumerate(text):
            new_text += Password.get_character(Password.DICT[c] + x)
        return new_text

    @staticmethod
    def iter_word_and_move(text: str, x: int):
        new_text = ''
        for i, c in enumerate(text):
            new_text += Password.get_character((i + 3) ** 5 + Password.DICT[c] ** (i + 1) + Password.f(x * i + 1))
        return new_text

    @staticmethod
    def f(x: int) -> int:
        return x ** 5 - 3 * x ** 3 + 7 * x - 2

    @staticmethod
    def sum_of_word(text: str) -> int:
        x = 0
        for i, c in enumerate(text):
            x += Password.DICT[c] + 1
        return x

    @staticmethod
    def gen_password(get_text: str, d: int):
        text = ''.join(str(translit(get_text, 'ru', reversed=True)).split())
        s = Password.sum_of_word(text)
        delta = Password.f(s + d) % 100

        shifted_text = Password.move_text(text, delta ** 3)
        password = ''
        for i, c in enumerate(shifted_text):
            x = Password.f(((i + 1) * Password.DICT[c] ** 2 ) * delta)
            password += Password.get_character(x)
            if i % 2 == 1:
                y = Password.f(((i + 1) * Password.DICT[password[-1]] * (1 + Password.DICT[password[-2]])) * delta)
                password += Password.get_character(y)
        password += Password.iter_word(password, Password.f(len(password) + delta))[::-1]
        password += Password.iter_word(password, Password.f(len(password) * delta + s + Password.sum_of_word(password)))
        password += Password.iter_word(password, Password.f(len(password) + delta ** 2))[::-1]
        password += Password.move_text(password, Password.f(int(len(password) // 2) + delta))[:: -1]
        password = Password.iter_word_and_move(password, Password.f(int(len(password) // 2) + delta))
        password *= 2
        password = password[:: s % 4 + 1]
        password = password[0: 8][::-1]
        password = Password.add_underscore(password)
        password = string.ascii_lowercase[(s ** 2) % len(string.ascii_lowercase)] + password
        password += string.ascii_uppercase[(s ** 2) % len(string.ascii_uppercase)]
        return password


class GenLongText(Password):

    @staticmethod
    def raise_numer(x: int):
        number = GenLongText.f(x ** 2 + x + 1230) ** 3 + x + 1
        return int(str(number // 10 ** 2) + str(number % (10 ** 12)))

    @staticmethod
    def gen_text_by_number(x: int) -> str:
        text = ''
        num_text = str(GenLongText.raise_numer(x))
        for i, c in enumerate(num_text):
            n = GenLongText.f(int(c) ** 2 + 1)
            text += GenLongText.get_character(n)
        text = GenLongText.iter_word(text, x)
        text = GenLongText.move_text(text, x ** 2)
        return text[:12]
