import time
import random
from graphics import *
from vector import *

win_w = 500
win_h = 500

max_speed = 300
neighbor_radius = 50
obstacle_radius = 50

class Boid(object):
    def __init__(self, x, y, win):
        self.pos = Vector(x, y)
        self.vel = Vector(0, 0)
        self.__drw = None

    def __wrap(self):
        if self.pos[0] < 0: self.pos += Vector(win_w, 0)
        if self.pos[0] > win_w: self.pos -= Vector(win_w, 0)
        if self.pos[1] < 0: self.pos += Vector(0, win_h)
        if self.pos[1] > win_h: self.pos -= Vector(0, win_h)

    def __crop(self):
        if self.vel.norm() > max_speed:
            self.vel = self.vel.normalize() * max_speed

    def rule1(self, others):  # Go in crowd
        v = Vector()

        for other in others:
            v += other.pos
        v = v / (len(others) or 1)
        v -= self.pos

        if len(others) == 0:
            v = Vector()

        return v

    def rule2(self, others):  # Go from crowd
        v = Vector()

        for other in others:
            u = (self.pos - other.pos)
            v += u / u.norm() ** 1.5

        return v

    def rule3(self, others):  # Align speed with crowd
        v = Vector()
        for other in others:
            v += other.vel

        return v

    def rule4(self, obstacles):  # Avoid obstacles
        v = Vector()

        for obs in obstacles:
            u = (self.pos - obs.pos)
            v += u / u.norm()

        return v

    def update(self, dt, boids, obstacles):
        v1 = self.rule1(boids)
        v2 = self.rule2(boids)
        v3 = self.rule3(boids)
        v4 = self.rule4(obstacles)

        self.vel += v1 * 5 + v2 * 1000 + v3 * 10 + v4 * 10000
        self.__crop()

        self.pos += self.vel * dt
        self.__wrap()

    def draw(self, win):
        self.__drw = Circle(Point(self.pos[0], self.pos[1]), 3)
        self.__drw.draw(win)

    def undraw(self):
        if self.__drw:
            self.__drw.undraw()


class Obstacle(Boid):
    def __init__(self, x, y, win):
        self.pos = Vector(x, y)
        self.__drw = Circle(Point(self.pos[0], self.pos[1]), 10)
        self.__drw.setFill("red")
        self.__drw.draw(win)
    def update(self, dt, boids):
        pass


class BoidList(list):
    def update(self, dt, obstacles):
        for boid in self:
            boid.update(dt,
                        self.get_neighbors(boid, neighbor_radius),
                        get_near_obstacles(boid,
                                           obstacles,
                                           obstacle_radius))

    def draw(self, win):
        for boid in self:
            boid.draw(win)

    def undraw(self):
        for boid in self:
            boid.undraw()

    def get_neighbors(self, boid, radius):
        neighbors = []
        for other in self:
            if boid is not other and boid.pos.distance(other.pos) < radius:
                neighbors.append(other)
        return neighbors

def get_near_obstacles(boid, obstacles, radius):
    neighbors = []
    for other in obstacles:
        if boid.pos.distance(other.pos) < radius:
            neighbors.append(other)
    return neighbors

def main():
    win = GraphWin("Boids", win_w, win_h, autoflush=False)
    win.setBackground("white")

    boids = BoidList()
    obstacles = []

    for i in range(0, 50):
        boids.append(Boid(random.randint(0, win_w),
                          random.randint(0, win_h), win))

    old_t = time.time()
    while True:
        dt = time.time() - old_t
        if dt > 0.03:
            boids.undraw()
            old_t = time.time()

            boids.update(dt, obstacles)
            boids.draw(win)

            win.update()
            if win.checkKey() == 'q':
                win.close()
                break

            mouse = win.checkMouse()
            if mouse:
                obstacles.append(Obstacle(mouse.x, mouse.y, win))


if __name__ == '__main__':
    main()