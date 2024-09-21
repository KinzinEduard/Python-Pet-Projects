import math
import typing as tp

class Vector:
    def __init__(self, *args: float):
        self.__numbers = args
        self.__n = len(self.numbers)

    @property
    def numbers(self):
        return self.__numbers

    @property
    def n(self):
        return self.__n

    def distance(self, vec: 'Vector'):
        return math.sqrt(sum((a - self.numbers[i]) ** 2 for i, a in enumerate(vec.numbers)))

    def __str__(self):
        return f'{self.numbers}'

    def __add__(self, other: 'Vector') -> 'Vector':
        vec1 = self if self.n <= other.n else other
        vec2 = other if self.n <= other.n else self
        args = list[vec2.numbers]
        for i, a in enumerate(vec1.numbers):
            args[i] += a
        return Vector(*iter(args))

    def __mul__(self, alph: float) -> 'Vector':
        return Vector(*(a * alph for a in self.numbers))

    def __sub__(self, other: 'Vector') -> 'Vector':
        vec1 = self if self.n <= other.n else other
        vec2 = other if self.n <= other.n else self
        args = list[vec2.numbers]
        for i, a in enumerate(vec1.numbers):
            args[i] -= a
        return Vector(*iter(args))

    def __iter__(self):
        return self.get_generator()

    def get_generator(self):
        for num in self.numbers:
            yield num

    def move_to(self, pos: 'Vector', distance: float) -> 'Vector':
        vec = (pos - self)
        return self + vec * ((1 / vec.magnitude()) * distance)

    def magnitude(self) -> float:
        return math.sqrt(sum(a ** 2 for a in self.numbers))

    def is_no_near_points(self, points: tp.Iterable['Vector'], distance: float = 1) -> bool:
        for point in points:
            if self.distance(point) <= distance:
                return False
        return True

class Vector2(Vector):
    def __init__(self, x: float, y: float):
        Vector.__init__(self, x, y)
        self.__x = x
        self.__y = y

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    def distance(self, vec: 'Vector2'):
        return math.sqrt((self.x - vec.x) ** 2 + (self.y - vec.y) ** 2)

    def __str__(self):
        return f'x:{self.x} y:{self.y}'

    def __add__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x + other.x, self.y + other.y)

    def __mul__(self, alph: float) -> 'Vector2':
        return Vector2(self.x * alph, self.y * alph)

    def __sub__(self, other: 'Vector2') -> 'Vector2':
        return Vector2(self.x - other.x, self.y - other.y)

    def move_to(self, pos: 'Vector2', distance: float) -> 'Vector2':
        vec = (pos - self)
        return self + vec * ((1 / vec.magnitude()) * distance)

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2)

    def is_no_near_points(self, points: tp.Iterable['Vector2'], distance: float = 1) -> bool:
        for point in points:
            if Vector2.distance(self, point) <= distance:
                return False
        return True


class Vector3(Vector):
    def __init__(self, x: float, y: float, z: float = 0):
        Vector.__init__(self, x, y, z)
        self.__x = x
        self.__y = y
        self.__z = z

    @property
    def x(self):
        return self.__x

    @property
    def y(self):
        return self.__y

    @property
    def z(self):
        return self.__z

    def __str__(self):
        return f'x:{self.x} y:{self.y}'

    def __add__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __mul__(self, alph: float) -> 'Vector3':
        return Vector3(self.x * alph, self.y * alph, self.z * alph)

    def __sub__(self, other: 'Vector3') -> 'Vector3':
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def move_to(self, pos: 'Vector3', distance: float) -> 'Vector3':
        vec = (pos - self)
        return self + vec * ((1 / vec.magnitude()) * distance)

    def magnitude(self) -> float:
        return math.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)
