from random import choice, randint

import pygame

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

# Цвет плохого яблока
BAD_APPLE_COLOR = (150, 0, 255)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 20

# Настройка игрового окна:
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """
    Базовый класс для игровых объектов.
    Содержит общие свойства, такие как позиция и цвет.
    """

    def __init__(self):
        """
        Инициализирует базовые параметры игрового объекта -
        начальная позиция и цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = BOARD_BACKGROUND_COLOR

    def draw(self):
        """Метод для отрисовки объекта на экране."""
        pass


class Apple(GameObject):
    """
    Класс, описывающий хорошее яблоко.

    При поедании увеличивает длину змейки на 1 сегмент.
    Управляет его цветом, случайным появлением на сетке поля
    и отрисовкой на экране.
    """

    def __init__(self):
        """
        Инициализирует хорошее яблоко,
        задает цвет и случайную начальную позицию.
        """
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Генерирует случайные координаты для хорошего яблока
        в сетке игрового поля.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """
        Отрисовывает хорошее яблоко на экране в виде
        красного квадрата с рамкой.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class BadApple(GameObject):
    """Класс, описывающий плохое яблоко (ядовитый объект).

    При поедании уменьшает длину змейки на 1 сегмент.
    Управляет его цветом, случайным появлением на сетке поля
    и отрисовкой на экране.
    """

    def __init__(self):
        """
        Инициализирует плохое яблоко,
        задает цвет и случайную начальную позицию.
        """
        super().__init__()
        self.body_color = BAD_APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """
        Генерирует случайные координаты для плохого яблока
        в сетке игрового поля.
        """
        x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self):
        """
        Отрисовывает плохое яблоко на экране в виде
        фиолетового квадрата с рамкой.
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """
    Класс, описывающий змейку и её поведение.

    Управляет движением, изменением направления, ростом
    и сбросом состояния при проигрыше.
    """

    def __init__(self):
        """Инициализирует начальное состояние змейки."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """
        Вычисляет новое положение змейки, добавляя голову и удаляя хвост.

        Реализует сквозной проход через границы экрана.
        """
        head_position = self.get_head_position()
        dx, dy = self.direction
        new_x = (head_position[0] + GRID_SIZE * dx) % SCREEN_WIDTH
        new_y = (head_position[1] + GRID_SIZE * dy) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)
        self.positions.insert(0, new_head_position)
        if len(self.positions) > self.length:
            self.last = self.positions.pop()
        else:
            self.last = None

    def update_direction(self):
        """Обновляет текущее направление движения на основе next_direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает все сегменты тела змейки и затирает след от хвоста."""
        for position in self.positions[:-1]:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        # Затирание последнего сегмента
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def reset(self):
        """Сбрасывает змейку в начальное состояние при столкновении с собой."""
        self.length = 1
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        directions = [RIGHT, LEFT, UP, DOWN]
        self.direction = choice(directions)
        self.next_direction = None
        self.last = None
        screen.fill(BOARD_BACKGROUND_COLOR)


def handle_keys(game_object):
    """
    Перехватывает нажатия клавиш и предлагает новое направление для змейки.

    Блокирует мгновенный разворот на 180 градусов.
    """
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
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
    """
    Главная функция игры.

    Инициализирует Pygame, создает объекты и запускает основной игровой цикл.
    """
    pygame.init()
    apple = Apple()
    bad_apple = BadApple()
    snake = Snake()

    while bad_apple.position == apple.position:
        bad_apple.randomize_position()

    while True:
        if SPEED - (snake.length // 3) > 5:
            current_speed = SPEED - (snake.length // 3)
        else:
            current_speed = 5

        clock.tick(current_speed)
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # 1. Проверка: змейка съела хорошее яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            while apple.position in snake.positions:
                apple.randomize_position()

        # 2. Проверка: змейка съела плохое яблоко
        if snake.get_head_position() == bad_apple.position:
            if snake.length > 1:
                snake.length -= 1
                snake.last = snake.positions.pop()
                last_rect = pygame.Rect(snake.last, (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

            bad_apple.randomize_position()
            while bad_apple.position in snake.positions:
                bad_apple.randomize_position()
            else:
                snake.quit()

        # 3. Проверка: змейка врезалась в себя
        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()

        snake.draw()
        apple.draw()
        bad_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
