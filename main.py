import math
import pygame
import sys

pygame.init()


# Variables
# size = width, height = 500, 500
# speed = [2, 2]
# a = 500.0
# k = 2.0
# x, y = 100, 100
# vx, self.vy = 0, 0
# g = 50.0
# s = 50.0
# clock = pygame.time.Clock()
# earth = 0
# baseline = 480.0


class MainGame:
    def __init__(self):
        pygame.init()
        # Variables
        size = width, height = 500, 500
        speed = [2, 2]
        self.a = 500.0
        self.k = 2.0
        self.x, self.y = 100, 100
        self.vx, self.vy = 0, 0
        g = 50.0
        s = 50.0
        self.clock = pygame.time.Clock()
        earth = 0
        self.baseline = 480.0

        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption('Game')

    def start_game(self):
        # self.init_window()
        prev_t = pygame.time.get_ticks()
        tt = 0
        ar = pygame.PixelArray(self.screen)
        while True:
            delta = self.clock.tick(50) / 1000.0
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
            tt += delta
            print("%f %f %f" % (tt, self.vx, self.x))
            pressed = pygame.key.get_pressed()
            if pressed[pygame.K_LEFT]:
                self.vx -= delta * self.a
            if pressed[pygame.K_RIGHT]:
                self.vx += delta * self.a
            if pressed[pygame.K_UP]:
                if self.y == self.baseline:
                    self.vy = -700.0
                else:
                    earth = 0

            if self.y <= self.baseline:
                gt = 1000 * delta
            else:
                gt = 0.0
                self.vy = 0.0
            self.vx -= delta * self.vx * self.k
            self.vy -= delta * self.vy * self.k - gt
            self.x += self.vx * delta
            self.y += self.vy * delta

            if self.x < 20:
                if self.vx < 0:
                    self.vx = -self.vx
                x = 20
            if self.y < 20:
                if self.vy < 0:
                    self.vy = -self.vy
                y = 20
            if self.x > 480:
                if self.vx > 0:
                    self.vx = -self.vx
                x = 480
            if self.y > 480:
                if self.vy > 0:
                    self.vy = 0
                self.y = 480

            aplatf = [150, 450, 50, 20]

            uy = self.y - 20.0
            by = self.y + 20.0

            rx = self.x + 20.0
            lx = self.x - 20.0

            if (by == 390.0) & (lx >= 100.0) & (rx <= 200):
                self.vy = 1000 * delta
                self.y = 370.0
                self.baseline = 370.0
            else:
                self.baseline = 480.0
            if rx == 100.0:
                if self.vx > 0.0:
                    self.vx = -self.vx
                self.x = 80.0
            if uy == 430.0:
                if self.vy < 0.0:
                    self.vy = -self.vy
                self.y = 450.0
            if lx == 200.0:
                if self.vx < 0.0:
                    self.vx = -self.vx
                self.x = 220.0
            self.screen.fill((0, 25, 75))
            col = min(255, int(math.sqrt(self.vx ** 2 + self.vy ** 2)) + 100)
            pygame.draw.lines(self.screen, (255, 0, 0), True, [(100, 390), (100, 430), (200, 430), (200, 390)], 2)

            pygame.draw.circle(self.screen, (col - 100, col - 25, col), (int(self.x), int(self.y)), 20)
            pygame.display.flip()


if __name__ == "__main__":
    game = MainGame()
    game.start_game()
