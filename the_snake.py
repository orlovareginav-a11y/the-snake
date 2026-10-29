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


class GameObject:
    """
    Базовый класс для игровых объектов.
    Содержит общие свойства, такие как позиция и цвет.
    """

    def __init__(self, color=BOARD_BACKGROUND_COLOR):
        """
        Инициализирует базовые параметры игрового объекта -
        начальная позиция и цвет объекта.
        """
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = color

    def draw(self):
        """Метод для отрисовки объекта на экране."""
        raise NotImplementedError('Метод draw должен быть переопределен',
                                  'в дочернем классе')


class Apple(GameObject):
    """
    Класс, описывающий хорошее яблоко.

    При поедании увеличивает длину змейки на 1 сегмент.
    Управляет его цветом, случайным появлением на сетке поля
    и отрисовкой на экране.
    """

    def __init__(self, color=APPLE_COLOR, forbidden_positions=None):
        """
        Инициализирует хорошее яблоко,
        задает цвет и случайную начальную позицию.
        """
        super().__init__(color)
        self.randomize_position(forbidden_positions)

    def randomize_position(self, forbidden_positions=None):
        """
        Генерирует случайные координаты,
        избегая тела змейки и других объектов.
        """
        if forbidden_positions is None:
            forbidden_positions = []

        new_position = None

        while new_position is None or new_position in forbidden_positions:
            position_x = randint(0, GRID_WIDTH - 1) * GRID_SIZE
            position_y = randint(0, GRID_HEIGHT - 1) * GRID_SIZE
            new_position = (position_x, position_y)

        self.position = new_position

    def draw(self):
        """
        Отрисовывает хорошее яблоко на экране в виде
        красного квадрата с рамкой.
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

    def __init__(self, color=SNAKE_COLOR):
        """Инициализирует начальное состояние змейки."""
        super().__init__(color)
        self.reset()

    def get_head_position(self):
        """Возвращает текущие координаты головы змейки."""
        return self.positions[0]

    def move(self):
        """
        Вычисляет новое положение змейки, добавляя голову и удаляя хвост.

        Реализует сквозной проход через границы экрана.
        """
        head_position = self.get_head_position()
        delta_x, delta_y = self.direction
        position_x, position_y = head_position
        new_x = (position_x + GRID_SIZE * delta_x) % SCREEN_WIDTH
        new_y = (position_y + GRID_SIZE * delta_y) % SCREEN_HEIGHT
        new_head_position = (new_x, new_y)
        self.positions.insert(0, new_head_position)
        while len(self.positions) > self.length:
            self.positions.pop()

    def update_direction(self):
        """Обновляет текущее направление движения на основе next_direction."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def draw(self):
        """Отрисовывает все сегменты тела змейки и затирает след от хвоста."""
        for position in self.positions:
            rect = (pygame.Rect(position, (GRID_SIZE, GRID_SIZE)))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pygame.Rect(self.get_head_position(),
                                (GRID_SIZE, GRID_SIZE))
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
        directions = (RIGHT, LEFT, UP, DOWN)
        self.direction = choice(directions)
        self.next_direction = None
        self.last = None


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
    snake = Snake()
    apple = Apple(APPLE_COLOR, forbidden_positions=snake.positions)
    bad_apple = Apple(BAD_APPLE_COLOR, forbidden_positions=snake.positions
                      + [apple.position])
    # Минимальный порог скорости, чтобы игра не остановилась полностью
    MIN_SPEED = 5
    while True:
        current_speed = max(MIN_SPEED, SPEED - (snake.length // 3))

        clock.tick(current_speed)
        handle_keys(snake)
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.move()

        # 1. Проверка: змейка съела хорошее яблоко
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions + [bad_apple.position])

        # 2. Проверка: змейка съела плохое яблоко
        elif snake.get_head_position() == bad_apple.position:
            if snake.length > 1:
                snake.length -= 1
                if len(snake.positions) > 0:
                    snake.last = snake.positions.pop()
                bad_apple.randomize_position(snake.positions
                                             + [apple.position])
            else:
                pygame.quit()
                raise SystemExit

        # 3. Проверка: змейка врезалась в себя
        elif snake.get_head_position() in snake.positions[1:]:
            screen.fill(BOARD_BACKGROUND_COLOR)
            snake.reset()

        snake.draw()
        apple.draw()
        bad_apple.draw()
        pygame.display.update()


if __name__ == '__main__':
    main()
