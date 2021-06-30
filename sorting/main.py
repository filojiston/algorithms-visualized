import pygame
import random
import sys
import time

WIDTH = 800
HEIGHT = 800

COLORS = {
    "white": pygame.Color("white"),
    "red": pygame.Color("red"),
    "green": pygame.Color("green"),
    "blue": pygame.Color("blue"),
    "black": pygame.Color("black"),
    "yellow": pygame.Color("yellow")
}

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sorting Algoritms Visualizer")

ARR_SIZE = 200


class Element:
    def __init__(self, value):
        self.value = value
        self.color = COLORS["white"]
        self.width = (WIDTH / ARR_SIZE)
        self.height = self.value


class Solver:
    def __init__(self, arr):
        self.arr = arr

    def bubble_sort(self):
        for i in range(len(self.arr)):
            for j in range(0, len(self.arr) - i - 1):
                if (self.arr[j].value > self.arr[j + 1].value):
                    self.arr[j], self.arr[j + 1] = self.arr[j + 1], self.arr[j]
            self.arr[len(self.arr) - 1 - i].color = COLORS["green"]
            draw_arr(self.arr)

    def selection_sort(self):
        for i in range(len(self.arr)):
            min_idx = i
            for j in range(i + 1, len(self.arr)):
                if self.arr[min_idx].value > self.arr[j].value:
                    min_idx = j
            self.arr[i], self.arr[min_idx] = self.arr[min_idx], self.arr[i]
            self.arr[i].color = COLORS["green"]
            draw_arr(self.arr)

    def insertion_sort(self):
        self.arr[0].color = COLORS["green"]
        for i in range(1, len(self.arr)):
            key = self.arr[i]
            key.color = COLORS["green"]

            j = i - 1
            while j >= 0 and key.value < self.arr[j].value:
                self.arr[j + 1] = self.arr[j]
                j -= 1
            self.arr[j + 1] = key
            draw_arr(self.arr)

    def merge_sort(self):
        current_size = 1
        while current_size < len(self.arr) - 1:
            left = 0
            while left < len(self.arr) - 1:
                mid = min((left + current_size - 1), (len(self.arr) - 1))
                right = ((2 * current_size + left - 1, len(self.arr) - 1)
                         [2 * current_size + left - 1 > len(self.arr) - 1])

                self.merge(left, mid, right)
                left = left + current_size * 2
                draw_arr(self.arr)
            current_size = 2 * current_size
        for elem in self.arr:
            elem.color = COLORS["green"]

    def merge(self, l, m, r):
        n1 = m - l + 1
        n2 = r - m
        L = [0] * n1
        R = [0] * n2
        for i in range(0, n1):
            L[i] = self.arr[l + i]
        for i in range(0, n2):
            R[i] = self.arr[m + i + 1]

        i, j, k = 0, 0, l
        while i < n1 and j < n2:
            if L[i].value > R[j].value:
                self.arr[k] = R[j]
                j += 1
            else:
                self.arr[k] = L[i]
                i += 1
            k += 1

        while i < n1:
            self.arr[k] = L[i]
            i += 1
            k += 1

        while j < n2:
            self.arr[k] = R[j]
            j += 1
            k += 1

    def bogo_sort(self):
        def is_sorted(arr):
            return all(arr[i].value < arr[i + 1].value for i in range(len(arr) - 1))
        while not is_sorted(self.arr):
            random.shuffle(self.arr)
            draw_arr(self.arr)


def draw_arr(arr):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                sys.exit()
    screen.fill(COLORS["black"])
    x = 0
    for elem in arr:
        pygame.draw.rect(screen, elem.color,
                         (x, HEIGHT - elem.height, elem.width, elem.height))
        x += elem.width
    pygame.time.delay(100)
    pygame.display.update()


def main():
    arr = []
    for i in range(1, ARR_SIZE + 1):
        val = random.randint(1, HEIGHT)
        arr.append(Element(val))
    random.shuffle(arr)

    solver = Solver(arr)
    solver.bubble_sort()

    while True:
        draw_arr(arr)


main()
