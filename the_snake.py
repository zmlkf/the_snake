from random import choice, randint

import pygame

# Инициализация PyGame
pygame.init()

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
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Скорость движения змейки
SPEED = 5

# Настройка игрового окна
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля
pygame.display.set_caption('Змейка')

# Настройка времени
clock = pygame.time.Clock()

# Цвета элементов
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Центр экрана
CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)


# Радномные координаты
def rand_coord():
    """Получаем рандомные координаты"""
    return randint(0, 31) * GRID_SIZE, randint(0, 23) * GRID_SIZE


class GameObject():
    """Родительский класс"""
    def __init__(self, position=CENTER, body_color=GREEN):
        """Создание объекта на основе позиции и цвета"""
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка объекта"""
        pass


class Apple(GameObject):
    """Дочерний класс"""
    def __init__(self, position=CENTER, body_color=RED):
        """Созднание превого объекта с наследованием от
        родительского класса"""
        super().__init__(position, body_color)

    # Метод draw класса Apple
    def draw(self, surface):
        """Отрисовка яблока"""
        rect = pygame.Rect(
            (self.position[0], self.position[1]),
            (GRID_SIZE, GRID_SIZE)
        )
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (93, 216, 228), rect, 1)

    def meeting_with_apple(self, snake):
        """Проверка на встречу с яблоком"""
        if snake.get_head_position() == self.position:
            snake.length += 1
            snake.grow(self.position)
            self.position = self.randomize_position()

    def randomize_position(self):
        """Получение новой рандомной позиции для яблока"""
        return randint(0, 31) * GRID_SIZE, randint(0, 23) * GRID_SIZE


class Snake(GameObject):
    """Создание дочернего класса"""
    def __init__(self, position=CENTER, body_color=GREEN):
        """Иницилизация объекта"""
        super().__init__(position, body_color)
        self.length = 1
        self.positions = [self.position]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    # Метод обновления направления после нажатия на кнопку
    def update_direction(self):
        """Обновление направления"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Движение змейкой"""
        snake_head = self.get_head_position()
        new_direction = tuple((i * GRID_SIZE for i in self.direction))
        self.last = self.positions[-1]
        new_head = tuple((sum(i) for i in zip(new_direction, snake_head)))
        self.positions.insert(0, new_head)
        self.positions.pop()

    # Метод draw класса Snake
    def draw(self, surface):
        """Отрисовка змеи и затирание хоста"""
        for position in self.positions[:-1]:
            rect = (
                pygame.Rect((position[0], position[1]), (GRID_SIZE, GRID_SIZE))
            )
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (93, 216, 228), rect, 1)

        # Отрисовка головы змейки
        head = self.positions[0]
        head_rect = pygame.Rect((head[0], head[1]), (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, head_rect)
        pygame.draw.rect(surface, (93, 216, 228), head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(
                (self.last[0], self.last[1]), (GRID_SIZE, GRID_SIZE)
            )
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Получение координатов головы змеи"""
        return self.positions[0]

    # Увеличение змеи
    def grow(self, apple):
        """Увеличение змея за счет съеденного яблока"""
        new_direction = tuple((i * GRID_SIZE for i in self.direction))
        new_head = tuple((sum(i) for i in zip(new_direction, apple)))
        self.positions.insert(0, new_head)

    def reset(self):
        """Сброс змейка до начального состояния"""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.next_direction = None
        screen.fill(BOARD_BACKGROUND_COLOR)
        self.last = None

    def сrash(self):
        """При столкновение со стеной голове присваеватся
        объект с противоположно стороны """
        snake_head = self.get_head_position()
        if snake_head[0] < 0:
            self.positions[0] = ((SCREEN_WIDTH, snake_head[1]))
        elif snake_head[0] >= SCREEN_WIDTH:
            self.positions[0] = ((0, snake_head[1]))
        elif snake_head[1] < 0:
            self.positions[0] = ((snake_head[0], SCREEN_HEIGHT))
        elif snake_head[1] >= SCREEN_HEIGHT:
            self.positions[0] = ((snake_head[0], 0))

    def crash_with_yourself(self):
        """Проверка на столкновение с собой"""
        if self.get_head_position() in self.positions[2:]:
            self.reset()


def handle_keys(game_object):
    """Функция обработки действий пользователя"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Функция запуска игры"""
    snake = Snake((randint(0, 31) * GRID_SIZE, randint(0, 23) * GRID_SIZE))
    apple = Apple(rand_coord())

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.meeting_with_apple(snake)
        snake.сrash()
        snake.crash_with_yourself()
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(SPEED)


if __name__ == '__main__':
    main()
