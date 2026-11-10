import tkinter as tk
from src.models.tetris_model import TetrisModel

class TetrisApp:
    """Главный класс приложения Тетрис."""
    def __init__(self, root):
        self.root = root
        self.root.title("Тетрис")
        self.block_size = 30
        self.width = 10
        self.height = 20
        
        self.model = TetrisModel(self.width, self.height)
        
        self.canvas = tk.Canvas(root, width=self.width * self.block_size, 
                                height=self.height * self.block_size, bg="black")
        self.canvas.pack(side=tk.LEFT)
        
        self.score_label = tk.Label(root, text="Счет: 0", font=("Arial", 16))
        self.score_label.pack(padx=20, pady=20)
        
        self.root.bind("<Key>", self.handle_keypress)
        self.colors = ["black", "cyan", "yellow", "purple", "orange", "blue", "green", "red"]
        
        self.update_game()

    def handle_keypress(self, event):
        """Обработка нажатий клавиш управления."""
        if event.keysym == "Left":
            self.model.move_left()
        elif event.keysym == "Right":
            self.model.move_right()
        elif event.keysym == "Down":
            self.model.move_down()
        elif event.keysym == "Up":
            self.model.rotate()
        self.redraw()

    def update_game(self):
        """Игровой цикл (таймер падения)."""
        moved = self.model.move_down()
        if not moved:
            if not self.model.spawn_new_piece():
                print("Игра окончена!")
        self.score_label.config(text=f"Счет: {self.model.score}")
        self.redraw()
        self.root.after(200, self.update_game)

    def redraw(self):
        """Перерисовка игрового поля."""
        self.canvas.delete("all")
        # Отрисовка стакана
        for r in range(self.height):
            for c in range(self.width):
                val = self.model.board[r][c]
                if val:
                    self.draw_block(c, r, self.colors[val])
        
        # Отрисовка текущей фигуры
        if self.model.current_shape:
            for r_idx, row in enumerate(self.model.current_shape):
                for c_idx, val in enumerate(row):
                    if val:
                        self.draw_block(self.model.x + c_idx, self.model.y + r_idx, 
                                        self.colors[self.model.current_color])

    def draw_block(self, x, y, color):
        x1 = x * self.block_size
        y1 = y * self.block_size
        x2 = x1 + self.block_size
        y2 = y1 + self.block_size
        self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="gray")
