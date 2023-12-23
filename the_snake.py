from random import choice, randint

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

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Настройка времени
clock = pg.time.Clock()

# Цвета элементов
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Центр экрана
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Рандомные координаты для запуска игры
# не совподающие с координатами других обьектов
def random_coord(position):
    while True:
        new_coord = (
            randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)
        )
        if new_coord != position:
            return new_coord


class GameObject():
    """Родительский класс"""

    def __init__(self, position=CENTER, body_color=GREEN):
        """Создание объекта на основе позиции и цвета"""
        self.position = position
        self.body_color = body_color

    def draw(self, position, surface=screen):
        """Отрисовка объекта"""
        pg.draw.rect(
            surface,
            self.body_color,
            (
                position[0] * GRID_SIZE,
                position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE
            )
        )


class Apples(GameObject):
    """Дочерний класс"""

    def __init__(self, position=CENTER, body_color=RED):
        """Созднание превого объекта с наследованием от
        родительского класса
        """
        super().__init__(position, body_color)

    def randomize_position(self, snake_positions, *apple_positions):
        """Получение новой рандомной позиции для яблока
        которая не совпадает с ячейками змеи
        """
        while True:
            new_pos = (
                randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)
            )
            if new_pos not in snake_positions + list(apple_positions):
                self.position = new_pos
                break


class Snake(GameObject):
    """Создание дочернего класса"""

    def __init__(self, position=CENTER, body_color=GREEN):
        """Иницилизация объекта"""
        super().__init__(position, body_color)
        self.reset()

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновление направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейкой c применением тороидальной геометрии"""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.positions.pop()

    # Метод draw класса Snake
    def draw(self, surface=screen):
        """Отрисовка змеи"""
        for position in self.positions:
            super().draw(position)

    def get_head_position(self):
        """Получение координатов головы змеи"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None  # Атрибут необходимый по условию задачи
        self.last = None
        self.speed = SPEED

    def crash_with_yourself(self):
        """Проверка на столкновение с собой"""
        if self.get_head_position() in self.positions[4:]:
            self.reset()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            return True
        elif event.type == pg.KEYDOWN:
            # Выход по esq
            if event.key == pg.K_ESCAPE:
                pg.quit()
                return True
            # Словарь для определения направления змейки
            dct = {
                (LEFT, pg.K_UP): UP, (RIGHT, pg.K_UP): UP,
                (UP, pg.K_LEFT): LEFT, (DOWN, pg.K_LEFT): LEFT,
                (UP, pg.K_RIGHT): RIGHT, (DOWN, pg.K_RIGHT): RIGHT,
                (LEFT, pg.K_DOWN): DOWN, (RIGHT, pg.K_DOWN): DOWN,
            }
            game_object.next_direction = dct.get(
                (game_object.direction, event.key), game_object.direction
            )
            # Обновление направления
            game_object.update_direction()


def main():
    """Функция запуска игры
    в которой красные яблоки - увеличивают змейку,
    а синие - уменьшают. А так же ускорение змейки
    при увеличении ее тела.
    """
    snake = Snake()
    apple = Apples(random_coord(snake.position))
    special_apple = Apples(random_coord(apple.position), body_color=BLUE)
    # Таймер для смены позиций яблок
    timer_for_apples = 0

    while True:
        # Нажатие клавиш
        if handle_keys(snake):
            break

        # Движение змеи
        snake.move()

        # Проверка на встречу с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Ускорение при достижении кол-ва объектов змеи кратного 3
            if not snake.length % 3:
                snake.speed += 1
            apple.randomize_position(snake.positions, special_apple.position)

        # Проверка на встречу со специальным ялоком
        # при котором змейка теряет длину, а при длине змейки в 1 объект
        # вызывается метод reset()
        if snake.get_head_position() == special_apple.position:
            snake.length -= 1
            if snake.length > 1:
                if not snake.length % 3:
                    snake.speed -= 1
                snake.positions.pop()
                special_apple.randomize_position(
                    snake.positions, apple.position
                )
            else:
                snake.reset()
                special_apple.randomize_position(
                    snake.positions, apple.position
                )

        # Проверка на столкновение с собой
        snake.crash_with_yourself()

        # Увеличения таймера с каждой итерацией
        timer_for_apples += 1
        # Каждый 100 шагов еда меняет местонахождение
        if timer_for_apples >= 100:
            timer_for_apples = 0
            special_apple.randomize_position(snake.positions, apple.position)
            apple.randomize_position(snake.positions, special_apple.position)

        # Отрисовка
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw()
        apple.draw(apple.position)
        special_apple.draw(special_apple.position)

        # Обновление экрана
        pg.display.flip()

        # Заголовок окна игрового поля
        pg.display.set_caption(
            f'Змейка |  Скорость: {snake.speed}  |  '
            f'Длина: {snake.length}  |  esq - для выхода '
        )

        # Ограничение скорости
        clock.tick(snake.speed)


if __name__ == '__main__':
    main()
