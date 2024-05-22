from random import choice
from sys import exit

import pygame as pg

# Initialize Pygame
pg.init()

# Constants for screen dimensions
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Movement directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BOARD_BACKGROUND_COLOR = (150, 150, 150)
BORDER_CELL_COLOR = (93, 216, 228)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initial game speed
INITIAL_SPEED = 5
SPEED_INCREMENT = 1
TIMER_RESET_THRESHOLD = 100

# Set up game window
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Set up clock
clock = pg.time.Clock()

# Center of the screen
CENTER = (GRID_WIDTH // 2, GRID_HEIGHT // 2)

# Dictionary for determining snake's direction
DIRECTION_MAP = {
    pg.K_UP: UP,
    pg.K_DOWN: DOWN,
    pg.K_LEFT: LEFT,
    pg.K_RIGHT: RIGHT,
}


def random_coord(occupied: set) -> tuple:
    """
    Generate a random coordinate that is not in the occupied positions.

    Args:
        occupied (set): Set of occupied coordinates.

    Returns:
        tuple: Random coordinate (x, y).
    """
    possible_positions = [
        (x, y)
        for x in range(GRID_WIDTH)
        for y in range(GRID_HEIGHT)
        if (x, y) not in occupied
    ]
    return choice(possible_positions)


class GameObject:
    """A base class for game objects."""

    def __init__(self, position: tuple = CENTER, body_color: tuple = GREEN):
        """
        Initialize the game object with a position and body color.

        Args:
            position (tuple): Initial position of the object.
            body_color (tuple): Color of the object.
        """
        self.position = position
        self.body_color = body_color

    def draw(self, surface: pg.Surface):
        """
        Draw the game object on the surface.

        Args:
            surface (pg.Surface): Surface to draw on.
        """
        pass

    def draw_a_cell(self, position: tuple,
                    surface: pg.Surface,
                    cell_color: tuple = None):
        """
        Draw a single cell of the game object.

        Args:
            position (tuple): Position of the cell to draw.
            surface (pg.Surface): Surface to draw on.
            cell_color (tuple, optional): Color of the cell.
        """
        rect = pg.Rect(
            (position[0] * GRID_SIZE, position[1] * GRID_SIZE),
            (GRID_SIZE, GRID_SIZE)
        )
        if not cell_color:
            cell_color = self.body_color
        pg.draw.rect(surface, cell_color, rect)
        pg.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect, 1)


class Apple(GameObject):
    """A class representing an apple."""

    def draw(self, surface: pg.Surface):
        """
        Draw the apple on the surface.

        Args:
            surface (pg.Surface): Surface to draw on.
        """
        self.draw_a_cell(self.position, surface)

    def randomize_position(self, occupied: set):
        """
        Randomize the position of the apple, avoiding occupied positions.

        Args:
            occupied (set): Set of occupied coordinates.
        """
        self.position = random_coord(occupied)


class Snake(GameObject):
    """A class representing the snake."""

    def __init__(self):
        """Initialize the snake."""
        super().__init__()
        self.reset()

    def update_direction(self, new_direction: tuple):
        """
        Update the direction of the snake.

        Args:
            new_direction (tuple): New direction for the snake.
        """
        self.direction = new_direction

    def move(self):
        """Move the snake in the current direction."""
        head = self.get_head_position()
        new_head = (
            (head[0] + self.direction[0]) % GRID_WIDTH,
            (head[1] + self.direction[1]) % GRID_HEIGHT
        )
        self.positions.insert(0, new_head)
        if self.length < len(self.positions):
            self.last = self.positions.pop()

    def draw(self, surface: pg.Surface):
        """
        Draw the snake on the surface.

        Args:
            surface (pg.Surface): Surface to draw on.
        """
        self.draw_a_cell(self.get_head_position(), surface)
        self.draw_a_cell(self.last, surface, BOARD_BACKGROUND_COLOR)

    def get_head_position(self) -> tuple:
        """
        Get the current position of the snake's head.

        Returns:
            tuple: Position of the snake's head.
        """
        return self.positions[0]

    def reset(self):
        """Reset the snake to the initial state."""
        self.length = 1
        self.positions = [CENTER]
        self.direction = choice((UP, DOWN, LEFT, RIGHT))
        self.last = self.positions[-1]


def handle_keys(snake: Snake):
    """
    Handle keyboard inputs to control the snake.

    Args:
        snake (Snake): The snake object to control.
    """
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            exit()
        if event.type == pg.KEYDOWN:
            # Exit on esc key
            if event.key == pg.K_ESCAPE:
                pg.quit()
                exit()
            # Update direction
            if event.key in DIRECTION_MAP:
                new_direction = DIRECTION_MAP[event.key]
                if (new_direction[0] != -snake.direction[0]
                        and new_direction[1] != -snake.direction[1]):
                    snake.update_direction(new_direction)


def set_caption(speed: int, length: int):
    """
    Set the window caption with current speed and snake length.

    Args:
        speed (int): Current speed of the game.
        length (int): Current length of the snake.
    """
    pg.display.set_caption(
        f'Snake | Speed: {speed} | Length: {length} | esc - to exit'
    )


def main():
    """The main game loop."""
    snake = Snake()
    apple = Apple(random_coord(set(snake.positions)), RED)
    bad_apple = Apple(random_coord(
        set((*snake.positions, apple.position))), BLUE)
    # Timer for changing apple positions
    timer_for_apples = 0
    screen.fill(BOARD_BACKGROUND_COLOR)
    speed = INITIAL_SPEED
    set_caption(speed, snake.length)

    while True:
        # Handle key presses
        handle_keys(snake)

        # Move the snake
        snake.move()
        # Check for collision with itself
        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        # Check for collision with apple
        elif snake.get_head_position() == apple.position:
            snake.length += 1
            # Speed up when the snake length is a multiple of 3
            if not snake.length % 3:
                speed += SPEED_INCREMENT
            apple.randomize_position(
                set((*snake.positions, bad_apple.position)))
            set_caption(speed, snake.length)
        # Check for collision with bad apple
        elif snake.get_head_position() == bad_apple.position:
            if snake.length == 1:
                bad_apple.randomize_position(
                    set((*snake.positions, apple.position)))
            else:
                if not snake.length % 3:
                    speed -= SPEED_INCREMENT
                snake.length -= 1
                snake.draw_a_cell(
                    snake.positions.pop(), screen, BOARD_BACKGROUND_COLOR)
                bad_apple.randomize_position(
                    set((*snake.positions, apple.position)))
                set_caption(speed, snake.length)

        # Increment the timer with each iteration
        timer_for_apples += 1
        # Every TIMER_RESET_THRESHOLD steps, the food changes position
        if timer_for_apples >= TIMER_RESET_THRESHOLD:
            timer_for_apples = 0
            apple.draw_a_cell(apple.position, screen, BOARD_BACKGROUND_COLOR)
            bad_apple.draw_a_cell(bad_apple.position,
                                  screen, BOARD_BACKGROUND_COLOR)
            bad_apple.randomize_position(
                set((*snake.positions, apple.position)))
            apple.randomize_position(
                set((*snake.positions, bad_apple.position)))

        # Drawing
        snake.draw(screen)
        apple.draw(screen)
        bad_apple.draw(screen)

        # Update the display
        pg.display.flip()

        # Limit the speed
        clock.tick(speed)


if __name__ == '__main__':
    main()
