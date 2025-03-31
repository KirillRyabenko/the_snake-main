from random import randrange

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()

# Словарь для handle_keys
DIRECTIONS = {(LEFT, pg.K_UP): UP,
              (RIGHT, pg.K_UP): UP,
              (UP, pg.K_LEFT): LEFT,
              (UP, pg.K_RIGHT): RIGHT,
              (LEFT, pg.K_DOWN): DOWN,
              (RIGHT, pg.K_DOWN): DOWN,
              (DOWN, pg.K_RIGHT): RIGHT,
              (DOWN, pg.K_LEFT): LEFT}


class GameObject:
    """Материнский класс"""

    def __init__(self, body_color=None, position=None):
        self.position = position
        self.body_color = body_color

    def draw(self):
        """Отрисовка для дочерних классов"""

    def make_draw(self, position=None):
        """Шаблон отрисовки для дочерних классов"""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Apple(GameObject):
    """Дочерний класс, отвечающий за отрисовку и позицию яблока"""

    def __init__(self):
        super().__init__(body_color=APPLE_COLOR)

    def draw(self):
        """Отрисовка яблока"""
        self.make_draw(self.position)

    def randomize_position(self, snake_coordinates):
        """Генерирует позицию яблока"""
        while True:
            self.position = (randrange(
                0, SCREEN_WIDTH, GRID_SIZE),
                randrange(0, SCREEN_HEIGHT, GRID_SIZE))
            if self.position not in snake_coordinates:
                break


class Snake(GameObject):
    """Дочерний класс, отвечающий за змейку"""

    def __init__(self):
        super().__init__(body_color=SNAKE_COLOR)
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None

    def update_direction(self):
        """Метод, отвечающей за изменение направления движения змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Метод, отрисовывающий змейку"""
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        for position in self.positions:
            self.make_draw(position)

        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def move(self):
        """Метод, описывающий движение змейки"""
        x, y = self.direction
        head_x, head_y = self.get_head_position()
        self.positions.insert(
            0,
            (
                (head_x + x * GRID_SIZE) % SCREEN_WIDTH,
                (head_y + y * GRID_SIZE) % SCREEN_HEIGHT))
        self.last = self.positions.pop()

    def get_head_position(self):
        """Возвращает координаты головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод, обнуляющий позицию змейки"""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None


def handle_keys(game_object):
    """Функция для обработки действий пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        if event.type == pg.KEYDOWN:
            game_object.next_direction = DIRECTIONS.get(
                (game_object.direction, event.key), game_object.direction)


def main():
    """Функция описывающая логику игры"""
    pg.init()
    apple = Apple()
    snake = Snake()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        snake.move()
        handle_keys(snake)
        snake.update_direction()
        snake.draw()
        apple.draw()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            snake.positions.append(snake.last)
            apple.randomize_position(snake.positions)
        head = snake.positions.pop(0)
        if head in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()
        else:
            snake.positions.insert(0, head)
        pg.display.update()


if __name__ == '__main__':
    main()
