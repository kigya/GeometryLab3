import matplotlib.pyplot as plt
import math
import random
from celluloid import Camera


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    def draw_point(self):
        plt.scatter(self.x, self.y)

    @staticmethod
    def input_point(name, i):
        x, y = input(name + "[" + str(i) + "]: ").split()
        return Point(float(x), float(y))

    @staticmethod
    def get_list_of_points(length):
        points = []
        xs = [random.randint(0, 10) for _ in range(length)]
        ys = [random.randint(0, 10) for _ in range(length)]
        for i in range(length):
            x = Point(xs[i], ys[i])
            points.append(x)
        return points


class Vector:
    def __init__(self, p1: Point, p2: Point):
        self.x = p2.x - p1.x
        self.y = p2.y - p1.y

    def get_length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __mul__(self, other):
        return self.x * other.x + self.y * other.y

    @staticmethod
    # вектор отражения
    def get_reflected_vector(a: Point, p1: Point, p2: Point):
        # reflectedVector = fallingVector - 2 * normalVector * ((fallingVector * normalVector) / ( normalVector^2))
        b = Point(p2.x - p1.x, p2.y - p1.y)
        result = b
        product = ((a * b) / (b * b)) * 2
        result.x *= product
        result.y *= product
        return result - a

    @staticmethod
    def get_list_of_vectors(length):
        vectors = []
        for i in range(length):
            p = Point(random.randint(-1, 1), random.randint(-1, 1))
            while p.x == 0 and p.y == 0:
                p = Point(random.randint(-1, 1), random.randint(-1, 1))
            vectors.append(p)
        return vectors


class Polygon:
    def __init__(self, points, name):
        self.points = points
        self.name = name

        self.points.append(self.points[0])

    def draw_polygon(self, color):
        # Вывод точки
        for i in range(len(self.points) - 1):
            plt.plot(self.points[i].x, self.points[i].y, marker="o", color=color)

        plt.plot(get_x_coords(self.points), get_y_coords(self.points), color=color)


# Определитель матрицы 2х2
def det(a11, a12, a21, a22):
    return a11 * a22 - a12 * a21


# Найти положение точки P0 относительно прямой P1P2
def find_pos(p1: Point, p2: Point, p0: Point):
    d = det(p2.x - p1.x, p2.y - p1.y, p0.x - p1.x, p0.y - p1.y)
    if d > 0:
        return -1  # Точка левее прямой
    elif d < 0:
        return 1  # Точка правее прямой
    else:
        return 0  # Точка лежит на прямой

# пересечение прямых
def check_intersection(p1: Point, p2: Point, p3: Point, p4: Point):
    d1 = det(p4.x - p3.x, p4.y - p3.y, p1.x - p3.x, p1.y - p3.y)
    d2 = det(p4.x - p3.x, p4.y - p3.y, p2.x - p3.x, p2.y - p3.y)
    d3 = det(p2.x - p1.x, p2.y - p1.y, p3.x - p1.x, p3.y - p1.y)
    d4 = det(p2.x - p1.x, p2.y - p1.y, p4.x - p1.x, p4.y - p1.y)

    if d1 * d2 <= 0 and d3 * d4 <= 0:
        return True  # пересекаются
    else:
        return False  # не пересекаются


# Получить список координат по x из списка точек
def get_x_coords(points: list):
    return [point.x for point in points]


# Получить список координат по y из списка точек
def get_y_coords(points: list):
    return [point.y for point in points]


# Вывод ответа в окно с графиком
def answer(string):
    plt.title(string, fontsize=17, zorder=15)


# Бинарный тест для выпуклого многоугольника
def get_point_position_binary_test(p0: Point, polygon: Polygon):

    if find_pos(polygon.points[0], polygon.points[1], p0) > 0 or \
       find_pos(polygon.points[0], polygon.points[len(polygon.points) - 1], p0) < 0:  # не попадает в сегмент Р1Р0Рn-1
        return False  # точка снаружи мн-ка

    start = 0
    end = len(polygon.points) - 1

    while end - start > 1:
        sep = math.floor((start + end) / 2)
        if find_pos(polygon.points[0], polygon.points[sep], p0) < 0:
            start = sep
        else:
            end = sep

    if find_pos(polygon.points[start], polygon.points[end], p0) < 0:
        return True  # точка внутри мн-ка
    else:
        return False  # точка снаружи мн-ка


# Угловой тест для простого многоугольника
def get_point_position_angle_test(p0: Point, polygon: Polygon):
    s = 0
    for i in range(len(polygon.points) - 1):
        beta1 = get_octane(p0, polygon.points[i])
        beta2 = get_octane(p0, polygon.points[i + 1])
        delta = beta2 - beta1
        if delta > 4:
            delta -= 8
        if delta < -4:
            delta += 8
        d = det(polygon.points[i].x - p0.x, polygon.points[i].y - p0.y,
                polygon.points[i + 1].x - p0.x, polygon.points[i + 1].y - p0.y)
        if delta == 4 or delta == -4:
            if d > 0:
                delta = 4
            if d < 0:
                delta = -4
            if d == 0:
                return True  # лежит на мн-ке
        s += delta
    if s == 8 or s == -8:
        return True  # внутри
    elif s == 0:
        return False  # снаружи
    else:
        ArithmeticError("s is not right")


def get_octane(p1: Point, p2: Point):
    x = p2.x - p1.x
    y = p2.y - p1.y

    if 0 <= y <= x:
        return 1
    elif 0 < x <= y:
        return 2
    elif 0 <= -x < y:
        return 3
    elif 0 < y <= -x:
        return 4
    elif 0 <= -y < -x:
        return 5
    elif 0 < -x <= -y:
        return 6
    elif 0 < x < -y:
        return 7
    elif 0 < -y <= -x:
        return 8
    else:
        return 1


def get_intersected_edge(p1: Point, p2: Point, polygon: Polygon):
    for i in range(len(polygon.points) - 1):
        if check_intersection(p1, p2, polygon.points[i], polygon.points[i + 1]):
            return [polygon.points[i], polygon.points[i + 1]]
    return []


def move(moving_points: list, vectors: list, i):
    moving_points[i] = moving_points[i] + vectors[i]


def has_trapped(p0: Point, v0: Point, moving_points: list, vectors: list):
    moving_points.remove(p0)
    vectors.remove(v0)


if __name__ == "__main__":
    fig = plt.figure()
    camera = Camera(fig)

    # Сетка
    plt.grid(which='major', color='k')

    # Внешний многоугольник
    Q = Polygon([Point(2, 3), Point(4, 1), Point(9, 1), Point(12, 3), Point(14, 9), Point(15, 12), Point(6, 13)], "Q")

    # Внутренний многоугольник
    P = Polygon([Point(7, 4), Point(9, 7), Point(12, 7), Point(11, 11), Point(7, 10), Point(6, 6)], "P")

    # Движущиеся точки
    moving_points = [Point(4, 8), Point(6, 4), Point(10, 4), Point(12, 12), Point(8, 12), Point(6, 8), Point(4, 4)]

    # Создание случайного списка скоростей точек
    vectors = Vector.get_list_of_vectors(len(moving_points))

    while len(moving_points) > 0:
        Q.draw_polygon("red")
        P.draw_polygon("blue")
        for i in range(len(moving_points)):
            moving_points[i].draw_point()
        camera.snap()

        for i in range(len(moving_points)):
            if i >= len(moving_points):
                break

            next_point = Point(moving_points[i].x + vectors[i].x, moving_points[i].y + vectors[i].y)

            while not get_point_position_binary_test(next_point, Q):
                edges = get_intersected_edge(moving_points[i], next_point, Q)
                if len(edges) == 0:
                    move(moving_points, vectors, i)
                    continue
                edge_p1 = edges[0]
                edge_p2 = edges[1]

                vectors[i] = Vector.get_reflected_vector(vectors[i], edge_p1, edge_p2)
                next_point = Point(moving_points[i].x + vectors[i].x, moving_points[i].y + vectors[i].y)

            if get_point_position_binary_test(next_point, P):
                has_trapped(moving_points[i], vectors[i], moving_points, vectors)
                continue
            move(moving_points, vectors, i)

    plt.grid(True)
    animation = camera.animate(blit=False, interval=100)
    animation.save("animation.gif")
    plt.show()
