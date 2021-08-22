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

    def move(self, x, y):
        gameObject.transform.pos = [self.transform.pos[0] + (x * Time.deltaTime), self.transform.pos[1] + (y * Time.deltaTime)]

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

player = GameObject(Circle(20, [255, 0, 0]), PlayerController())

class Ball():
    transform = Transform()
    centralPos = [0, 0]
    transform.pos = [250, 250]
    radius = 20

    velocity = [0, 0]
    speed = 40

    player = GameObject(Circle(5, [255, 0, 0]), PlayerController())

    def __init__(self, player):
        gameObjects.append(self)
        self.velocity = [-5, random.randint(-4, 4)]

        if self.velocity[1] > 0 and self.velocity[1] < 1: self.velocity[1] = 2
        if self.velocity[1] < 0 and self.velocity[1] > -1: self.velocity[1] = -2

        self.player = player

    def draw(self):
        self.body = pygame.draw.circle(screen, (255, 0, 0), (self.transform.pos[0] + self.radius, self.transform.pos[1] - self.radius), self.radius, 5)
    
    def collisions(self):
        if self.transform.pos[0] <= 0 :
            if(self.transform.pos[0] < 0):
                self.velocity[0] = -self.velocity[0]
        
        if self.transform.pos[0] >= 500 and self.transform.pos[0] <= 505:
            if self.transform.pos[1] >= player.transform.pos[1] and self.transform.pos[1] <= player.transform.pos[1] + player.heigth:
                if(self.velocity[0] > 0):
                    self.velocity[0] = -self.velocity[0] - 1
                    self.velocity[1] = -((player.transform.pos[1] + player.heigth / 2) - self.transform.pos[1]) / 5
        elif self.transform.pos[0] >= 500: player.Dead()

        if self.transform.pos[1] - self.radius <= 0:
            if(self.velocity[1] < 0):
                self.velocity[1] = -self.velocity[1]
        
        if self.transform.pos[1] >= 500:
            if(self.velocity[1] > 0):
                self.velocity[1] = -self.velocity[1]

    def move(self):
        self.collisions()
        self.transform.pos = [self.transform.pos[0] + (self.velocity[0] * self.speed * Time.deltaTime), self.transform.pos[1] + (self.velocity[1] * self.speed * Time.deltaTime)]
    
    def update(self):
        self.centralPos = (self.transform.pos[0] + self.radius, self.transform.pos[1] - self.radius)
        self.move()
        self.draw()

ball = Ball(player)

while running:
    pygame.display.flip()
    screen.fill((255,255,255))

    for gameObject in gameObjects:
        gameObject.update()

    keys = pygame.key.get_pressed()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False