# Snake Game

Welcome to the classic Snake game implemented in Python using Pygame. Guide the snake to eat apples, avoid bad apples, and grow as long as possible!

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Game Controls](#game-controls)
- [Code Structure](#code-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Classic Gameplay**: Move the snake around the grid to eat apples and grow longer.
- **Bad Apples**: Avoid bad apples which reduce the snake's length.
- **Dynamic Speed**: The snake speeds up as it grows and slows down when bad apples are consumed.
- **Randomized Apples**: Apples change position every few seconds for an added challenge.

## Installation

1. **Clone the repository:**
    ```sh
    git clone git@github.com:zmlkf/the_snake.git
    cd the_snake
    ```

2. **Create a virtual environment (optional but recommended):**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

## Usage

1. **Run the game:**
    ```sh
    python the_snake.py
    ```

2. **Enjoy playing!** Use the arrow keys to control the snake.

## Game Controls

- **Arrow Keys**: Move the snake up, down, left, or right.
- **ESC**: Quit the game.

## Code Structure

- **`snake.py`**: The main game file containing all the logic and game loop.
- **`README.md`**: This readme file.

### Key Classes and Functions

- **`GameObject`**: Base class for game objects.
- **`Apple`**: Class representing an apple.
- **`Snake`**: Class representing the snake.
- **`handle_keys(snake)`**: Function to handle keyboard inputs.
- **`set_caption(speed, length)`**: Function to set the game window caption.
- **`main()`**: Main game loop function.

## Testing

The repository includes tests developed by engineers at Yandex. To run the tests, follow this step:

1. **Run the tests:**
    ```sh
    pytest
    ```

The test files included are:

- **`conftest.py`**: Configuration for pytest.
- **`test_code_structure.py`**: Tests for the code structure.
- **`test_main.py`**: Tests for the main game logic.

## Author

Developed by [Roman Zemliakov](https://github.com/zmlkf).