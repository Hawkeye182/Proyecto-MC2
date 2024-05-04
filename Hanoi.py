import tkinter as tk
import tkinter.messagebox as messagebox
import sys

class Hanoi:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Torres de Hanoi")
        self.disks = 3
        self.towers = [[i for i in range(self.disks, 0, -1)], [], []]
        self.selected_tower = None
        self.game_over = False
        self.moves = []
        self.colors = ['red', 'orange', 'yellow', 'green', 'blue', 'indigo', 'violet'] 
        self.create_gui()

    def create_gui(self):
        self.frame = tk.Frame(self.window, bg='lightgrey')
        self.frame.pack(fill=tk.X, side=tk.BOTTOM, pady=20)
        self.canvas = tk.Canvas(self.window, width=1000, height=600, bg='white') 
        self.canvas.pack(fill=tk.BOTH, expand=True)
        self.canvas.bind("<Button-1>", self.click)
        self.center_window()
        self.entry = tk.Entry(self.frame, font=('Arial', 14))
        self.entry.pack(side=tk.LEFT, padx=10)
        self.button = tk.Button(self.frame, text="Iniciar juego", command=self.start_game, font=('Arial', 14), bg='lightblue')
        self.button.pack(side=tk.LEFT, padx=10)
        self.canvas.bind("<Button-1>", self.click)
        self.canvas.bind("<Button-3>", self.right_click) 
        self.solve_button = tk.Button(self.frame, text="Resolver", command=self.solve, font=('Arial', 14), bg='lightgreen')
        self.solve_button.pack(side=tk.LEFT, padx=10)

    def center_window(self):
        window_width = max(800, self.disks * 250) 
        window_height = 400
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        self.window.geometry(f"{window_width}x{window_height}+{position_right}+{position_top}")

    def start_game(self):
        self.disks = int(self.entry.get())
        if self.disks < 1 or self.disks > 7:
            messagebox.showerror("Error", "Por favor, elija un número entre 1 y 7.")
        else:
            self.towers = [[i for i in range(self.disks, 0, -1)], [], []]
            self.moves = self.hanoi(self.disks, 0, 2)
            self.draw_game()

    def hanoi(self, n, source, target):
        if n > 0:
            aux = 3 - source - target
            return self.hanoi(n - 1, source, aux) + [(source, target)] + self.hanoi(n - 1, aux, target)
        else:
            return []

    def solve(self):
        if self.moves:
            self.solve_button.config(state=tk.DISABLED)
            self.animate_solution()

    def animate_solution(self):
        if self.moves:
            source, target = self.moves.pop(0)
            self.move_disk(source, target)
            self.window.after(500, self.animate_solution)  
        else:
            self.solve_button.config(state=tk.NORMAL)

    def move_disk(self, from_tower, to_tower):
        if len(self.towers[from_tower]) > 0 and (len(self.towers[to_tower]) == 0 or self.towers[from_tower][-1] < self.towers[to_tower][-1]):
            self.towers[to_tower].append(self.towers[from_tower].pop())
            self.draw_game()
    
    def right_click(self, event):
        self.selected_tower = None
        self.draw_game()

    def create_rounded_rectangle(self, x1, y1, x2, y2, r, **kwargs):
        points = [x1+r, y1,
                x1+r, y1,
                x2-r, y1,
                x2-r, y1,
                x2, y1,
                x2, y1+r,
                x2, y1+r,
                x2, y2-r,
                x2, y2-r,
                x2, y2,
                x2-r, y2,
                x2-r, y2,
                x1+r, y2,
                x1+r, y2,
                x1, y2,
                x1, y2-r,
                x1, y2-r,
                x1, y1+r,
                x1, y1+r,
                x1, y1]
        return self.canvas.create_polygon(points, **kwargs, smooth=True)

    def draw_game(self):
        self.canvas.delete('all')
        for i, tower in enumerate(self.towers):
            x = (i + 1) * self.canvas.winfo_width() / 4  
            self.canvas.create_rectangle(x - 10, 50, x + 10, 350, fill='black')  
            for j, disk in enumerate(tower):
                disk_width = disk * 20
                color = self.colors[disk - 1] 
                self.create_rounded_rectangle(x - disk_width, 350 - (j * 20), x + disk_width, 370 - (j * 20), 10, fill=color)  
                if i == self.selected_tower and j == len(tower) - 1:
                    self.canvas.create_line(x, 350 - (j * 20) - 10, x, 350 - (j * 20) - 30, arrow=tk.LAST, fill='blue', width=2)  
            if self.selected_tower is not None: 
                x = (self.selected_tower + 1) * self.canvas.winfo_width() / 4
                self.canvas.create_line(x, 50, x, 30, arrow=tk.LAST, fill='red', width=2)
        if len(self.towers[2]) == self.disks and not self.game_over:
            self.game_over = True
            messagebox.showinfo("Felicidades", "¡Ganaste!")

    def click(self, event):
        tower = min(range(3), key=lambda i: abs(event.x - ((i + 1) * self.canvas.winfo_width() / 4)))  
        if self.selected_tower is None:
            if len(self.towers[tower]) > 0:
                self.selected_tower = tower
        else:
            if tower != self.selected_tower and (len(self.towers[tower]) == 0 or self.towers[self.selected_tower][-1] < self.towers[tower][-1]):
                self.move_disk(self.selected_tower, tower)
                self.selected_tower = None
            else:
                messagebox.showwarning("Movimiento no permitido", "No puedes mover un disco más grande encima de uno más pequeño.")
        self.draw_game()

    def play(self):
        self.window.mainloop()

if __name__ == "__main__":
    game = Hanoi()
    game.play()