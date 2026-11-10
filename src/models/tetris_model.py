import random

class TetrisModel:
    """Модель данных и логика игры Тетрис."""
    def __init__(self, width=10, height=20):
        self.width = width
        self.height = height
        self.board = [[0] * width for _ in range(height)]
        self.score = 0
        
        # Описания фигур (тетрамино)
        self.shapes = [
            [[1, 1, 1, 1]],  # I
            [[1, 1], [1, 1]],  # O
            [[0, 1, 0], [1, 1, 1]],  # T
            [[1, 0, 0], [1, 1, 1]],  # L
            [[0, 0, 1], [1, 1, 1]],  # J
            [[0, 1, 1], [1, 1, 0]],  # S
            [[1, 1, 0], [0, 1, 1]]   # Z
        ]
        self.current_shape = None
        self.current_color = 1
        self.x = 0
        self.y = 0
        self.spawn_new_piece()

    def spawn_new_piece(self):
        """Создание новой фигуры на поле."""
        self.current_shape = random.choice(self.shapes)
        self.current_color = random.randint(1, 7)
        self.x = self.width // 2 - len(self.current_shape[0]) // 2
        self.y = 0
        if not self.check_collision(self.x, self.y, self.current_shape):
            return False
        return True

    def check_collision(self, offset_x, offset_y, shape):
        """Проверка столкновений фигуры со стенами и другими блоками."""
        for r_idx, row in enumerate(shape):
            for c_idx, val in enumerate(row):
                if val:
                    new_x = offset_x + c_idx
                    new_y = offset_y + r_idx
                    if new_x < 0 or new_x >= self.width or new_y >= self.height:
                        return False
                    if new_y >= 0 and self.board[new_y][new_x]:
                        return False
        return True

    def merge_piece(self):
        """Фиксация текущей фигуры на игровом поле."""
        for r_idx, row in enumerate(self.current_shape):
            for c_idx, val in enumerate(row):
                if val and self.y + r_idx >= 0:
                    self.board[self.y + r_idx][self.x + c_idx] = self.current_color
        self.clear_lines()

    def clear_lines(self):
        """Удаление заполненных линий и начисление очков."""
        full_lines = [i for i, row in enumerate(self.board) if all(row)]
        for idx in full_lines:
            del self.board[idx]
            self.board.insert(0, [0] * self.width)
        self.score += len(full_lines) * 100

    def move_left(self):
        if self.check_collision(self.x - 1, self.y, self.current_shape):
            self.x -= 1

    def move_right(self):
        if self.check_collision(self.x + 1, self.y, self.current_shape):
            self.x += 1

    def move_down(self):
        if self.check_collision(self.x, self.y + 1, self.current_shape):
            self.y += 1
            return True
        else:
            self.merge_piece()
            return False

    def rotate(self):
        """Поворот фигуры."""
        rotated = [list(row) for row in zip(*self.current_shape[::-1])]
        if self.check_collision(self.x, self.y, rotated):
            self.current_shape = rotated
