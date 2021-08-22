import pygame
import random

pygame.init()

screen = pygame.display.set_mode((720,720))

pygame.display.set_caption("PyGolf")

running = True

gameObjects = []

class Transform():
    pos = [0, 0]

class Time():
    getTicksLastFrame = 0
    deltaTime = 1
    t = 0
    def __init__(self):
        gameObjects.append(self)

    def update(self):
        self.t = pygame.time.get_ticks()
        self.deltaTime = (self.t - self.getTicksLastFrame) / 1000.0
        self.getTicksLastFrame = self.t


Time = Time()

class Circle():
    radius = 0
    color = [0, 0, 0]
    def __init__(self, radius, color):
        self.radius = radius
        self.color = color

    def draw(self, pos):
        pygame.draw.circle(screen, self.color, (pos[0] + self.radius, pos[1] + self.radius), self.radius, 5)

class obj():
    transform = Transform()

class PlayerController():
    gameObject = obj()
    vel = [200,150]

    def move(self, x, y):
        gameObject.transform.pos = [self.transform.pos[0] + (x * Time.deltaTime), self.transform.pos[1] + (y * Time.deltaTime)]
    def collisions(self):
        if self.transform.pos[0] <= 0 :
            if(self.transform.pos[0] < 0):
                self.vel[0] = -self.vel[0]
        
        if self.transform.pos[0] + self.gameObject.body.radius * 2 >= 720:
            if(self.vel[0] > 0):
                self.vel[0] = -self.vel[1]

        if self.transform.pos[1] <= 0:
            if(self.vel[1] < 0):
                self.vel[1] = -self.vel[1]
        
        if self.transform.pos[1] + self.gameObject.body.radius * 2 >= 720:
            if(self.vel[1] > 0):
                self.vel[1] = -self.vel[1]
    def update(self):
        self.move(self.vel[0], self.vel[1])
        self.collisions()

class nullController():
    transform = Transform()

class GameObject():
    body = Circle(5, [255, 0, 0])
    transform = Transform()
    controller = nullController()
    def __init__(self, body, controller):
        gameObjects.append(self)
        self.body = body
        self.controller = controller
        self.controller.transform = self.transform
        self.controller.gameObject = self

    def update(self):
        self.body.draw(self.transform.pos)
        self.controller.update()

player = GameObject(Circle(20, [255, 0, 0]), PlayerController())

while running:
    pygame.display.flip()
    screen.fill((255,255,255))

    for gameObject in gameObjects:
        gameObject.update()

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False