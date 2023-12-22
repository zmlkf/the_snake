from random import choice, randrange

import pygame as pg

import sys

# Инициализация Pgpg
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
BOARD_BACKGROUND_COLOR = (110, 110, 110)

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)
screen.fill(BOARD_BACKGROUND_COLOR)

# Заголовок окна игрового поля
pg.display.set_caption('Змейка')

# Настройка времени
clock = pg.time.Clock()

# Цвета элементов
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)


# Центр экрана
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Радномные координаты
def rand_coord():
    """Получаем рандомные координаты"""
    return (
        randrange(0, SCREEN_WIDTH, GRID_SIZE),
        randrange(0, SCREEN_HEIGHT, GRID_SIZE)
    )


class GameObject():
    """Родительский класс"""

    def __init__(self, position=CENTER, body_color=GREEN):
        """Создание объекта на основе позиции и цвета"""
        self.position = position
        self.body_color = body_color

    def draw(self, position, surface=screen):
        """Отрисовка объекта"""
        rect = pg.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(surface, self.body_color, rect)


class Apple(GameObject):
    """Дочерний класс"""

    def __init__(self, position=CENTER, body_color=RED):
        """Созднание превого объекта с наследованием от
        родительского класса
        """
        super().__init__(position, body_color)

    def randomize_position(self, snake):
        """Получение новой рандомной позиции для яблока
        которая не совпадает с координатами змеи
        """
        while self.position in snake.positions:
            self.position = (
                randrange(0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE)
            )


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
        """Движение змейкой"""
        new_direction = tuple((i * GRID_SIZE for i in self.direction))
        self.last = self.positions[-1]
        new_head = tuple(
            (sum(i) for i in zip(new_direction, self.get_head_position()))
        )
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.positions.pop()

    # Метод draw класса Snake
    def draw(self, position, surface=screen):
        """Отрисовка змеи и затирание хоста"""
        super().draw(position)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение координатов головы змеи"""
        return self.positions[0]

    def reset(self):
        """Сброс змейки до начального состояния"""
        self.length = 1
        self.positions = [self.position]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.last = None
        global SPEED
        SPEED = 5

    def сrash(self):
        """При столкновение со стеной голове присваеватся
        объект с противоположно стороны
        """
        head = self.get_head_position()
        if head[0] < 0:
            self.positions[0] = ((SCREEN_WIDTH, head[1]))
        elif head[0] >= SCREEN_WIDTH:
            self.positions[0] = ((0, head[1]))
        elif head[1] < 0:
            self.positions[0] = ((head[0], SCREEN_HEIGHT))
        elif head[1] >= SCREEN_HEIGHT:
            self.positions[0] = ((head[0], 0))

    def crash_with_yourself(self):
        """Проверка на столкновение с собой"""
        if self.get_head_position() in self.positions[4:]:
            self.reset()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        elif event.type == pg.KEYDOWN:
            dct = {
                (LEFT, pg.K_UP): UP,
                (RIGHT, pg.K_UP): UP,
                (UP, pg.K_LEFT): LEFT,
                (DOWN, pg.K_LEFT): LEFT,
                (UP, pg.K_RIGHT): RIGHT,
                (DOWN, pg.K_RIGHT): RIGHT,
                (LEFT, pg.K_DOWN): DOWN,
                (RIGHT, pg.K_DOWN): DOWN,
            }
            game_object.next_direction = dct.get(
                (game_object.direction, event.key),
                game_object.direction
            )
            game_object.update_direction()


def main():
    """Функция запуска игры"""
    snake = Snake()
    apple = Apple(rand_coord())

    while True:
        handle_keys(snake)

        snake.move()
        snake.сrash()

        # Проверка на встречу с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Ускорение при достижении кол-ва объектов змеи кратного 5
            if not snake.length % 5:
                global SPEED
                SPEED += 1
            snake.draw(apple.position)
            apple.randomize_position(snake)
        snake.crash_with_yourself()
        snake.draw(snake.get_head_position())
        apple.draw(apple.position)
        pg.display.update()
        clock.tick(SPEED)
        pg.display.flip()


if __name__ == '__main__':
    main()
