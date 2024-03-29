from random import choice, randint
from sys import exit

import pygame as pg

# Инициализация Pygame
pg.init()

# Константы для размеров
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвета фона - черный
BOARD_BACKGROUND_COLOR = (150, 150, 150)

# Цвет границы ячейки
BORDER_CELL_COLOR = (93, 216, 228)

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Настройка времени
clock = pg.time.Clock()

# Цвета элементов
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Центр экрана
CENTER = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Словарь для определения направления змейки
TURNS = {
    (LEFT, pg.K_UP): UP, (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT, (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT, (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_DOWN): DOWN, (RIGHT, pg.K_DOWN): DOWN,
}


def random_coord(occupied):
    """Рандомные координаты не совподающие с координатами
    переданными в арументах.
    """
    while True:
        pos = (randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1))
        if pos not in occupied:
            return pos


class GameObject():
    """Базовый класс, иницилизирующий цвет и позицию объекта игры,
    содержащий методы для отрисовки и затирания этих объектов.
    """

    def __init__(self, position=CENTER, body_color=GREEN):
        """Создание объекта на основе позиции и цвета"""
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Абстрактный метод, который предназначен для переопределения
        в дочерних классах
        """
        pass

    def draw_a_cell(
            self, position, surface, cell_color=None):
        """Отрисовка ячейки объекта на основе местоположения и затирание
        объекта old_position
        """
        rect = (
            pg.Rect(
                (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
        )
        if not cell_color:
            cell_color = self.body_color
        pg.draw.rect(surface, cell_color, rect)
        pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)


class Apple(GameObject):
    """Класс, содеражащий съедобные и несъедобные яблоки для змейки.

    Класс содержит переопределенный метод draw и метод
    присваюващий новую рандомную позицию яблоку.
    """

    def draw(self, surface):
        """Метод для отрисовки яблок"""
        self.draw_a_cell(self.position, surface)

    def randomize_position(self, occupied):
        """Вызов функции для получения рандомной позиции"""
        self.position = random_coord(occupied)


class Snake(GameObject):
    """Класс змейки содержащий дополнительные артибуты относительно
    базового класса.

    Содержит методы для обновления местоположения, движения,
    переопределленого метода draw, метода для получения головы змейки
    и сброс змейки до начального состояния.
    """

    def __init__(self):
        """Иницилизация объекта"""
        super().__init__()
        self.reset()

    def update_direction(self, new_direction):
        """Смена направления"""
        self.direction = new_direction

    def move(self):
        """Движение с применением тороидальной геометрии"""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self, surface):
        """Вызов базового метода для отрисовки ячейки и затирания хвоста"""
        self.draw_a_cell(self.get_head_position(), surface)
        self.draw_a_cell(self.last, surface, BOARD_BACKGROUND_COLOR)

    def get_head_position(self):
        """Получение координатов головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = self.positions[-1]


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            # Выход по esc
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            # Обновление направления
            game_object.update_direction(
                TURNS.get(
                    (game_object.direction, event.key), game_object.direction
                )
            )


def set_caption(speed, length):
    """Заголовок окна игрового поля"""
    pg.display.set_caption(
        f'Змейка |  Скорость: {speed}  |  '
        f'Длина: {length}  |  esc - для выхода '
    )


def main():
    """Функция запуска игры в которой красные яблоки - увеличивают змейку,
    а синие - уменьшают. А так же ускорение змейки
    по мере увеличения ее тела.
    """
    snake = Snake()
    apple = Apple(random_coord(snake.positions), RED)
    bad_apple = Apple(random_coord((*snake.positions, apple.position)), BLUE)
    # Таймер для смены позиций яблок
    timer_for_apples = 0
    screen.fill(BOARD_BACKGROUND_COLOR)
    speed = SPEED
    set_caption(speed, snake.length)

    while True:
        # Нажатие клавиш
        handle_keys(snake)

        # Движение змеи
        snake.move()
        # Проверка на столкновение с собой
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Проверка на встречу с яблоком
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            # Ускорение при достижении кол-ва объектов змеи кратного 3
            if not snake.length % 3:
                speed += 1
            apple.randomize_position(
                (*snake.positions, bad_apple.position)
            )
            set_caption(speed, snake.length)
        # Проверка на встречу с плохим ялоком при котором змейка теряет длину,
        # а при длине змейки в 1 объект плохое яблоко просто меняет позицию
        elif snake.get_head_position() == bad_apple.position:
            if snake.length == 1:
                bad_apple.randomize_position(
                    (*snake.positions, apple.position)
                )
            else:
                if not snake.length % 3:
                    speed -= 1
                snake.length -= 1
                snake.draw_a_cell(
                    snake.positions.pop(), screen, BOARD_BACKGROUND_COLOR
                )
                bad_apple.randomize_position(
                    (*snake.positions, apple.position)
                )
                set_caption(speed, snake.length)

        # Увеличения таймера с каждой итерацией
        timer_for_apples += 1
        # Каждый 100 шагов еда меняет местонахождение
        if timer_for_apples >= 100:
            timer_for_apples = 0
            apple.draw_a_cell(apple.position, screen, BOARD_BACKGROUND_COLOR)
            bad_apple.draw_a_cell(
                bad_apple.position, screen, BOARD_BACKGROUND_COLOR
            )
            bad_apple.randomize_position(
                (*snake.positions, apple.position)
            )
            apple.randomize_position(
                (*snake.positions, bad_apple.position)
            )

        # Отрисовка
        snake.draw(screen)
        apple.draw(screen)
        bad_apple.draw(screen)

        # Обновление экрана
        pg.display.flip()

        # Ограничение скорости
        clock.tick(speed)


if __name__ == '__main__':
    main()
