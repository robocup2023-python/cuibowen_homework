import random
import os
import time


class Universe:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid1 = [[' ' for _ in range(width)] for _ in range(height)]
        self.grid2 = [[' ' for _ in range(width)] for _ in range(height)]
        self.current_grid = self.grid1
        self.next_grid = self.grid2

    def show(self):
        os.system('clear')
        for row in self.current_grid:
            print(''.join(row))
        time.sleep(2)

    def seed(self, probability=0.25):
        for row in self.current_grid:
            for i in range(len(row)):
                if random.random() < probability:
                    row[i] = '*'

    def is_alive(self, x, y):
        if x < 0 or x >= self.width or y < 0 or y >= self.height:
            return False
        return self.current_grid[y][x] == '*'

    def count_neighbors(self, x, y):
        alive_neighbors = 0
        for dx in [-1, 0, 1]:
            for dy in [-1, 0, 1]:
                if dx == 0 and dy == 0:
                    continue
                nx, ny = x + dx, y + dy
                if (0 <= nx < self.width) and (0 <= ny < self.height) and self.is_alive(nx, ny):
                    alive_neighbors += 1
        return alive_neighbors

    def next(self, x, y):
        alive = self.is_alive(x, y)
        neighbors = self.count_neighbors(x, y)

        if alive:
            if neighbors < 2 or neighbors > 3:
                return False
            else:
                return True
        else:
            if neighbors == 3:
                return True
            else:
                return False

    def update(self):
        self.current_grid, self.next_grid = self.next_grid, self.current_grid  # 交换当前和下一状态的世界
        for y in range(self.height):
            for x in range(self.width):
                self.current_grid[y][x] = '*' if self.next(x, y) else ' '


def main():
    world = Universe(80, 15)
    world.seed()

    # 主循环
    for _ in range(100):
        world.show()
        world.update()


if __name__ == '__main__':
    main()
