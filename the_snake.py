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
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Словарь для определения направления змейки
ORIENTATION = {
    (LEFT, pg.K_UP): UP, (RIGHT, pg.K_UP): UP,
    (UP, pg.K_LEFT): LEFT, (DOWN, pg.K_LEFT): LEFT,
    (UP, pg.K_RIGHT): RIGHT, (DOWN, pg.K_RIGHT): RIGHT,
    (LEFT, pg.K_DOWN): DOWN, (RIGHT, pg.K_DOWN): DOWN,
}


def random_coord(occupied_positions):
    """Рандомные координаты не совподающие с координатами
    переданными в арументах
    """
    while True:
        new_coord = (
            randint(0, GRID_WIDTH - 1), randint(0, GRID_HEIGHT - 1)
        )
        if new_coord not in occupied_positions:
            return new_coord


class GameObject():
    """Базовый класс"""

    def __init__(self, position=CENTER, body_color=GREEN):
        """Создание объекта на основе позиции и цвета"""
        self.position = position
        self.body_color = body_color
        self.last = None

    def draw(self, surface):
        """Это абстрактный метод, который предназначен для переопределения
        # в дочерних классах. Этот метод должен определять, как объект
        # будет отрисовываться на экране. По умолчанию - pass
        """
        pass


class Apple(GameObject):
    """Дочерний класс"""

    def draw(self, surface):
        """Отрисовка объекта, ячейки и при наличии,
        затирание прошлого местоположения
        """
        rect = (
            pg.Rect(
                (self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)
        # Затирание прошлого местоположения
        if self.last:
            last_rect = pg.Rect(
                (self.last[0] * GRID_SIZE, self.last[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
            self.last = None

    def randomize_position(self, occupied_positions):
        """Вызов функции для получения рандомной позиции"""
        return random_coord(occupied_positions)


class Snake(GameObject):
    """Дочерний класс"""

    # Присутствие этого атрибута - условие задачи,
    # хотя ему и нет достойного применения
    next_direction = None

    def __init__(self, body_color):
        """Иницилизация объекта"""
        super().__init__(body_color=body_color)
        self.reset()

    def update_direction(self):
        """Метод, необходимый по условию задачи"""

    def move(self):
        """Проверка на столкновение с собой и дальнейшее движение
        # с применением тороидальной геометрии
        """
        head = self.get_head_position()
        if head in self.positions[4:]:
            self.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self, surface):
        """Отрисовка головы змейки с последующим затирание хвоста
        и при наличии - затирание потерянного хвоста
        """
        head = self.get_head_position()
        rect = (
            pg.Rect(
                (head[0] * GRID_SIZE, head[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
        )
        pg.draw.rect(surface, self.body_color, rect)
        pg.draw.rect(surface, (93, 216, 228), rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0] * GRID_SIZE, self.last[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
        # Затирание потерянного хвоста
        if self.lost_tail:
            lost_rect = pg.Rect(
                (self.lost_tail[0] * GRID_SIZE, self.lost_tail[1] * GRID_SIZE),
                (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, lost_rect)
            self.lost_tail = None

    def get_head_position(self):
        """Получение координатов головы змейки"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = None
        self.lost_tail = None


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
            game_object.direction = ORIENTATION.get(
                (game_object.direction, event.key), game_object.direction
            )


def main():
    """Функция запуска игры
    в которой красные яблоки - увеличивают змейку,
    а синие - уменьшают. А так же ускорение змейки
    по мере увеличения ее тела.
    """
    snake = Snake(body_color=GREEN)
    apple = Apple(random_coord(snake.positions), body_color=RED)
    special_apple = Apple(random_coord(apple.position), body_color=BLUE)
    # Таймер для смены позиций яблок
    timer_for_apples = 0
    screen.fill(BOARD_BACKGROUND_COLOR)
    speed = SPEED

    while True:
        # Нажатие клавиш
        handle_keys(snake)

        # Движение змеи
        snake.move()

        # Проверка на встречу с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Ускорение при достижении кол-ва объектов змеи кратного 3
            if not snake.length % 3:
                speed += 1
            apple.position = apple.randomize_position(
                tuple(snake.positions) + special_apple.position
            )

        # Проверка на встречу со специальным ялоком
        # при котором змейка теряет длину, а при длине змейки в 1 объект
        # вызывается метод reset()
        if snake.get_head_position() == special_apple.position:
            snake.length -= 1
            if snake.length >= 1:
                snake.lost_tail = snake.positions.pop()
                special_apple.position = special_apple.randomize_position(
                    tuple(snake.positions) + apple.position
                )
            else:
                snake.reset()
                # Затирка оторванного хвоста
                special_apple.last = special_apple.position
                screen.fill(BOARD_BACKGROUND_COLOR)

                special_apple.position = special_apple.randomize_position(
                    tuple(snake.positions) + apple.position
                )

        # Увеличения таймера с каждой итерацией
        timer_for_apples += 1
        # Каждый 100 шагов еда меняет местонахождение
        if timer_for_apples >= 100:
            timer_for_apples = 0
            apple.last = apple.position
            special_apple.last = special_apple.position
            special_apple.position = special_apple.randomize_position(
                tuple(snake.positions) + apple.position
            )
            apple.position = apple.randomize_position(
                tuple(snake.positions) + special_apple.position
            )

        # Отрисовка
        snake.draw(screen)
        apple.draw(screen)
        special_apple.draw(screen)

        # Обновление экрана
        pg.display.flip()
        # Заголовок окна игрового поля
        pg.display.set_caption(
            f'Змейка |  Скорость: {speed}  |  '
            f'Длина: {snake.length}  |  esc - для выхода '
        )

        # Ограничение скорости
        clock.tick(speed)


if __name__ == '__main__':
    main()
